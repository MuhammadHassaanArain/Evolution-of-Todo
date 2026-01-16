"""Utility functions for the MCP Server."""

import logging
import os
from typing import Dict, Any
from .config import settings


def setup_logging():
    """Setup logging configuration."""
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
        ]
    )


def log_error(error_message: str, context: Dict[str, Any] = None):
    """Log an error with optional context."""
    logger = logging.getLogger(__name__)
    if context:
        logger.error(f"{error_message} | Context: {context}")
    else:
        logger.error(error_message)


def log_info(message: str, context: Dict[str, Any] = None):
    """Log an info message with optional context."""
    logger = logging.getLogger(__name__)
    if context:
        logger.info(f"{message} | Context: {context}")
    else:
        logger.info(message)


def format_error_response(error_code: str, message: str, details: str = None) -> Dict[str, Any]:
    """Format a standardized error response."""
    response = {
        "error": error_code,
        "message": message
    }
    if details:
        response["details"] = details

    return response


def validate_task_id(task_id: int) -> bool:
    """Validate that the task ID is a positive integer."""
    return isinstance(task_id, int) and task_id > 0


def validate_title(title: str) -> bool:
    """Validate that the title is a non-empty string."""
    return isinstance(title, str) and len(title.strip()) > 0