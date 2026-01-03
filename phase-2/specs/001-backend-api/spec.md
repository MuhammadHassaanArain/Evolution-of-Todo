# Feature Specification: Backend API (Business Logic)

**Feature Branch**: `001-backend-api`
**Created**: 2026-01-03
**Status**: Draft
**Input**: User description: "# Phase II — Chunk 3: Backend API (BUSINESS LOGIC)

## Status
DRAFT — Requires approval before implementation.

## Purpose
Define a secure, user-scoped REST API for Todo management.

This chunk introduces:
- Business logic
- Ownership enforcement
- Request/response contracts

🚫 No frontend logic
🚫 No database schema changes
🚫 No authentication implementation (auth is assumed)

---

## Scope

This specification defines:
- Todo CRUD endpoints
- Request and response schemas
- Authorization rules
- Error behavior

---

# 3.1 API Principles

## 3.1.1 Authentication Requirement

All Todo endpoints:
- REQUIRE a valid JWT
- Use backend auth dependency
- Reject unauthenticated requests

---

## 3.1.2 Authorization Rule (Ownership)

A user MAY:
- Access only their own Todos

A user MUST NOT:
- Read, modify, or delete another user's Todos

Ownership is enforced server-side on every request.

---

# 3.2 Todo Endpoints

## 3.2.1 Create Todo

**POST** `/todos`

- Creates a Todo owned by the authenticated user
- Owner is derived from JWT, not request body

---

## 3.2.2 List Todos

**GET** `/todos`

- Returns only Todos owned by the authenticated user
- No cross-user data exposure

---

## 3.2.3 Get Todo by ID

**GET** `/todos/{id}`

- Returns Todo only if owned by the user
- Non-owned or non-existent IDs are not distinguishable

---

## 3.2.4 Update Todo

**PUT** `/todos/{id}`

- Updates Todo fields
- Ownership is revalidated before update

---

## 3.2.5 Delete Todo

**DELETE** `/todos/{id}`

- Deletes Todo if owned by the user
- Operation is idempotent

---

# 3.3 Request & Response Schemas

## 3.3.1 Request Rules

- Client MUST NOT supply user_id
- Only domain fields are accepted
- Invalid fields result in request rejection

---

## 3.3.2 Response Rules

Responses:
- Contain only user-owned data
- Never expose internal identifiers unrelated to domain
- Use consistent JSON structure

---

# 3.4 Error Handling

## 3.4.1 401 Unauthorized

Returned when:
- JWT is missing or invalid

---

## 3.4.2 404 Not Found

Returned when:
- Todo does not exist
- Todo exists but is not owned by the user

(No ownership leakage)

---

## 3.4.3 400 Bad Request

Returned when:
- Request body is invalid
- Schema validation fails

---

## 3.4.4 500 Internal Server Error

Returned only for unexpected failures.

---

# 3.5 Testability

The API MUST:
- Be fully discoverable via Swagger
- Be testable using curl or HTTP clients
- Clearly document auth requirements per endpoint

---

# Success Criteria

This chunk is complete when:

- All Todo CRUD endpoints exist
- Ownership is enforced on every operation
- Unauthorized access is impossible
- API is testable via Swagger UI

---

## Lock-In Clause

Once approved:
- API contracts are immutable
- Frontend and tests rely on this spec
- Changes require a new versioned API spec

Approval is REQUIRED before generating `api.implement.md`."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Todo Creation (Priority: P1)

As an authenticated user, I want to create a new todo through the API so that I can track my tasks securely without other users accessing them.

**Why this priority**: This is the foundational functionality that enables users to add tasks to their personal todo list. Without this, the entire system has no value.

**Independent Test**: Can be fully tested by making a POST request to `/todos` with a valid JWT and verifying that the todo is created under the authenticated user's ownership and is not accessible to other users.

**Acceptance Scenarios**:
1. **Given** an authenticated user with a valid JWT, **When** they make a POST request to `/todos` with valid todo data, **Then** a new todo is created and assigned to their account
2. **Given** an unauthenticated request without a valid JWT, **When** a POST request is made to `/todos`, **Then** a 401 Unauthorized response is returned

