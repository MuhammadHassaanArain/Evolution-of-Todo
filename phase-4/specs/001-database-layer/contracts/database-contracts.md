# Database Contracts: User and Todo Models

## User Model Contract

### Schema Definition
```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column("email", String, unique=True, nullable=False))
    username: str = Field(sa_column=Column("username", String, unique=True, nullable=False))
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    todos: List["Todo"] = Relationship(back_populates="owner")
```

### Constraints
- `id` is auto-incrementing primary key
- `email` is unique and non-nullable
- `username` is unique and non-nullable
- `hashed_password` is non-nullable
- `created_at` and `updated_at` are automatically set

### Indexes
- Primary key index on `id`
- Unique index on `email`
- Unique index on `username`

## Todo Model Contract

### Schema Definition
```python
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column("title", String, nullable=False))
    description: Optional[str] = None
    is_completed: bool = False
    owner_id: int = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None

    # Relationship
    owner: User = Relationship(back_populates="todos")
```

### Constraints
- `id` is auto-incrementing primary key
- `title` is non-nullable
- `owner_id` is non-nullable foreign key to User
- Foreign key constraint prevents orphaned todos

### Indexes
- Primary key index on `id`
- Foreign key index on `owner_id`
- Index on `is_completed` for filtering
- Index on `created_at` for chronological queries

## Database Relationship Contract

### User-Todo Relationship
- One User to Many Todos (1:N relationship)
- Foreign key constraint on `todos.owner_id` references `users.id`
- ON DELETE CASCADE: When a User is deleted, all associated Todos are also deleted
- NOT NULL constraint on `todos.owner_id` prevents orphaned todos

## Validation Contract

### User Validation
- Email format validation (before database insertion)
- Username uniqueness validation
- Required fields validation

### Todo Validation
- Title non-empty validation
- Owner reference validation
- Required fields validation

## Access Contract

### Ownership Enforcement
- Database-level enforcement of user ownership via foreign keys
- No cross-user data access at database level
- Isolation achieved through foreign key relationships