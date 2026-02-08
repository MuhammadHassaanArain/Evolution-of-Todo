"""
Task Service

This module provides the business logic for managing tasks,
including adding, viewing, updating, deleting, and toggling
completion status of tasks. All operations are performed in-memory.
"""

from typing import List, Optional, Dict, Any
from todo.models.task import Task


class TaskService:
    """
    Service class for managing tasks with in-memory storage.
    Provides methods for all CRUD operations and status toggling.
    """

    def __init__(self):
        """
        Initialize the TaskService with an empty in-memory task list
        and a counter for generating unique IDs.
        """
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def _generate_id(self) -> int:
        """
        Generate a unique ID for a new task.

        Returns:
            int: Unique ID for the new task
        """
        new_id = self._next_id
        self._next_id += 1
        return new_id

    def add_task(self, title: str, description: str = "") -> Dict[str, Any]:
        """
        Add a new task to the in-memory list.

        Args:
            title (str): Task title (required)
            description (str): Task description (optional)

        Returns:
            dict: Result dictionary with success status, message, and task ID
        """
        try:
            # Validate title before creating the task
            if not title or not isinstance(title, str) or not title.strip():
                return {
                    "success": False,
                    "message": "Title is required and must be a non-empty string",
                    "task_id": None
                }

            # Generate unique ID for the new task
            task_id = self._generate_id()

            # Create and add the new task
            task = Task(task_id=task_id, title=title, description=description)
            self._tasks.append(task)

            return {
                "success": True,
                "message": f"Task added with ID {task_id}",
                "task_id": task_id
            }
        except ValueError as e:
            return {
                "success": False,
                "message": str(e),
                "task_id": None
            }

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from memory.

        Returns:
            List[Task]: List of all tasks in memory
        """
        return self._tasks.copy()  # Return a copy to prevent external modification

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a specific task by ID.

        Args:
            task_id (int): ID of the task to retrieve

        Returns:
            Task | None: Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Update task details.

        Args:
            task_id (int): ID of the task to update
            title (str | None): New title (optional)
            description (str | None): New description (optional)

        Returns:
            dict: Result dictionary with success status and message
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return {
                "success": False,
                "message": f"Task with ID {task_id} not found"
            }

        # Update only the provided fields
        if title is not None:
            task.title = title.strip()
        if description is not None:
            task.description = description

        return {
            "success": True,
            "message": f"Task {task_id} updated successfully"
        }

    def delete_task(self, task_id: int) -> Dict[str, Any]:
        """
        Delete a task by ID.

        Args:
            task_id (int): ID of the task to delete

        Returns:
            dict: Result dictionary with success status and message
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return {
                "success": False,
                "message": f"Task with ID {task_id} not found"
            }

        self._tasks.remove(task)
        return {
            "success": True,
            "message": f"Task {task_id} deleted successfully"
        }

    def toggle_task_completion(self, task_id: int) -> Dict[str, Any]:
        """
        Toggle completion status of a task.

        Args:
            task_id (int): ID of the task to toggle

        Returns:
            dict: Result dictionary with success status, message, and new completion status
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return {
                "success": False,
                "message": f"Task with ID {task_id} not found",
                "completed": None
            }

        # Toggle the completion status
        task.completed = not task.completed

        status_text = "Complete" if task.completed else "Incomplete"
        return {
            "success": True,
            "message": f"Task {task_id} marked as {status_text}",
            "completed": task.completed
        }

    def get_next_id(self) -> int:
        """
        Get the next available ID without incrementing the counter.

        Returns:
            int: The next available ID
        """
        return self._next_id