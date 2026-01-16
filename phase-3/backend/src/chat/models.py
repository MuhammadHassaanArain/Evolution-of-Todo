"""Base models for the chatbot agent using OpenAI Agent SDK."""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class MessageRole(str, Enum):
    """Enumeration of message roles."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ToolCall(BaseModel):
    """Model representing a tool call made by the agent."""
    id: Optional[str] = None
    function: str
    arguments: Dict[str, Any]
    result: Optional[Any] = None  # Filled after tool execution


class ChatRequest(BaseModel):
    """Model for incoming chat requests."""
    conversation_id: Optional[int] = None
    message: str
    user_id: Optional[int] = None


class ChatResponse(BaseModel):
    """Model for outgoing chat responses."""
    conversation_id: Optional[int] = None
    response: str
    tool_calls: List[ToolCall] = []
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentState(BaseModel):
    """Model representing the state of the chat agent."""
    conversation_id: int
    user_id: int
    history: List[Dict[str, Any]] = []
    current_intent: Optional[str] = None
    pending_tool_calls: List[ToolCall] = []


class ConversationContext(BaseModel):
    """Model for conversation context information."""
    conversation_id: int
    user_id: int
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_message: Optional[str] = None
    history: List[Dict[str, Any]] = []  # Full conversation history
