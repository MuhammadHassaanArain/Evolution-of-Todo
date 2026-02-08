---
id: 003
title: Backend API Tasks
stage: tasks
date: 2026-01-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: backend-api
branch: 001-backend-api
user: Claude Code User
command: /sp.tasks
labels: [api, backend, todos, authentication, authorization, tasks]
links:
  spec: specs/001-backend-api/spec.md
  plan: specs/001-backend-api/plan.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-backend-api/tasks.md
tests:
 - null
---

## Prompt

```text
$ARGUMENTS
```

## Response snapshot

# Tasks: Backend API (Business Logic)

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend structure**: `backend/src/`, `backend/tests/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend directory structure with src/ and tests/ directories
- [ ] T002 Initialize Python project with FastAPI, python-jose, passlib, and other dependencies in backend/
- [ ] T003 [P] Configure linting and formatting tools (ruff, black) in backend/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Setup JWT authentication configuration and security settings in backend/src/config/auth.py
- [ ] T005 [P] Create JWT utility functions for token creation and validation in backend/src/utils/jwt.py
- [ ] T006 [P] Setup database connection management in backend/src/database/connection.py
- [ ] T007 Create authentication dependency for FastAPI in backend/src/api/deps.py
- [ ] T008 Configure error handling and response formatting infrastructure in backend/src/utils/errors.py
- [ ] T009 Setup API router and base configuration in backend/src/api/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Secure Todo Creation (Priority: P1) 🎯 MVP

**Goal**: Implementation of the POST /todos endpoint to allow authenticated users to create new todos with proper ownership validation.

**Independent Test**: Can be fully tested by making a POST request to `/todos` with a valid JWT and verifying that the todo is created under the authenticated user's ownership and is not accessible to other users.

### Implementation for User Story 1

- [ ] T010 [P] [US1] Create Todo schema models in backend/src/schemas/todo.py
- [ ] T011 [P] [US1] Create Todo model with proper fields and relationships in backend/src/models/todo.py
- [ ] T012 [US1] Implement Todo service for creation operations in backend/src/services/todo_service.py
- [ ] T013 [US1] Implement POST /todos endpoint with JWT validation in backend/src/api/routers/todos.py
- [ ] T014 [US1] Add validation logic for Todo creation in backend/src/models/todo.py
- [ ] T015 [US1] Add ownership derivation from JWT in backend/src/api/routers/todos.py
- [ ] T016 [US1] Implement error handling for unauthorized access in backend/src/api/routers/todos.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Personal Todo Access (Priority: P1)

**Goal**: Implementation of the GET /todos and GET /todos/{id} endpoints to allow authenticated users to access only their own todos with proper ownership validation.

### Implementation for User Story 2

- [ ] T017 [P] [US2] Implement GET /todos endpoint for listing user's todos in backend/src/api/routers/todos.py
- [ ] T018 [US2] Add ownership validation for listing todos in backend/src/services/todo_service.py
- [ ] T019 [US2] Implement GET /todos/{id} endpoint with ownership check in backend/src/api/routers/todos.py
- [ ] T020 [US2] Add todo retrieval with ownership validation in backend/src/services/todo_service.py
- [ ] T021 [US2] Add proper error responses for non-owned todos in backend/src/api/routers/todos.py
- [ ] T022 [US2] Update Todo schema to match response requirements in backend/src/schemas/todo.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Todo Management (Priority: P2)

**Goal**: Implementation of the PUT /todos/{id} and DELETE /todos/{id} endpoints to allow authenticated users to update and delete only their own todos with proper ownership validation.

### Implementation for User Story 3

- [ ] T023 [P] [US3] Implement PUT /todos/{id} endpoint with ownership validation in backend/src/api/routers/todos.py
- [ ] T024 [US3] Add todo update with ownership validation in backend/src/services/todo_service.py
- [ ] T025 [US3] Implement DELETE /todos/{id} endpoint with ownership validation in backend/src/api/routers/todos.py
- [ ] T026 [US3] Add todo deletion with ownership validation in backend/src/services/todo_service.py
- [ ] T027 [US3] Add validation logic for Todo updates in backend/src/models/todo.py
- [ ] T028 [US3] Add comprehensive error handling for all operations in backend/src/api/routers/todos.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T029 [P] Documentation updates in backend/docs/api-reference.md
- [ ] T030 Code cleanup and refactoring across all API endpoints
- [ ] T031 Performance optimization of database queries
- [ ] T032 [P] Additional unit tests in backend/tests/unit/
- [ ] T033 Security hardening of authentication and authorization
- [ ] T034 Run quickstart validation and testing
- [ ] T035 Integration testing of all endpoints together in backend/tests/integration/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Depends on Todo models from US1
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Uses all models and services from US1 and US2

### Within Each User Story

- Models before services
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Todo schema models in backend/src/schemas/todo.py"
Task: "Create Todo model with proper fields and relationships in backend/src/models/todo.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

## Outcome

- ✅ Impact: Created comprehensive task list for backend API implementation with JWT authentication and user ownership
- 🧪 Tests: Tasks organized by user stories with clear dependencies and parallelization opportunities
- 📁 Files: Created tasks.md with 35 specific, actionable tasks across 6 phases
- 🔁 Next prompts: Ready for implementation phase
- 🧠 Reflection: Tasks follow checklist format and enable independent implementation of each user story

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A