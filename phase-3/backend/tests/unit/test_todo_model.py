import pytest
from src.models.todo import Todo, TodoCreate, TodoUpdate
from src.models.user import User
from datetime import datetime


class TestTodoModel:
    """
    Unit tests for the Todo model.
    """
    
    def test_todo_creation(self):
        """
        Test creating a new Todo instance.
        """
        todo_data = {
            "title": "Test Todo",
            "description": "Test description",
            "is_completed": False
        }
        
        todo = Todo(**todo_data, owner_id=1)
        
        assert todo.title == "Test Todo"
        assert todo.description == "Test description"
        assert todo.is_completed is False
        assert todo.owner_id == 1
        assert todo.id is None  # ID is set by the database
    
    def test_todo_default_values(self):
        """
        Test that Todo model sets proper default values.
        """
        todo_data = {
            "title": "Test Todo",
            "description": "Test description"
        }
        
        todo = Todo(**todo_data, owner_id=1)
        
        assert todo.is_completed is False  # Default value
        assert isinstance(todo.created_at, datetime)
        assert isinstance(todo.updated_at, datetime)
    
    def test_todo_required_fields(self):
        """
        Test that required fields are properly validated.
        """
        # Title is required
        with pytest.raises(ValueError):
            Todo(title="", description="Test", owner_id=1)
    
    def test_todo_update_model(self):
        """
        Test TodoUpdate model functionality.
        """
        update_data = {
            "title": "Updated Title",
            "is_completed": True
        }
        
        update = TodoUpdate(**update_data)
        
        assert update.title == "Updated Title"
        assert update.is_completed is True
        assert update.description is None  # Not provided, so None
    
    def test_todo_update_partial(self):
        """
        Test that TodoUpdate model allows partial updates.
        """
        # Only update the completion status
        update = TodoUpdate(is_completed=True)
        
        assert update.is_completed is True
        assert update.title is None
        assert update.description is None


class TestTodoCreateModel:
    """
    Unit tests for the TodoCreate model.
    """
    
    def test_todo_create_model(self):
        """
        Test creating a TodoCreate instance.
        """
        create_data = {
            "title": "New Todo",
            "description": "New description",
            "is_completed": False
        }
        
        todo_create = TodoCreate(**create_data)
        
        assert todo_create.title == "New Todo"
        assert todo_create.description == "New description"
        assert todo_create.is_completed is False
    
    def test_todo_create_required_fields(self):
        """
        Test that TodoCreate model validates required fields.
        """
        # Title is required
        with pytest.raises(ValueError):
            TodoCreate(title="")
    
    def test_todo_create_defaults(self):
        """
        Test default values in TodoCreate model.
        """
        create_data = {
            "title": "New Todo",
            "description": "New description"
        }
        
        todo_create = TodoCreate(**create_data)
        
        assert todo_create.title == "New Todo"
        assert todo_create.description == "New description"
        assert todo_create.is_completed is False  # Default value
