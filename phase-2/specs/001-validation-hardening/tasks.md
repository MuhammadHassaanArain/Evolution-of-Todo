# Tasks: Validation & Hardening

**Feature**: Validation & Hardening | **Branch**: `001-validation-hardening` | **Date**: 2026-01-04

## Overview

This document defines the implementation tasks for the validation and hardening feature. The feature focuses on authentication failure validation, ownership enforcement, and API misuse protection.

## Dependencies

- Backend API with existing authentication system
- Better Auth + JWT implementation
- SQLModel ORM with existing User and Todo models

## Parallel Execution Examples

- Authentication validation tasks can run in parallel with API validation tasks
- User Story 1 (Security Validation) and User Story 2 (Ownership Enforcement) can be developed independently after foundational tasks are complete

## Implementation Strategy

- MVP: Basic authentication validation with 401 responses
- Incremental delivery: Add ownership validation, then API misuse protection
- Each user story is independently testable

---

## Phase 1: Setup

**Goal**: Prepare project structure and dependencies for validation implementation

- [x] T001 Install required validation dependencies (python-jose, pydantic validation extensions)
- [x] T002 Set up JWT configuration constants and environment variables
- [x] T003 Create validation error response models in backend/src/models/validation.py

## Phase 2: Foundational

**Goal**: Implement core validation infrastructure used across all validation scenarios

- [x] T004 Create authentication middleware for JWT validation in backend/src/middleware/auth.py
- [x] T005 Create reusable validation functions for request payload validation in backend/src/utils/validation.py
- [x] T006 Implement consistent error response format in backend/src/schemas/error.py
- [x] T007 Update existing API endpoints to use authentication dependency injection
- [x] T008 Create validation utility functions for checking user ownership in backend/src/utils/ownership.py

---

## Phase 3: User Story 1 - Security Validation (Priority: P1)

**Goal**: Ensure authentication failures are properly handled with consistent 401 responses

**Independent Test**: Can be fully tested by making API requests with invalid authentication tokens and verifying that they are consistently rejected with 401 Unauthorized status codes.

- [x] T009 [P] [US1] Create JWT token validation utility in backend/src/utils/jwt_validator.py
- [x] T010 [P] [US1] Implement authentication dependency for protected endpoints in backend/src/api/deps.py
- [x] T011 [US1] Add missing Authorization header validation to all protected endpoints
- [x] T012 [US1] Implement malformed Authorization header validation in authentication middleware
- [x] T013 [US1] Add expired JWT token validation to authentication middleware
- [x] T014 [US1] Implement invalid JWT signature validation in authentication middleware
- [x] T015 [US1] Ensure all protected endpoints return 401 for invalid authentication
- [x] T016 [US1] Test authentication failure scenarios with unit tests in backend/tests/test_auth_validation.py

## Phase 4: User Story 2 - Ownership Enforcement (Priority: P1)

**Goal**: Ensure users can only access their own todos, with 404 responses for non-owned resources

**Independent Test**: Can be fully tested by attempting to access, update, or delete another user's todos and verifying that operations fail with 404 Not Found responses.

- [x] T017 [P] [US2] Create user ownership validation function in backend/src/utils/ownership.py
- [x] T018 [P] [US2] Update GET /tasks/{id} endpoint to validate user ownership
- [x] T019 [US2] Update PUT /tasks/{id} endpoint to validate user ownership
- [x] T020 [US2] Update DELETE /tasks/{id} endpoint to validate user ownership
- [x] T021 [US2] Ensure 404 responses for non-owned resources (not 403)
- [x] T022 [US2] Update all task-related endpoints to include ownership validation
- [x] T023 [US2] Test ownership enforcement scenarios with unit tests in backend/tests/test_ownership.py

## Phase 5: User Story 3 - API Misuse Protection (Priority: P2)

**Goal**: Ensure the API handles malformed or abusive requests safely without crashing

**Independent Test**: Can be fully tested by sending various malformed requests to the API and verifying that they are rejected with appropriate error responses without crashing the system.

- [x] T024 [P] [US3] Create request payload validation utilities in backend/src/utils/validation.py
- [x] T025 [P] [US3] Implement user_id field rejection in request validation for task endpoints
- [x] T026 [US3] Add unexpected fields validation to request processing
- [x] T027 [US3] Implement invalid data types validation for all endpoints
- [x] T028 [US3] Add payload size validation to prevent oversized requests
- [x] T029 [US3] Ensure all validation returns 400 Bad Request for invalid input
- [x] T030 [US3] Test API misuse protection with unit tests in backend/tests/test_api_validation.py

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Ensure consistent validation behavior and proper error handling across the system

- [x] T031 Update all API endpoints to use consistent error response format
- [x] T032 Ensure no stack traces are exposed in error responses
- [x] T033 Add logging for validation failures in backend/src/utils/logging.py
- [x] T034 Test all validation scenarios together for integration issues
- [x] T035 Update documentation with validation behavior changes
- [x] T036 Perform security validation testing to ensure all scenarios are covered

---

## Acceptance Criteria

### User Story 1 Acceptance
- [ ] Given a user with no authentication token, When they attempt to access protected endpoints, Then the request is rejected with 401 Unauthorized
- [ ] Given a user with an expired JWT token, When they attempt to access protected endpoints, Then the request is rejected with 401 Unauthorized
- [ ] Given a user with a malformed JWT token, When they attempt to access protected endpoints, Then the request is rejected with 401 Unauthorized
- [ ] Given a user with an invalid JWT signature, When they attempt to access protected endpoints, Then the request is rejected with 401 Unauthorized

### User Story 2 Acceptance
- [ ] Given a user authenticated with valid credentials, When they attempt to access another user's todo by ID, Then the operation fails with 404 Not Found
- [ ] Given a user authenticated with valid credentials, When they attempt to update another user's todo, Then the operation fails with 404 Not Found
- [ ] Given a user authenticated with valid credentials, When they attempt to delete another user's todo, Then the operation fails with 404 Not Found
- [ ] Given a user authenticated with valid credentials, When they attempt to access their own todo, Then the operation succeeds

### User Story 3 Acceptance
- [ ] Given a user with valid authentication, When they send a request with user_id in the payload, Then the request is rejected with 400 Bad Request
- [ ] Given a user with valid authentication, When they send a request with unexpected fields, Then the request is rejected with 400 Bad Request
- [ ] Given a user with valid authentication, When they send a request with invalid data types, Then the request is rejected with 400 Bad Request
- [ ] Given a user with valid authentication, When they send an empty or oversized payload, Then the request is rejected with 400 Bad Request

## Success Metrics

- [ ] Authentication failures are consistently rejected with 401 Unauthorized status (100% success rate)
- [ ] Ownership violations are impossible - users cannot access other users' resources (0% success rate for unauthorized access)
- [ ] API misuse does not crash the system - all invalid requests are handled gracefully (0 system crashes during testing)
- [ ] Error responses are predictable and safe - no internal errors or stack traces exposed (100% of error responses follow standard format)