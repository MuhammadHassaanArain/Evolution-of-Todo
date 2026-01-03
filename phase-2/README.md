# Hackathon Todo Application

## Overview
This is a full-stack todo web application with user authentication and task management capabilities.

## Architecture
- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.13+, SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth + JWT

## Project Structure
```
hackathon-todo/
├── frontend/                   # Next.js frontend application
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/             # Next.js pages and API routes
│   │   ├── services/          # API clients and auth services
│   │   ├── hooks/             # Custom React hooks
│   │   └── utils/             # Utility functions
│   └── package.json
├── backend/                    # FastAPI backend application
│   ├── src/
│   │   ├── models/            # SQLModel database models
│   │   ├── services/          # Business logic services
│   │   ├── api/               # API route definitions
│   │   ├── database/          # Database session management
│   │   ├── middleware/        # Request middleware
│   │   ├── utils/             # Utility functions
│   │   └── config/            # Configuration management
│   └── requirements.txt
├── specs/                      # Feature specifications
├── docs/                       # Documentation
├── .env.example               # Environment variable template
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.13+
- Node.js 18+
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