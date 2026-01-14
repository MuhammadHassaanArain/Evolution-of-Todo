---
id: 1
title: "AI Chatbot Specification"
stage: spec
date: "2026-01-14"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "1-ai-chatbot"
branch: "1-ai-chatbot"
user: "Claude Code"
command: "/sp.specify"
labels: ["specification", "ai", "chatbot", "todo"]
links:
  spec: "specs/1-ai-chatbot/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/1-ai-chatbot/spec.md"
  - "specs/1-ai-chatbot/checklists/requirements.md"
tests:
  - "specification created"
  - "quality checklist validated"
prompt_text: |
  ## Phase III – AI-Powered Todo Chatbot (Agent + MCP)

  ---

  ## 1. Objective

  Extend the Phase II Todo application by adding an **AI-powered chatbot** that allows users to manage todos using **natural language**.

  The chatbot:
  - Lives inside the existing web app (opened via button/icon)
  - Uses **OpenAI Agents SDK** for reasoning
  - Uses an **MCP Server (Official MCP SDK)** for task tools
  - Reuses **existing FastAPI CRUD APIs** from Phase II
  - Is **fully stateless**, persisting all state in the database

  No manual coding. All implementation must be generated via **Claude Code** using Spec-Driven Development.

  ---

  ## 2. In Scope

  - Conversational task management (add, list, update, delete, complete)
  - Custom chatbot UI (no ChatKit)
  - MCP tools mapped to existing backend APIs
  - Stateless `/chat` endpoint
  - Conversation persistence in database
  - Agent-driven tool invocation

  ---

  ## 3. Out of Scope

  - Rewriting existing CRUD APIs
  - ChatKit UI or hosted ChatKit
  - Advanced NLP fine-tuning
  - Multi-agent orchestration
  - Voice or multimodal input

  ---

  ## 4. Architecture Overview

  Frontend (Next.js)
  - Existing Todo UI
  - Chatbot button/icon
  - Custom chat panel/modal UI

  Backend (FastAPI)
  - `/api/chat` endpoint (stateless)
  - OpenAI Agents SDK (Agent + Runner)
  - MCP Server (tools only)
  - SQLModel + Neon PostgreSQL

  The agent never mutates state directly.
  **All state changes happen through MCP tools calling existing APIs.**

  ---

  ## 5. Data Models (SQLModel)

  ### Task (existing)
  - id
  - user_id
  - title
  - description
  - completed
  - created_at
  - updated_at

  ### Conversation
  - id
  - user_id
  - created_at
  - updated_at

  ### Message
  - id
  - user_id
  - conversation_id
  - role (`user` | `assistant`)
  - content
  - created_at

  ---

  ## 6. Chat API Contract

  ### Endpoint
  `POST /api/chat`

  ### Request
  ```json
  {
    "conversation_id": 1,
    "message": "Add a task to buy groceries"
  }
  ```
  conversation_id optional (create new if missing)

  Authentication via existing Better Auth

  Response
  ```json
  {
    "conversation_id": 1,
    "response": "I've added 'Buy groceries' to your tasks.",
    "tool_calls": [
      { "tool": "add_task", "task_id": 5 }
    ]
  }
  ```

  7. Stateless Conversation Flow
  - Receive user message
  - Load conversation + message history from DB
  - Append new user message
  - Run OpenAI Agent with MCP tools
  - Agent invokes MCP tool(s)
  - MCP tools call existing FastAPI CRUD APIs
  - Store assistant message in DB
  - Return response
  - Server holds no memory

  8. MCP Server – Tool Specification
  The MCP server exposes tools only, no business logic.

  Tool: add_task
  - Calls: existing POST /tasks
  - Params: user_id, title, description?
  - Returns: task_id, status, title

  Tool: list_tasks
  - Calls: existing GET /tasks
  - Params: user_id, status?
  - Returns: array of tasks

  Tool: complete_task
  - Calls: existing PATCH /tasks/{id}/complete
  - Params: user_id, task_id
  - Returns: task_id, status

  Tool: update_task
  - Calls: existing PUT /tasks/{id}
  - Params: user_id, task_id, title?, description?
  - Returns: task_id, status

  Tool: delete_task
  - Calls: existing DELETE /tasks/{id}
  - Params: user_id, task_id
  - Returns: task_id, status

  9. Agent Behavior Rules
  | User Intent | Agent Action |
  |-------------|--------------|
  | Add / remember | add_task |
  | Show / list | list_tasks |
  | Done / completed | complete_task |
  | Delete / remove | delete_task |
  | Change / update | update_task |

  Additional Rules
  - Confirm every successful action
  - Gracefully handle missing tasks
  - Chain tools when required (e.g. list → delete)
  - Never expose internal tool errors directly to user

  10. Frontend Chat UI Requirements
  - Chatbot icon/button in main app layout
  - Opens modal or side panel
  - Message list (user / assistant)
  - Input box + send button
  - Loading indicator during agent execution
  - Conversation resumes after refresh

  11. Security & Auth
  - Uses existing Better Auth session
  - user_id inferred from auth context
  - Agent never receives credentials
  - MCP tools enforce user ownership

  12. Success Criteria
  - User manages todos via natural language
  - Agent correctly invokes MCP tools
  - No server-side state
  - Conversations persist across restarts
  - Existing APIs remain unchanged
  - Fully spec-driven, Claude-generated code

  13. Phase Readiness
  This architecture must be compatible with:
  - Phase IV: Kubernetes + Minikube
  - Phase V: Dapr, Kafka, Cloud deployment
response_text: |
  Created comprehensive specification for AI-powered todo chatbot feature including:
  - User scenarios with priorities (P1-P3)
  - Functional requirements (FR-001 to FR-010)
  - Key entities (Conversation, Message, Task)
  - Success criteria with measurable outcomes (SC-001 to SC-005)
  - Quality validation checklist
outcome: |
  Successfully created feature specification document that defines the AI-powered todo chatbot functionality. The specification covers user scenarios, functional requirements, and success criteria while maintaining focus on user value rather than implementation details. The spec is ready for the planning phase.
evaluation: |
  The specification meets all quality criteria:
  - Clear user-focused requirements
  - Testable acceptance scenarios
  - Measurable success criteria
  - Proper separation of concerns
  - Technology-agnostic success metrics
---