---

### User Story 2 - Personal Todo Access (Priority: P1)

As an authenticated user, I want to view only my own todos through the API so that I can manage my tasks without seeing other users' data.

**Why this priority**: This is essential for data privacy and security. Users must be able to access their own data while being completely isolated from others' data.

**Independent Test**: Can be fully tested by creating todos for multiple users and verifying that each user can only access their own todos via the GET endpoints.

**Acceptance Scenarios**:
1. **Given** an authenticated user with valid JWT, **When** they make a GET request to `/todos`, **Then** they receive only their own todos
2. **Given** an authenticated user with valid JWT, **When** they make a GET request to `/todos/{id}` for a todo that belongs to another user, **Then** a 404 Not Found response is returned

---

### User Story 3 - Todo Management (Priority: P2)

As an authenticated user, I want to update and delete my own todos through the API so that I can manage my task list effectively.

**Why this priority**: This provides the full CRUD functionality that users expect for task management, allowing them to modify or remove their tasks as needed.

**Independent Test**: Can be fully tested by creating a todo, updating it via PUT, and deleting it via DELETE, verifying that ownership is enforced at each step.

**Acceptance Scenarios**:
1. **Given** an authenticated user with valid JWT, **When** they make a PUT request to `/todos/{id}` for their own todo, **Then** the todo is updated successfully
2. **Given** an authenticated user with valid JWT, **When** they make a DELETE request to `/todos/{id}` for a todo that belongs to another user, **Then** a 404 Not Found response is returned

---

### Edge Cases

- What happens when a user attempts to access a todo ID that doesn't exist? (Should return 404 Not Found)
- How does the system handle concurrent access to the same todo? (Should handle appropriately with proper locking if needed)
- What occurs when a request has an invalid JWT? (Should return 401 Unauthorized)
- What happens when request body validation fails? (Should return 400 Bad Request with validation errors)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST require a valid JWT for all Todo endpoints
- **FR-002**: System MUST enforce user ownership on every Todo operation (create, read, update, delete)
- **FR-003**: System MUST return only user-owned data in all responses
- **FR-004**: System MUST prevent cross-user data exposure in all operations
- **FR-005**: System MUST implement POST `/todos` endpoint for creating user-owned todos
- **FR-006**: System MUST implement GET `/todos` endpoint for listing user's own todos
- **FR-007**: System MUST implement GET `/todos/{id}` endpoint for retrieving owned todos
- **FR-008**: System MUST implement PUT `/todos/{id}` endpoint for updating owned todos
- **FR-009**: System MUST implement DELETE `/todos/{id}` endpoint for deleting owned todos
- **FR-010**: System MUST return 401 Unauthorized for invalid or missing JWT
- **FR-011**: System MUST return 404 Not Found for non-existent or non-owned todos
- **FR-012**: System MUST return 400 Bad Request for invalid request bodies
- **FR-013**: System MUST derive todo ownership from JWT, not request body
- **FR-014**: System MUST validate request schemas and reject invalid data
- **FR-015**: System MUST return consistent JSON structure in all responses

### Key Entities *(include if feature involves data)*

- **Todo**: Represents a task owned by a single authenticated user. Contains fields like title, description, completion status, and timestamps. Cannot be accessed by other users.
- **JWT Token**: Authentication token that identifies the authenticated user and their permissions. Used to derive ownership for all operations.
- **User**: The authenticated account that owns todos. Each user can only access their own todos through the API.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All Todo CRUD endpoints exist and are accessible via HTTP methods (POST, GET, PUT, DELETE)
- **SC-002**: Ownership is enforced on every operation with unauthorized access completely prevented
- **SC-003**: API is testable via Swagger UI with all endpoints properly documented
- **SC-004**: All error conditions return appropriate HTTP status codes (401, 404, 400, 500)
- **SC-005**: Cross-user data exposure is impossible through any API endpoint
- **SC-006**: API follows RESTful principles with consistent request/response schemas