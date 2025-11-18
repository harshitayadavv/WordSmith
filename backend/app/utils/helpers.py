import hashlib
import time
import logging
from typing import Optional, Dict, Any
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleCache:
    """Simple in-memory cache with TTL support."""
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.ttl = ttl
    
    def _make_key(self, text: str, transformation_type: str, additional_instructions: Optional[str] = None) -> str:
        """Create a cache key from input parameters."""
        content = f"{text}|{transformation_type}|{additional_instructions or ''}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _cleanup_expired(self):
        """Remove expired cache entries."""
        current_time = time.time()
        expired_keys = [
            key for key, value in self.cache.items()
            if current_time - value.get('timestamp', 0) > self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]
    
    def _enforce_size_limit(self):
        """Remove oldest entries if cache exceeds max size."""
        if len(self.cache) >= self.max_size:
            # Remove 20% of oldest entries
            entries_to_remove = int(self.max_size * 0.2)
            sorted_entries = sorted(
                self.cache.items(),
                key=lambda x: x[1].get('timestamp', 0)
            )
            for key, _ in sorted_entries[:entries_to_remove]:
                del self.cache[key]
    
    def get(self, text: str, transformation_type: str, additional_instructions: Optional[str] = None) -> Optional[str]:
        """Get cached transformation result."""
        self._cleanup_expired()
        key = self._make_key(text, transformation_type, additional_instructions)
        
        if key in self.cache:
            logger.info(f"Cache hit for transformation type: {transformation_type}")
            return self.cache[key]['result']
        
        return None
    
    def set(self, text: str, transformation_type: str, result: str, additional_instructions: Optional[str] = None):
        """Cache transformation result."""
        self._cleanup_expired()
        self._enforce_size_limit()
        
        key = self._make_key(text, transformation_type, additional_instructions)
        self.cache[key] = {
            'result': result,
            'timestamp': time.time()
        }
        logger.info(f"Cached result for transformation type: {transformation_type}")
    
    def clear(self):
        """Clear all cache entries."""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        self._cleanup_expired()
        return {
            'total_entries': len(self.cache),
            'max_size': self.max_size,
            'ttl_seconds': self.ttl,
            'memory_usage_mb': len(str(self.cache)) / (1024 * 1024)
        }

def validate_text_input(text: str) -> tuple[bool, Optional[str]]:
    """Validate text input."""
    if not text or not text.strip():
        return False, "Text cannot be empty"
    
    if len(text) > 5000:
        return False, "Text is too long. Maximum 5000 characters allowed"
    
    if len(text.strip()) < 1:
        return False, "Text must contain at least one character"
    
    return True, None

def sanitize_text(text: str) -> str:
    """Basic text sanitization."""
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    # Remove potential harmful characters (basic cleanup)
    dangerous_chars = ['<script', '</script', 'javascript:', 'onclick=', 'onerror=']
    for char in dangerous_chars:
        text = text.replace(char.lower(), '')
        text = text.replace(char.upper(), '')
    
    return text.strip()

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate basic similarity between two texts."""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 and not words2:
        return 1.0
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

def format_processing_time(seconds: float) -> str:
    """Format processing time for display."""
    if seconds < 1:
        return f"{int(seconds * 1000)}ms"
    else:
        return f"{seconds:.2f}s"

def create_error_response(error_msg: str, status_code: int = 500) -> Dict[str, Any]:
    """Create standardized error response."""
    return {
        "error": "Processing Error",
        "message": error_msg,
        "status_code": status_code,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }

# Global cache instance
cache = SimpleCache(
    max_size=settings.max_cache_size,
    ttl=settings.cache_ttl
)