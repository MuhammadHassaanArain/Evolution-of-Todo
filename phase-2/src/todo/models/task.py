"""
Task Model

This module defines the Task class that represents a single todo item
with attributes like id, title, description, and completion status.
"""

from typing import Optional


class Task:
    """
    Represents a single todo item with ID, title, description, and completion status.

    Attributes:
        id (int): Unique identifier for the task
        title (str): Task title (required)
        description (str): Task description (optional, default: "")
        completed (bool): Completion status (default: False)
    """

    def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False):
        """
        Initialize a Task instance.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Task title (required)
            description (str): Task description (optional)
            completed (bool): Completion status (optional, default: False)

        Raises:
            ValueError: If title is empty or None
        """
        if not title or not isinstance(title, str) or not title.strip():
            raise ValueError("Title is required and must be a non-empty string")

        self.id = task_id
        self.title = title.strip()
        self.description = description or ""
        self.completed = completed

    def __str__(self) -> str:
        """
        Return a string representation of the task.

        Returns:
            str: Formatted string with task details
        """
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}. {self.title}"

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the task.

        Returns:
            str: Detailed representation with all attributes
        """
        return (f"Task(id={self.id}, title='{self.title}', "
                f"description='{self.description}', completed={self.completed})")

    def to_dict(self) -> dict:
        """
        Convert the task to a dictionary representation.

        Returns:
            dict: Dictionary with task attributes
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """
        Create a Task instance from a dictionary.

        Args:
            data (dict): Dictionary with task attributes

        Returns:
            Task: New Task instance
        """
        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False)
        )