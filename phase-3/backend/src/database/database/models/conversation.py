"""Database models for conversation and message entities."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

if TYPE_CHECKING:
    from backend.database.models.user import User  # Assuming user model exists


class ConversationBase(SQLModel):
    """Base model for Conversation with common fields."""
    title: Optional[str] = Field(default=None, max_length=255)
    user_id: int = Field(foreign_key="user.id")


class Conversation(ConversationBase, table=True):
    """Conversation model representing a user's ongoing dialogue with the chatbot."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: list["Message"] = Relationship(back_populates="conversation")


class MessageBase(SQLModel):
    """Base model for Message with common fields."""
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str = Field(max_length=10000)  # Allow longer messages
    conversation_id: int = Field(foreign_key="conversation.id")
    tool_calls: Optional[str] = Field(default=None)  # JSON string of tool calls
    tool_responses: Optional[str] = Field(default=None)  # JSON string of tool responses


class Message(MessageBase, table=True):
    """Message model representing an individual exchange in a conversation."""
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Optional[Conversation] = Relationship(back_populates="messages")


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""
    pass


class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    pass


class ConversationRead(ConversationBase):
    """Schema for reading a conversation."""
    id: int
    created_at: datetime
    updated_at: datetime
    messages: list["MessageRead"] = []


class MessageRead(MessageBase):
    """Schema for reading a message."""
    id: int
    timestamp: datetime