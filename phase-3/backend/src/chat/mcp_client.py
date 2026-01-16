import os
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams

class MCPClient:
    """MCP client wrapper for Agent SDK."""

    def __init__(self):
        self.mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp/")
        self._mcp_server = None

    def get_server(self) -> MCPServerStreamableHttp:
        """Get or initialize the MCP server."""
        if not self._mcp_server:
            params = MCPServerStreamableHttpParams(url=self.mcp_server_url)
            self._mcp_server = MCPServerStreamableHttp(name="todo_tools", params=params)
        return self._mcp_server


# Global MCP client instance
mcp_client = MCPClient()
