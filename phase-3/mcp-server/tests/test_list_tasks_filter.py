"""Contract tests for the list_tasks tool with status filtering (User Story 3)."""

import pytest
from unittest.mock import AsyncMock, patch
from ..src.tools import list_tasks


@pytest.mark.asyncio
async def test_list_tasks_with_pending_filter():
    """Test that list_tasks works with 'pending' status filter."""
    # Mock the backend client response
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_response = [
            {"id": 1, "title": "Pending task 1", "completed": False},
            {"id": 3, "title": "Pending task 2", "completed": False}
        ]
        mock_client.get.return_value = mock_response

        # Call the list_tasks function with pending status
        result = await list_tasks(status="pending")

        # Assert the result matches expected format
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["title"] == "Pending task 1"
        assert result[0]["completed"] == False
        assert result[1]["id"] == 3
        assert result[1]["title"] == "Pending task 2"
        assert result[1]["completed"] == False

        # Verify the backend client was called with correct endpoint
        mock_client.get.assert_called_once_with("/api/tasks?status=pending")


@pytest.mark.asyncio
async def test_list_tasks_with_completed_filter():
    """Test that list_tasks works with 'completed' status filter."""
    # Mock the backend client response
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_response = [
            {"id": 2, "title": "Completed task 1", "completed": True},
            {"id": 4, "title": "Completed task 2", "completed": True}
        ]
        mock_client.get.return_value = mock_response

        # Call the list_tasks function with completed status
        result = await list_tasks(status="completed")

        # Assert the result matches expected format
        assert len(result) == 2
        assert result[0]["id"] == 2
        assert result[0]["title"] == "Completed task 1"
        assert result[0]["completed"] == True
        assert result[1]["id"] == 4
        assert result[1]["title"] == "Completed task 2"
        assert result[1]["completed"] == True

        # Verify the backend client was called with correct endpoint
        mock_client.get.assert_called_once_with("/api/tasks?status=completed")


@pytest.mark.asyncio
async def test_list_tasks_with_all_filter():
    """Test that list_tasks works with 'all' status filter."""
    # Mock the backend client response
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_response = [
            {"id": 1, "title": "Pending task", "completed": False},
            {"id": 2, "title": "Completed task", "completed": True}
        ]
        mock_client.get.return_value = mock_response

        # Call the list_tasks function with all status
        result = await list_tasks(status="all")

        # Assert the result matches expected format
        assert len(result) == 2

        # Verify the backend client was called with correct endpoint
        mock_client.get.assert_called_once_with("/api/tasks?status=all")


@pytest.mark.asyncio
async def test_list_tasks_with_invalid_status():
    """Test that list_tasks handles invalid status values properly."""
    # Test with invalid status
    result = await list_tasks(status="invalid_status")

    # Assert the result contains validation error
    assert len(result) == 1
    assert "error" in result[0]
    assert result[0]["error"] == "validation_error"
    assert "Status must be one of" in result[0]["message"]
    assert "invalid_status" in result[0]["details"]


@pytest.mark.asyncio
async def test_list_tasks_optional_status():
    """Test that list_tasks works without status parameter (defaults to all)."""
    # Mock the backend client response
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_response = [
            {"id": 1, "title": "Task 1", "completed": False},
            {"id": 2, "title": "Task 2", "completed": True}
        ]
        mock_client.get.return_value = mock_response

        # Call the list_tasks function without status
        result = await list_tasks()

        # Assert the result matches expected format
        assert len(result) == 2

        # Verify the backend client was called with correct endpoint (no status filter)
        mock_client.get.assert_called_once_with("/api/tasks")