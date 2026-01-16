"""Integration tests for the MCP Server tools."""

import pytest
from unittest.mock import AsyncMock, patch
from ..src.tools import add_task, list_tasks, update_task, complete_task, delete_task


@pytest.mark.asyncio
async def test_full_task_lifecycle():
    """Test the complete lifecycle of a task using all tools."""
    # Mock the backend client responses for the full lifecycle
    with patch('mcp_server.src.client.backend_client') as mock_client:
        # Step 1: Add a task
        mock_client.post.return_value = {"id": 1, "title": "Test task", "completed": False}
        add_result = await add_task(title="Test task", description="A test task")

        assert add_result["task_id"] == 1
        assert add_result["status"] == "created"
        assert add_result["title"] == "Test task"

        # Verify add_task called the right endpoint
        mock_client.post.assert_called_with("/api/tasks", json_data={
            "title": "Test task",
            "description": "A test task"
        })

        # Reset the mock to control the next call
        mock_client.reset_mock()
        mock_client.get.return_value = [{"id": 1, "title": "Test task", "completed": False, "description": "A test task"}]

        # Step 2: List tasks
        list_result = await list_tasks()

        assert len(list_result) == 1
        assert list_result[0]["id"] == 1
        assert list_result[0]["title"] == "Test task"

        # Verify list_tasks called the right endpoint
        mock_client.get.assert_called_with("/api/tasks")

        # Reset the mock to control the next call
        mock_client.reset_mock()
        mock_client.put.return_value = {"id": 1, "title": "Updated test task", "completed": False, "description": "A test task"}

        # Step 3: Update task
        update_result = await update_task(task_id=1, title="Updated test task")

        assert update_result["task_id"] == 1
        assert update_result["status"] == "updated"
        assert update_result["title"] == "Updated test task"

        # Verify update_task called the right endpoint
        mock_client.put.assert_called_with("/api/tasks/1", json_data={"title": "Updated test task"})

        # Reset the mock to control the next call
        mock_client.reset_mock()
        mock_client.patch.return_value = {"id": 1, "title": "Updated test task", "completed": True}

        # Step 4: Complete task
        complete_result = await complete_task(task_id=1)

        assert complete_result["task_id"] == 1
        assert complete_result["status"] == "completed"
        assert complete_result["title"] == "Updated test task"

        # Verify complete_task called the right endpoint
        mock_client.patch.assert_called_with("/api/tasks/1/complete")

        # Reset the mock to control the next call
        mock_client.reset_mock()
        mock_client.delete.return_value = {"id": 1, "title": "Updated test task", "completed": True}

        # Step 5: Delete task
        delete_result = await delete_task(task_id=1)

        assert delete_result["task_id"] == 1
        assert delete_result["status"] == "deleted"
        assert delete_result["title"] == "Updated test task"

        # Verify delete_task called the right endpoint
        mock_client.delete.assert_called_with("/api/tasks/1")


@pytest.mark.asyncio
async def test_multiple_tasks_lifecycle():
    """Test working with multiple tasks."""
    with patch('mcp_server.src.client.backend_client') as mock_client:
        # Add first task
        mock_client.post.return_value = {"id": 1, "title": "First task", "completed": False}
        first_add = await add_task(title="First task")
        assert first_add["task_id"] == 1

        # Add second task
        mock_client.reset_mock()
        mock_client.post.return_value = {"id": 2, "title": "Second task", "completed": False}
        second_add = await add_task(title="Second task")
        assert second_add["task_id"] == 2

        # List all tasks
        mock_client.reset_mock()
        mock_client.get.return_value = [
            {"id": 1, "title": "First task", "completed": False},
            {"id": 2, "title": "Second task", "completed": False}
        ]
        all_tasks = await list_tasks()
        assert len(all_tasks) == 2

        # Update only the second task
        mock_client.reset_mock()
        mock_client.put.return_value = {"id": 2, "title": "Updated Second task", "completed": False}
        update_second = await update_task(task_id=2, title="Updated Second task")
        assert update_second["task_id"] == 2
        assert update_second["title"] == "Updated Second task"

        # Complete the first task
        mock_client.reset_mock()
        mock_client.patch.return_value = {"id": 1, "title": "First task", "completed": True}
        complete_first = await complete_task(task_id=1)
        assert complete_first["task_id"] == 1
        assert complete_first["status"] == "completed"