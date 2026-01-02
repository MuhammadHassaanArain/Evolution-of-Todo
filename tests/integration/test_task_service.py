"""
Integration tests for the Task Service.

This module tests the TaskService class functionality including
all CRUD operations and status toggling.
"""

import pytest
from todo.services.task_service import TaskService


class TestTaskService:
    """Test cases for the TaskService."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.service = TaskService()

    def test_initial_state(self):
        """Test initial state of the service."""
        assert len(self.service.get_all_tasks()) == 0
        assert self.service.get_next_id() == 1

    def test_add_task_success(self):
        """Test successful addition of a task."""
        result = self.service.add_task("Test Task", "Test Description")

        assert result["success"] is True
        assert result["message"] == "Task added with ID 1"
        assert result["task_id"] == 1

        tasks = self.service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 1
        assert tasks[0].title == "Test Task"
        assert tasks[0].description == "Test Description"
        assert tasks[0].completed is False

    def test_add_task_without_description(self):
        """Test adding a task without a description."""
        result = self.service.add_task("Test Task")

        assert result["success"] is True
        assert result["message"] == "Task added with ID 1"
        assert result["task_id"] == 1

        tasks = self.service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].description == ""

    def test_add_task_invalid_title(self):
        """Test adding a task with invalid title."""
        result = self.service.add_task("")
        assert result["success"] is False
        assert "Title is required" in result["message"]

        result = self.service.add_task("   ")
        assert result["success"] is False
        assert "Title is required" in result["message"]

        tasks = self.service.get_all_tasks()
        assert len(tasks) == 0

    def test_get_all_tasks(self):
        """Test retrieving all tasks."""
        # Add a few tasks
        self.service.add_task("Task 1")
        self.service.add_task("Task 2", "Description for Task 2")

        tasks = self.service.get_all_tasks()
        assert len(tasks) == 2

        # Verify the tasks
        assert tasks[0].id == 1
        assert tasks[0].title == "Task 1"
        assert tasks[1].id == 2
        assert tasks[1].title == "Task 2"
        assert tasks[1].description == "Description for Task 2"

    def test_get_task_by_id_success(self):
        """Test retrieving a task by ID."""
        self.service.add_task("Test Task", "Description")

        task = self.service.get_task_by_id(1)
        assert task is not None
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Description"
        assert task.completed is False

    def test_get_task_by_id_not_found(self):
        """Test retrieving a non-existent task."""
        task = self.service.get_task_by_id(999)
        assert task is None

        # Add a task and try to get a different ID
        self.service.add_task("Test Task")
        task = self.service.get_task_by_id(2)
        assert task is None

    def test_update_task_success(self):
        """Test successful task update."""
        self.service.add_task("Original Task", "Original Description")

        result = self.service.update_task(1, title="Updated Task", description="Updated Description")
        assert result["success"] is True
        assert result["message"] == "Task 1 updated successfully"

        task = self.service.get_task_by_id(1)
        assert task.title == "Updated Task"
        assert task.description == "Updated Description"

    def test_update_task_partial(self):
        """Test partial task update (only title or only description)."""
        self.service.add_task("Original Task", "Original Description")

        # Update only the title
        result = self.service.update_task(1, title="Updated Title")
        assert result["success"] is True

        task = self.service.get_task_by_id(1)
        assert task.title == "Updated Title"
        assert task.description == "Original Description"  # Should remain unchanged

        # Update only the description
        result = self.service.update_task(1, description="Updated Description")
        assert result["success"] is True

        task = self.service.get_task_by_id(1)
        assert task.title == "Updated Title"  # Should remain unchanged
        assert task.description == "Updated Description"

    def test_update_task_not_found(self):
        """Test updating a non-existent task."""
        result = self.service.update_task(999, title="New Title")
        assert result["success"] is False
        assert "not found" in result["message"]

    def test_delete_task_success(self):
        """Test successful task deletion."""
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")

        result = self.service.delete_task(1)
        assert result["success"] is True
        assert result["message"] == "Task 1 deleted successfully"

        tasks = self.service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 2

        # Verify task 1 is gone
        task = self.service.get_task_by_id(1)
        assert task is None

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        result = self.service.delete_task(999)
        assert result["success"] is False
        assert "not found" in result["message"]

    def test_toggle_task_completion_success(self):
        """Test successful toggling of task completion."""
        self.service.add_task("Test Task")

        # Initially should be incomplete
        task = self.service.get_task_by_id(1)
        assert task.completed is False

        # Toggle to complete
        result = self.service.toggle_task_completion(1)
        assert result["success"] is True
        assert "marked as Complete" in result["message"]
        assert result["completed"] is True

        task = self.service.get_task_by_id(1)
        assert task.completed is True

        # Toggle back to incomplete
        result = self.service.toggle_task_completion(1)
        assert result["success"] is True
        assert "marked as Incomplete" in result["message"]
        assert result["completed"] is False

        task = self.service.get_task_by_id(1)
        assert task.completed is False

    def test_toggle_task_completion_not_found(self):
        """Test toggling completion of a non-existent task."""
        result = self.service.toggle_task_completion(999)
        assert result["success"] is False
        assert "not found" in result["message"]
        assert result["completed"] is None

    def test_unique_id_generation(self):
        """Test that unique IDs are generated correctly."""
        result1 = self.service.add_task("Task 1")
        result2 = self.service.add_task("Task 2")
        result3 = self.service.add_task("Task 3")

        assert result1["task_id"] == 1
        assert result2["task_id"] == 2
        assert result3["task_id"] == 3

        # Verify the next ID would be 4
        assert self.service.get_next_id() == 4

    def test_multiple_operations_sequence(self):
        """Test a sequence of operations."""
        # Add multiple tasks
        result1 = self.service.add_task("Task 1", "Description 1")
        result2 = self.service.add_task("Task 2", "Description 2")
        result3 = self.service.add_task("Task 3", "Description 3")

        assert result1["success"] and result2["success"] and result3["success"]

        # Verify all tasks exist
        tasks = self.service.get_all_tasks()
        assert len(tasks) == 3

        # Update one task
        update_result = self.service.update_task(2, title="Updated Task 2")
        assert update_result["success"] is True

        # Toggle completion of another
        toggle_result = self.service.toggle_task_completion(1)
        assert toggle_result["success"] is True

        # Delete one task
        delete_result = self.service.delete_task(3)
        assert delete_result["success"] is True

        # Verify final state
        tasks = self.service.get_all_tasks()
        assert len(tasks) == 2

        # Check specific task properties
        task1 = self.service.get_task_by_id(1)
        assert task1.completed is True
        assert task1.title == "Task 1"

        task2 = self.service.get_task_by_id(2)
        assert task2.title == "Updated Task 2"