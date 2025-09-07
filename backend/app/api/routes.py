import time
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from app.models.schemas import (
    TextTransformRequest,
    TextTransformResponse,
    BatchTransformRequest,
    BatchTransformResponse,
    HealthResponse,
    ErrorResponse
)
from app.services.text_processor_simple import text_processor
from app.utils.helpers import (
    cache,
    validate_text_input,
    sanitize_text,
    create_error_response,
    format_processing_time
)
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Check Groq API status
        groq_status = await text_processor.health_check()
        
        return HealthResponse(
            status="healthy",
            app_name=settings.app_name,
            version=settings.app_version,
            groq_api_status=groq_status.get("status", "unknown"),
            langchain_status="active" if settings.langchain_tracing_v2 else "inactive",
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
            timestamp=datetime.now().isoformat()
        )

@router.post("/transform", response_model=TextTransformResponse)
async def transform_text(request: TextTransformRequest):
    """Transform text using the specified transformation type."""
    try:
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
            return TextTransformResponse(
                original_text=request.text,
                transformed_text=cached_result,
                transformation_type=request.transformation_type,
                processing_time=0.01,  # Minimal time for cache hit
                word_count_original=len(request.text.split()),
                word_count_transformed=len(cached_result.split())
            )
        
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
        
        return TextTransformResponse(**result)
        
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
async def batch_transform_text(request: BatchTransformRequest):
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