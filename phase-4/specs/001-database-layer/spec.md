# Feature Specification: Database Layer with User Ownership

**Feature Branch**: `001-database-layer`
**Created**: 2026-01-03
**Status**: Draft
**Input**: User description: "# Phase II — Chunk 2: Database Layer (OWNERSHIP FIRST)

## Status
DRAFT — Requires approval before implementation.

## Purpose
Define the persistent data model with **explicit user ownership guarantees**.

This chunk ensures:
- Data isolation between users
- Ownership enforced at the database level
- A stable schema foundation for all future API layers

🚫 No API routes
🚫 No request/response logic
🚫 No authorization logic beyond ownership modeling
✅ Database is backend-only

---

## Scope

This specification defines:

- SQLModel schemas
- Entity relationships
- Indexes and constraints
- Ownership rules
- Database connection assumptions

---

# 2.1 Database Strategy

## 2.1.1 Persistence Technology

The backend SHALL use:
- **PostgreSQL** as the database
- **SQLModel** as the ORM / schema definition layer

SQLModel models are the **single source of truth** for persistence.

---

## 2.1.2 Ownership Philosophy

All user-owned data MUST:
- Be explicitly linked to a user
- Enforce ownership via foreign keys
- Never exist without a valid owner

There is no concept of:
- Global Todos
- Anonymous data
- Shared ownership (in this phase)

---

# 2.2 Core Entities

## 2.2.1 User Entity

The User entity represents an authenticated account.

User MUST:
- Have a unique identifier
- Be uniquely identifiable by a login credential (e.g. email or username)
- Serve as the ownership root for all domain data

User data is created only via authentication flows.

---

## 2.2.2 Todo Entity

The Todo entity represents a task owned by a user.

Todo MUST:
- Belong to exactly one user
- Be inaccessible without ownership context
- Not exist without an associated user

Todo is a **dependent entity**.

---

# 2.3 Relationships

## 2.3.1 User ↔ Todo Relationship

Relationship rules:
- One User → Many Todos
- One Todo → One User

This relationship MUST be enforced using:
- Foreign key constraints
- Non-null ownership fields

Orphaned Todos are not allowed.

---

## 2.3.2 Cascading Rules

Deletion behavior:
- Deleting a User MAY cascade to owned Todos
- Cascading behavior must be explicit and intentional

Silent orphan creation is forbidden.

---

# 2.4 Schema Constraints

## 2.4.1 Primary Keys

All entities MUST:
- Have a primary key
- Use stable, unique identifiers

---

## 2.4.2 Foreign Keys

Todo MUST:
- Reference User via a foreign key
- Enforce referential integrity at the database level

---

## 2.4.3 Uniqueness Constraints

User MUST:
- Enforce uniqueness on login credential (e.g. email or username)

Todo MAY:
- Have additional constraints (e.g. title length)
- Not enforce cross-user uniqueness

---

## 2.4.4 Nullability Rules

- Ownership fields MUST NOT be nullable
- Required domain fields MUST be non-null
- Optional metadata fields MAY be nullable

---

# 2.5 Indexing Strategy

Indexes SHALL be defined for:
- User lookup by login credential
- Todo lookup by owner
- Frequent ownership-based query paths

Indexes MUST:
- Optimize user-scoped queries
- Never optimize cross-user scans

---

# 2.6 Database Initialization

## 2.6.1 Schema Creation

The database layer SHALL:
- Define schema via SQLModel
- Support deterministic initialization
- Avoid runtime schema mutation

---

## 2.6.2 Environment Configuration

Database connection details are:
- Backend-owned
- Supplied via environment variables
- Never exposed to the frontend

---

## 2.6.3 Neon Compatibility

The database layer MUST:
- Be compatible with Neon (PostgreSQL)
- Use standard PostgreSQL features
- Avoid vendor-specific extensions unless required

---

# 2.7 Isolation Rules

This chunk MUST NOT:
- Define API routes
- Contain request handling
- Include authentication logic
- Perform authorization checks

Ownership is **modeled**, not enforced here.

---

# Success Criteria

This chunk is complete when:

- SQLModel schemas exist for User and Todo
- Ownership is enforced via foreign keys
- Indexes support user-scoped queries
- Schema prevents orphaned data
- Database can be initialized deterministically

