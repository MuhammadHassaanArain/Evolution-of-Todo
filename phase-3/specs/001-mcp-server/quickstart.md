# Quickstart Guide: MCP Server for Todo Task Management

## Setup and Installation

### Prerequisites
- Python 3.13+
- uv (runtime manager)
- Access to the existing FastAPI backend (Phase II) running on port 8000
- Valid JWT token for authentication

### Installation Steps

1. Clone the repository and navigate to the MCP server directory
2. Install dependencies using uv:
   ```bash
   uv venv
   uv pip install fastmcp httpx
   ```

3. Set environment variables:
   ```bash
   export BACKEND_API_URL=http://localhost:8000
   export DEFAULT_JWT_TOKEN=your_jwt_token_here
   ```

4. Run the MCP server:
   ```bash
   uv run python main.py
   ```

## Configuration

### Environment Variables
- `BACKEND_API_URL`: URL of the FastAPI backend (default: http://localhost:8000)
- `MCP_SERVER_PORT`: Port for the MCP server (default: 8001)
- `LOG_LEVEL`: Logging level (default: INFO)

### Service Dependencies
- The MCP server must be able to reach the backend API at the configured URL
- Authentication tokens must be valid and properly formatted

## Running the Server

### Development Mode
```bash
uv run python main.py
```

### Production Mode
```bash
# Using a WSGI/ASGI server as appropriate for FastMCP
uv run gunicorn main:app
```

## Testing the Connection

### Verify Backend Connectivity
```bash
curl -X GET http://localhost:8000/api/health
```

### Verify MCP Server
The server should be available at `http://localhost:8001/mcp`

## Using with AI Agents

### OpenAI Agent Configuration
Configure your OpenAI agent to use the MCP server at `http://localhost:8001/mcp` with appropriate authentication.

### Available Tools
Once connected, the agent will have access to:
- add_task
- list_tasks
- update_task
- complete_task
- delete_task