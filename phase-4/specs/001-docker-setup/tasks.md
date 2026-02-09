# Tasks: Docker Containerization for Phase-4 Todo Application

**Input**: Design documents from `/specs/001-docker-setup/`
**Prerequisites**: plan.md (completed), spec.md (completed), research.md (completed), data-model.md (completed), contracts/ (completed)

**Tests**: No test tasks included - this is infrastructure configuration work, not application logic.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

This is a web application with the following structure:
- `phase-4/` - Repository root
- `phase-4/frontend/` - Next.js frontend
- `phase-4/backend/` - FastAPI backend
- `phase-4/backend/mcp-server/` - FastMCP server

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create environment configuration template and build optimization files

- [x] T001 Create .env.example template in phase-4/.env.example with all required environment variables
- [x] T002 [P] Create .dockerignore file in phase-4/frontend/.dockerignore to exclude node_modules, .next, .git, .env files
- [x] T003 [P] Create .dockerignore file in phase-4/backend/.dockerignore to exclude .venv, __pycache__, .git, .env files
- [x] T004 [P] Create .dockerignore file in phase-4/backend/mcp-server/.dockerignore to exclude .venv, __pycache__, .git, .env files

---

## Phase 2: Foundational (Individual Service Dockerfiles)

**Purpose**: Create Dockerfiles for each service that can build and run independently

**⚠️ CRITICAL**: These Dockerfiles must be complete before docker-compose orchestration can work

- [x] T005 [P] Create Dockerfile for MCP server in phase-4/backend/mcp-server/Dockerfile using python:3.13-slim base image
- [x] T006 [P] Create Dockerfile for backend in phase-4/backend/Dockerfile using python:3.13-slim base image
- [x] T007 [P] Create Dockerfile for frontend in phase-4/frontend/Dockerfile using node:20-alpine with multi-stage build

**Checkpoint**: All three Dockerfiles created - individual service builds can now be tested

---

## Phase 3: User Story 1 - Local Development Environment Setup (Priority: P1) 🎯 MVP

**Goal**: Enable developers to start the entire application stack with a single `docker-compose up --build` command

**Independent Test**: Run `docker-compose up --build` on a fresh machine with only Docker installed, verify all three services start successfully and can communicate with each other

### Implementation for User Story 1

- [x] T008 [US1] Create docker-compose.yml in phase-4/docker-compose.yml with all three services defined
- [x] T009 [US1] Configure Docker network named 'todo-network' in docker-compose.yml for service communication
- [x] T010 [US1] Add port mappings in docker-compose.yml (frontend:3000, backend:8000, mcp-server:8001)
- [x] T011 [US1] Configure environment variables in docker-compose.yml for all services using env_file directive
- [x] T012 [US1] Add health checks in docker-compose.yml for all three services using curl commands
- [x] T013 [US1] Configure service dependencies in docker-compose.yml (frontend depends on backend, backend depends on mcp-server)
- [x] T014 [US1] Add restart policies (on-failure) in docker-compose.yml for all services
- [ ] T015 [US1] Test full stack startup with docker-compose up --build and verify all services reach healthy state
- [ ] T016 [US1] Verify frontend at localhost:3000 can communicate with backend at localhost:8000
- [ ] T017 [US1] Verify backend can communicate with MCP server using service name http://mcp-server:8001

**Checkpoint**: At this point, User Story 1 should be fully functional - all services start with one command and communicate successfully

---

## Phase 4: User Story 2 - Service Isolation and Independent Testing (Priority: P2)

**Goal**: Enable developers to build and run individual services in isolation for targeted testing

**Independent Test**: Build and run each Docker image independently (e.g., `docker build -t frontend ./frontend && docker run -p 3000:3000 frontend`) and verify the service starts correctly

### Implementation for User Story 2

