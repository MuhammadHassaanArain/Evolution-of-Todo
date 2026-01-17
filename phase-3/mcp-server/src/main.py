# """Main entry point for the MCP Server for Todo Task Management."""

# import asyncio
# import os
# from mcp.server.fastmcp import FastMCP
# from .config import settings


# def create_mcp_server():
#     """Create and configure the MCP server."""
#     from .tools import add_task, list_tasks, update_task, complete_task, delete_task

#     mcp = FastMCP(
#         "todo-mcp-server",
#         stateless_http=True
#     )


#     return mcp


# # Create the global server instance
# mcp = create_mcp_server()

# # Create the ASGI application
# app = mcp.streamable_http_app(mcp)


# if __name__ == "__main__":
#     import uvicorn

#     port = int(os.getenv("MCP_SERVER_PORT", settings.mcp_port))
#     host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")

#     uvicorn.run(
#         app,
#         host=host,
#         port=port,
#         reload=False  # Disable reload in production
#     )


# main.py
import os
from mcp.server.fastmcp import FastMCP
from .config import settings

mcp = FastMCP("todo-mcp-server", stateless_http=True)

app = mcp.streamable_http_app()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("MCP_SERVER_PORT", settings.mcp_port))
    host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port, reload=False)
