from sqlmodel import SQLModel
from typing import Any
import uuid
from datetime import datetime
from pydantic import Field


class BaseUUIDModel(SQLModel):
    """
    Base model that includes common fields for all models
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Override to automatically update the updated_at field when any field is changed
        """
        if name != "updated_at":
            super().__setattr__("updated_at", datetime.utcnow())
        super().__setattr__(name, value)