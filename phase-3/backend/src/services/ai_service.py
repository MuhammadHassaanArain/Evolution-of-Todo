# src/services/ai_service.py
import os
from dotenv import load_dotenv
from agents import (
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    RunConfig,
    Agent,
    Runner
)

# Load environment variables
load_dotenv()

class AIService:
    """
    AI Service using OpenAI Agent SDK with Gemini model
    """
    def __init__(self):
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")

        # Setup external client
        self.client = AsyncOpenAI(
            api_key=gemini_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        # Setup the Gemini model
        self.model = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=self.client
        )

        # Create default run configuration
        self.config = RunConfig(
            model=self.model,
            model_provider=self.client,
            tracing_disabled=True
        )

        # Create an agent for Todo tasks
        self.agent = Agent(
            name="todo-assistant",
            instructions=(
                "You are a helpful assistant for managing todo lists. "
                "You can add, list, update, complete, and delete tasks using natural language. "
                "Always respond in a friendly and concise manner."
            )
        )

        # Runner for synchronous execution
        self.runner = Runner()

    def run(self, message: str) -> str:
        """
        Run the agent synchronously and get a response
        """
        result = self.runner.run_sync(self.agent, message, run_config=self.config)
        return result.final_output if hasattr(result, "final_output") else str(result)

    async def run_async(self, message: str) -> str:
        """
        Run the agent asynchronously and get a response
        """
        result = await self.runner.run(self.agent, message, run_config=self.config)
        return result.final_output if hasattr(result, "final_output") else str(result)


# Global instance
ai_service = AIService()
