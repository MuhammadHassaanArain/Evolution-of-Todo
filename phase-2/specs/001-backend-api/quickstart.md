# Quickstart: Backend API (Business Logic)

## API Setup

1. **Install Dependencies**
   ```bash
   pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart
   ```

2. **Environment Configuration**
   Set up required environment variables:
   ```bash
   export SECRET_KEY="your-secret-key-here"
   export ALGORITHM="HS256"
   export ACCESS_TOKEN_EXPIRE_MINUTES=30
   export DATABASE_URL="postgresql://user:password@localhost:5432/todo_app"
   ```

## API Usage Examples

### Authentication
All endpoints require a valid JWT token in the Authorization header:

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/v1/todos
```

### Create a Todo
```bash
curl -X POST http://localhost:8000/api/v1/todos \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Buy groceries",
       "description": "Milk, bread, eggs",
       "is_completed": false
     }'
```

### List Todos
```bash
curl -X GET http://localhost:8000/api/v1/todos \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get a Specific Todo
```bash
curl -X GET http://localhost:8000/api/v1/todos/1 \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Update a Todo
```bash
curl -X PUT http://localhost:8000/api/v1/todos/1 \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Buy groceries (updated)",
       "is_completed": true
     }'
```

### Delete a Todo
```bash
curl -X DELETE http://localhost:8000/api/v1/todos/1 \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Key Features

- **JWT Authentication**: All endpoints require a valid JWT token
- **User Isolation**: Users can only access their own todos
- **Ownership Validation**: Server-side checks ensure proper authorization
- **RESTful Design**: Standard HTTP methods and status codes
- **Error Handling**: Consistent error response format
- **Input Validation**: Request schema validation with Pydantic
- **OpenAPI Documentation**: Auto-generated API documentation at `/docs`

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful GET/PUT requests
- `201 Created`: Successful POST requests
- `204 No Content`: Successful DELETE requests
- `400 Bad Request`: Invalid request body
- `401 Unauthorized`: Invalid or missing JWT
- `404 Not Found`: Resource doesn't exist or not owned by user
- `500 Internal Server Error`: Unexpected server errors

## Security

- JWT tokens are validated on every request
- User ownership is verified for each operation
- No cross-user data exposure is possible
- Request bodies are validated against schemas
- Sensitive internal identifiers are not exposed in responses