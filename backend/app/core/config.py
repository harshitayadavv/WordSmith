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
    
    # Database Configuration
    # For local development, use SQLite by default
    # For production (AWS), use PostgreSQL
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./wordsmith.db"  # Local SQLite for testing
    )
    
    # PostgreSQL settings (used when DATABASE_URL is PostgreSQL)
    postgres_user: str = os.getenv("POSTGRES_USER", "wordsmith")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "")
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")
    postgres_db: str = os.getenv("POSTGRES_DB", "wordsmith_db")
    
    # Application Settings
    app_name: str = "WordSmith Backend"
    app_version: str = "1.0.0"
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",  # Vite dev server
        "chrome-extension://*",
        "https://*.chrome-extension.invalid",
        "https://word-smith-three.vercel.app",
        "https://word-smith-1vbnprsgu-harshita-yadavs-projects-63189c67.vercel.app",
        "https://word-smith-git-main-harshita-yadavs-projects-63189c67.vercel.app",
        "https://*.vercel.app",
    ]
    
    # Cache Settings
    cache_ttl: int = 3600
    max_cache_size: int = 1000
    
    # Model Configuration
    default_model: str = "llama-3.1-8b-instant"
    temperature: float = 0.3
    max_tokens: int = 1000
    
    # History Settings
    history_retention_days: int = 7  # Keep history for 7 days
    max_history_per_user: int = 100  # Maximum history items per user
    
    # LangChain (optional)
    langchain_tracing_v2: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

# Global settings instance
settings = Settings()

# Build PostgreSQL URL if credentials are provided
if settings.postgres_password and "sqlite" not in settings.database_url:
    settings.database_url = (
        f"postgresql://{settings.postgres_user}:{settings.postgres_password}"
        f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    )

# Validate required API key
if not settings.groq_api_key:
    print("⚠️  WARNING: GROQ_API_KEY not found in environment variables")
    print("Please add your Groq API key to the .env file")
else:
    print("✅ Groq API key loaded successfully")

print(f"✅ Database: {settings.database_url.split('@')[0]}@***")