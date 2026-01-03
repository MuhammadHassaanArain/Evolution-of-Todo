"""
Unit tests for the Task model.

This module tests the Task class functionality including
initialization, validation, and string representations.
"""

import pytest
from todo.models.task import Task


class TestTask:
    """Test cases for the Task model."""

    def test_task_initialization(self):
        """Test successful task initialization with valid data."""
        task = Task(task_id=1, title="Test Task", description="Test Description", completed=False)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_task_initialization_with_defaults(self):
        """Test task initialization with default values."""
        task = Task(task_id=1, title="Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False

    def test_task_initialization_with_empty_description(self):
        """Test task initialization with empty description."""
        task = Task(task_id=1, title="Test Task", description="")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""

    def test_task_initialization_with_completed_true(self):
        """Test task initialization with completed=True."""
        task = Task(task_id=1, title="Test Task", completed=True)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.completed is True

    def test_task_initialization_invalid_title(self):
        """Test task initialization with invalid title raises ValueError."""
        with pytest.raises(ValueError):
            Task(task_id=1, title="")

        with pytest.raises(ValueError):
            Task(task_id=1, title="   ")  # Only whitespace

        with pytest.raises(ValueError):
            Task(task_id=1, title=None)

    def test_task_initialization_title_stripping(self):
        """Test that title is properly stripped of whitespace."""
        task = Task(task_id=1, title="  Test Task  ")

        assert task.title == "Test Task"

    def test_task_str_representation(self):
        """Test string representation of the task."""
        task = Task(task_id=1, title="Test Task", completed=False)
        expected = "[○] 1. Test Task"

        assert str(task) == expected

    def test_task_str_representation_completed(self):
        """Test string representation of a completed task."""
        task = Task(task_id=1, title="Test Task", completed=True)
        expected = "[✓] 1. Test Task"

        assert str(task) == expected

    def test_task_repr_representation(self):
        """Test detailed string representation of the task."""
        task = Task(task_id=1, title="Test Task", description="Test Description", completed=True)
        expected = "Task(id=1, title='Test Task', description='Test Description', completed=True)"

        assert repr(task) == expected

    def test_task_to_dict(self):
        """Test conversion of task to dictionary."""
        task = Task(task_id=1, title="Test Task", description="Test Description", completed=True)
        expected_dict = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "completed": True
        }

        assert task.to_dict() == expected_dict

    def test_task_from_dict(self):
        """Test creation of task from dictionary."""
        data = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "completed": True
        }
        task = Task.from_dict(data)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is True

    def test_task_from_dict_with_missing_description(self):
        """Test creation of task from dictionary with missing description."""
        data = {
            "id": 1,
            "title": "Test Task",
            "completed": False
        }
        task = Task.from_dict(data)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False

    def test_task_from_dict_with_missing_completed(self):
        """Test creation of task from dictionary with missing completed status."""
        data = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description"
        }
        task = Task.from_dict(data)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False