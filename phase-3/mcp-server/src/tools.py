"""MCP tools for task management operations."""

import asyncio
import httpx
from typing import Dict, Any, Optional
from .main import mcp
from .client import backend_client


@mcp.tool("Add a new task for the authenticated user.")
async def add_task(title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new task for the authenticated user.

    Args:
        title: Title of the task to create (required)
        description: Description of the task (optional)

    Returns:
        Dictionary with task_id, status, and title
    """
    # Validate required parameters
    if not title or not isinstance(title, str) or len(title.strip()) == 0:
        return {
            "error": "validation_error",
            "message": "Title is required and must be a non-empty string",
            "details": "Parameter 'title' is missing or invalid"
        }

    # Prepare the request payload
    payload = {
        "title": title
    }

    if description is not None:
        payload["description"] = description

    try:
        # Make the request to the backend API
        response_data = await backend_client.post("/api/tasks", json_data=payload)

        # Return the response in the expected format
        return {
            "task_id": response_data.get("id"),
            "status": "created",
            "title": response_data.get("title")
        }
    except httpx.HTTPStatusError as e:
        # Handle HTTP errors from the backend API
        return {
            "error": "http_error",
            "message": f"Backend API returned error: {e.response.status_code}",
            "details": await e.response.text()
        }
    except httpx.RequestError as e:
        # Handle request errors (connection, timeout, etc.)
        return {
            "error": "request_error",
            "message": f"Failed to connect to backend API: {str(e)}",
            "details": str(e)
        }
    except Exception as e:
        # Handle any other errors
        return {
            "error": "create_failed",
            "message": f"Unexpected error creating task: {str(e)}",
            "details": str(e)
        }


@mcp.tool("Retrieve tasks for the authenticated user.")
async def list_tasks(status: Optional[str] = None) -> list:
    """
    Retrieve tasks for the authenticated user.

    Args:
        status: Filter by status - 'all', 'pending', or 'completed' (optional)

    Returns:
        List of tasks in the expected format
    """
    # Validate status parameter if provided
    if status is not None and status not in ["all", "pending", "completed"]:
        return [{
            "error": "validation_error",
            "message": "Status must be one of: 'all', 'pending', 'completed'",
            "details": f"Invalid status value: {status}"
        }]

    # Build the endpoint with optional status filter
    endpoint = "/api/tasks"
    if status:
        endpoint += f"?status={status}"

    try:
        # Make the request to the backend API
        response_data = await backend_client.get(endpoint)

        # Format the response as expected
        formatted_tasks = []
        for task in response_data:
            formatted_task = {
                "id": task.get("id"),
                "title": task.get("title"),
                "completed": task.get("completed", False)
            }
            # Add description if present
            if "description" in task:
                formatted_task["description"] = task["description"]

            formatted_tasks.append(formatted_task)

        return formatted_tasks
    except httpx.HTTPStatusError as e:
        # Handle HTTP errors from the backend API
        return [{
            "error": "http_error",
            "message": f"Backend API returned error: {e.response.status_code}",
            "details": await e.response.text()
        }]
    except httpx.RequestError as e:
        # Handle request errors (connection, timeout, etc.)
        return [{
            "error": "request_error",
            "message": f"Failed to connect to backend API: {str(e)}",
            "details": str(e)
        }]
    except Exception as e:
        # Handle any other errors
        return [{
            "error": "list_failed",
            "message": f"Unexpected error listing tasks: {str(e)}",
            "details": str(e)
        }]


@mcp.tool("Update an existing task.")
async def update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Modify task title or description.

    Args:
        task_id: ID of the task to update (required)
        title: New title for the task (optional)
        description: New description for the task (optional)

    Returns:
        Dictionary with task_id, status, and updated title
    """
    # Validate required parameters
    if not isinstance(task_id, int) or task_id <= 0:
        return {
            "error": "validation_error",
            "message": "Task ID must be a positive integer",
            "details": f"Invalid task_id: {task_id}"
        }

    if title is None and description is None:
        return {
            "error": "validation_error",
            "message": "At least one of title or description must be provided",
            "details": "Both title and description parameters were None"
        }

    # Prepare the request payload
    payload = {}

    if title is not None:
        if not isinstance(title, str) or len(title.strip()) == 0:
            return {
                "error": "validation_error",
                "message": "Title must be a non-empty string if provided",
                "details": f"Invalid title: {title}"
            }
        payload["title"] = title

    if description is not None:
        if not isinstance(description, str):
            return {
                "error": "validation_error",
                "message": "Description must be a string if provided",
                "details": f"Invalid description type: {type(description)}"
            }
        payload["description"] = description

    try:
        # Make the request to the backend API
        response_data = await backend_client.put(f"/api/tasks/{task_id}", json_data=payload)

        # Return the response in the expected format
        return {
            "task_id": task_id,
            "status": "updated",
            "title": response_data.get("title")
        }
    except httpx.HTTPStatusError as e:
        # Handle HTTP errors from the backend API
        return {
            "error": "http_error",
            "message": f"Backend API returned error: {e.response.status_code}",
            "details": await e.response.text()
        }
    except httpx.RequestError as e:
        # Handle request errors (connection, timeout, etc.)
        return {
            "error": "request_error",
            "message": f"Failed to connect to backend API: {str(e)}",
            "details": str(e)
        }
    except Exception as e:
        # Handle any other errors
        return {
            "error": "update_failed",
            "message": f"Unexpected error updating task {task_id}: {str(e)}",
            "details": str(e)
        }


@mcp.tool("Mark a task as completed.")
async def complete_task(task_id: int) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        task_id: ID of the task to mark as completed (required)

    Returns:
        Dictionary with task_id, status, and title
    """
    # Validate required parameters
    if not isinstance(task_id, int) or task_id <= 0:
        return {
            "error": "validation_error",
            "message": "Task ID must be a positive integer",
            "details": f"Invalid task_id: {task_id}"
        }

    try:
        # Make the request to the backend API
        response_data = await backend_client.patch(f"/api/tasks/{task_id}/complete")

        # Return the response in the expected format
        return {
            "task_id": task_id,
            "status": "completed",
            "title": response_data.get("title")
        }
    except httpx.HTTPStatusError as e:
        # Handle HTTP errors from the backend API
        return {
            "error": "http_error",
            "message": f"Backend API returned error: {e.response.status_code}",
            "details": await e.response.text()
        }
    except httpx.RequestError as e:
        # Handle request errors (connection, timeout, etc.)
        return {
            "error": "request_error",
            "message": f"Failed to connect to backend API: {str(e)}",
            "details": str(e)
        }
    except Exception as e:
        # Handle any other errors
        return {
            "error": "complete_failed",
            "message": f"Unexpected error completing task {task_id}: {str(e)}",
            "details": str(e)
        }


@mcp.tool("Delete a task.")
async def delete_task(task_id: int) -> Dict[str, Any]:
    """
    Delete a task.

    Args:
        task_id: ID of the task to delete (required)

    Returns:
        Dictionary with task_id, status, and title
    """
    # Validate required parameters
    if not isinstance(task_id, int) or task_id <= 0:
        return {
            "error": "validation_error",
            "message": "Task ID must be a positive integer",
            "details": f"Invalid task_id: {task_id}"
        }

    try:
        # Make the request to the backend API
        response_data = await backend_client.delete(f"/api/tasks/{task_id}")

        # Return the response in the expected format
        return {
            "task_id": task_id,
            "status": "deleted",
            "title": response_data.get("title")
        }
    except httpx.HTTPStatusError as e:
        # Handle HTTP errors from the backend API
        return {
            "error": "http_error",
            "message": f"Backend API returned error: {e.response.status_code}",
            "details": await e.response.text()
        }
    except httpx.RequestError as e:
        # Handle request errors (connection, timeout, etc.)
        return {
            "error": "request_error",
            "message": f"Failed to connect to backend API: {str(e)}",
            "details": str(e)
        }
    except Exception as e:
        # Handle any other errors
        return {
            "error": "delete_failed",
            "message": f"Unexpected error deleting task {task_id}: {str(e)}",
            "details": str(e)
        }