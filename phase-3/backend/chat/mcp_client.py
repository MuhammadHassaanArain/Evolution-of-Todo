"""MCP client integration for the chatbot backend."""

import os
from typing import Dict, Any, Optional, List
from openai import OpenAI
from agents.mcp import MCPServerStreamableHttp


class MCPClient:
    """Client for integrating with MCP servers."""

    def __init__(self):
        self.mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8001/mcp")
        self._mcp_server = None

    def get_mcp_server(self) -> MCPServerStreamableHttp:
        """
        Get the MCP server instance.

        Returns:
            MCPServerStreamableHttp instance
        """
        if self._mcp_server is None:
            self._mcp_server = MCPServerStreamableHttp(url=self.mcp_server_url)
        return self._mcp_server

    def attach_to_agent(self, agent: Any) -> None:
        """
        Attach MCP servers to the agent.

        Args:
            agent: The agent to attach MCP servers to
        """
        mcp_server = self.get_mcp_server()
        # Attach the MCP server to the agent (implementation depends on the agent framework)
        if hasattr(agent, 'attach_mcp_server'):
            agent.attach_mcp_server(mcp_server)
        else:
            # Alternative approach depending on the agent framework
            setattr(agent, '_mcp_servers', [mcp_server])


# Global MCP client instance
mcp_client = MCPClient()


def get_mcp_client() -> MCPClient:
    """Get the global MCP client instance."""
    return mcp_client