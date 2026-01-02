# Quickstart Guide: Phase II Architecture Foundation

## Overview
This guide provides the essential information needed to set up and understand the Phase II architecture foundation for the Todo application.

## Project Structure
```
hackathon-todo/                 # Root directory
├── frontend/                   # Next.js frontend application
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/             # Next.js pages and API routes
│   │   ├── services/          # API clients and auth services
│   │   └── hooks/             # Custom React hooks
│   └── package.json
├── backend/                    # FastAPI backend application
│   ├── src/
│   │   ├── models/            # SQLModel database models
│   │   ├── services/          # Business logic services
│   │   ├── api/               # API route definitions
│   │   └── database/          # Database session management
│   └── requirements.txt
├── specs/                      # Feature specifications
│   ├── 001-todo-cli/
│   └── 002-phase-ii-arch/     # Current feature specs
├── .env.example               # Environment variable template
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.13+
- Node.js 18+ (for frontend)
- PostgreSQL (or Neon Serverless PostgreSQL account)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (copy from .env.example):
   ```bash
   cp ../.env.example .env
   # Update with your database connection details
   ```

5. Run database migrations:
   ```bash
   python -m src.database.migrate
   ```

6. Start the backend server:
   ```bash
   uvicorn src.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Update with your backend API URL
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## Key Architecture Decisions

### 1. Frontend-Backend Separation
- Frontend and backend are completely separate codebases
- Communication happens only through defined API contracts
- No shared runtime code between frontend and backend

### 2. Authentication Flow
- JWT-based authentication managed by Better Auth
- Backend issues tokens after successful login
- All protected routes require valid JWT in Authorization header
- Frontend stores tokens but does not validate them

### 3. Data Isolation
- Each user can only access their own tasks
- Backend enforces ownership at the database/api level
- No cross-user data access is possible

### 4. Security Model
- Server-side validation for all authentication/authorization
- Frontend decisions are advisory only
- Backend is the single source of truth

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout

### Tasks
- `GET /api/tasks` - Get all user tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost/dbname
JWT_SECRET=your_jwt_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Development Workflow

1. **Specification First**: All features must originate from written specs
2. **Contract Definition**: API contracts defined before implementation
3. **Implementation**: Claude Code generates all application logic
4. **Testing**: Tests written for all functionality
5. **Validation**: Implementation validated against original spec

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Troubleshooting

### Common Issues
1. **401 Unauthorized errors**: Check that JWT token is properly included in Authorization header
2. **Cross-user access**: Verify backend ownership validation is working correctly
3. **Environment variables**: Ensure all required variables are set in both frontend and backend

### Debugging API Calls
- Check that the Authorization header is properly formatted: `Bearer {token}`
- Verify JWT token hasn't expired
- Confirm API endpoint URLs are correct