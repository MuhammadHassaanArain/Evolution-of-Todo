"""Chat runner for executing the chatbot agent and managing conversation flow."""

from typing import Dict, Any, List, Optional
from sqlmodel import Session
from .agent import agent, ChatBotAgent
from ..database.models.conversation import Conversation, Message, ConversationCreate, MessageCreate
from ..utils.logging import setup_logger, log_chat_interaction
from ..utils.errors import handle_chat_error, ConversationError, MCPIntegrationError
from .models import ChatRequest, ChatResponse
import json


class ChatRunner:
    """Handles the execution of chat requests and conversation management."""

    def __init__(self):
        self.agent = agent
        self.logger = setup_logger("chat_runner")

    def execute_chat(
        self,
        chat_request: ChatRequest,
        db_session: Session
    ) -> ChatResponse:
        """
        Execute a chat request and return the response.

        Args:
            chat_request: The incoming chat request
            db_session: Database session for persistence

        Returns:
            ChatResponse with conversation ID, response, and tool calls
        """
        # Validate and sanitize input
        if not chat_request.message or not chat_request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message cannot be empty"
            )

        # Check for excessively long messages
        if len(chat_request.message) > 10000:  # 10k character limit
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message is too long. Please limit your message to 10,000 characters."
            )

        # Sanitize the message (basic example - in production, use proper sanitization)
        chat_request.message = chat_request.message.strip()

        self.logger.info(f"Starting chat execution for user {chat_request.user_id}, conversation {chat_request.conversation_id}")
        try:
            # Get or create conversation
            if chat_request.conversation_id:
                # Load existing conversation
                conversation = db_session.get(Conversation, chat_request.conversation_id)
                if not conversation:
                    raise ConversationError(f"Conversation with ID {chat_request.conversation_id} not found")
            else:
                # Create new conversation
                conversation_data = ConversationCreate(
                    user_id=chat_request.user_id
                )
                conversation = Conversation.model_validate(conversation_data)
                db_session.add(conversation)
                db_session.commit()
                db_session.refresh(conversation)

            # Add user message to conversation
            user_message = Message(
                role="user",
                content=chat_request.message,
                conversation_id=conversation.id
            )
            db_session.add(user_message)
            db_session.commit()
            db_session.refresh(user_message)

            # Load conversation history for context
            conversation_history = self._load_conversation_history(db_session, conversation.id)

            # Enhance conversation with memory capabilities
            enhanced_history = self.agent.enhance_with_memory(conversation_history)

            # Process message with agent
            agent_response = self.agent.process_message(chat_request.message, enhanced_history)

            # Handle potential MCP tool failures
            if not agent_response.get("response") and agent_response.get("tool_calls"):
                # If there were tool calls but no response, check if any failed
                # In a real implementation, we would check the actual tool responses
                pass

            # Create assistant message
            assistant_message = Message(
                role="assistant",
                content=agent_response.get("response", ""),
                conversation_id=conversation.id,
                tool_calls=json.dumps(agent_response.get("tool_calls", [])),
                tool_responses=json.dumps(agent_response.get("tool_responses", []))
            )
            db_session.add(assistant_message)
            db_session.commit()

            # Update conversation timestamp
            conversation.updated_at = user_message.timestamp
            db_session.add(conversation)
            db_session.commit()

            # Log the interaction
            log_chat_interaction(
                self.logger,
                chat_request.user_id,
                conversation.id,
                chat_request.message,
                agent_response.get("response", ""),
                agent_response.get("tool_calls", [])
            )

            # Return response
            response = ChatResponse(
                conversation_id=conversation.id,
                response=agent_response.get("response", "I processed your request."),
                tool_calls=agent_response.get("tool_calls", []),
            )

            self.logger.info(f"Chat execution completed for conversation {conversation.id}")
            return response

        except Exception as e:
            self.logger.error(f"Error executing chat: {str(e)}")
            error_response = handle_chat_error(
                e,
                self.logger,
                context={"request": chat_request.dict() if hasattr(chat_request, 'dict') else chat_request.__dict__}
            )
            # Even if there's an error, we should still return a conversation ID if we created one
            conversation_id = chat_request.conversation_id or -1
            return ChatResponse(
                conversation_id=conversation_id,
                response=error_response.get("message", "Sorry, I encountered an error processing your request."),
                tool_calls=[]
            )

    def _load_conversation_history(
        self,
        db_session: Session,
        conversation_id: int,
        limit: int = 20
    ) -> List[Dict[str, str]]:
        """
        Load conversation history for context.

        Args:
            db_session: Database session
            conversation_id: ID of the conversation
            limit: Maximum number of messages to load

        Returns:
            List of message dictionaries for context
        """
        try:
            # Query messages for the conversation, ordered by timestamp
            messages = db_session.query(Message).filter(
                Message.conversation_id == conversation_id
            ).order_by(Message.timestamp.asc()).limit(limit).all()

            # Format messages for AI context
            formatted_messages = []
            for msg in messages:
                formatted_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            return formatted_messages

        except Exception as e:
            self.logger.error(f"Error loading conversation history: {str(e)}")
            raise ConversationError(f"Failed to load conversation history: {str(e)}")


# Global chat runner instance
chat_runner = ChatRunner()


def get_chat_runner() -> ChatRunner:
    """Get the global chat runner instance."""
    return chat_runner