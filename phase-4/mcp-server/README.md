# MCP Server for Todo Task Management

This is an MCP (Model Context Protocol) server that acts as a stateless proxy layer between AI agents and the existing FastAPI backend. The server exposes standardized tools for task management operations while delegating all business logic, authentication, and authorization to the backend API.

## Architecture

The server follows a thin proxy pattern:
- AI agents connect to the MCP server
- The MCP server forwards requests to the backend API
- Authentication and user isolation are handled by the backend
- The MCP server returns responses to the AI agents

## Prerequisites

- Python 3.13+
- uv (runtime manager)
- Access to the existing FastAPI backend (Phase II) running on port 8000
- Valid JWT token for authentication

## Installation

1. Clone the repository
2. Install dependencies using uv:
   ```bash
   uv venv
   uv pip install -e .
   ```

## Configuration

Set the following environment variables:
- `BACKEND_API_URL`: URL of the FastAPI backend (default: http://localhost:8000)
- `MCP_SERVER_PORT`: Port for the MCP server (default: 8001)
- `LOG_LEVEL`: Logging level (default: INFO)

## Running the Server

```bash
uv run python -m mcp-server.src.main
```

## Available Tools

The server exposes the following MCP tools for AI agents:

- `add_task`: Create a new task for the authenticated user
- `list_tasks`: Retrieve tasks for the authenticated user
- `update_task`: Modify task title or description
- `complete_task`: Mark a task as completed
- `delete_task`: Delete a task

## Environment Variables

- `BACKEND_API_URL`: URL of the backend API (default: http://localhost:8000)
- `BACKEND_API_TIMEOUT`: Timeout for backend API calls in seconds (default: 30)
- `MCP_SERVER_PORT`: Port for the MCP server (default: 8001)
- `MCP_SERVER_HOST`: Host for the MCP server (default: 0.0.0.0)
- `LOG_LEVEL`: Logging level (default: INFO)

## Development

To run tests:
```bash
uv run pytest
```

To format code:
```bash
uv run black .
```

## License

MIT