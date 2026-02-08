from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings
    database_url: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://user:password@localhost:5432/todo_app"
    )
    
    # App settings
    app_name: str = "Todo Backend API"
    app_version: str = "0.1.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # JWT settings for authentication
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS settings
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")

    class Config:
        env_file = ".env"

# Create a single instance of settings
settings = Settings()
