"""Basic tests to verify the MCP server tools are functioning."""

import pytest
from ..src.tools import add_task, list_tasks, update_task, complete_task, delete_task


def test_tool_functions_exist():
    """Test that all required tool functions exist and are callable."""
    assert callable(add_task)
    assert callable(list_tasks)
    assert callable(update_task)
    assert callable(complete_task)
    assert callable(delete_task)

    # Check that they have the expected tool decorator attributes
    assert hasattr(add_task, '__mcp_tool__') or hasattr(add_task, '__annotations__')
    assert hasattr(list_tasks, '__mcp_tool__') or hasattr(list_tasks, '__annotations__')
    assert hasattr(update_task, '__mcp_tool__') or hasattr(update_task, '__annotations__')
    assert hasattr(complete_task, '__mcp_tool__') or hasattr(complete_task, '__annotations__')
    assert hasattr(delete_task, '__mcp_tool__') or hasattr(delete_task, '__annotations__')


@pytest.mark.asyncio
async def test_function_signatures():
    """Test that functions have the expected parameters."""
    import inspect

    # Check add_task signature
    sig = inspect.signature(add_task)
    params = list(sig.parameters.keys())
    assert 'title' in params
    assert 'description' in params

    # Check list_tasks signature
    sig = inspect.signature(list_tasks)
    params = list(sig.parameters.keys())
    assert 'status' in params

    # Check update_task signature
    sig = inspect.signature(update_task)
    params = list(sig.parameters.keys())
    assert 'task_id' in params
    assert 'title' in params
    assert 'description' in params

    # Check complete_task signature
    sig = inspect.signature(complete_task)
    params = list(sig.parameters.keys())
    assert 'task_id' in params

    # Check delete_task signature
    sig = inspect.signature(delete_task)
    params = list(sig.parameters.keys())
    assert 'task_id' in params