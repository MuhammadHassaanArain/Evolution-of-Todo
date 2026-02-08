"""Test configuration and fixtures for the MCP Server."""

import pytest
import os
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_backend_client():
    """Mock backend client for testing."""
    mock_client = AsyncMock()
    mock_client.get = AsyncMock()
    mock_client.post = AsyncMock()
    mock_client.put = AsyncMock()
    mock_client.patch = AsyncMock()
    mock_client.delete = AsyncMock()
    return mock_client


@pytest.fixture
def sample_task():
    """Sample task data for testing."""
    return {
        "id": 1,
        "title": "Test task",
        "description": "Test description",
        "completed": False
    }


@pytest.fixture
def sample_auth_headers():
    """Sample authentication headers for testing."""
    return {
        "Authorization": "Bearer fake-jwt-token"
    }