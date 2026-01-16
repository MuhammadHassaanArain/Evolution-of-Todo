"""Contract tests for the complete_task tool."""

import pytest
from unittest.mock import AsyncMock, patch
from mcp import tool
from ..src.tools import complete_task


@pytest.mark.asyncio
async def test_complete_task_success():
    """Test that complete_task successfully marks a task as completed."""
    # Mock the backend client response
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_response = {"id": 1, "title": "Task to complete", "completed": True}
        mock_client.patch.return_value = mock_response

        # Call the complete_task function
        result = await complete_task(task_id=1)

        # Assert the result matches expected format
        assert result == {
            "task_id": 1,
            "status": "completed",
            "title": "Task to complete"
        }

        # Assert the backend client was called with correct parameters
        mock_client.patch.assert_called_once_with("/api/tasks/1/complete")


@pytest.mark.asyncio
async def test_complete_task_validation_error():
    """Test that complete_task handles validation errors properly."""
    # Test with invalid task_id
    result = await complete_task(task_id=-1)
    assert "error" in result
    assert result["error"] == "validation_error"

    # Test with invalid task_id type
    result = await complete_task(task_id="invalid")
    assert "error" in result
    assert result["error"] == "validation_error"


@pytest.mark.asyncio
async def test_complete_task_backend_error():
    """Test that complete_task handles backend API errors gracefully."""
    from httpx import RequestError

    # Mock the backend client to raise a RequestError
    with patch('mcp_server.src.client.backend_client') as mock_client:
        mock_client.patch.side_effect = RequestError("Connection failed", request=None)

        # Call the complete_task function
        result = await complete_task(task_id=1)

        # Assert the result contains error information
        assert "error" in result
        assert "request_error" in result["error"]
        assert "Connection failed" in result["message"]