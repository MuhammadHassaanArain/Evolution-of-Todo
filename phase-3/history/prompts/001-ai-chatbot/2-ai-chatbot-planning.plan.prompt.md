---
id: 2
title: "AI Chatbot Planning"
stage: plan
date: "2026-01-14"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "001-ai-chatbot"
branch: "001-ai-chatbot"
user: "Claude Code"
command: "/sp.plan"
labels: ["planning", "architecture", "ai", "chatbot"]
links:
  spec: "specs/001-ai-chatbot/spec.md"
  plan: "specs/001-ai-chatbot/plan.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-ai-chatbot/plan.md"
  - "specs/001-ai-chatbot/research.md"
  - "specs/001-ai-chatbot/data-model.md"
  - "specs/001-ai-chatbot/quickstart.md"
  - "specs/001-ai-chatbot/contracts/chat-api.yaml"
tests:
  - "implementation plan created"
  - "research completed"
  - "data models designed"
  - "api contracts defined"
prompt_text: |
  # sp.plan.md
  ## Phase III – AI-Powered Todo Chatbot

  ---

  ## Goal

  Introduce a natural-language chatbot into the existing Todo application that uses:
  - **OpenAI Agents SDK** for reasoning
  - **MCP Server** for tool execution
  - **Existing Phase II FastAPI CRUD APIs** for all task operations

  All development is **spec-driven** and generated via **Claude Code**.

  ---

  ## High-Level Plan

  ### 1. Extend Architecture (No Breaking Changes)
  - Keep Phase II backend APIs unchanged
  - Add chatbot-specific backend modules
  - Add chatbot UI to existing frontend via button/icon

  ---

  ## Backend Plan (FastAPI)

  ### 2. Database Extensions
  - Add `Conversation` and `Message` models
  - Create migrations for new tables
  - Ensure all chat state is DB-persisted

  ---

  ### 3. MCP Server Layer
  - Create standalone MCP server using Official MCP SDK
  - Define MCP tools:
    - `add_task`
    - `list_tasks`
    - `update_task`
    - `complete_task`
    - `delete_task`
  - Each tool:
    - Is stateless
    - Calls existing Phase II CRUD endpoints
    - Enforces user ownership

  ---

  ### 4. OpenAI Agent Layer
  - Configure Agent using OpenAI Agents SDK
  - Attach MCP tools to agent
  - Define behavior rules from `sp.specify.md`
  - Enable multi-tool chaining when needed
  - Ensure friendly confirmations & error handling

  ---

  ### 5. Chat API Endpoint
  - Implement `POST /api/chat`
  - Stateless request lifecycle:
    1. Load conversation history
    2. Append user message
    3. Run agent
    4. Capture tool calls
    5. Store assistant message
    6. Return response

  ---

  ## Frontend Plan (Next.js)

  ### 6. Chatbot UI
  - Add chatbot icon/button to main layout
  - Open chat panel or modal
  - Implement message list (user/assistant)
  - Input box + send button
  - Loading state during agent execution

  ---

  ### 7. Frontend Chat Integration
  - Call `/api/chat` endpoint
  - Maintain conversation_id client-side
  - Render assistant responses
  - Display action confirmations clearly
  - Handle errors gracefully

  ---

  ## Integration Plan

  ### 8. Authentication
  - Reuse Better Auth session
  - Infer `user_id` server-side
  - Prevent cross-user data access

  ---

  ### 9. Testing & Validation
  - Validate all natural language flows
  - Confirm MCP tool invocation correctness
  - Test chained tool calls
  - Verify statelessness via server restart
  - Ensure conversation resumes correctly

  ---

  ## Documentation Plan

  ### 10. Deliverables
  - Update `/specs` with Phase III documents
  - Add MCP & Agent documentation
  - Update README with chatbot usage
  - Maintain CLAUDE.md prompts

  ---

  ## Exit Criteria

  - Chatbot manages todos via natural language
  - Agent uses MCP tools exclusively
  - No duplication of CRUD logic
  - Stateless backend verified
  - Phase IV-ready architecture
response_text: |
  Completed comprehensive planning for AI-powered todo chatbot feature:
  - Created implementation plan with technical context
  - Researched key unknowns (OpenAI integration, MCP setup, etc.)
  - Designed data models for Conversation and Message entities
  - Defined API contracts for chat functionality
  - Created quickstart guide for development
  - All deliverables created according to plan workflow
outcome: |
  Successfully completed Phase 1 planning for the AI-powered todo chatbot. All required artifacts created including plan, research, data models, API contracts, and quickstart guide. The plan aligns with constitutional principles and is ready for the task generation phase.
evaluation: |
  Planning phase successful:
  - All required artifacts created (plan, research, data models, contracts)
  - Constitutional compliance verified
  - Technical unknowns resolved through research
  - Architecture aligns with existing system
  - Ready for task breakdown and implementation
---