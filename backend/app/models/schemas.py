from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

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
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "hey there how r u doing today",
                "transformation_type": "grammar_fix",
                "additional_instructions": "Make it more professional"
            }
        }

class TextTransformResponse(BaseModel):
    original_text: str
    transformed_text: str
    transformation_type: TransformationType
    processing_time: float = Field(..., description="Processing time in seconds")
    word_count_original: int
    word_count_transformed: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "original_text": "hey there how r u doing today",
                "transformed_text": "Hello there, how are you doing today?",
                "transformation_type": "grammar_fix",
                "processing_time": 1.23,
                "word_count_original": 7,
                "word_count_transformed": 7
            }
        }

class BatchTransformRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1, max_items=10)
    transformation_type: TransformationType
    additional_instructions: Optional[str] = None

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
    timestamp: str

class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int
    timestamp: str