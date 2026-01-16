# Quickstart Guide: Chatbot Backend for Todo Task Management

## Setup and Installation

### Prerequisites
- Python 3.13+
- uv (runtime manager)
- Access to the existing FastAPI backend with task CRUD APIs
- MCP server running and accessible
- Valid API key for OpenAI-compatible provider (e.g., Gemini)
- Neon PostgreSQL database with conversation/message tables

### Installation Steps

1. Navigate to the backend directory
2. Install dependencies using uv:
   ```bash
   cd backend
   uv venv
   uv pip install openai-agents sqlmodel psycopg[binary]
   ```

3. Set environment variables:
   ```bash
   export API_KEY=your_openai_compatible_api_key
   export MCP_SERVER_URL=http://localhost:8001/mcp
   export DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
   ```

4. The chatbot backend integrates with the existing FastAPI application

## Configuration

### Environment Variables
- `API_KEY`: API key for OpenAI-compatible AI provider (required)
- `MCP_SERVER_URL`: URL of the MCP server (required)
- `DATABASE_URL`: PostgreSQL database connection string (required)
- `MODEL_NAME`: Name of the AI model to use (default: gemini-2.5-flash)
- `MAX_CHAT_HISTORY_TOKENS`: Maximum tokens for conversation history (default: 4000)

### Service Dependencies
- The chatbot backend must be able to reach the MCP server
- Database must be accessible for conversation persistence
- Authentication must be handled by upstream middleware

## Running the Service

### Development Mode
The chatbot backend runs as part of the existing FastAPI application:
```bash
cd backend
uv run python -m uvicorn main:app --reload
```

### Production Mode
Deploy as part of the existing backend service following the same deployment patterns as other backend components.

## Testing the Integration

### Verify MCP Server Connectivity
```bash
curl -X GET http://localhost:8001/mcp/health
```

### Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

### Security Validation

The chatbot backend ensures proper user isolation by:
1. Requiring authentication via JWT tokens for all requests
2. Scoping conversations to the authenticated user via the `user_id` field
3. Only allowing users to access their own conversations in the database
4. Using the existing authentication system from the backend API

## Using the Chat API

### Starting a New Conversation
Send a message without a conversation_id to start a new conversation:
```json
{
  "message": "Add a task to schedule dentist appointment"
}
```

### Continuing an Existing Conversation
Include the conversation_id to continue an existing conversation:
```json
{
  "conversation_id": 123,
  "message": "Show me my tasks"
}
```

### Expected Response Format
The API returns responses in the following format:
```json
{
  "conversation_id": 123,
  "response": "I've added the task 'schedule dentist appointment'.",
  "tool_calls": ["add_task"],
  "timestamp": "2026-01-16T10:30:00Z"
}
```