"""Contract tests for the add_task tool."""

import pytest
from unittest.mock import AsyncMock, patch
from mcp import tool
from ..src.tools import add_task


@pytest.mark.asyncio
async def test_add_task_success():
    """Test that add_task successfully creates a task."""
    # Mock the backend client response
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_response = {
            "id": 5,
            "title": "Buy groceries",
            "description": "Milk and bread",
            "completed": False
        }
        mock_client.post.return_value = mock_response

        # Call the add_task function
        result = await add_task(title="Buy groceries", description="Milk and bread")

        # Assert the result matches expected format
        assert result == {
            "task_id": 5,
            "status": "created",
            "title": "Buy groceries"
        }

        # Assert the backend client was called with correct parameters
        mock_client.post.assert_called_once_with("/api/tasks", json_data={
            "title": "Buy groceries",
            "description": "Milk and bread"
        })


@pytest.mark.asyncio
async def test_add_task_without_description():
    """Test that add_task works when description is not provided."""
    # Mock the backend client response
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_response = {
            "id": 6,
            "title": "Call mom",
            "completed": False
        }
        mock_client.post.return_value = mock_response

        # Call the add_task function without description
        result = await add_task(title="Call mom")

        # Assert the result matches expected format
        assert result == {
            "task_id": 6,
            "status": "created",
            "title": "Call mom"
        }

        # Assert the backend client was called with correct parameters
        mock_client.post.assert_called_once_with("/api/tasks", json_data={
            "title": "Call mom"
        })


@pytest.mark.asyncio
async def test_add_task_validation_error():
    """Test that add_task handles validation errors properly."""
    # Test with empty title
    result = await add_task(title="")

    # Assert the result contains validation error
    assert "error" in result
    assert result["error"] == "validation_error"
    assert "Title is required" in result["message"]


@pytest.mark.asyncio
async def test_add_task_backend_error():
    """Test that add_task handles backend API errors gracefully."""
    from httpx import RequestError

    # Mock the backend client to raise a RequestError
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_client.post.side_effect = RequestError("Connection failed", request=None)

        # Call the add_task function
        result = await add_task(title="Test task")

        # Assert the result contains error information
        assert "error" in result
        assert "request_error" in result["error"]
        assert "Connection failed" in result["message"]