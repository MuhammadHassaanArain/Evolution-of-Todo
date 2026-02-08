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

    api_key: str = os.getenv("API_KEY", "")
    model_name: str = os.getenv("MODEL_NAME", "gemini-2.5-flash")
    mcp_server_url: str = os.getenv("MCP_SERVER_URL", "http://localhost:8001/mcp")

    # Chat settings
    max_chat_history_tokens: int = int(os.getenv("MAX_CHAT_HISTORY_TOKENS", "4000"))

    class Config:
        env_file = ".env"


settings = Settings()