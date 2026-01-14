# import asyncio
# import os
# from typing import Dict, Any, Optional
# from openai import OpenAI
# from openai.types.beta.threads.runs.run_step import RunStep
# from openai.types.beta.assistant import Assistant
# from openai.types.beta.thread import Thread
# import json


# class AIService:
#     """
#     Service for interacting with OpenAI Assistant API
#     """
#     def __init__(self):
#         self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#         self.model = os.getenv("OPENAI_MODEL", "gpt-4o")

#         # Create or retrieve the assistant with MCP tools
#         self.assistant = self._create_or_get_assistant()

#     def _create_or_get_assistant(self) -> Assistant:
#         """
#         Create or retrieve the AI assistant configured for todo management
#         """
#         # For now, we'll create a new assistant each time during development
#         # In production, you'd want to store and reuse the assistant ID
#         assistant = self.client.beta.assistants.create(
#             name="Todo Manager Assistant",
#             description="An AI assistant that helps users manage their todo lists using natural language",
#             model=self.model,
#             instructions="""
#             You are a helpful assistant that helps users manage their todo lists.
#             You can add, list, update, complete, and delete tasks using natural language.
#             Always confirm actions with the user before making changes.
#             Be friendly and concise in your responses.

#             When a user wants to:
#             - Add a task: Use the add_task tool
#             - See tasks: Use the list_tasks tool
#             - Complete a task: Use the complete_task tool
#             - Update a task: Use the update_task tool
#             - Delete a task: Use the delete_task tool

#             Always respond in a conversational tone after using tools.
#             """
#         )
#         return assistant

#     def create_thread(self) -> Thread:
#         """
#         Create a new conversation thread
#         """
#         thread = self.client.beta.threads.create()
#         return thread

#     def get_thread(self, thread_id: str) -> Thread:
#         """
#         Retrieve an existing thread by ID
#         """
#         thread = self.client.beta.threads.retrieve(thread_id=thread_id)
#         return thread

#     def add_message_to_thread(self, thread_id: str, message: str, role: str = "user") -> Any:
#         """
#         Add a message to a thread
#         """
#         message_obj = self.client.beta.threads.messages.create(
#             thread_id=thread_id,
#             role=role,
#             content=message
#         )
#         return message_obj

#     def run_assistant(self, thread_id: str, user_id: str) -> Any:
#         """
#         Run the assistant on a thread and return the response
#         """
#         # Create a run with the assistant
#         run = self.client.beta.threads.runs.create(
#             thread_id=thread_id,
#             assistant_id=self.assistant.id,
#             # Pass the user_id as metadata so tools can access it
#             additional_instructions=f"Remember that the current user ID is {user_id}. All operations should be performed for this user only."
#         )

#         # Wait for the run to complete
#         while run.status in ["queued", "in_progress"]:
#             run = self.client.beta.threads.runs.retrieve(
#                 thread_id=thread_id,
#                 run_id=run.id
#             )
#             if run.status == "requires_action":
#                 # Handle tool calls
#                 run = self._handle_tool_calls(run, thread_id, user_id)
#             elif run.status in ["completed", "failed", "cancelled", "expired"]:
#                 break
#             else:
#                 # Wait a bit before checking again
#                 import time
#                 time.sleep(1)

#         # Get the latest messages from the thread
#         messages = self.client.beta.threads.messages.list(
#             thread_id=thread_id,
#             order="desc",
#             limit=1
#         )

#         return {
#             "status": run.status,
#             "response": messages.data[0].content[0].text.value if messages.data else "No response generated",
#             "run_id": run.id,
#             "tool_calls": self._extract_tool_calls_from_run(run)
#         }

#     def _handle_tool_calls(self, run, thread_id: str, user_id: str):
#         """
#         Handle tool calls when the assistant requires action
#         """
#         tool_calls = run.required_action.submit_tool_outputs.tool_calls

