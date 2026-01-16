from .chat_agent import run_agent
from .models import ChatRequest, ChatResponse

async def execute_chat(chat_request: ChatRequest) -> ChatResponse:
    """
    Simplified runner for OpenAI Agent SDK.

    Args:
        chat_request: Incoming chat request

    Returns:
        ChatResponse containing assistant response and tool calls
    """
    result = await run_agent(chat_request.message)

    return ChatResponse(
        conversation_id=chat_request.conversation_id or 0,
        response=result["response"],
        tool_calls=result.get("tool_calls", [])
    )
