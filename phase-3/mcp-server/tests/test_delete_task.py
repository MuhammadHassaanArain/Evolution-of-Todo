"""Contract tests for the delete_task tool."""

import pytest
from unittest.mock import AsyncMock, patch
from mcp import tool
from ..src.tools import delete_task


@pytest.mark.asyncio
async def test_delete_task_success():
    """Test that delete_task successfully deletes a task."""
    # Mock the backend client response
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_response = {"id": 1, "title": "Task to delete", "completed": False}
        mock_client.delete.return_value = mock_response

        # Call the delete_task function
        result = await delete_task(task_id=1)

        # Assert the result matches expected format
        assert result == {
            "task_id": 1,
            "status": "deleted",
            "title": "Task to delete"
        }

        # Assert the backend client was called with correct parameters
        mock_client.delete.assert_called_once_with("/api/tasks/1")


@pytest.mark.asyncio
async def test_delete_task_validation_error():
    """Test that delete_task handles validation errors properly."""
    # Test with invalid task_id
    result = await delete_task(task_id=-1)
    assert "error" in result
    assert result["error"] == "validation_error"

    # Test with invalid task_id type
    result = await delete_task(task_id="invalid")
    assert "error" in result
    assert result["error"] == "validation_error"


@pytest.mark.asyncio
async def test_delete_task_backend_error():
    """Test that delete_task handles backend API errors gracefully."""
    from httpx import RequestError

    # Mock the backend client to raise a RequestError
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_client.delete.side_effect = RequestError("Connection failed", request=None)

        # Call the delete_task function
        result = await delete_task(task_id=1)

        # Assert the result contains error information
        assert "error" in result
        assert "request_error" in result["error"]
        assert "Connection failed" in result["message"]