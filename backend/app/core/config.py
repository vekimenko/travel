"""Application configuration"""
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings"""

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Interactive Article System"
    SECRET_KEY: str = "change-me-in-production"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/interactive_article_db"
    SQLALCHEMY_ECHO: bool = False

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    # External APIs
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Environment
    ENVIRONMENT: str = "development"

    # NLP
    SPACY_MODEL: str = "en_core_web_sm"
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
