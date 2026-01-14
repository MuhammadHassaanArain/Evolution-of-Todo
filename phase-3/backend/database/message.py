from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
import json


class MessageBase(SQLModel):
    user_id: str = Field(index=True)
    conversation_id: int = Field(index=True, foreign_key="conversations.id")
    role: str = Field(regex="^(user|assistant)$")  # Either 'user' or 'assistant'
    content: str = Field(min_length=1)
    tool_calls: Optional[str] = Field(default=None)  # JSON string of tool calls


class Message(MessageBase, table=True):
    """
    Individual exchanges between user and assistant
    """
    __tablename__ = "messages"

    id: int = Field(primary_key=True)
    user_id: str = Field(index=True)
    conversation_id: int = Field(index=True, foreign_key="conversations.id")
    role: str = Field(regex="^(user|assistant)$")  # Either 'user' or 'assistant'
    content: str = Field(min_length=1)
    tool_calls: Optional[str] = Field(default=None)  # JSON string of tool calls
    created_at: datetime = Field(default_factory=datetime.utcnow)