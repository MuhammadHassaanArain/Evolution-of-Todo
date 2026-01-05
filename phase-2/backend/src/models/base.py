from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class TimestampMixin:
    """
    Mixin class to add created_at and updated_at timestamp fields to models.
    """
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class BaseUUIDModel(SQLModel):
    """
    Base model with UUID primary key.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class BaseSQLModel(BaseUUIDModel, TimestampMixin):
    """
    Base class for all SQLModel models in the application.
    Includes UUID primary key and timestamps.
    """
    pass
