"""Application configuration settings."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings.

    Loads configuration from environment variables.
    """
    # Application
    app_name: str = "Visual Editor API"
    app_version: str = "1.0.0"
    debug: bool = False

    # API
    api_v1_prefix: str = "/api/v1"
    cors_origins: list = ["*"]

    # Storage
    storage_base_path: str = "./storage"

    # Database (for future PostgreSQL implementation)
    database_url: Optional[str] = None

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
