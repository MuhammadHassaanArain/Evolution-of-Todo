from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL")
    app_name: str = "Todo Backend API"
    app_version: str = "0.1.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    # JWT settings (match your env names)
    jwt_secret: str = os.getenv("JWT_SECRET", "dev-secret-key-change-in-production")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expiration_minutes: int = int(os.getenv("JWT_EXPIRATION_MINUTES", "30"))

    # CORS settings
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")
    # API settings
    api_prefix: str = os.getenv("API_PREFIX", "/api")


    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
