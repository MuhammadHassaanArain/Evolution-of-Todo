"""Contract tests for the update_task tool."""

import pytest
from unittest.mock import AsyncMock, patch
from mcp import tool
from ..src.tools import update_task


@pytest.mark.asyncio
async def test_update_task_success():
    """Test that update_task successfully updates a task."""
    # Mock the backend client response
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_response = {"id": 1, "title": "Updated task", "completed": False}
        mock_client.put.return_value = mock_response

        # Call the update_task function
        result = await update_task(task_id=1, title="Updated task")

        # Assert the result matches expected format
        assert result == {
            "task_id": 1,
            "status": "updated",
            "title": "Updated task"
        }

        # Assert the backend client was called with correct parameters
        mock_client.put.assert_called_once_with("/api/tasks/1", json_data={"title": "Updated task"})


@pytest.mark.asyncio
async def test_update_task_with_description():
    """Test that update_task works with description parameter."""
    # Mock the backend client response
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_response = {"id": 1, "title": "Updated task", "description": "Updated desc", "completed": False}
        mock_client.put.return_value = mock_response

        # Call the update_task function
        result = await update_task(task_id=1, title="Updated task", description="Updated desc")

        # Assert the result matches expected format
        assert result == {
            "task_id": 1,
            "status": "updated",
            "title": "Updated task"
        }

        # Assert the backend client was called with correct parameters
        mock_client.put.assert_called_once_with("/api/tasks/1", json_data={
            "title": "Updated task",
            "description": "Updated desc"
        })


@pytest.mark.asyncio
async def test_update_task_validation_errors():
    """Test that update_task handles validation errors properly."""
    # Test with invalid task_id
    result = await update_task(task_id=-1, title="Updated task")
    assert "error" in result
    assert result["error"] == "validation_error"

    # Test with invalid task_id type
    result = await update_task(task_id="invalid", title="Updated task")
    assert "error" in result
    assert result["error"] == "validation_error"

    # Test with no update parameters
    result = await update_task(task_id=1)
    assert "error" in result
    assert result["error"] == "validation_error"

    # Test with empty title
    result = await update_task(task_id=1, title="")
    assert "error" in result
    assert result["error"] == "validation_error"


@pytest.mark.asyncio
async def test_update_task_backend_error():
    """Test that update_task handles backend API errors gracefully."""
    from httpx import RequestError

    # Mock the backend client to raise a RequestError
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_client.put.side_effect = RequestError("Connection failed", request=None)

        # Call the update_task function
        result = await update_task(task_id=1, title="Updated task")

        # Assert the result contains error information
        assert "error" in result
        assert "request_error" in result["error"]
        assert "Connection failed" in result["message"]