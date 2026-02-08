# Quickstart: Database Layer with User Ownership

## Setup

1. **Install Dependencies**
   ```bash
   pip install sqlmodel
   pip install psycopg2-binary  # or asyncpg for async
   ```

2. **Environment Configuration**
   Set up your PostgreSQL connection string:
   ```bash
   export DATABASE_URL="postgresql://username:password@localhost:5432/your_database_name"
   # For Neon: export DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
   ```

## Database Initialization

1. **Create the Models**
   Import and define your SQLModel models as specified in data-model.md

2. **Initialize the Database**
   ```python
   from sqlmodel import SQLModel, create_engine
   from your_models import User, Todo  # Import your models

   # Create database engine
   engine = create_engine("your_database_url_here")

   # Create all tables
   SQLModel.metadata.create_all(engine)
   ```

## Usage Examples

### Creating a User
```python
from sqlmodel import Session
from your_models import User

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
from your_models import Todo

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
from your_models import Todo

with Session(engine) as session:
    # Get all todos for a specific user
    statement = select(Todo).where(Todo.owner_id == 1)
    results = session.exec(statement)
    user_todos = results.all()
```

## Key Features

- **User Ownership**: Each todo is tied to a specific user via foreign key
- **Data Isolation**: Users can only access their own todos through the database model
- **Referential Integrity**: Foreign key constraints prevent orphaned todos
- **Cascading Deletes**: When a user is deleted, their todos are automatically deleted
- **Proper Indexing**: Optimized for user-scoped queries