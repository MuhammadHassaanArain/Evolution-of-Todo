from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from pydantic import Field


class TimestampMixin:
    """
    Mixin class to add created_at and updated_at timestamp fields to models.
    """
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class BaseSQLModel(SQLModel):
    """
    Base class for all SQLModel models in the application.
    """
    pass