---

## Lock-In Clause

Once approved:
- This schema becomes the foundation for all APIs
- Ownership rules are immutable
- Changes require a new versioned database specification

Approval is REQUIRED before generating `database.implement.md`."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Data Isolation (Priority: P1)

As a user, I want my data to be isolated from other users so that my personal information and tasks remain private and secure.

**Why this priority**: Data isolation is fundamental to user privacy and security. Without proper isolation, the entire system would be vulnerable to data breaches and unauthorized access.

**Independent Test**: Can be fully tested by creating multiple users with their own data and verifying that one user cannot access another user's data through direct database queries or API calls.

**Acceptance Scenarios**:

1. **Given** a user has created their own todos, **When** another user attempts to access those todos, **Then** the second user should receive an access denied response
2. **Given** a user logs in to the system, **When** they request their data, **Then** they should only see data that belongs to them

---

### User Story 2 - Data Ownership Modeling (Priority: P1)

As a system, I need to model data ownership at the database level so that data relationships are enforced by the database itself.

**Why this priority**: Database-level enforcement ensures data integrity even if application-level logic fails. This provides a robust foundation for all future API development.

**Independent Test**: Can be fully tested by examining the database schema to verify foreign key constraints, primary keys, and ownership relationships are properly defined.

**Acceptance Scenarios**:

1. **Given** a database schema definition, **When** the schema is validated, **Then** all user-owned entities should have foreign key references to the User entity
2. **Given** an attempt to create a Todo without a valid user reference, **When** the database constraint is enforced, **Then** the operation should fail

---

### User Story 3 - Database Initialization (Priority: P2)

As a developer, I want to initialize the database with the correct schema so that the system can be deployed consistently across environments.

**Why this priority**: Consistent database initialization is essential for reliable deployments and prevents data integrity issues in production.

**Independent Test**: Can be fully tested by running the database initialization script in a clean environment and verifying that all tables, constraints, and indexes are created correctly.

**Acceptance Scenarios**:

1. **Given** a clean database environment, **When** the initialization script is run, **Then** all required tables and constraints should be created successfully
2. **Given** a database with the correct schema, **When** sample data is inserted, **Then** all foreign key constraints should be satisfied

---

### Edge Cases

- What happens when a user is deleted but has associated todos? (Cascading deletion should be handled appropriately)
- How does the system handle concurrent access to the same data by different users? (Should be prevented by design through ownership)
- What occurs when attempting to create orphaned data without a valid owner? (Should be prevented by foreign key constraints)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST define SQLModel schemas for User and Todo entities with proper relationships
- **FR-002**: System MUST enforce user ownership through foreign key constraints at the database level
- **FR-003**: System MUST ensure that all user-owned data has a non-nullable reference to a valid user
- **FR-004**: System MUST prevent orphaned data by using foreign key constraints and appropriate cascading rules
- **FR-005**: System MUST include indexes optimized for user-scoped queries to ensure performance
- **FR-006**: System MUST support deterministic database schema initialization across environments
- **FR-007**: System MUST be compatible with PostgreSQL and Neon Serverless PostgreSQL
- **FR-008**: System MUST enforce uniqueness constraints on user login credentials
- **FR-009**: System MUST use stable, unique primary keys for all entities
- **FR-010**: System MUST support proper nullability rules as defined in the specification

### Key Entities *(include if feature involves data)*

- **User**: Represents an authenticated account with unique identifiers and login credentials. Serves as the ownership root for all domain data.
- **Todo**: Represents a task owned by a single user. Cannot exist without an associated user and must have a non-nullable foreign key reference to the User entity.
- **User-Todo Relationship**: One-to-many relationship where one User can own many Todos, but each Todo belongs to exactly one User.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: SQLModel schemas exist for User and Todo entities with proper foreign key relationships enforced at the database level
- **SC-002**: Database schema prevents orphaned data by enforcing referential integrity through foreign key constraints
- **SC-003**: Indexes are defined and optimized for user-scoped queries, enabling efficient retrieval of user-specific data
- **SC-004**: Database can be initialized deterministically from schema definitions with all constraints properly applied
- **SC-005**: System ensures complete data isolation between users, with no cross-user data access possible