---
id: 001
title: Create MCP Server Spec
stage: spec
date: 2026-01-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-mcp-server
user: Claude Code User
command: /sp.specify
labels: ["specification", "mcp", "todo", "server"]
links:
  spec: specs/001-mcp-server/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-mcp-server/spec.md
  - specs/001-mcp-server/checklists/requirements.md
tests:
  - spec quality validation
---

## Prompt

```text
# sp.specify.md
## Phase III – MCP Server (Todo Task Tools)

---
## Purpose
The MCP Server provides a **standardized, stateless tool interface** for AI agents to manage
Todo tasks via natural language.
It exposes **task-related operations as MCP tools** using `FastMCP` and delegates **all
business logic, authentication, and authorization** to the existing **Phase II FastAPI backend APIs**.
The MCP server acts strictly as a **thin proxy layer** between AI agents and backend APIs.
---

## Scope

### In Scope
- MCP tool definitions for task CRUD
- Stateless HTTP MCP server using FastMCP
- Proxying requests to existing FastAPI backend APIs
- Task operations scoped implicitly by authenticated user context

### Out of Scope
- Authentication or authorization logic
- JWT parsing or validation
- Database access
- Chat logic or agent reasoning
- Frontend UI

---

## Architecture
Agent (OpenAI Agents SDK)
|
v
MCP Server (FastMCP)
|
v
FastAPI Backend (Auth + CRUD)
|
v
PostgreSQL (Neon)

yaml
Copy code
---
## Technology Stack

| Component | Technology |
|---------|------------|
| MCP SDK | `mcp.server.fastmcp` |
| Language | Python 3.13 |
| HTTP Client | httpx |
| Runtime | uv |
| Port | 8001 (configurable) |

---

## Server Configuration

```python
mcp = FastMCP(
  "todo-mcp-server",
  stateless_http=True
)
Runs as a standalone UV project
Exposes mcp.streamable_http_app()
Listens on port 8001
Holds no runtime state

Design Principles
MCP server is a thin proxy layer
No authentication logic
No JWT parsing or validation
No database access
All security and user isolation enforced by backend
Tools are deterministic and stateless

MCP Tools Specification
Tool: add_task
Purpose
Create a new task for the authenticated user.

Parameters
title (string, required)
description (string, optional)

Behavior
Calls POST /api/tasks
Backend assigns task to authenticated user

Returns
json
Copy code
{
  "task_id": 5,
  "status": "created",
  "title": "Buy groceries"
}
Tool: list_tasks
Purpose
Retrieve tasks for the authenticated user.

Parameters
status (string, optional: all | pending | completed)
Behavior
Calls GET /api/tasks
Applies status filter if provided

Returns
json
Copy code
[
  { "id": 1, "title": "Buy groceries", "completed": false }
]
Tool: update_task
Purpose
Modify task title or description.

Parameters
task_id (integer, required)
title (string, optional)
description (string, optional)

Behavior
Calls PUT /api/tasks/{id}

Returns
json
Copy code
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy groceries and fruits"
}
Tool: complete_task
Purpose
Mark a task as completed.

Parameters
task_id (integer, required)

Behavior
Calls PATCH /api/tasks/{id}/complete

Returns
json
Copy code
{
  "task_id": 3,
  "status": "completed",
  "title": "Call mom"
}
Tool: delete_task
Purpose
Delete a task.

Parameters
task_id (integer, required)

Behavior
Calls DELETE /api/tasks/{id}

Returns
json
Copy code
{
  "task_id": 2,
  "status": "deleted",
  "title": "Old task"
}
Error Handling
MCP server does not interpret authentication errors
Backend errors are passed through as structured responses
No stack traces are exposed to agents

Deployment & Runtime
Standalone UV project

Run command
bash
Copy code
uv run python main.py
Example endpoint

text
Copy code
http://localhost:8001/mcp

Acceptance Criteria
MCP server runs independently on port ≠ 8000
No authentication or user logic exists in MCP
All tools correctly proxy to backend APIs
Tools are callable via OpenAI Agents SDK
Server remains fully stateless
```

## Response snapshot

Created a comprehensive specification for the MCP Server feature that enables AI agents to manage todo tasks through standardized tools. The specification includes:

- User scenarios for AI agent task management with priority levels
- Functional requirements covering all MCP operations (add, list, update, complete, delete)
- Success criteria with measurable outcomes
- Edge cases and error handling considerations
- Dependencies and assumptions
- Quality validation checklist

The specification defines a stateless proxy server that exposes task management operations as MCP tools while delegating all business logic, authentication, and authorization to the existing backend API.

## Outcome

- ✅ Impact: Created complete feature specification for MCP server enabling AI agent task management
- 🧪 Tests: Spec quality validation completed successfully
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready for planning phase with /sp.plan
- 🧠 Reflection: Specification successfully abstracts technical implementation while maintaining necessary detail for planning

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase