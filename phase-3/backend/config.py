"""Configuration settings for the chatbot backend."""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "")

    # API settings
    api_key: str = os.getenv("API_KEY", "")
    model_name: str = os.getenv("MODEL_NAME", "gemini-2.5-flash")

    # MCP server settings
    mcp_server_url: str = os.getenv("MCP_SERVER_URL", "http://localhost:8001/mcp")

    # Chat settings
    max_chat_history_tokens: int = int(os.getenv("MAX_CHAT_HISTORY_TOKENS", "4000"))

    # CORS settings
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")

    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the application settings."""
    return settings