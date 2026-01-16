"""Logging utilities for the chatbot backend."""

import logging
from typing import Any
import json
from datetime import datetime


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the specified name and level.

    Args:
        name: Name of the logger
        level: Logging level

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding multiple handlers if logger already exists
    if logger.handlers:
        return logger

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def log_chat_interaction(
    logger: logging.Logger,
    user_id: int,
    conversation_id: int,
    input_message: str,
    output_response: str,
    tool_calls: list = None
) -> None:
    """
    Log a chat interaction with structured data.

    Args:
        logger: Logger instance to use
        user_id: ID of the user
        conversation_id: ID of the conversation
        input_message: Original user message
        output_response: Agent's response
        tool_calls: List of tools called during the interaction
    """
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "conversation_id": conversation_id,
        "input_message": input_message,
        "output_response": output_response,
        "tool_calls": tool_calls or [],
        "event_type": "chat_interaction"
    }

    logger.info(json.dumps(log_data))


def log_error(
    logger: logging.Logger,
    error: Exception,
    context: dict = None,
    user_id: int = None,
    conversation_id: int = None
) -> None:
    """
    Log an error with context information.

    Args:
        logger: Logger instance to use
        error: Exception that occurred
        context: Additional context information
        user_id: ID of the user (if applicable)
        conversation_id: ID of the conversation (if applicable)
    """
    error_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context or {},
        "user_id": user_id,
        "conversation_id": conversation_id,
        "event_type": "error"
    }

    logger.error(json.dumps(error_data))