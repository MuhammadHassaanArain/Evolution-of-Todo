"""Chat endpoint for the chatbot backend."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict, Any
from ..api.auth_dependency import get_current_user
from ..database.session import get_session  # Updated import path
from ..chat.runner import execute_chat  # Updated import path
from ..chat.models import ChatRequest, ChatResponse  # Updated import path
from ..utils.logging import setup_logger  # Updated import path
from ..utils.errors import handle_chat_error  # Updated import path


router = APIRouter(tags=["chat"])
logger = setup_logger("chat_endpoint")


@router.post("/chat", response_model=ChatResponse)
def chat(
    chat_request: ChatRequest,
    current_user = Depends(get_current_user),
    db_session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Main chat endpoint that processes user messages and returns AI-generated responses.

    Args:
        chat_request: The incoming chat request with message and optional conversation ID
        current_user: The authenticated user making the request
        db_session: Database session for persistence

    Returns:
        ChatResponse with conversation ID, response, and tool calls made
    """
    try:
        # Validate input
        if not chat_request.message or not chat_request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message cannot be empty"
            )

        # Set the user ID from the authenticated user
        chat_request.user_id = current_user.id

        # Execute the chat request using the chat runner
        response = execute_chat.execute_chat(chat_request, db_session)

        return response

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the error
        logger.error(f"Error in chat endpoint: {str(e)}")

        # Handle the error gracefully
        error_response = handle_chat_error(
            e,
            logger,
            context={
                "user_id": current_user.id if current_user else None,
                "conversation_id": chat_request.conversation_id
            }
        )

        # Return a user-friendly error response
        return ChatResponse(
            conversation_id=chat_request.conversation_id or -1,
            response=error_response.get("message", "Sorry, I encountered an error processing your request."),
            tool_calls=[]
        )


@router.get("/chat/health")
def chat_health() -> Dict[str, Any]:
    """
    Health check endpoint for the chat service.

    Returns:
        Dictionary with health status information
    """
    try:
        return {
            "status": "healthy",
            "service": "chatbot-backend",
            "details": {
                "agent_loaded": True,
                "mcp_connection": True  # In a real implementation, you'd check actual MCP connectivity
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chat service is not healthy"
        )