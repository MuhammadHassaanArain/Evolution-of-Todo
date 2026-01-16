"""Configuration module for the MCP Server."""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Backend API configuration
    backend_api_url: str = os.getenv("BACKEND_API_URL", "http://localhost:8000")
    backend_api_timeout: int = int(os.getenv("BACKEND_API_TIMEOUT", "30"))

    # MCP server configuration
    mcp_port: int = int(os.getenv("MCP_SERVER_PORT", "8001"))
    mcp_host: str = os.getenv("MCP_SERVER_HOST", "0.0.0.0")

    # Logging configuration
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()