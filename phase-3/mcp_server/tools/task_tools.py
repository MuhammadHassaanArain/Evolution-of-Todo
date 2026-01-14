"""
MCP tools for todo task management
These tools map to existing FastAPI CRUD endpoints
"""
import asyncio
import httpx
from typing import Dict, Any, Optional
from mcp.server import Server
from mcp.types import Tool, ArgumentsSchema, CallToolResult


# Initialize MCP server
server = Server("todo-task-tools")


@server.tool(
    "add_task",
    description="Add a new task to the user's todo list",
    input_schema=ArgumentsSchema(
        properties={
            "user_id": {"type": "string", "description": "The ID of the user"},
            "title": {"type": "string", "description": "The title of the task to add"},
            "description": {"type": "string", "description": "Optional description of the task"}
        },
        required=["user_id", "title"]
    )
)
async def add_task(user_id: str, title: str, description: Optional[str] = None) -> CallToolResult:
    """
    MCP tool to add a new task using the existing POST /tasks endpoint
    """
    try:
        # Call the existing backend API to add the task
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {generate_temp_token(user_id)}",
                "Content-Type": "application/json"
            }
            data = {
                "title": title,
                "description": description or ""
            }

            response = await client.post(
                f"{get_backend_url()}/api/tasks",
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                task_data = response.json()
                result = {
                    "status": "success",
                    "message": f"Task '{title}' added successfully",
                    "task_id": task_data.get("id"),
                    "title": title
                }
            else:
                result = {
                    "status": "error",
                    "message": f"Failed to add task: {response.text}",
                    "error_code": response.status_code
                }

        return CallToolResult(content=str(result))
    except Exception as e:
        return CallToolResult(
            content=str({
                "status": "error",
                "message": f"Exception occurred while adding task: {str(e)}"
            })
        )


@server.tool(
    "list_tasks",
    description="List all tasks for the user",
    input_schema=ArgumentsSchema(
        properties={
            "user_id": {"type": "string", "description": "The ID of the user"},
            "status": {"type": "string", "description": "Filter by status: 'all', 'pending', 'completed'"}
        },
        required=["user_id"]
    )
)
async def list_tasks(user_id: str, status: Optional[str] = "all") -> CallToolResult:
    """
    MCP tool to list tasks using the existing GET /tasks endpoint
    """
    try:
        # Call the existing backend API to list tasks
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {generate_temp_token(user_id)}",
                "Content-Type": "application/json"
            }

            params = {}
            if status != "all":
                params["completed"] = "false" if status == "pending" else "true"

            response = await client.get(
                f"{get_backend_url()}/api/tasks",
                headers=headers,
                params=params
            )

            if response.status_code == 200:
                tasks = response.json()
                result = {
                    "status": "success",
                    "tasks": tasks,
                    "count": len(tasks)
                }
            else:
                result = {
                    "status": "error",
                    "message": f"Failed to list tasks: {response.text}",
                    "error_code": response.status_code
                }

        return CallToolResult(content=str(result))
    except Exception as e:
        return CallToolResult(
            content=str({
                "status": "error",
                "message": f"Exception occurred while listing tasks: {str(e)}"
            })
        )


@server.tool(
    "complete_task",
    description="Mark a task as completed",
    input_schema=ArgumentsSchema(
        properties={
            "user_id": {"type": "string", "description": "The ID of the user"},
            "task_id": {"type": "integer", "description": "The ID of the task to complete"}
        },
        required=["user_id", "task_id"]
    )
)
async def complete_task(user_id: str, task_id: int) -> CallToolResult:
    """
    MCP tool to complete a task using the existing PATCH /tasks/{id}/complete endpoint
    """
    try:
        # Call the existing backend API to complete the task
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {generate_temp_token(user_id)}",
                "Content-Type": "application/json"
            }

            response = await client.patch(
                f"{get_backend_url()}/api/tasks/{task_id}/complete",
                headers=headers
            )

            if response.status_code == 200:
                result = {
                    "status": "success",
                    "message": f"Task {task_id} marked as completed",
                    "task_id": task_id
                }
            else:
                result = {
                    "status": "error",
                    "message": f"Failed to complete task: {response.text}",
                    "error_code": response.status_code
                }

        return CallToolResult(content=str(result))
    except Exception as e:
        return CallToolResult(
            content=str({
                "status": "error",
                "message": f"Exception occurred while completing task: {str(e)}"
            })
        )


@server.tool(
    "update_task",
    description="Update an existing task",
    input_schema=ArgumentsSchema(
        properties={
            "user_id": {"type": "string", "description": "The ID of the user"},
            "task_id": {"type": "integer", "description": "The ID of the task to update"},
            "title": {"type": "string", "description": "The new title for the task"},
            "description": {"type": "string", "description": "The new description for the task"}
        },
        required=["user_id", "task_id"]
    )
)
async def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> CallToolResult:
    """
    MCP tool to update a task using the existing PUT /tasks/{id} endpoint
    """
    try:
        # Prepare update data
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description

        # Call the existing backend API to update the task
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {generate_temp_token(user_id)}",
                "Content-Type": "application/json"
            }

            response = await client.put(
                f"{get_backend_url()}/api/tasks/{task_id}",
                headers=headers,
                json=update_data
            )

            if response.status_code == 200:
                result = {
                    "status": "success",
                    "message": f"Task {task_id} updated successfully",
                    "task_id": task_id
                }
            else:
                result = {
                    "status": "error",
                    "message": f"Failed to update task: {response.text}",
                    "error_code": response.status_code
                }

        return CallToolResult(content=str(result))
    except Exception as e:
        return CallToolResult(
            content=str({
                "status": "error",
                "message": f"Exception occurred while updating task: {str(e)}"
            })
        )


@server.tool(
    "delete_task",
    description="Delete a task from the user's list",
    input_schema=ArgumentsSchema(
        properties={
            "user_id": {"type": "string", "description": "The ID of the user"},
            "task_id": {"type": "integer", "description": "The ID of the task to delete"}
        },
        required=["user_id", "task_id"]
    )
)
async def delete_task(user_id: str, task_id: int) -> CallToolResult:
    """
    MCP tool to delete a task using the existing DELETE /tasks/{id} endpoint
    """
    try:
        # Call the existing backend API to delete the task
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {generate_temp_token(user_id)}",
                "Content-Type": "application/json"
            }

            response = await client.delete(
                f"{get_backend_url()}/api/tasks/{task_id}",
                headers=headers
            )

            if response.status_code == 200:
                result = {
                    "status": "success",
                    "message": f"Task {task_id} deleted successfully",
                    "task_id": task_id
                }
            else:
                result = {
                    "status": "error",
                    "message": f"Failed to delete task: {response.text}",
                    "error_code": response.status_code
                }

        return CallToolResult(content=str(result))
    except Exception as e:
        return CallToolResult(
            content=str({
                "status": "error",
                "message": f"Exception occurred while deleting task: {str(e)}"
            })
        )


def get_backend_url():
    """Get the backend URL from environment or default to localhost"""
    import os
    return os.getenv("BACKEND_URL", "http://localhost:8000")


def generate_temp_token(user_id: str):
    """
    Generate a temporary token for API authentication.
    In a real implementation, this would use proper JWT signing.
    """
    import jwt
    import os
    from datetime import datetime, timedelta

    secret = os.getenv("JWT_SECRET", "fallback_secret_for_dev")
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, secret, algorithm="HS256")