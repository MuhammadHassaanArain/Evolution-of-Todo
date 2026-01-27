---
id: 1
title: make-tasks-endpoints-public
stage: general
date_iso: 2026-01-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 002-chatbot-backend
user: Claude
command: "Implement changes to make tasks endpoints public"
labels: ["security", "api", "authentication"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/src/api/tasks.py
  - backend/src/main.py
  - backend/src/services/task_service.py
  - backend/src/models/task.py
  - backend/src/database/migrate.py
  - frontend/services/task.ts
  - frontend/services/api-client.js
  - frontend/middleware.ts
  - mcp-server/src/main.py
tests_yaml: |
  - "Manual testing of tasks endpoints without authentication"
prompt_text: |
  You are working on a full-stack TODO application with:
  - FastAPI backend (src-based structure)
  - Frontend (Next.js or similar)
  - Token-based authentication already implemented and working

  Goal:
  Make ONLY the "tasks" endpoints public.

  Important constraints (must follow strictly):
  - ❌ Do NOT remove authentication from all endpoints
  - ❌ Do NOT change or break existing auth logic
  - ❌ Do NOT touch auth for users, chat, or any other protected routes
  - ✅ ONLY remove authentication requirements from TASKS endpoints

  Your tasks:

  BACKEND (FastAPI):
  1. Locate all "tasks" related endpoints (e.g. `/tasks`, `/tasks/{id}`, create/update/delete tasks).
  2. Remove authentication dependencies ONLY from these task routes:
     - Remove `Depends(get_current_user)`
     - Remove token checks for tasks routes
  3. Ensure tasks endpoints can be accessed WITHOUT passing an Authorization token.
  4. Do NOT delete or modify the authentication service itself.
  5. Keep all other endpoints protected exactly as they are.

  FRONTEND:
  6. Find all frontend API calls related to TASKS.
  7. Remove Authorization headers or token usage ONLY for task-related requests.
  8. Leave token usage untouched for all other API calls (chat, user, auth, etc).
  9. Ensure frontend works correctly with public task routes.

  CODE QUALITY:
  10. Keep imports clean and correct for the `src.` backend structure.
  11. Do not introduce duplicate logic or unnecessary changes.
  12. Keep changes minimal and focused only on tasks functionality.

  RESULT:
  - Tasks endpoints are public
  - No token is required for any task request
  - All other endpoints remain protected
  - Backend runs successfully with:
  uvicorn src.main:app --reload

  - Frontend works without passing tokens for tasks

  Proceed carefully and implement the changes.
response_text: |
  Successfully implemented changes to make tasks endpoints public:

  BACKEND CHANGES:
  - Removed authentication dependency from all task endpoints in backend/src/api/tasks.py
  - Updated task endpoints to use new public service methods (get_all_tasks, create_task_public, etc.)
  - Modified OpenAPI schema in backend/src/main.py to remove security requirements for task endpoints
  - Added new public service methods in backend/src/services/task_service.py that don't enforce user ownership
  - Updated backend/src/models/task.py to allow nullable user_id for public tasks

  FRONTEND CHANGES:
  - Updated frontend/services/task.ts to set requiresAuth: false for all task API calls
  - Updated frontend/services/api-client.js to set requiresAuth: false for all task API calls
  - Updated frontend/middleware.ts to remove '/api/tasks' from protected paths

  MCP SERVER CHANGES:
  - Updated mcp-server/src/main.py to remove authentication headers from all task-related API calls

  Security Note:
  This change makes all tasks publicly accessible without authentication. Previously, tasks were user-specific and required authentication to access. The new implementation allows anyone to access, create, update, and delete any task without authentication. This represents a significant security change where task data is now public rather than user-specific.

  The implementation maintains the same API contract but removes the user isolation layer.
outcome: |
  Tasks endpoints are now public and accessible without authentication while all other endpoints remain protected.
evaluation: |
  - All task endpoints removed authentication requirements ✓
  - Other endpoints still require authentication ✓
  - Backend compiles and runs successfully ✓
  - Frontend API calls updated to not require auth for tasks ✓
  - MCP server updated to not send auth tokens for task operations ✓
  - Database model updated to support public tasks with nullable user_id ✓
  - Database schema updated to make user_id column nullable in tasks table ✓
---
