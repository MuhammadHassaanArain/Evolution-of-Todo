from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class ConversationBase(SQLModel):
    user_id: str = Field(index=True)
    thread_id: str = Field(unique=True, index=True)
    title: Optional[str] = Field(default=None)


class Conversation(ConversationBase, table=True):
    """
    Represents a user's chat session with the AI assistant
    """
    __tablename__ = "conversations"

    id: int = Field(primary_key=True)
    user_id: str = Field(index=True)
    thread_id: str = Field(unique=True, index=True)
    title: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)