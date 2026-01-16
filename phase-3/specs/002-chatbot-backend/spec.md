# Feature Specification: Chatbot Backend for Todo Task Management

**Feature Branch**: `002-chatbot-backend`
**Created**: 2026-01-16
**Status**: Draft
**Input**: User description: "# sp.specify.md
## Phase III – Chatbot Backend (Agent + Chat API)

---
## Purpose
The Chatbot Backend provides a **stateless conversational API** that allows authenticated
users to manage their Todo tasks using **natural language**.
It uses the **OpenAI Agents SDK** to interpret user intent and invokes **MCP tools**
(via MCP Streamable HTTP) to perform task operations. Conversation state is persisted
in the database.
This backend lives inside the existing **`backend/`** service alongside Todo CRUD APIs.
---

## Scope

### In Scope
- Chat API endpoint (`POST /api/chat`)
- Agent creation and execution using OpenAI Agents SDK
- MCP tool invocation using `agents.mcp`
- Conversation and message persistence
- Stateless request handling

### Out of Scope
- Authentication or authorization
- UI rendering
- MCP server implementation
- Task CRUD logic (handled by existing backend APIs)

---

## Architecture
Frontend Chat UI
↓
FastAPI Chat Endpoint
↓
OpenAI Agent (openai-agents)
↓
MCP Server (Streamable HTTP)
↓
FastAPI CRUD APIs → PostgreSQL

---

## Technology Stack

| Component | Technology |
|---------|------------|
| Web Framework | FastAPI |
| AI Framework | openai-agents |
| MCP Integration | agents.mcp (Streamable HTTP) |
| ORM | SQLModel |
| Database | Neon PostgreSQL |
| Runtime | uv |
| Python | 3.13 |

---

## Directory Placement
All chatbot-related code resides under:
backend/
├── chat/
│ ├── agent.py
│ ├── runner.py
│ ├── prompts.py
│ └── mcp_client.py
├── routes/
│ └── chat.py

yaml
Copy code

---
## Chat API Specification
### Endpoint
POST /api/chat

pgsql
Copy code

### Request Body

| Field | Type | Required | Description |
|-----|------|----------|-------------|
| conversation_id | integer | No | Existing conversation ID |
| message | string | Yes | User input message |

### Behavior

1. Identify authenticated user from request context
2. Load conversation history from database
3. Append user message
4. Execute OpenAI agent with MCP servers attached
5. Store assistant response
6. Return response and conversation ID

