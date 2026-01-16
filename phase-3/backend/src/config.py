import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    jwt_secret: str = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expiration_minutes: int = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))
    db_echo: bool = os.getenv("DB_ECHO", "False").lower() == "true"
    api_prefix: str = "/api"
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")
    next_public_api_url: str | None = None
    next_public_api_base_url: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()