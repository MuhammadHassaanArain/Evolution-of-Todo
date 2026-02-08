"""Contract tests for the list_tasks tool."""

import pytest
from unittest.mock import AsyncMock, patch
from mcp import tool
from ..src.tools import list_tasks


@pytest.mark.asyncio
async def test_list_tasks_success():
    """Test that list_tasks successfully retrieves tasks."""
    # Mock the backend client response
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_response = [
            {"id": 1, "title": "Task 1", "completed": False},
            {"id": 2, "title": "Task 2", "completed": True, "description": "A description"}
        ]
        mock_client.get.return_value = mock_response

        # Call the list_tasks function
        result = await list_tasks()

        # Assert the result matches expected format
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["title"] == "Task 1"
        assert result[0]["completed"] == False
        assert result[1]["id"] == 2
        assert result[1]["title"] == "Task 2"
        assert result[1]["completed"] == True
        assert result[1]["description"] == "A description"

        # Assert the backend client was called with correct parameters
        mock_client.get.assert_called_once_with("/api/tasks")


@pytest.mark.asyncio
async def test_list_tasks_with_status_filter():
    """Test that list_tasks works with status filter."""
    # Mock the backend client response
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_response = [{"id": 1, "title": "Pending task", "completed": False}]
        mock_client.get.return_value = mock_response

        # Call the list_tasks function with status filter
        result = await list_tasks(status="pending")

        # Assert the result matches expected format
        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["title"] == "Pending task"
        assert result[0]["completed"] == False

        # Assert the backend client was called with correct parameters
        mock_client.get.assert_called_once_with("/api/tasks?status=pending")


@pytest.mark.asyncio
async def test_list_tasks_invalid_status():
    """Test that list_tasks handles invalid status parameter."""
    # Call the list_tasks function with invalid status
    result = await list_tasks(status="invalid_status")

    # Assert the result contains validation error
    assert len(result) == 1
    assert "error" in result[0]
    assert result[0]["error"] == "validation_error"
    assert "Status must be one of" in result[0]["message"]


@pytest.mark.asyncio
async def test_list_tasks_backend_error():
    """Test that list_tasks handles backend API errors gracefully."""
    from httpx import RequestError

    # Mock the backend client to raise a RequestError
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_client.get.side_effect = RequestError("Connection failed", request=None)

        # Call the list_tasks function
        result = await list_tasks()

        # Assert the result contains error information
        assert len(result) == 1
        assert "error" in result[0]
        assert "request_error" in result[0]["error"]
        assert "Connection failed" in result[0]["message"]