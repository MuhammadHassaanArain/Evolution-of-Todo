# Quickstart Guide: AI-Powered Todo Chatbot

**Feature**: 001-ai-chatbot
**Date**: 2026-01-14

## Overview
This guide provides essential information to get the AI-powered todo chatbot up and running. The chatbot allows users to manage their todos using natural language commands.

## Prerequisites
- Python 3.13+
- Node.js 18+
- OpenAI API key
- Neon PostgreSQL database
- Better Auth configured

## Environment Setup

### Backend Configuration
1. Set up environment variables:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   DATABASE_URL=your_neon_database_url
   JWT_SECRET=your_jwt_secret
   ```

2. Install Python dependencies:
   ```bash
   pip install fastapi openai sqlmodel python-jose[cryptography] passlib[bcrypt] uvicorn
   ```

3. Run database migrations to create Conversation and Message tables

### MCP Server Setup
1. Create a standalone MCP server application
2. Configure it to connect to the main API
3. Define the tool mappings to existing CRUD endpoints

## Running the Application

### Start Backend Services
1. Start the main FastAPI application:
   ```bash
   uvicorn main:app --reload
   ```

2. Start the MCP server:
   ```bash
   python mcp_server.py
   ```

### Start Frontend
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies and start:
   ```bash
   npm install
   npm run dev
   ```

## Usage Examples

Once the application is running, users can interact with the chatbot using natural language:

- "Add a task to buy groceries"
- "Show me my tasks"
- "Mark the grocery task as complete"
- "Update the grocery task to buy milk and bread"
- "Delete the grocery task"

## Architecture Components

### Database Schema
- `conversations` table: Stores conversation metadata
- `messages` table: Stores individual chat messages
- `tasks` table: Existing todo items (unchanged)

### API Endpoints
- `POST /api/chat`: Process natural language input
- `GET /api/conversations`: List user's conversations
- `GET /api/conversations/{id}/messages`: Get messages for conversation

### MCP Tools
- `add_task`: Maps to existing POST /tasks
- `list_tasks`: Maps to existing GET /tasks
- `complete_task`: Maps to existing PATCH /tasks/{id}/complete
- `update_task`: Maps to existing PUT /tasks/{id}
- `delete_task`: Maps to existing DELETE /tasks/{id}

## Key Features
- Natural language processing for todo management
- Persistent conversation history
- Integration with existing task management system
- User authentication and authorization
- Real-time chat interface