#         tool_outputs = []
#         for tool_call in tool_calls:
#             # For now, we'll simulate tool execution
#             # In a real implementation, you'd call the MCP server tools
#             tool_name = tool_call.function.name
#             tool_args = json.loads(tool_call.function.arguments)

#             # Add the user_id to the tool arguments for security
#             tool_args["user_id"] = user_id

#             # Simulate the tool call execution
#             # In a real implementation, you'd call the actual MCP tools
#             output = self._execute_tool_call(tool_name, tool_args)

#             tool_outputs.append({
#                 "tool_call_id": tool_call.id,
#                 "output": json.dumps(output)
#             })

#         # Submit the tool outputs to continue the run
#         run = self.client.beta.threads.runs.submit_tool_outputs(
#             thread_id=thread_id,
#             run_id=run.id,
#             tool_outputs=tool_outputs
#         )

#         return run

#     def _execute_tool_call(self, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
#         """
#         Execute a tool call (simulated - in real implementation would call MCP server)
#         """
#         # In a real implementation, this would call the MCP server
#         # For now, we'll simulate the response
#         print(f"Simulating tool call: {tool_name} with args: {tool_args}")

#         # Remove user_id from args before simulating (since it's for internal use)
#         user_id = tool_args.pop("user_id", None)

#         # Simulate different tool responses based on the tool name
#         if tool_name == "add_task":
#             return {
#                 "status": "success",
#                 "message": f"Task '{tool_args.get('title', 'Untitled')}' added successfully",
#                 "task_id": 1  # Simulated ID
#             }
#         elif tool_name == "list_tasks":
#             return {
#                 "status": "success",
#                 "tasks": [{"id": 1, "title": "Sample task", "completed": False}],
#                 "count": 1
#             }
#         elif tool_name == "complete_task":
#             return {
#                 "status": "success",
#                 "message": f"Task {tool_args.get('task_id')} marked as completed"
#             }
#         elif tool_name == "update_task":
#             return {
#                 "status": "success",
#                 "message": f"Task {tool_args.get('task_id')} updated successfully"
#             }
#         elif tool_name == "delete_task":
#             return {
#                 "status": "success",
#                 "message": f"Task {tool_args.get('task_id')} deleted successfully"
#             }
#         else:
#             return {
#                 "status": "error",
#                 "message": f"Unknown tool: {tool_name}"
#             }

#     def _extract_tool_calls_from_run(self, run) -> list:
#         """
#         Extract tool calls from a run for logging purposes
#         """
#         if hasattr(run, 'required_action') and run.required_action:
#             if hasattr(run.required_action, 'submit_tool_outputs'):
#                 tool_calls = run.required_action.submit_tool_outputs.tool_calls
#                 return [
#                     {
#                         "id": tc.id,
#                         "name": tc.function.name,
#                         "arguments": tc.function.arguments
#                     } for tc in tool_calls
#                 ]
#         return []


# # Global instance
# ai_service = AIService()

import os
import asyncio
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))
class AIService:
    """
    AI Service using Google Gemini model with OpenAI-compatible API.
    """
    def __init__(self):
        # Load API key from .env and strip whitespace
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing in .env")

        # Gemini client with OpenAI-compatible API
        self.client = OpenAI(
            api_key="AIzaSyCCMH6abI1g0ki25t8bYwfSaH1qOg2bWX0",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        self.model = "gemini-2.5-flash"

    async def run_async(self, message: str) -> str:
        """
        Run the agent asynchronously and return the assistant's response.
        """
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_completion, message)

    def _sync_completion(self, message: str) -> str:
        """
        Helper method to run the completion synchronously.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful assistant that helps users manage their todo lists.
                    You can add, list, update, complete, and delete tasks using natural language.
                    Always confirm actions with the user before making changes.
                    Be friendly and concise in your responses."""
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content

    def run_sync(self, message: str) -> str:
        """
        Run the agent synchronously and return the assistant's response.
        """
        return self._sync_completion(message)


# Global instance
ai_service = AIService()
