"""MCP tools for task management operations."""

import os
import httpx
from .config import settings
from mcp.server.fastmcp import FastMCP, Context
from typing import Dict, Any, Optional, List


mcp = FastMCP("todo-mcp-server", stateless_http=True)

@mcp.tool(title="Add a new task for the authenticated user.")
async def add_task(title: str, description: Optional[str] = None, ctx: Context = None) -> Dict[str, Any]:
    """
    Create a new task for the authenticated user via backend API.

    Args:
        title: Title of the task (required)
        description: Optional task description
        ctx: Request context to access headers

    Returns:
        Dictionary with task_id, status, title, or error info
    """
    # Validate input
    if not title or not isinstance(title, str) or not title.strip():
        return {
            "error": "validation_error",
            "message": "Title is required and must be a non-empty string",
            "details": "Parameter 'title' is missing or invalid"
        }

    payload = {"title": title}
    if description:
        payload["description"] = description

    base_url = getattr(settings, "backend_api_url", "http://localhost:8000")
    endpoint = f"{base_url}/api/tasks"

    # Extract auth header from context
    headers = {}
    if ctx and hasattr(ctx, 'request') and hasattr(ctx.request, 'headers'):
        auth_header = ctx.request.headers.get("authorization")
        if auth_header:
            # Ensure the header is in the correct format "Bearer <token>"
            if auth_header.startswith("Bearer ") or auth_header.startswith("bearer "):
                headers["Authorization"] = auth_header
            else:
                # If it's just the token, add the Bearer prefix
                headers["Authorization"] = f"Bearer {auth_header}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            return {
                "task_id": data.get("id"),
                "status": "created",
                "title": data.get("title")
            }

    except httpx.HTTPStatusError as e:
        return {
            "error": "http_error",
            "message": f"Backend returned status {e.response.status_code}",
            "details": await e.response.aread() if hasattr(e.response, "aread") else str(e)
        }
    except httpx.RequestError as e:
        return {
            "error": "request_error",
            "message": f"Failed to connect to backend: {str(e)}",
            "details": str(e)
        }
    except Exception as e:
        return {
            "error": "create_failed",
            "message": f"Unexpected error creating task: {str(e)}",
            "details": str(e)
        }


@mcp.tool(title="Retrieve tasks for the authenticated user.")
async def list_tasks(status: Optional[str] = "all", ctx: Context = None) -> List[Dict[str, Any]]:
    """
    Retrieve tasks for the authenticated user via backend API.

    Args:
        status: Optional filter - 'all', 'pending', or 'completed'. Defaults to 'all'.
        ctx: Request context to access headers

    Returns:
        List of tasks or a single-item list containing error info.
    """
    valid_status = ["all", "pending", "completed"]
    if status not in valid_status:
        return [{
            "error": "validation_error",
            "message": f"Status must be one of {valid_status}",
            "details": f"Invalid status value: {status}"
        }]

    base_url = getattr(settings, "backend_api_url", "http://localhost:8000")
    endpoint = f"{base_url}/api/tasks"
    if status != "all":
        endpoint += f"?status={status}"

    # Extract auth header from context
    headers = {}
    if ctx and hasattr(ctx, 'request') and hasattr(ctx.request, 'headers'):
        auth_header = ctx.request.headers.get("authorization")
        if auth_header:
            # Ensure the header is in the correct format "Bearer <token>"
            if auth_header.startswith("Bearer ") or auth_header.startswith("bearer "):
                headers["Authorization"] = auth_header
            else:
                # If it's just the token, add the Bearer prefix
                headers["Authorization"] = f"Bearer {auth_header}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(endpoint, headers=headers)
            response.raise_for_status()
            tasks_data = response.json()

            formatted_tasks = []
            for task in tasks_data:
                formatted_task = {
                    "id": task.get("id"),
                    "title": task.get("title"),
                    "completed": task.get("is_completed", False)
                }
                if "description" in task:
                    formatted_task["description"] = task["description"]
                formatted_tasks.append(formatted_task)

            return formatted_tasks

    except httpx.HTTPStatusError as e:
        return [{
            "error": "http_error",
            "message": f"Backend returned status {e.response.status_code}",
            "details": await e.response.aread() if hasattr(e.response, "aread") else str(e)
        }]
    except httpx.RequestError as e:
        return [{
            "error": "request_error",
            "message": f"Failed to connect to backend: {str(e)}",
            "details": str(e)
        }]
    except Exception as e:
        return [{
            "error": "unknown_error",
            "message": f"Unexpected error: {str(e)}",
            "details": str(e)
        }]


