import time
import logging
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.schemas import (
    TextTransformRequest,
    TextTransformResponse,
    BatchTransformRequest,
    BatchTransformResponse,
    HealthResponse,
    ErrorResponse,
    HistoryResponse,
    HistoryItem,
    SaveHistoryRequest,
    DeleteHistoryRequest
)
from app.models.database import TransformationHistory
from app.services.text_processor_simple import text_processor
from app.utils.helpers import (
    cache,
    validate_text_input,
    sanitize_text,
    create_error_response,
    format_processing_time
)
from app.core.config import settings
from app.core.database import get_db, check_db_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Check Groq API status
        groq_status = await text_processor.health_check()
        
        # Check database connection
        db_status = "healthy" if check_db_connection() else "unhealthy"
        
        return HealthResponse(
            status="healthy" if db_status == "healthy" else "degraded",
            app_name=settings.app_name,
            version=settings.app_version,
            groq_api_status=groq_status.get("status", "unknown"),
            langchain_status="active" if settings.langchain_tracing_v2 else "inactive",
            database_status=db_status,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            app_name=settings.app_name,
            version=settings.app_version,
            groq_api_status="error",
            langchain_status="disabled",
            database_status="error",
            timestamp=datetime.now().isoformat()
        )

@router.post("/transform", response_model=TextTransformResponse)
async def transform_text(request: TextTransformRequest, db: Session = Depends(get_db)):
    """Transform text using the specified transformation type."""
    history_id = None  # Initialize history_id
    
    try:
        logger.info(f"Transform request from user: {request.user_id}")
        
        # Validate input
        is_valid, error_msg = validate_text_input(request.text)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Sanitize text
        cleaned_text = sanitize_text(request.text)
        
        # Check cache first
        cached_result = cache.get(
            cleaned_text,
            request.transformation_type.value,
            request.additional_instructions
        )
        
        if cached_result:
            logger.info(f"Returning cached result for {request.transformation_type}")
            response_data = {
                "original_text": request.text,
                "transformed_text": cached_result,
                "transformation_type": request.transformation_type,
                "processing_time": 0.01,
                "word_count_original": len(request.text.split()),
                "word_count_transformed": len(cached_result.split())
            }
        else:
            # Process the text
            result = await text_processor.transform_text(
                cleaned_text,
                request.transformation_type,
                request.additional_instructions
            )
            
            # Cache the result
            cache.set(
                cleaned_text,
                request.transformation_type.value,
                result['transformed_text'],
                request.additional_instructions
            )
            
            response_data = {
                "original_text": result['original_text'],
                "transformed_text": result['transformed_text'],
                "transformation_type": result['transformation_type'],
                "processing_time": result['processing_time'],
                "word_count_original": result['word_count_original'],
                "word_count_transformed": result['word_count_transformed']
            }
        
        # Save to history (for both cached and non-cached results)
        try:
            logger.info(f"Attempting to save history for user: {request.user_id}")
            
            history_record = TransformationHistory(
                user_id=request.user_id or "anonymous",
                original_text=request.text,
                transformed_text=response_data['transformed_text'],
                transformation_type=request.transformation_type.value,
                additional_instructions=request.additional_instructions,
                processing_time=response_data['processing_time'],
                word_count_original=response_data['word_count_original'],
                word_count_transformed=response_data['word_count_transformed'],
                is_saved=False
            )
            
            db.add(history_record)
            db.commit()
            db.refresh(history_record)
            
            history_id = history_record.id
            logger.info(f"✅ Successfully saved to history with ID: {history_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save history: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception details: {repr(e)}")
            db.rollback()
            # Continue without history - don't fail the whole request
        
        # Add history_id to response
        response_data['history_id'] = history_id
        
        return TextTransformResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in transform_text: {str(e)}")
        error_response = create_error_response(str(e), 500)
        raise HTTPException(
            status_code=error_response["status_code"],
            detail=error_response["message"]
        )

@router.post("/batch-transform", response_model=BatchTransformResponse)
async def batch_transform_text(request: BatchTransformRequest, db: Session = Depends(get_db)):
    """Transform multiple texts at once."""
    try:
        # Validate each text
        for i, text in enumerate(request.texts):
            is_valid, error_msg = validate_text_input(text)
            if not is_valid:
                raise HTTPException(
                    status_code=400,
                    detail=f"Text at index {i}: {error_msg}"
                )
        
        # Sanitize texts
        cleaned_texts = [sanitize_text(text) for text in request.texts]
        
        # Process all texts
        result = await text_processor.batch_transform(
            cleaned_texts,
            request.transformation_type,
            request.additional_instructions
        )
        
        # Save batch to history
        try:
            for i, res in enumerate(result['results']):
                history_record = TransformationHistory(
                    user_id=request.user_id or "anonymous",
                    original_text=res['original_text'],
                    transformed_text=res['transformed_text'],
                    transformation_type=request.transformation_type.value,
                    additional_instructions=request.additional_instructions,
                    processing_time=res['processing_time'],
                    word_count_original=res['word_count_original'],
                    word_count_transformed=res['word_count_transformed'],
                    is_saved=False
                )
                db.add(history_record)
            
            db.commit()
            logger.info(f"Saved {len(result['results'])} items to history")
        except Exception as e:
            logger.error(f"Failed to save batch history: {str(e)}")
            db.rollback()
        
        return BatchTransformResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in batch_transform_text: {str(e)}")
        error_response = create_error_response(str(e), 500)
        raise HTTPException(
            status_code=error_response["status_code"],
            detail=error_response["message"]
        )

