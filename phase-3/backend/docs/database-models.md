# Database Models Documentation

## Overview

This document describes the database models used in the Todo application with user ownership. The models are implemented using SQLModel and follow the principles of data isolation and ownership enforcement.

## Models

### User Model

The User model represents an authenticated account in the system.

#### Fields
- `id` (int, primary key): Unique identifier for the user
- `email` (str, unique, non-nullable): User's email address for authentication
- `username` (str, unique, non-nullable): User's chosen username
- `hashed_password` (str, non-nullable): BCrypt hashed password
- `first_name` (str, nullable): User's first name
- `last_name` (str, nullable): User's last name
- `is_active` (bool, default=True): Whether the user account is active
- `created_at` (datetime, non-nullable): Timestamp when user was created
- `updated_at` (datetime, non-nullable): Timestamp when user was last updated

#### Constraints
- Email must be unique across all users
- Username must be unique across all users
- Email must be a valid email format
- Username must be 3-50 characters and contain only letters, numbers, and underscores
- Password must be at least 8 characters long

#### Relationships
- `todos`: One-to-many relationship with Todo model (one user can own many todos)

### Todo Model

The Todo model represents a task owned by a user.

#### Fields
- `id` (int, primary key): Unique identifier for the todo
- `title` (str, non-nullable): Title of the todo item
- `description` (str, nullable): Optional description of the todo
- `is_completed` (bool, default=False): Whether the todo is completed
- `owner_id` (int, non-nullable, foreign key): Reference to the user who owns this todo
- `created_at` (datetime, non-nullable): Timestamp when todo was created
- `updated_at` (datetime, non-nullable): Timestamp when todo was last updated
- `due_date` (datetime, nullable): Optional due date for the todo

#### Constraints
- Title cannot be empty
- Owner_id must reference a valid user
- Owner_id cannot be null (enforced by database constraint)
- On user deletion, todos are automatically deleted (CASCADE)

#### Relationships
- `owner`: Many-to-one relationship with User model (todo belongs to one user)

## Database Schema

### Constraints & Relationships

#### Foreign Key Constraints
- `todos.owner_id` references `users.id` with ON DELETE CASCADE
- Prevents orphaned todos when users are deleted

#### Unique Constraints
- `users.email` must be unique
- `users.username` must be unique

#### Not-Null Constraints
- `todos.owner_id` cannot be null
- All required fields as specified above

### Indexes

#### Primary Indexes
- `users.id` (primary key)
- `todos.id` (primary key)

#### Unique Indexes
- `users.email` (unique)
- `users.username` (unique)

#### Foreign Key Indexes
- `todos.owner_id` (foreign key to users)

#### Additional Indexes
- `todos.is_completed` (for filtering completed/incomplete todos)
- `todos.created_at` (for chronological ordering)

## Usage Examples

### Creating a User
```python
from sqlmodel import Session
from models.user import User

with Session(engine) as session:
    user = User(
        email="user@example.com",
        username="johndoe",
        hashed_password="hashed_password_here"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
```

### Creating a Todo for a User
```python
from sqlmodel import Session
from models.todo import Todo

with Session(engine) as session:
    todo = Todo(
        title="My first task",
        description="A detailed description of the task",
        owner_id=1  # Reference to the user
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)
```

### Querying User's Todos
```python
from sqlmodel import Session, select
from models.todo import Todo

with Session(engine) as session:
    # Get all todos for a specific user
    statement = select(Todo).where(Todo.owner_id == 1)
    results = session.exec(statement)
    user_todos = results.all()
```

## Security & Data Isolation

The database models enforce data isolation between users through:

1. **Ownership Enforcement**: Each todo is tied to a specific user via foreign key
2. **Data Isolation**: Users can only access their own todos through the database model
3. **Referential Integrity**: Foreign key constraints prevent orphaned todos
4. **Cascading Deletes**: When a user is deleted, their todos are automatically deleted
5. **Proper Indexing**: Optimized for user-scoped queries

## Validation

The models include validation logic to ensure data integrity:

- Email format validation
- Username format validation
- Password strength validation
- Title non-empty validation
- Foreign key reference validation

## Error Handling

The system includes comprehensive error handling for database operations:

- DatabaseError for database-related issues
- ValidationError for validation failures
- NotFoundError for missing resources
- Custom HTTP exceptions for API responses

## Testing

The models are designed to be easily testable with proper separation of concerns and dependency injection patterns.
