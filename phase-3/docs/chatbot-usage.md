# AI-Powered Todo Chatbot

The AI-Powered Todo Chatbot allows users to manage their todos using natural language commands. The chatbot is integrated directly into the application interface with a floating chat button.

## Features

- **Natural Language Processing**: Communicate with your todo list using everyday language
- **Persistent Conversations**: Your conversation history is saved and can be resumed later
- **Task Management**: Add, list, update, complete, and delete tasks using simple commands
- **Real-time Feedback**: Get instant confirmation of your actions

## Supported Commands

- **Add tasks**: "Add a task to buy groceries", "Create a task to finish report"
- **List tasks**: "Show me my tasks", "What do I need to do?"
- **Complete tasks**: "Mark the grocery task as complete", "Finish the report"
- **Update tasks**: "Change the grocery task to buy milk and bread"
- **Delete tasks**: "Remove the grocery task"

## How to Use

1. Click the chat icon in the bottom-right corner of the screen
2. Type your command in natural language
3. The AI assistant will process your request and confirm the action
4. Your task list will be updated automatically

## Technical Architecture

- **Frontend**: React components with Next.js
- **Backend**: FastAPI with OpenAI integration
- **AI Service**: OpenAI Assistant API with custom tools
- **Database**: PostgreSQL with conversation and message persistence
- **Authentication**: JWT-based security ensuring user isolation

## MCP Server

The system uses an MCP (Model Context Protocol) server to securely connect the AI assistant to your existing todo management functionality. The MCP server exposes tools that map directly to your existing API endpoints, ensuring all security and validation rules are properly enforced.