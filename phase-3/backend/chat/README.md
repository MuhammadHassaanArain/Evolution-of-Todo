# Chatbot Backend for Todo Task Management

This module provides a stateless conversational API that allows authenticated users to manage their Todo tasks using natural language.

## Architecture

The chatbot backend follows a modular architecture:

- `agent.py`: Contains the ChatBotAgent that interprets natural language and manages tasks using MCP tools
- `runner.py`: Handles the execution of chat requests and conversation management
- `models.py`: Defines Pydantic models for request/response validation
- `mcp_client.py`: Manages integration with MCP servers for task operations
- `prompts.py`: Contains prompt templates (to be implemented)

## Key Features

- Natural language processing for task management
- Conversation state persistence
- MCP tool integration for task operations (add, list, update, complete, delete)
- Error handling and clarification for ambiguous requests
- User authentication and authorization

## Environment Variables

- `API_KEY`: API key for the AI model provider
- `MODEL_NAME`: Name of the AI model to use (default: gemini-2.5-flash)
- `MCP_SERVER_URL`: URL of the MCP server for task operations

## Error Handling

The system handles various error conditions:

- AI model unavailability
- MCP tool failures
- Ambiguous user requests
- Authentication issues
- Database connection problems

## Integration Points

- Integrates with the existing authentication system via `dependencies/auth.py`
- Persists conversations and messages in the database via `database/models/conversation.py`
- Uses MCP tools for actual task operations