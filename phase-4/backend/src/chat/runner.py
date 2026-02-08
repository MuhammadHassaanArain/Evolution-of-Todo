from .chat_agent import run_agent
from .models import ChatRequest, ChatResponse
from sqlmodel import Session


async def execute_chat(chat_request: ChatRequest, db_session: Session, auth_header: str = None) -> ChatResponse:
    """
    Simplified runner for OpenAI Agent SDK.

    Args:
        chat_request: Incoming chat request
        auth_header: The raw Authorization header to pass to MCP tools

    Returns:
        ChatResponse containing assistant response and tool calls
    """
    # Pass the user information and auth header to the agent
    result = await run_agent(chat_request.message, user_id=chat_request.user_id, auth_header=auth_header)

    return ChatResponse(
        conversation_id=chat_request.conversation_id or 0,
        response=result["response"],
        tool_calls=result.get("tool_calls", [])
    )
