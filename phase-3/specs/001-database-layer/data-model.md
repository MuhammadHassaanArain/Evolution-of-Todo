# Data Model: Database Layer with User Ownership

## Entity: User

**Fields:**
- `id` (int, primary key, auto-increment) - Unique identifier for the user
- `email` (str, unique, non-nullable) - User's email address for authentication
- `username` (str, unique, non-nullable) - User's chosen username
- `hashed_password` (str, non-nullable) - BCrypt hashed password
- `first_name` (str, nullable) - User's first name
- `last_name` (str, nullable) - User's last name
- `is_active` (bool, default=True) - Whether the user account is active
- `created_at` (datetime, non-nullable) - Timestamp when user was created
- `updated_at` (datetime, non-nullable) - Timestamp when user was last updated

**Relationships:**
- `todos` (one-to-many) - User owns many todos, todos reference this user

**Validation Rules:**
- Email must be a valid email format
- Username must be unique across all users
- Email must be unique across all users
- Password must be properly hashed before storage

## Entity: Todo

**Fields:**
- `id` (int, primary key, auto-increment) - Unique identifier for the todo
- `title` (str, non-nullable) - Title of the todo item
- `description` (str, nullable) - Optional description of the todo
- `is_completed` (bool, default=False) - Whether the todo is completed
- `owner_id` (int, non-nullable, foreign key) - Reference to the user who owns this todo
- `created_at` (datetime, non-nullable) - Timestamp when todo was created
- `updated_at` (datetime, non-nullable) - Timestamp when todo was last updated
- `due_date` (datetime, nullable) - Optional due date for the todo

**Relationships:**
- `owner` (many-to-one) - Todo belongs to one user (the owner)

**Validation Rules:**
- Title must not be empty
- Owner_id must reference a valid user
- Owner_id cannot be null (enforced by database constraint)

## Constraints & Relationships

**Foreign Key Constraints:**
- `todos.owner_id` references `users.id` with ON DELETE CASCADE
- Prevents orphaned todos when users are deleted

**Unique Constraints:**
- `users.email` must be unique
- `users.username` must be unique

**Not-Null Constraints:**
- `todos.owner_id` cannot be null
- All required fields as specified above

## Indexes

**Primary Indexes:**
- `users.id` (primary key)
- `todos.id` (primary key)

**Unique Indexes:**
- `users.email` (unique)
- `users.username` (unique)

**Foreign Key Indexes:**
- `todos.owner_id` (foreign key to users)

**Additional Indexes:**
- `todos.is_completed` (for filtering completed/incomplete todos)
- `todos.created_at` (for chronological ordering)