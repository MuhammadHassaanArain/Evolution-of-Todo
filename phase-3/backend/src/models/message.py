from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum


class RoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"


class MessageBase(SQLModel):
    user_id: str = Field(index=True)
    conversation_id: int = Field(index=True)
    role: RoleEnum
    content: str = Field(min_length=1)
    tool_calls: Optional[str] = Field(default=None)  # JSON string of tool calls


class Message(MessageBase, table=True):
    """
    Individual exchanges between user and assistant
    """
    __tablename__ = "messages"

    id: int = Field(primary_key=True)
    user_id: str = Field(index=True)
    conversation_id: int = Field(index=True)
    role: RoleEnum
    content: str = Field(min_length=1)
    tool_calls: Optional[str] = Field(default=None)  # JSON string of tool calls
    created_at: datetime = Field(default_factory=datetime.utcnow)