# API Contracts: MCP Server for Todo Task Management

## Overview
The MCP server exposes standardized tools for AI agents to interact with the todo task management system. These tools follow the Model Context Protocol specification and act as a proxy to the existing FastAPI backend.

## Tool Specifications

### add_task
**Purpose**: Create a new task for the authenticated user

**Request Parameters**:
- title (string, required): Title of the task to create
- description (string, optional): Description of the task

**Response**:
```json
{
  "task_id": 5,
  "status": "created",
  "title": "Buy groceries"
}
```

**Backend API Call**: `POST /api/tasks` with auth header

### list_tasks
**Purpose**: Retrieve tasks for the authenticated user

**Request Parameters**:
- status (string, optional): Filter by status - "all", "pending", or "completed"

**Response**:
```json
[
  { "id": 1, "title": "Buy groceries", "completed": false }
]
```

**Backend API Call**: `GET /api/tasks?status={status}` with auth header

### update_task
**Purpose**: Modify task title or description

**Request Parameters**:
- task_id (integer, required): ID of the task to update
- title (string, optional): New title for the task
- description (string, optional): New description for the task

**Response**:
```json
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy groceries and fruits"
}
```

**Backend API Call**: `PUT /api/tasks/{id}` with auth header

### complete_task
**Purpose**: Mark a task as completed

**Request Parameters**:
- task_id (integer, required): ID of the task to mark as completed

**Response**:
```json
{
  "task_id": 3,
  "status": "completed",
  "title": "Call mom"
}
```

**Backend API Call**: `PATCH /api/tasks/{id}/complete` with auth header

### delete_task
**Purpose**: Delete a task

**Request Parameters**:
- task_id (integer, required): ID of the task to delete

**Response**:
```json
{
  "task_id": 2,
  "status": "deleted",
  "title": "Old task"
}
```

**Backend API Call**: `DELETE /api/tasks/{id}` with auth header

## Error Responses
All tools return standard error responses when issues occur:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": "Additional error details"
}
```

## Authentication
All tool calls require a valid JWT token in the Authorization header which is passed through to the backend API unchanged.