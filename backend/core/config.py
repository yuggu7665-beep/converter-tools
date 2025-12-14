"""Application configuration"""
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # App Info
    APP_NAME: str = "Converter Tools API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Production-grade converter tools for AI, Media, Finance, Developer, Utility, and Education"
    
    # API Config
    API_PREFIX: str = "/api"
    DEBUG: bool = True
    
    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "https://*.netlify.app",
        "https://*.netlify.com"
    ]
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_HOUR: int = 100
    PREMIUM_RATE_LIMIT: int = 1000
    
    # External APIs (for converters that need them)
    CURRENCY_API_KEY: Optional[str] = None  # For currency converter
    CRYPTO_API_KEY: Optional[str] = None    # For crypto tracker
    
    # File Upload Limits
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB for Netlify free tier
    ALLOWED_IMAGE_TYPES: list = ["image/jpeg", "image/png", "image/webp", "image/gif"]
    ALLOWED_FILE_TYPES: list = ["application/pdf", "text/csv", "application/json"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