@mcp.tool(title="Update an existing task.")
async def update_task(task_id: str, title: str | None = None, description: str | None = None, ctx: Context = None) -> Dict[str, Any]:
    """
    Update task title or description via backend API.

    Args:
        task_id: ID of the task to update (required)
        title: New title (optional)
        description: New description (optional)
        ctx: Request context to access headers

    Returns:
        Dictionary with task_id, status, updated title, or error info
    """
    # if not isinstance(task_id, str) or task_id <= 0:
    #     return {"error": "validation_error", "message": "Task ID must be a positive integer", "details": f"Invalid task_id: {task_id}"}
    if not isinstance(task_id, str) or not task_id.strip():
        return {
            "error": "validation_error",
            "message": "Task ID must be a non-empty string (UUID)",
            "details": f"Invalid task_id: {task_id}"
        }
    if title is None and description is None:
        return {"error": "validation_error", "message": "Provide at least one of title or description", "details": "Both title and description are None"}

    payload = {}
    if title is not None:
        if not isinstance(title, str) or not title.strip():
            return {"error": "validation_error", "message": "Title must be a non-empty string if provided", "details": f"Invalid title: {title}"}
        payload["title"] = title

    if description is not None:
        if not isinstance(description, str):
            return {"error": "validation_error", "message": "Description must be a string if provided", "details": f"Invalid description type: {type(description)}"}
        payload["description"] = description

    base_url = getattr(settings, "backend_api_url", "http://localhost:8000")
    endpoint = f"{base_url}/api/tasks/{task_id}"

    # Extract auth header from context
    headers = {}
    if ctx and hasattr(ctx, 'request') and hasattr(ctx.request, 'headers'):
        auth_header = ctx.request.headers.get("authorization")
        if auth_header:
            # Ensure the header is in the correct format "Bearer <token>"
            if auth_header.startswith("Bearer ") or auth_header.startswith("bearer "):
                headers["Authorization"] = auth_header
            else:
                # If it's just the token, add the Bearer prefix
                headers["Authorization"] = f"Bearer {auth_header}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.put(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return {"task_id": task_id, "status": "updated", "title": data.get("title")}

    except httpx.HTTPStatusError as e:
        return {"error": "http_error", "message": f"Backend returned {e.response.status_code}", "details": await e.response.aread() if hasattr(e.response, "aread") else str(e)}
    except httpx.RequestError as e:
        return {"error": "request_error", "message": f"Failed to connect: {str(e)}", "details": str(e)}
    except Exception as e:
        return {"error": "update_failed", "message": f"Unexpected error updating task {task_id}: {str(e)}", "details": str(e)}


@mcp.tool(title="Mark a task as completed.")
async def complete_task(task_id: str, ctx: Context = None) -> Dict[str, Any]:
    """
    Mark a task as completed via backend API.

    Args:
        task_id: ID of the task to complete
        ctx: Request context to access headers

    Returns:
        Dictionary with task_id, status, title, or error info
    """
    if not isinstance(task_id, str) or not task_id.strip():
        return {
            "error": "validation_error",
            "message": "Task ID must be a non-empty string (UUID)",
            "details": f"Invalid task_id: {task_id}"
        }
    # if not isinstance(task_id, int) or task_id <= 0:
    #     return {"error": "validation_error", "message": "Task ID must be positive", "details": f"Invalid task_id: {task_id}"}

    base_url = getattr(settings, "backend_api_url", "http://localhost:8000")
    endpoint = f"{base_url}/api/tasks/{task_id}/complete"

    # Extract auth header from context
    headers = {}
    if ctx and hasattr(ctx, 'request') and hasattr(ctx.request, 'headers'):
        auth_header = ctx.request.headers.get("authorization")
        if auth_header:
            # Ensure the header is in the correct format "Bearer <token>"
            if auth_header.startswith("Bearer ") or auth_header.startswith("bearer "):
                headers["Authorization"] = auth_header
            else:
                # If it's just the token, add the Bearer prefix
                headers["Authorization"] = f"Bearer {auth_header}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.patch(endpoint, headers=headers)
            response.raise_for_status()
            data = response.json()
            return {"task_id": task_id, "status": "completed", "title": data.get("title")}

    except httpx.HTTPStatusError as e:
        return {"error": "http_error", "message": f"Backend returned {e.response.status_code}", "details": await e.response.aread() if hasattr(e.response, "aread") else str(e)}
    except httpx.RequestError as e:
        return {"error": "request_error", "message": f"Failed to connect: {str(e)}", "details": str(e)}
    except Exception as e:
        return {"error": "complete_failed", "message": f"Unexpected error completing task {task_id}: {str(e)}", "details": str(e)}


@mcp.tool(title="Delete a task.")
async def delete_task(task_id: str, ctx: Context = None) -> Dict[str, Any]:
    """
    Delete a task via backend API.

    Args:
        task_id: ID of the task to delete
        ctx: Request context to access headers

    Returns:
        Dictionary with task_id, status, title, or error info
    """
    if not isinstance(task_id, str) or not task_id.strip():
        return {
            "error": "validation_error",
            "message": "Task ID must be a non-empty string (UUID)",
            "details": f"Invalid task_id: {task_id}"
        }
    # if not isinstance(task_id, int) or task_id <= 0:
    #     return {"error": "validation_error", "message": "Task ID must be positive", "details": f"Invalid task_id: {task_id}"}

    base_url = getattr(settings, "backend_api_url", "http://localhost:8000")
    endpoint = f"{base_url}/api/tasks/{task_id}"

    # Extract auth header from context
    headers = {}
    if ctx and hasattr(ctx, 'request') and hasattr(ctx.request, 'headers'):
        auth_header = ctx.request.headers.get("authorization")
        if auth_header:
            # Ensure the header is in the correct format "Bearer <token>"
            if auth_header.startswith("Bearer ") or auth_header.startswith("bearer "):
                headers["Authorization"] = auth_header
            else:
                # If it's just the token, add the Bearer prefix
                headers["Authorization"] = f"Bearer {auth_header}"


    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.delete(endpoint, headers=headers)
            response.raise_for_status()
            data = response.json()
            return {"task_id": task_id, "status": "deleted", "title": data.get("title")}

    except httpx.HTTPStatusError as e:
        return {"error": "http_error", "message": f"Backend returned {e.response.status_code}", "details": await e.response.aread() if hasattr(e.response, "aread") else str(e)}
    except httpx.RequestError as e:
        return {"error": "request_error", "message": f"Failed to connect: {str(e)}", "details": str(e)}
    except Exception as e:
        return {"error": "delete_failed", "message": f"Unexpected error deleting task {task_id}: {str(e)}", "details": str(e)}


app = mcp.streamable_http_app()



if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("MCP_SERVER_PORT", settings.mcp_port))
    host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port, reload=False)