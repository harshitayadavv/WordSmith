import os
from typing import List
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # FastAPI Configuration
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True
    reload: bool = True
    
    # API Keys
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    
    # Application Settings
    app_name: str = "WordSmith Backend"
    app_version: str = "1.0.0"
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "chrome-extension://*",
        "https://*.chrome-extension.invalid",
        "https://word-smith-three.vercel.app/"
        "https://word-smith-1vbnprsgu-harshita-yadavs-projects-63189c67.vercel.app",  # Domain 1
        "https://word-smith-git-main-harshita-yadavs-projects-63189c67.vercel.app",  # Domain 2
        "https://*.vercel.app",  # Allow all future Vercel deployments
    ]
    
    # Cache Settings
    cache_ttl: int = 3600
    max_cache_size: int = 1000
    
    # Model Configuration
    default_model: str = "llama-3.1-8b-instant"  # Current supported production model
    temperature: float = 0.3
    max_tokens: int = 1000
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env file

# Global settings instance
settings = Settings()

# Validate required API key
if not settings.groq_api_key:
    print("⚠️  WARNING: GROQ_API_KEY not found in environment variables")
    print("Please add your Groq API key to the .env file")
else:
    print("✅ Groq API key loaded successfully")