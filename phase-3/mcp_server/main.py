"""
Main entry point for the MCP Server
"""
import asyncio
import os
from mcp.server import Server
from mcp.server.models import InitializationOptions
from .tools.task_tools import server as tools_server


async def serve():
    """Run the MCP server"""
    # Get port from environment, default to 8001
    port = int(os.getenv("MCP_PORT", "8001"))

    # Create server instance
    server = Server("todo-chatbot-mcp", "1.0.0")

    # Register all tools from the tools module
    # The tools are already registered with the tools_server instance
    for tool in tools_server.tools:
        server.add_tool(tool)

    # Initialize and run the server
    async with server.serve_io(port=port) as (read_stream, write_stream):
        print(f"MCP Server running on port {port}")
        await asyncio.gather(
            server.start(read_stream, write_stream),
            # Keep the server running
            asyncio.Future()
        )


if __name__ == "__main__":
    asyncio.run(serve())