- [ ] T018 [P] [US2] Test individual MCP server build with docker build -t mcp-server ./backend/mcp-server
- [ ] T019 [P] [US2] Test individual backend build with docker build -t backend ./backend
- [ ] T020 [P] [US2] Test individual frontend build with docker build -t frontend ./frontend
- [ ] T021 [US2] Run MCP server container independently with required environment variables and verify it starts
- [ ] T022 [US2] Run backend container independently with required environment variables and verify it starts
- [ ] T023 [US2] Run frontend container independently with required environment variables and verify it starts
- [ ] T024 [US2] Document individual service build and run commands in specs/001-docker-setup/quickstart.md

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - services can run together or independently

---

## Phase 5: User Story 3 - Environment Configuration Management (Priority: P2)

**Goal**: Enable developers to configure different environments using environment variables without modifying code or Dockerfiles

**Independent Test**: Run the same Docker images with different .env files and verify that services use the correct configuration for each environment

### Implementation for User Story 3

- [ ] T025 [US3] Verify .dockerignore files exclude .env from all Docker build contexts
- [ ] T026 [US3] Test environment variable changes by modifying .env and restarting containers without rebuild
- [ ] T027 [US3] Verify sensitive credentials in .env are not included in built Docker images
- [ ] T028 [US3] Document environment variable configuration in specs/001-docker-setup/quickstart.md
- [ ] T029 [US3] Create example configurations for development vs production in quickstart.md

**Checkpoint**: All user stories 1-3 should now be independently functional - full orchestration, isolation, and configuration management work

---

## Phase 6: User Story 4 - Production Deployment Readiness (Priority: P3)

**Goal**: Ensure Docker images follow best practices and are optimized for production deployment

**Independent Test**: Analyze Dockerfiles for best practices (multi-stage builds, small base images, proper layer caching) and verify images can be pushed to a container registry

### Implementation for User Story 4

- [ ] T030 [P] [US4] Verify frontend Dockerfile uses multi-stage build (builder + runner stages)
- [ ] T031 [P] [US4] Verify all Dockerfiles use non-root users (node for frontend, appuser for backend/MCP)
- [ ] T032 [P] [US4] Verify all Dockerfiles have proper layer ordering (dependencies before code)
- [ ] T033 [US4] Measure and validate image sizes (frontend <500MB, backend <300MB, mcp-server <300MB)
- [ ] T034 [US4] Test Docker layer caching by making code-only changes and verifying rebuild time <2 minutes
- [ ] T035 [US4] Verify health checks are properly configured in all Dockerfiles and docker-compose.yml
- [ ] T036 [US4] Document production deployment considerations in specs/001-docker-setup/quickstart.md
- [ ] T037 [US4] Add comments to all Dockerfiles explaining each step for maintainability

**Checkpoint**: All user stories should now be independently functional with production-ready optimizations

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation that affect the entire Docker setup

- [ ] T038 [P] Add troubleshooting section to specs/001-docker-setup/quickstart.md for common issues
- [ ] T039 [P] Document development workflow with hot-reload in quickstart.md
- [ ] T040 [P] Add cleanup commands to quickstart.md (docker-compose down, docker system prune)
- [ ] T041 Validate all success criteria from spec.md are met (SC-001 through SC-008)
- [ ] T042 Test Docker setup on Windows to verify cross-platform compatibility
- [ ] T043 Test Docker setup on macOS to verify cross-platform compatibility
- [ ] T044 Test Docker setup on Linux to verify cross-platform compatibility
- [ ] T045 Create README.md section in phase-4/ explaining Docker setup and linking to quickstart.md
- [ ] T046 Run full validation: docker-compose up --build, verify all services healthy within 60 seconds

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User Story 1 (Phase 3): Can start after Foundational - Creates orchestration
  - User Story 2 (Phase 4): Depends on US1 completion - Tests isolation
  - User Story 3 (Phase 5): Depends on US1 completion - Tests configuration
  - User Story 4 (Phase 6): Can start after Foundational - Optimizes images
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on US1 - Uses the Dockerfiles created in Foundational but validates them independently
- **User Story 3 (P2)**: Depends on US1 - Validates environment configuration in the orchestrated setup
- **User Story 4 (P3)**: Depends on Foundational - Can be done in parallel with US1-3 but typically done after to optimize existing Dockerfiles

### Within Each User Story

