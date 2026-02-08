---
id: 001
title: Create Chatbot Spec
stage: spec
date: 2026-01-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-chatbot-backend
branch: 002-chatbot-backend
user: Claude Code User
command: /sp.specify
labels: ["specification", "chatbot", "ai", "conversational"]
links:
  spec: specs/002-chatbot-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-chatbot-backend/spec.md
  - specs/002-chatbot-backend/checklists/requirements.md
tests:
  - spec quality validation
---

## Prompt

```text
# sp.specify.md
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
Fully stateless execution
```

## Response snapshot

Created a comprehensive specification for the Chatbot Backend feature that enables users to manage todo tasks through natural language conversations. The specification includes:

- User scenarios for natural language task management with priority levels
- Functional requirements covering the chat API, agent integration, and MCP tool invocation
- Success criteria with measurable outcomes
- Edge cases and error handling considerations
- Dependencies and assumptions
- Quality validation checklist

The specification defines a stateless conversational API that uses OpenAI Agents SDK to interpret user intent and invokes MCP tools to perform task operations, with conversation state persisted in the database.

## Outcome

- ✅ Impact: Created complete feature specification for chatbot backend enabling natural language task management
- 🧪 Tests: Spec quality validation completed successfully
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready for planning phase with /sp.plan
- 🧠 Reflection: Specification successfully abstracts technical implementation while maintaining necessary detail for planning

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase