---
id: 003
title: Database Layer Tasks
stage: tasks
date: 2026-01-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: database-layer
branch: 001-database-layer
user: Claude Code User
command: /sp.tasks
labels: [database, sqlmodel, ownership, tasks, planning]
links:
  spec: specs/001-database-layer/spec.md
  plan: specs/001-database-layer/plan.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-database-layer/tasks.md
tests:
 - null
---

## Prompt

```text
$ARGUMENTS
```

## Response snapshot

# Tasks: Database Layer with User Ownership

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
- [ ] T002 Initialize Python project with SQLModel, psycopg2-binary, and other dependencies in backend/
- [ ] T003 [P] Configure linting and formatting tools (ruff, black) in backend/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Setup database configuration and connection management in backend/src/config/database.py
- [ ] T005 [P] Create base SQLModel with common fields in backend/src/models/base.py
- [ ] T006 [P] Setup environment configuration management in backend/src/config/settings.py
- [ ] T007 Create database utility functions for initialization in backend/src/database/utils.py
- [ ] T008 Configure error handling and logging infrastructure in backend/src/utils/errors.py
- [ ] T009 Setup database migration framework in backend/src/database/migrations.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Data Isolation (Priority: P1) 🎯 MVP

**Goal**: Implementation of SQLModel schemas for User and Todo entities with proper foreign key relationships to enforce user ownership at the database level, ensuring data isolation between users.

**Independent Test**: Can be fully tested by creating multiple users with their own data and verifying that one user cannot access another user's data through direct database queries.

### Implementation for User Story 1

- [ ] T010 [P] [US1] Create User model with proper fields and constraints in backend/src/models/user.py
- [ ] T011 [P] [US1] Create Todo model with proper fields and foreign key to User in backend/src/models/todo.py
- [ ] T012 [US1] Implement User-Todo relationship with proper constraints in backend/src/models/user.py and backend/src/models/todo.py
- [ ] T013 [US1] Add proper indexing for user-scoped queries in backend/src/models/user.py and backend/src/models/todo.py
- [ ] T014 [US1] Implement database schema creation with all constraints in backend/src/database/schema.py
- [ ] T015 [US1] Add validation logic for User model in backend/src/models/user.py
- [ ] T016 [US1] Add validation logic for Todo model in backend/src/models/todo.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Data Ownership Modeling (Priority: P1)

**Goal**: Database-level enforcement of user ownership through foreign key constraints, ensuring that data relationships are enforced by the database itself.

### Implementation for User Story 2

- [ ] T017 [P] [US2] Implement foreign key constraint validation in backend/src/models/todo.py
- [ ] T018 [US2] Add cascading delete behavior for User deletion in backend/src/models/todo.py
- [ ] T019 [US2] Implement non-nullable owner_id constraint in backend/src/models/todo.py
- [ ] T020 [US2] Add unique constraints for email and username in backend/src/models/user.py
- [ ] T021 [US2] Add referential integrity checks in backend/src/database/constraints.py
- [ ] T022 [US2] Create database session management for ownership validation in backend/src/database/session.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Database Initialization (Priority: P2)

**Goal**: Implementation of deterministic database schema initialization across environments to ensure consistent deployments.

### Implementation for User Story 3

- [ ] T023 [P] [US3] Create database initialization function in backend/src/database/init.py
- [ ] T024 [US3] Implement proper database connection handling in backend/src/database/connection.py
- [ ] T025 [US3] Add database health check functionality in backend/src/database/health.py
- [ ] T026 [US3] Create initialization script with environment support in backend/src/database/scripts.py
- [ ] T027 [US3] Add sample data creation for testing in backend/src/database/sample_data.py
- [ ] T028 [US3] Implement proper cleanup and validation after initialization in backend/src/database/init.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T029 [P] Documentation updates in backend/docs/database-models.md
- [ ] T030 Code cleanup and refactoring across all models
- [ ] T031 Performance optimization of database queries
- [ ] T032 [P] Additional unit tests in backend/tests/unit/
- [ ] T033 Security hardening of database connections
- [ ] T034 Run quickstart validation and testing
- [ ] T035 Integration testing of all models together in backend/tests/integration/

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
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Depends on User models from US1
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Uses all models from US1 and US2

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
Task: "Create User model with proper fields and constraints in backend/src/models/user.py"
Task: "Create Todo model with proper fields and foreign key to User in backend/src/models/todo.py"
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

- ✅ Impact: Created comprehensive task list for database layer implementation with user ownership
- 🧪 Tests: Tasks organized by user stories with clear dependencies and parallelization opportunities
- 📁 Files: Created tasks.md with 35 specific, actionable tasks across 6 phases
- 🔁 Next prompts: Ready for implementation phase
- 🧠 Reflection: Tasks follow checklist format and enable independent implementation of each user story

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A