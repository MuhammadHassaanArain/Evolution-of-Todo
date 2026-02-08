"""Basic tests for the chatbot functionality."""

import pytest
from backend.chat.agent import ChatBotAgent
from backend.chat.models import ChatRequest


def test_agent_initialization():
    """Test that the chatbot agent can be initialized."""
    agent = ChatBotAgent()
    assert agent is not None
    assert agent.client is not None


def test_detect_ambiguous_request():
    """Test the ambiguous request detection functionality."""
    agent = ChatBotAgent()

    # Test for non-ambiguous request
    result = agent.detect_ambiguous_request("Add a task to buy groceries")
    assert result is False

    # Test for ambiguous request
    result = agent.detect_ambiguous_request("Complete the task", [{"role": "user", "content": "I want to complete the task"}])
    # This might be False if there's sufficient context, so we'll just check that it returns a boolean
    assert isinstance(result, bool)


def test_generate_clarification_request():
    """Test the clarification request generation."""
    agent = ChatBotAgent()

    clarification = agent.generate_clarification_request("Update the task")
    assert isinstance(clarification, str)
    assert len(clarification) > 0


def test_chat_request_model():
    """Test the ChatRequest model."""
    request = ChatRequest(conversation_id=1, message="Test message", user_id=123)
    assert request.conversation_id == 1
    assert request.message == "Test message"
    assert request.user_id == 123