- **US1**: docker-compose.yml tasks are sequential (network → ports → env → health checks → dependencies)
- **US2**: All individual service tests can run in parallel [P]
- **US3**: Configuration validation tasks are sequential
- **US4**: Optimization validation tasks can run in parallel [P]

### Parallel Opportunities

- **Phase 1 (Setup)**: All .dockerignore files (T002, T003, T004) can be created in parallel
- **Phase 2 (Foundational)**: All three Dockerfiles (T005, T006, T007) can be created in parallel
- **Phase 4 (US2)**: Individual service builds (T018, T019, T020) can run in parallel
- **Phase 6 (US4)**: Image validation tasks (T030, T031, T032) can run in parallel
- **Phase 7 (Polish)**: Documentation tasks (T038, T039, T040) can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# Launch all Dockerfile creation tasks together:
Task: "Create Dockerfile for MCP server in phase-4/backend/mcp-server/Dockerfile"
Task: "Create Dockerfile for backend in phase-4/backend/Dockerfile"
Task: "Create Dockerfile for frontend in phase-4/frontend/Dockerfile"
```

## Parallel Example: User Story 2

```bash
# Launch all individual service build tests together:
Task: "Test individual MCP server build with docker build -t mcp-server ./backend/mcp-server"
Task: "Test individual backend build with docker build -t backend ./backend"
Task: "Test individual frontend build with docker build -t frontend ./frontend"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (.env.example, .dockerignore files)
2. Complete Phase 2: Foundational (all three Dockerfiles)
3. Complete Phase 3: User Story 1 (docker-compose.yml and orchestration)
4. **STOP and VALIDATE**: Test `docker-compose up --build` and verify all services start
5. Deploy/demo if ready - this is a working Docker setup!

### Incremental Delivery

1. Complete Setup + Foundational → Individual services can be built
2. Add User Story 1 → Test orchestration → Deploy/Demo (MVP!)
3. Add User Story 2 → Test isolation → Validate independent builds
4. Add User Story 3 → Test configuration → Validate environment management
5. Add User Story 4 → Optimize images → Production-ready
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup together (4 tasks, quick)
2. Team completes Foundational together (3 Dockerfiles in parallel)
3. Once Foundational is done:
   - Developer A: User Story 1 (orchestration)
   - Developer B: User Story 4 (optimization) - can work in parallel
4. After US1 complete:
   - Developer C: User Story 2 (isolation testing)
   - Developer D: User Story 3 (configuration testing)
5. All developers: Polish phase together

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No test tasks included - this is infrastructure configuration, not application code
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Focus on US1 first for MVP - it delivers the core value (single command startup)
- US2-US4 add validation and optimization on top of US1

---

## Success Criteria Validation

After completing all tasks, verify these success criteria from spec.md:

- **SC-001**: ✅ Developers can start entire stack with `docker-compose up --build` in <5 minutes
- **SC-002**: ✅ All three services start and pass health checks within 60 seconds
- **SC-003**: ✅ Frontend can make API calls to backend, backend can communicate with MCP server
- **SC-004**: ✅ Image sizes: frontend <500MB, backend <300MB, MCP server <300MB
- **SC-005**: ✅ Services can be stopped and restarted without data loss
- **SC-006**: ✅ Environment variables can be modified in .env and applied by restarting (no rebuild)
- **SC-007**: ✅ Docker setup works on Windows, macOS, and Linux
- **SC-008**: ✅ Subsequent builds complete in <2 minutes with layer caching

---

## Task Count Summary

- **Total Tasks**: 46
- **Phase 1 (Setup)**: 4 tasks
- **Phase 2 (Foundational)**: 3 tasks
- **Phase 3 (US1 - MVP)**: 10 tasks
- **Phase 4 (US2)**: 7 tasks
- **Phase 5 (US3)**: 5 tasks
- **Phase 6 (US4)**: 8 tasks
- **Phase 7 (Polish)**: 9 tasks

**Parallel Opportunities**: 15 tasks marked [P] can run in parallel within their phases

**MVP Scope**: Phases 1-3 (17 tasks) deliver the core value - single command to start all services
