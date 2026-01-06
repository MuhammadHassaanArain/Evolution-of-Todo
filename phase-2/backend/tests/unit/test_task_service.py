"""
Unit tests for the task service
"""
import pytest
from unittest.mock import Mock, patch
from src.models.task import TaskCreate
from src.services.task_service import TaskService


def test_create_task():
    """Test creating a task"""
    task_service = TaskService()

    # Create a mock session
    mock_session = Mock()

    # Create a task to create
    task_create = TaskCreate(title="Test Task", description="Test Description")
    user_id = 123  # Use integer for user_id

    # Mock the session.add, commit, and refresh methods
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock()

    # Since we can't easily create a real Task object without a DB,
    # we'll test the method call flow
    with patch('src.services.task_service.Task') as MockTask:
        mock_task_instance = Mock()
        mock_task_instance.id = "test_task_id"
        MockTask.return_value = mock_task_instance

        # Call the method
        result = task_service.create_task(mock_session, task_create, user_id)

        # Verify the session methods were called
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

        # The result should be the created task
        assert result is not None


def test_get_task_by_id():
    """Test getting a task by ID"""
    from uuid import uuid4
    task_service = TaskService()

    # Create a mock session
    mock_session = Mock()

    task_id = str(uuid4())  # Use a valid UUID string
    user_id = 123  # Use integer for user_id

    # Mock the select query and result
    mock_statement = Mock()
    mock_exec_result = Mock()
    mock_task = Mock()
    mock_task.id = task_id
    mock_exec_result.first.return_value = mock_task
    mock_session.exec.return_value = mock_exec_result

    # Call the method
    result = task_service.get_task_by_id(mock_session, task_id, user_id)

    # Verify the result
    assert result is not None
    assert result.id == task_id


def test_update_task():
    """Test updating a task"""
    from uuid import uuid4
    task_service = TaskService()

    # Create a mock session
    mock_session = Mock()

    task_id = str(uuid4())  # Use a valid UUID string
    user_id = 123  # Use integer for user_id

    # Create a task update
    from src.models.task import TaskUpdate
    task_update = TaskUpdate(title="Updated Title")

    # Mock the get_task_by_id method to return a task
    original_task = Mock()
    original_task.title = "Original Title"

    # Mock the get_task_by_id method
    with patch.object(task_service, 'get_task_by_id', return_value=original_task):
        # Call the method
        result = task_service.update_task(mock_session, task_id, task_update, user_id)

        # Verify the session methods were called
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

        # The result should be the updated task
        assert result is not None


def test_delete_task():
    """Test deleting a task"""
    from uuid import uuid4
    task_service = TaskService()

    # Create a mock session
    mock_session = Mock()

    task_id = str(uuid4())  # Use a valid UUID string
    user_id = 123  # Use integer for user_id

    # Mock the get_task_by_id method to return a task
    mock_task = Mock()

    # Mock the get_task_by_id method
    with patch.object(task_service, 'get_task_by_id', return_value=mock_task):
        # Mock the session.delete method
        mock_session.delete = Mock()

        # Call the method
        result = task_service.delete_task(mock_session, task_id, user_id)

        # Verify the session methods were called
        mock_session.delete.assert_called_once()
        mock_session.commit.assert_called_once()

        # The result should be True (success)
        assert result is True