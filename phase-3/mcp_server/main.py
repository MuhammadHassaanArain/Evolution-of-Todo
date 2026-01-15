"""
MCP tools for TODO task management using FastMCP
These tools map to existing FastAPI CRUD endpoints
"""
import asyncio
import httpx
import os
from typing import Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("todo-task-tools", stateless_http=True)

def get_backend_url():
    """Get the backend URL from environment or default to localhost"""
    return os.getenv("BACKEND_URL", "http://localhost:8000")

def generate_temp_token(user_id: str):
    """Generate a temporary token for API authentication (JWT)"""
    import jwt
    from datetime import datetime, timedelta

    secret = os.getenv("JWT_SECRET", "fallback_secret_for_dev")
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, secret, algorithm="HS256")


async def _call_api(method: str, endpoint: str, user_id: str, data: Optional[dict] = None, params: Optional[dict] = None):
    """Helper function to call backend API"""
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {generate_temp_token(user_id)}",
                "Content-Type": "application/json"
            }
            response = await client.request(
                method=method,
                url=f"{get_backend_url()}{endpoint}",
                headers=headers,
                json=data,
                params=params
            )
            if response.status_code in (200, 201):
                return {"status": "success", "data": response.json()}
            else:
                return {"status": "error", "message": response.text, "error_code": response.status_code}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool(name="add_task")
async def add_task(user_id: str, title: str, description: Optional[str] = None):
    """Add a new task to the user's todo list"""
    data = {"title": title, "description": description or ""}
    result = await _call_api("POST", "/api/tasks", user_id, data=data)
    if result["status"] == "success":
        task_id = result["data"].get("id")
        return {"status": "success", "message": f"Task '{title}' added successfully", "task_id": task_id}
    return result


@mcp.tool(name="list_tasks")
async def list_tasks(user_id: str, status: Optional[str] = "all"):
    """List all tasks for the user"""
    params = {}
    if status != "all":
        params["completed"] = "false" if status == "pending" else "true"
    result = await _call_api("GET", "/api/tasks", user_id, params=params)
    if result["status"] == "success":
        tasks = result["data"]
        return {"status": "success", "tasks": tasks, "count": len(tasks)}
    return result


@mcp.tool(name="complete_task")
async def complete_task(user_id: str, task_id: int):
    """Mark a task as completed"""
    result = await _call_api("PATCH", f"/api/tasks/{task_id}/complete", user_id)
    if result["status"] == "success":
        return {"status": "success", "message": f"Task {task_id} marked as completed", "task_id": task_id}
    return result


@mcp.tool(name="update_task")
async def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None):
    """Update an existing task"""
    data = {}
    if title is not None:
        data["title"] = title
    if description is not None:
        data["description"] = description
    result = await _call_api("PUT", f"/api/tasks/{task_id}", user_id, data=data)
    if result["status"] == "success":
        return {"status": "success", "message": f"Task {task_id} updated successfully", "task_id": task_id}
    return result


@mcp.tool(name="delete_task")
async def delete_task(user_id: str, task_id: int):
    """Delete a task from the user's list"""
    result = await _call_api("DELETE", f"/api/tasks/{task_id}", user_id)
    if result["status"] == "success":
        return {"status": "success", "message": f"Task {task_id} deleted successfully", "task_id": task_id}
    return result


# Expose FastMCP app
mcp_app = mcp.streamable_http_app()
