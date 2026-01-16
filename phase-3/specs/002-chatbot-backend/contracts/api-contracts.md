# API Contracts: Chatbot Backend for Todo Task Management

## Overview
The chatbot backend exposes a conversational API endpoint that allows users to manage their todo tasks using natural language. The system uses AI agents to interpret user intent and invoke MCP tools to perform task operations.

## API Endpoint

### POST /api/chat
**Purpose**: Process natural language messages from users and manage their tasks

**Request Body**:
```json
{
  "conversation_id": 123,
  "message": "Add a task to buy groceries"
}
```

**Request Parameters**:
- conversation_id (integer, optional): Existing conversation ID to continue a conversation; if omitted, a new conversation is created
- message (string, required): The user's natural language message

**Response**:
```json
{
  "conversation_id": 123,
  "response": "I've added a task to buy groceries for you.",
  "tool_calls": ["add_task"],
  "timestamp": "2026-01-16T10:30:00Z"
}
```

**Response Fields**:
- conversation_id (integer): The conversation ID (newly created if not provided)
- response (string): The AI agent's natural language response to the user
- tool_calls (array): List of MCP tools that were invoked
- timestamp (string): ISO 8601 formatted timestamp of the response

**Authentication**: Requires valid JWT token in Authorization header (handled by upstream middleware)

**Behavior**:
1. Identify authenticated user from request context
2. Load conversation history from database
3. Append user message to conversation
4. Execute OpenAI agent with MCP servers attached
5. Store assistant response in database
6. Return response and conversation ID

## MCP Tool Contracts

### add_task (via MCP)
**Called by**: AI agent when user requests to create a task
**Input**: title (string, required), description (string, optional)
**Output**: task_id, status, title

### list_tasks (via MCP)
**Called by**: AI agent when user requests to view tasks
**Input**: status (string, optional: all, pending, completed)
**Output**: Array of tasks

### update_task (via MCP)
**Called by**: AI agent when user requests to modify a task
**Input**: task_id (integer, required), title (string, optional), description (string, optional)
**Output**: task_id, status, title

### complete_task (via MCP)
**Called by**: AI agent when user requests to complete a task
**Input**: task_id (integer, required)
**Output**: task_id, status, title

### delete_task (via MCP)
**Called by**: AI agent when user requests to delete a task
**Input**: task_id (integer, required)
**Output**: task_id, status, title

## Error Responses
The API returns standard error responses when issues occur:

**400 Bad Request**:
```json
{
  "error": "validation_error",
  "message": "Invalid request parameters"
}
```

**401 Unauthorized**:
```json
{
  "error": "unauthorized",
  "message": "Authentication required"
}
```

**500 Internal Server Error**:
```json
{
  "error": "internal_error",
  "message": "An error occurred processing your request"
}
```

## Environment Configuration
- API_KEY: OpenAI-compatible API key for AI model access
- MCP_SERVER_URL: URL of the MCP server for tool access
- DATABASE_URL: Connection string for PostgreSQL database