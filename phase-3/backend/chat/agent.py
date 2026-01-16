"""Chatbot agent implementation for task management."""

import os
from typing import Dict, Any, List, Optional
from openai import OpenAI
from openai.types.chat import ChatCompletion
from .models import ChatRequest, ChatResponse, ToolCall
from .mcp_client import mcp_client
from ..utils.logging import setup_logger
from ..utils.errors import handle_chat_error, AgentError


class ChatBotAgent:
    """Agent that interprets natural language and manages tasks using MCP tools."""

    def __init__(self):
        self.logger = setup_logger("chatbot_agent")
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY environment variable must be set")

        self.client = OpenAI(api_key=self.api_key)
        self.model_name = os.getenv("MODEL_NAME", "gemini-2.5-flash")

        # Initialize MCP integration
        self.mcp_client = mcp_client

    def enhance_with_memory(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Enhance conversation with memory capabilities to track context.

        Args:
            messages: List of messages in the conversation

        Returns:
            Enhanced list of messages with memory context
        """
        # In a real implementation, this would use more sophisticated memory mechanisms
        # For now, we'll just return the messages as-is since the AI model handles context
        return messages

    def detect_ambiguous_request(self, message: str, context: Optional[List[Dict[str, str]]] = None) -> bool:
        """
        Detect if a user's request is ambiguous and needs clarification.

        Args:
            message: The user's message
            context: The conversation context

        Returns:
            True if the request is ambiguous, False otherwise
        """
        # Simple heuristic to detect ambiguous requests
        ambiguous_indicators = [
            "the task",  # Vague reference without specific ID or title
            "that task",  # Vague reference
            "the thing",  # Vague reference
            "it",  # Ambiguous pronoun without clear antecedent
        ]

        lower_message = message.lower()

        # Check for ambiguous indicators
        for indicator in ambiguous_indicators:
            if indicator in lower_message:
                # Check if there's sufficient context to resolve the ambiguity
                if not self._has_sufficient_context(indicator, context):
                    return True

        return False

    def _has_sufficient_context(self, ambiguous_phrase: str, context: Optional[List[Dict[str, str]]]) -> bool:
        """
        Check if the conversation context provides sufficient information to resolve ambiguity.

        Args:
            ambiguous_phrase: The ambiguous phrase detected
            context: The conversation context

        Returns:
            True if context is sufficient, False otherwise
        """
        if not context:
            return False

        # Look for recent references that might clarify the ambiguous phrase
        for message in reversed(context[-5:]):  # Check last 5 messages
            if 'task' in ambiguous_phrase and ('task' in message['content'].lower() or
                                              'title' in message['content'].lower() or
                                              'id' in message['content'].lower()):
                return True

        return False

    def generate_clarification_request(self, message: str) -> str:
        """
        Generate a clarification request for an ambiguous user message.

        Args:
            message: The ambiguous user message

        Returns:
            A clarification request message
        """
        # Generate a contextually appropriate clarification request
        if "the task" in message.lower() or "that task" in message.lower():
            return ("I'm not sure which task you're referring to. Could you please specify the task by its title or ID?")
        elif "it" in message.lower():
            return ("I'm not sure what you're referring to. Could you please be more specific?")
        else:
            return ("I'm not sure I understood your request correctly. Could you please provide more details?")

    def process_message(
        self,
        message: str,
        conversation_context: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Process a user message and return an appropriate response.

        Args:
            message: The user's message
            conversation_context: Previous conversation history

        Returns:
            Dictionary with response and any tool calls made
        """
        try:
            # Check if the message is ambiguous and needs clarification
            if self.detect_ambiguous_request(message, conversation_context):
                clarification = self.generate_clarification_request(message)
                return {
                    "response": clarification,
                    "tool_calls": [],
                    "tool_responses": []
                }

            # Prepare the conversation history for the AI model
            messages = []

            # Add system message to instruct the agent
            messages.append({
                "role": "system",
                "content": (
                    "You are a helpful assistant that manages tasks for users. "
                    "Use the available tools to create, list, update, complete, or delete tasks. "
                    "Always confirm actions with the user before performing them. "
                    "If the user's request is ambiguous, ask for clarification. "
                    "Never fabricate task data - always use the tools to interact with the task system."
                )
            })

            # Add conversation history if available
            if conversation_context:
                messages.extend(conversation_context)

            # Add the current user message
            messages.append({
                "role": "user",
                "content": message
            })

            # Create the chat completion with available tools
            response: ChatCompletion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "add_task",
                            "description": "Add a new task",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string", "description": "Title of the task"},
                                    "description": {"type": "string", "description": "Description of the task"}
                                },
                                "required": ["title"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "list_tasks",
                            "description": "List tasks with optional status filter",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "status": {"type": "string", "enum": ["all", "pending", "completed"]}
                                }
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "update_task",
                            "description": "Update an existing task",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "task_id": {"type": "integer", "description": "ID of the task to update"},
                                    "title": {"type": "string", "description": "New title for the task"},
                                    "description": {"type": "string", "description": "New description for the task"}
                                },
                                "required": ["task_id"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "complete_task",
                            "description": "Mark a task as completed",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "task_id": {"type": "integer", "description": "ID of the task to complete"}
                                },
                                "required": ["task_id"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "delete_task",
                            "description": "Delete a task",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "task_id": {"type": "integer", "description": "ID of the task to delete"}
                                },
                                "required": ["task_id"]
                            }
                        }
                    }
                ],
                tool_choice="auto"  # Let the model decide which tool to use
            )

            # Process the response
            choice = response.choices[0]
            message_response = choice.message

            result = {
                "response": "",
                "tool_calls": [],
                "tool_responses": []
            }

            # Get the agent's response text
            if message_response.content:
                result["response"] = message_response.content

            # Process any tool calls
            import json
            if message_response.tool_calls:
                self.logger.info(f"Processing {len(message_response.tool_calls)} tool calls for user message: {message[:50]}...")

                for tool_call in message_response.tool_calls:
                    tool_name = tool_call.function.name
                    try:
                        tool_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        tool_args = {}
                        self.logger.warning(f"Failed to parse tool arguments for {tool_name}")

                    result["tool_calls"].append(tool_name)
                    self.logger.info(f"Tool call: {tool_name} with args: {tool_args}")

                    # In a real implementation, we would call the actual tools
                    # For now, we'll just record what tools were called
                    tool_response = f"Called {tool_name} with args: {tool_args}"
                    result["tool_responses"].append(tool_response)

                self.logger.info(f"Completed tool calls: {result['tool_calls']}")

            return result

        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")

            # Check if the error is related to AI model unavailability
            error_str = str(e).lower()
            if any(keyword in error_str for keyword in ["api", "rate limit", "timeout", "connection", "model"]):
                self.logger.warning("AI model unavailability detected")
                return {
                    "response": "I'm currently unable to process your request. The AI service might be temporarily unavailable. Please try again in a moment.",
                    "tool_calls": [],
                    "tool_responses": []
                }

            error_response = handle_chat_error(
                e,
                self.logger,
                context={"message": message, "model": self.model_name}
            )
            return {
                "response": error_response.get("message", "Sorry, I encountered an error processing your request."),
                "tool_calls": [],
                "tool_responses": []
            }


# Global agent instance
agent = ChatBotAgent()


def get_agent() -> ChatBotAgent:
    """Get the global agent instance."""
    return agent