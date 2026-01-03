# Research: Database Layer with User Ownership

## Decision: SQLModel Implementation Approach
**Rationale**: Following the constitution requirement to use SQLModel ORM for database interaction with Neon Serverless PostgreSQL. This provides type-safe database models with proper relationships and constraints.

**Alternatives considered**:
- Pure SQLAlchemy (rejected - SQLModel provides better type safety and integration)
- Direct PostgreSQL queries (rejected - violates constitution's ORM requirement)

## Decision: User Model Design
**Rationale**: User model must include unique identifier and login credential (email/username) with uniqueness constraints. Following security best practices for user authentication models.

**Alternatives considered**:
- Separate user profile model (rejected - simpler to have core fields in main user model)

## Decision: Todo Model Design
**Rationale**: Todo model requires foreign key relationship to User with non-nullable constraint to enforce ownership. Includes standard todo fields like title, description, completion status, and timestamps.

**Alternatives considered**:
- Soft delete vs hard delete (pending decision based on requirements)

## Decision: Indexing Strategy
**Rationale**: Indexes needed on user login credentials for authentication performance, and on todo owner_id for user-scoped queries. Additional indexes on frequently queried fields.

**Alternatives considered**:
- Over-indexing (rejected - impacts write performance)
- Minimal indexing (rejected - impacts read performance for user queries)

## Decision: Cascade Behavior for User Deletion
**Rationale**: When a user is deleted, their todos should cascade delete to prevent orphaned data, as specified in the feature requirements.

**Alternatives considered**:
- Soft delete of todos (rejected - specification requires prevention of orphaned data)
- Manual cleanup (rejected - violates database-level enforcement principle)

## Decision: Primary Key Strategy
**Rationale**: Using auto-incrementing integer primary keys for both User and Todo models, which is standard for SQLModel and PostgreSQL.

**Alternatives considered**:
- UUID primary keys (rejected - integer keys are more efficient for joins and indexing)