# ============= HISTORY ENDPOINTS =============

@router.get("/history", response_model=HistoryResponse)
async def get_history(
    user_id: str = Query("anonymous", description="User ID"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    transformation_type: Optional[str] = Query(None, description="Filter by transformation type"),
    saved_only: bool = Query(False, description="Show only saved items"),
    db: Session = Depends(get_db)
):
    """Get transformation history for a user (last 7 days)."""
    try:
        logger.info(f"Fetching history for user: {user_id}")
        
        # Calculate date 7 days ago
        seven_days_ago = datetime.now() - timedelta(days=settings.history_retention_days)
        
        # Build query
        query = db.query(TransformationHistory).filter(
            TransformationHistory.user_id == user_id,
            TransformationHistory.created_at >= seven_days_ago
        )
        
        # Apply filters
        if transformation_type:
            query = query.filter(TransformationHistory.transformation_type == transformation_type)
        
        if saved_only:
            query = query.filter(TransformationHistory.is_saved == True)
        
        # Get total count
        total_count = query.count()
        logger.info(f"Found {total_count} history items")
        
        # Apply pagination and ordering
        items = query.order_by(desc(TransformationHistory.created_at))\
            .offset((page - 1) * page_size)\
            .limit(page_size)\
            .all()
        
        # Convert to dict
        history_items = [HistoryItem(**item.to_dict()) for item in items]
        
        return HistoryResponse(
            items=history_items,
            total_count=total_count,
            page=page,
            page_size=page_size,
            has_more=(page * page_size) < total_count
        )
        
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")

@router.post("/history/save")
async def save_to_history(request: SaveHistoryRequest, db: Session = Depends(get_db)):
    """Mark a history item as saved (permanent)."""
    try:
        history_item = db.query(TransformationHistory).filter(
            TransformationHistory.id == request.history_id
        ).first()
        
        if not history_item:
            raise HTTPException(status_code=404, detail="History item not found")
        
        history_item.is_saved = True
        db.commit()
        
        logger.info(f"Marked item {request.history_id} as saved")
        
        return {
            "message": "Item saved successfully",
            "history_id": request.history_id,
            "is_saved": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving history item: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save item: {str(e)}")

@router.delete("/history")
async def delete_history(request: DeleteHistoryRequest, db: Session = Depends(get_db)):
    """Delete history items by IDs."""
    try:
        deleted_count = db.query(TransformationHistory).filter(
            TransformationHistory.id.in_(request.history_ids)
        ).delete(synchronize_session=False)
        
        db.commit()
        
        logger.info(f"Deleted {deleted_count} history items")
        
        return {
            "message": f"Deleted {deleted_count} items successfully",
            "deleted_count": deleted_count
        }
        
    except Exception as e:
        logger.error(f"Error deleting history: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete items: {str(e)}")

@router.delete("/history/cleanup")
async def cleanup_old_history(db: Session = Depends(get_db)):
    """Clean up history older than retention period (except saved items)."""
    try:
        cutoff_date = datetime.now() - timedelta(days=settings.history_retention_days)
        
        deleted_count = db.query(TransformationHistory).filter(
            TransformationHistory.created_at < cutoff_date,
            TransformationHistory.is_saved == False
        ).delete(synchronize_session=False)
        
        db.commit()
        
        return {
            "message": f"Cleaned up {deleted_count} old items",
            "deleted_count": deleted_count,
            "cutoff_date": cutoff_date.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error cleaning up history: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to cleanup: {str(e)}")

# ============= ORIGINAL ENDPOINTS =============

@router.get("/transformations")
async def get_available_transformations():
    """Get list of available transformation types."""
    transformations = {
        "grammar_fix": {
            "name": "Grammar Fix",
            "description": "Fix grammar, spelling, and punctuation errors",
            "icon": "✏️"
        },
        "formal": {
            "name": "Formal",
            "description": "Convert to formal, professional tone",
            "icon": "👔"
        },
        "friendly": {
            "name": "Friendly",
            "description": "Make text warm and conversational",
            "icon": "😊"
        },
        "shorten": {
            "name": "Shorten",
            "description": "Make text more concise",
            "icon": "✂️"
        },
        "expand": {
            "name": "Expand",
            "description": "Add more details and explanations",
            "icon": "📝"
        },
        "bullet": {
            "name": "Bullet Points",
            "description": "Convert to bullet point format",
            "icon": "•"
        },
        "emoji": {
            "name": "Add Emojis",
            "description": "Add appropriate emojis to text",
            "icon": "😎"
        },
        "tweetify": {
            "name": "Tweetify",
            "description": "Convert to tweet format",
            "icon": "🐦"
        }
    }
    
    return {
        "transformations": transformations,
        "total_count": len(transformations)
    }

@router.get("/cache/stats")
async def get_cache_stats():
    """Get cache statistics."""
    try:
        stats = cache.get_stats()
        return {
            "cache_stats": stats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get cache statistics")

@router.delete("/cache")
async def clear_cache():
    """Clear the cache."""
    try:
        cache.clear()
        return {
            "message": "Cache cleared successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear cache")

@router.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "WordSmith Backend API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
        "timestamp": datetime.now().isoformat()
    }