import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from openai import AsyncOpenAI
# Note: Replace 'agents' imports with the standard OpenAI SDK if you can't install Agent SDK
from agents import Agent, Runner ,OpenAIChatCompletionsModel, RunConfig, ModelSettings
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams

# from .models import ChatRequest, ChatResponse, ToolCall

load_dotenv()
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
MCP_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8001/mcp/")

# Initialize OpenAI client
client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Initialize model
model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=client
)

# Run config for the agent
config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)


async def run_agent(
    user_input: str,
    conversation_context: Optional[List[Dict[str, str]]] = None,
    user_id: Optional[int] = None,
    auth_header: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run the chatbot agent with MCP tools.

    Args:
        user_input: The user's message
        conversation_context: Optional conversation history
        user_id: The ID of the authenticated user
        auth_header: The raw Authorization header to pass to MCP tools

    Returns:
        Dict containing 'response', 'tool_calls', 'tool_responses'
    """
    # Setup MCP server with headers if auth header is provided
    if auth_header:
        mcp_params = MCPServerStreamableHttpParams(
            url=MCP_URL,
            headers={"Authorization": auth_header}  # Forward the auth header
        )
    else:
        mcp_params = MCPServerStreamableHttpParams(url=MCP_URL)

    async with MCPServerStreamableHttp(name="todo_tools", params=mcp_params) as server:

        # Create the agent
        agent = Agent(
            name="Assistant",
            instructions=(
                "You are a helpful assistant that manages tasks. "
                "Use the available tools when necessary."
            ),
            model=model,
            mcp_servers=[server],
            model_settings=ModelSettings(tool_choice="auto")
        )

        # Use the original config
        run_config = config

        # Run the agent
        result = await Runner.run(agent, input=user_input, run_config=run_config)

        # Structure the output
        final_result = {
            "response": result.final_output,
            "tool_calls": getattr(result, "tool_calls", []),
            "tool_responses": getattr(result, "tool_responses", [])
        }

        return final_result
