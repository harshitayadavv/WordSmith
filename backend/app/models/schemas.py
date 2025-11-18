from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

class TransformationType(str, Enum):
    GRAMMAR_FIX = "grammar_fix"
    FORMAL = "formal"
    FRIENDLY = "friendly"
    SHORTEN = "shorten"
    EXPAND = "expand"
    BULLET = "bullet"
    EMOJI = "emoji"
    TWEETIFY = "tweetify"

class TextTransformRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Text to transform")
    transformation_type: TransformationType = Field(..., description="Type of transformation to apply")
    additional_instructions: Optional[str] = Field(None, max_length=500, description="Additional custom instructions")
    user_id: Optional[str] = Field(default="anonymous", description="User ID for history tracking")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "hey there how r u doing today",
                "transformation_type": "grammar_fix",
                "additional_instructions": "Make it more professional",
                "user_id": "user_123"
            }
        }

class TextTransformResponse(BaseModel):
    original_text: str
    transformed_text: str
    transformation_type: TransformationType
    processing_time: float = Field(..., description="Processing time in seconds")
    word_count_original: int
    word_count_transformed: int
    history_id: Optional[str] = None  # ID of saved history record
    
    class Config:
        json_schema_extra = {
            "example": {
                "original_text": "hey there how r u doing today",
                "transformed_text": "Hello there, how are you doing today?",
                "transformation_type": "grammar_fix",
                "processing_time": 1.23,
                "word_count_original": 7,
                "word_count_transformed": 7,
                "history_id": "abc123"
            }
        }

class BatchTransformRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1, max_items=10)
    transformation_type: TransformationType
    additional_instructions: Optional[str] = None
    user_id: Optional[str] = Field(default="anonymous")

class BatchTransformResponse(BaseModel):
    results: List[TextTransformResponse]
    total_processing_time: float
    successful_transformations: int
    failed_transformations: int

class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    groq_api_status: str
    langchain_status: str
    database_status: str
    timestamp: str

class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int
    timestamp: str

# History-related schemas
class HistoryItem(BaseModel):
    id: str
    user_id: str
    original_text: str
    transformed_text: str
    transformation_type: str
    additional_instructions: Optional[str]
    processing_time: float
    word_count_original: int
    word_count_transformed: int
    is_saved: bool
    created_at: str
    updated_at: Optional[str]
    
    class Config:
        from_attributes = True

class HistoryResponse(BaseModel):
    items: List[HistoryItem]
    total_count: int
    page: int
    page_size: int
    has_more: bool

class SaveHistoryRequest(BaseModel):
    history_id: str

class DeleteHistoryRequest(BaseModel):
    history_ids: List[str]