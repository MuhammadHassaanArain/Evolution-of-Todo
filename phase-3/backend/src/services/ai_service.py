import os
import asyncio
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    ModelSettings,
    RunConfig
)
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams

# Load environment variables
load_dotenv()
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

class AIService:
    """
    AI Service using Google Gemini model with OpenAI-compatible API and MCP tools.
    """
    def __init__(self):
        # Load API key from .env
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing in .env")

        # 1️⃣ Async OpenAI client with Gemini base URL
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        # 2️⃣ Define the model for Agent SDK
        self.model = OpenAIChatCompletionsModel(
            model="gemini-2.5-flash",
            openai_client=self.client
        )

        # 3️⃣ Run configuration for the agent
        self.config = RunConfig(
            model=self.model,
            model_provider=self.client,
            tracing_disabled=True
        )

        # 4️⃣ Setup MCP server connection (FastMCP)
        self.mcp_params = MCPServerStreamableHttpParams(url="http://localhost:8001/mcp/")
        self.mcp_server = MCPServerStreamableHttp(name="todo_tools_server", params=self.mcp_params)

        # 5️⃣ Agent instructions
        self.agent = Agent(
            name="Todo Assistant",
            instructions="""
            You are a helpful assistant that helps users manage their todo lists.
            You can add, list, update, complete, and delete tasks using natural language.
            Always confirm actions with the user before making changes.
            Be friendly and concise in your responses.
            """,
            model=self.model,
            mcp_servers=[self.mcp_server],  # Attach MCP server
            model_settings=ModelSettings(tool_choice="auto")
        )

    def run_sync(self, message: str) -> str:
        """
        Run the agent synchronously and return the assistant's response.
        """
        # Use Runner.run_sync with MCP attached
        result = Runner.run_sync(self.agent, message, run_config=self.config)
        return result.final_output if hasattr(result, "final_output") else str(result)

    async def run_async(self, message: str) -> str:
        """
        Run the agent asynchronously and return the assistant's response.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.run_sync, message)


# Global instance
ai_service = AIService()
