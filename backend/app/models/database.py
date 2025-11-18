from sqlalchemy import Column, String, Text, Float, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()

class TransformationHistory(Base):
    """Model for storing transformation history."""
    __tablename__ = "transformation_history"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(100), nullable=False, index=True)  # For future auth
    
    # Transformation data
    original_text = Column(Text, nullable=False)
    transformed_text = Column(Text, nullable=False)
    transformation_type = Column(String(50), nullable=False, index=True)
    additional_instructions = Column(Text, nullable=True)
    
    # Metadata
    processing_time = Column(Float, nullable=False)
    word_count_original = Column(Integer, nullable=False)
    word_count_transformed = Column(Integer, nullable=False)
    
    # Saved status
    is_saved = Column(Boolean, default=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<TransformationHistory {self.id} - {self.transformation_type}>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "original_text": self.original_text,
            "transformed_text": self.transformed_text,
            "transformation_type": self.transformation_type,
            "additional_instructions": self.additional_instructions,
            "processing_time": self.processing_time,
            "word_count_original": self.word_count_original,
            "word_count_transformed": self.word_count_transformed,
            "is_saved": self.is_saved,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }