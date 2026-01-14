from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    database_url: str = "sqlite:///./todo_app.db"
    jwt_secret: str = "your-super-secret-key-change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30
    db_echo: bool = False
    api_prefix: str = "/api"
    allowed_origins: str = "*"

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()