### Response
```json
{
  "conversation_id": 12,
  "response": "Your task has been added.",
  "tool_calls": ["add_task"]
}
Agent & MCP Configuration
Model Setup
Uses OpenAIChatCompletionsModel

OpenAI-compatible external provider (Gemini)
Configured via environment variables

python
Copy code
OpenAIChatCompletionsModel(
  model="gemini-2.5-flash",
  openai_client=client
)
MCP Integration (via OpenAI Agents SDK)
MCP servers are attached directly to the agent
Uses MCPServerStreamableHttp
No separate MCP client implementation
Tool selection handled automatically by the agent

Available MCP Tools
add_task
list_tasks
update_task
complete_task
delete_task

The agent never accesses the database directly.

Agent Responsibilities
Interpret natural language input
Decide which MCP tool(s) to invoke
Chain multiple tool calls if required
Produce clear, user-friendly confirmations
Handle tool errors gracefully

Agent Instructions
The agent must:
Manage Todo tasks using MCP tools only
Never fabricate task data
Always confirm performed actions
Ask for clarification when intent is ambiguous

Conversation Persistence
Models
Conversation

Message
Flow
Create conversation if not provided

Append user and assistant messages per request
No in-memory or session-based state
Stateless Design
Each request is independent
Conversation state reconstructed from database
Server restarts do not affect conversations

Horizontally scalable

Error Handling
MCP/tool errors returned as assistant messages
Task-not-found handled gracefully
No internal stack traces exposed to clients

Environment Variables
env
Copy code
API_KEY=...
MCP_SERVER_URL=http://localhost:8000/mcp/

Acceptance Criteria
Chat endpoint responds correctly
Agent uses MCP tools for all task operations
Conversation resumes correctly after restart
No authentication logic present
Fully stateless execution"

## Dependencies and Assumptions

- **Dependency**: MCP Server is operational and accessible at the configured URL
- **Dependency**: Existing FastAPI backend with task CRUD APIs is available
- **Dependency**: Database with conversation/message tables is available
- **Assumption**: Authentication is handled by upstream middleware
- **Assumption**: OpenAI-compatible AI provider (e.g., Gemini) is configured
- **Assumption**: Database schema for conversations and messages is available
- **Assumption**: Users have valid authentication tokens for the existing system

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Task Management (Priority: P1)

A user interacts with the chatbot through the frontend UI using natural language to manage their tasks. The user can say things like "Add a task to buy groceries" or "Show me my pending tasks" and the system processes these requests using AI to call the appropriate task management functions.

**Why this priority**: This is the core functionality that enables natural language interaction with the task management system, providing the primary value proposition of the feature.

**Independent Test**: A user can send a natural language message to the chat endpoint and receive a proper response that indicates the task operation was performed successfully, with the conversation state properly persisted.

**Acceptance Scenarios**:

1. **Given** a user is authenticated and has access to the chat interface, **When** the user sends a message "Add a task to buy milk", **Then** a new task titled "buy milk" is created and the user receives confirmation
2. **Given** a user has existing tasks, **When** the user sends a message "What are my tasks?", **Then** the system returns a list of the user's tasks in natural language format

---

### User Story 2 - Conversational Task Workflow (Priority: P1)

A user engages in a multi-turn conversation with the chatbot to perform complex task management operations. The system maintains conversation context and can handle follow-up requests like "Update the grocery task to include bread" after the initial task was created.

**Why this priority**: This enables more sophisticated task management interactions beyond simple one-off commands, making the system more useful and natural to use.

**Independent Test**: A user can have a multi-turn conversation where subsequent requests reference previous context (e.g., task IDs or titles) and the system correctly processes these requests.

**Acceptance Scenarios**:

1. **Given** a user has just created a task, **When** the user sends a follow-up message "Mark that task as completed", **Then** the system identifies the referenced task and marks it as completed
2. **Given** a user has multiple tasks, **When** the user sends a message "Update the meeting task to tomorrow", **Then** the system identifies the correct task and updates its details

---

### User Story 3 - Error Handling and Clarification (Priority: P2)

When a user's request is ambiguous or cannot be processed, the system asks for clarification rather than failing silently or making incorrect assumptions. The system gracefully handles errors from underlying services.

**Why this priority**: This ensures a good user experience even when requests are unclear or backend services are temporarily unavailable.

**Independent Test**: When a user sends an ambiguous request, the system responds with a clarifying question rather than guessing incorrectly or failing.

**Acceptance Scenarios**:

1. **Given** a user sends an ambiguous request like "Update the task", **When** the system cannot determine which task to update, **Then** the system asks for clarification
2. **Given** the MCP server is temporarily unavailable, **When** a user sends a task management request, **Then** the system returns an appropriate error message to the user

---

### Edge Cases

- What happens when the AI model is temporarily unavailable? The system should return a graceful error message to the user
- How does the system handle extremely long user messages that exceed API limits? The system should truncate or reject with appropriate error
- What occurs when conversation history becomes very large? The system should implement conversation history limiting to prevent performance issues
- How does the system handle malformed requests from the frontend? The system should validate inputs and return appropriate error responses
- What happens when the MCP server returns errors? The system should propagate meaningful error messages to the user

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a POST /api/chat endpoint that accepts user messages and returns AI-generated responses
- **FR-002**: System MUST use OpenAI Agents SDK to interpret natural language and determine appropriate actions
- **FR-003**: System MUST integrate with MCP server using streamable HTTP to invoke task management tools
- **FR-004**: System MUST persist conversation history in the database with user context
- **FR-005**: System MUST support both new conversations and continuation of existing conversations
- **FR-006**: System MUST handle the full set of task operations: add_task, list_tasks, update_task, complete_task, delete_task
- **FR-007**: System MUST maintain statelessness at the request level while persisting conversation state in the database
- **FR-008**: System MUST return structured responses including conversation ID, response text, and tool calls made
- **FR-009**: System MUST validate user inputs and handle errors gracefully without exposing internal details
- **FR-010**: System MUST support configurable AI model settings via environment variables

### Key Entities

- **Conversation**: Represents a user's ongoing dialogue with the chatbot, containing metadata like user_id and creation timestamp
- **Message**: Represents an individual exchange in a conversation, including sender (user/assistant), content, timestamp, and associated tool calls
- **User Context**: Represents the authenticated user making the request, used to scope conversations and tasks appropriately

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully create, read, update, and delete tasks using natural language with 90%+ success rate
- **SC-002**: The chat endpoint responds to 95% of requests within 5 seconds under normal load conditions
- **SC-003**: Conversation state is properly maintained across requests with 99%+ accuracy
- **SC-004**: The system can handle 100 concurrent users engaging in chat interactions without performance degradation
- **SC-005**: Error rates for AI interpretation and tool invocation remain below 5% during normal operation