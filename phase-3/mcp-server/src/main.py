"""Main entry point for the MCP Server for Todo Task Management."""

import asyncio
import os
from mcp.server import FastMCP
from mcp.server.http import streamable_http_app
from .config import settings


def create_mcp_server():
    """Create and configure the MCP server."""
    from .tools import add_task, list_tasks, update_task, complete_task, delete_task

    mcp = FastMCP(
        "todo-mcp-server",
        stateless_http=True
    )

    # Register all the task management tools
    mcp.tools.add(add_task)
    mcp.tools.add(list_tasks)
    mcp.tools.add(update_task)
    mcp.tools.add(complete_task)
    mcp.tools.add(delete_task)

    return mcp


# Create the global server instance
mcp = create_mcp_server()

# Create the ASGI application
app = streamable_http_app(mcp)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("MCP_SERVER_PORT", settings.mcp_port))
    host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False  # Disable reload in production
    )