"""Error handling utilities for the chatbot backend."""

from typing import Optional, Dict, Any
from fastapi import HTTPException, status
import logging


class ChatBotError(Exception):
    """Base exception class for chatbot-related errors."""
    pass


class AgentError(ChatBotError):
    """Exception raised when there's an error with the AI agent."""
    pass


class MCPIntegrationError(ChatBotError):
    """Exception raised when there's an error with MCP integration."""
    pass


class ConversationError(ChatBotError):
    """Exception raised when there's an error with conversation handling."""
    pass


def handle_chat_error(
    error: Exception,
    logger: logging.Logger,
    user_id: Optional[int] = None,
    conversation_id: Optional[int] = None,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Handle chat-related errors and return appropriate responses.

    Args:
        error: The error that occurred
        logger: Logger to log the error
        user_id: ID of the user (if available)
        conversation_id: ID of the conversation (if available)
        context: Additional context information

    Returns:
        Dictionary with error information formatted for response
    """
    from .logging import log_error

    log_error(logger, error, context, user_id, conversation_id)

    # Determine response based on error type
    if isinstance(error, AgentError):
        return {
            "error": "agent_error",
            "message": "Sorry, I had trouble processing your request. Please try again.",
            "details": str(error) if context and context.get("include_details", False) else None
        }
    elif isinstance(error, MCPIntegrationError):
        return {
            "error": "mcp_error",
            "message": "I'm having trouble connecting to my task management tools. Please try again later.",
            "details": str(error) if context and context.get("include_details", False) else None
        }
    elif isinstance(error, ConversationError):
        return {
            "error": "conversation_error",
            "message": "There was an issue with your conversation. Please start a new one.",
            "details": str(error) if context and context.get("include_details", False) else None
        }
    else:
        return {
            "error": "unknown_error",
            "message": "An unexpected error occurred. Please try again.",
            "details": str(error) if context and context.get("include_details", False) else None
        }


def raise_validation_error(detail: str) -> None:
    """
    Raise a validation error with the given detail.

    Args:
        detail: Detail message for the error
    """
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )


def raise_not_found_error(item_type: str, item_id: Any) -> None:
    """
    Raise a not found error for a specific item.

    Args:
        item_type: Type of item that was not found
        item_id: ID of the item that was not found
    """
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{item_type} with ID {item_id} not found"
    )


def raise_unauthorized_error(detail: str = "Not authorized") -> None:
    """
    Raise an unauthorized error.

    Args:
        detail: Detail message for the error
    """
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail
    )