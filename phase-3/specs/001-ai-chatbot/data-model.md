# Data Model Design: AI-Powered Todo Chatbot

**Feature**: 001-ai-chatbot
**Date**: 2026-01-14
**Status**: Draft

## Entity Definitions

### Conversation
Represents a user's chat session with the AI assistant

**Fields**:
- `id`: Integer, Primary Key, Auto-increment
- `user_id`: String, Foreign Key to user table, Required
- `thread_id`: String, OpenAI Thread ID, Required
- `title`: String, Optional, Generated from first message
- `created_at`: DateTime, Required, Auto-set
- `updated_at`: DateTime, Required, Auto-updated

**Validation Rules**:
- user_id must exist in users table
- thread_id must be unique across all conversations
- created_at and updated_at automatically managed

**Relationships**:
- Belongs to one user
- Has many messages

### Message
Individual exchanges between user and assistant

**Fields**:
- `id`: Integer, Primary Key, Auto-increment
- `user_id`: String, Foreign Key to user table, Required
- `conversation_id`: Integer, Foreign Key to conversation table, Required
- `role`: String, Enum ['user', 'assistant'], Required
- `content`: Text, Message content, Required
- `tool_calls`: JSON, Optional, Contains tool call information
- `created_at`: DateTime, Required, Auto-set

**Validation Rules**:
- user_id must match conversation owner
- conversation_id must exist in conversations table
- role must be either 'user' or 'assistant'
- content must not be empty

**Relationships**:
- Belongs to one user
- Belongs to one conversation

### Task (Existing)
Existing todo item entity that the chatbot interacts with

**Fields** (from existing model):
- `id`: Integer, Primary Key, Auto-increment
- `user_id`: String, Foreign Key to user table, Required
- `title`: String, Required
- `description`: Text, Optional
- `completed`: Boolean, Default: false
- `created_at`: DateTime, Required, Auto-set
- `updated_at`: DateTime, Required, Auto-updated

**Validation Rules** (from existing model):
- user_id must exist in users table
- title must not be empty
- completed defaults to false

**Relationships** (from existing model):
- Belongs to one user

## State Transitions

### Conversation State
- Created when user initiates first chat
- Updated when new messages are added
- Remains active indefinitely (no expiration)

### Message State
- Created when user sends message or assistant responds
- Immutable once created (no updates/deletes through API)

### Task State (Existing)
- Created with completed=false
- Updated to completed=true when marked complete
- Deleted when removed from user's list

## Indexes

### Conversation
- Index on (user_id, created_at) for efficient user conversation listing
- Unique index on thread_id for OpenAI thread lookup

### Message
- Index on (conversation_id, created_at) for chronological message retrieval
- Index on (user_id, created_at) for user activity queries

## Constraints

### Business Logic Constraints
- Users can only access their own conversations and messages
- Messages must belong to conversations owned by the same user
- Conversation thread_id must be valid for OpenAI API

### Data Integrity Constraints
- All foreign keys have proper references
- Timestamps automatically managed by database
- Required fields enforced at database level