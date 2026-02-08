# Data Model: Chatbot Backend for Todo Task Management

## Entities

### Conversation
**Description**: Represents a user's ongoing dialogue with the chatbot

**Fields**:
- id (integer): Unique identifier for the conversation
- user_id (integer): Reference to the authenticated user who owns the conversation
- created_at (datetime): Timestamp when the conversation was initiated
- updated_at (datetime): Timestamp when the conversation was last updated
- title (string): Optional title for the conversation (derived from first message or topic)

**Validation Rules**:
- user_id must be a valid user in the system
- created_at must be in the past
- updated_at must be equal to or after created_at

### Message
**Description**: Represents an individual exchange in a conversation

**Fields**:
- id (integer): Unique identifier for the message
- conversation_id (integer): Reference to the conversation this message belongs to
- role (string): Role of the message sender ('user' or 'assistant')
- content (string): The actual content of the message
- timestamp (datetime): When the message was created
- tool_calls (JSON): List of tools called by the assistant in this message
- tool_responses (JSON): Responses from tools called by the assistant

**Validation Rules**:
- conversation_id must reference an existing conversation
- role must be either 'user' or 'assistant'
- content must not be empty
- timestamp must be in the past
- tool_calls must be a valid JSON array of tool calls

### User Context
**Description**: Represents the authenticated user making the request, used for scoping conversations and tasks

**Fields**:
- user_id (integer): Unique identifier for the authenticated user
- jwt_token (string): Authentication token from the request context

**Validation Rules**:
- user_id must be a valid user in the system
- jwt_token must be present and valid for all requests

## Relationships

### Conversation ↔ Message
- One-to-Many relationship: One conversation can have many messages
- Foreign key: Message.conversation_id references Conversation.id
- Constraint: Messages are deleted when their conversation is deleted

## State Transitions

### Conversation State Transitions
- Active: New conversation created when user starts chatting
- Active: Conversation updated when new messages are added
- (No explicit termination - conversations remain for history)

### Message State Transitions
- Created: When a new message is added to a conversation
- Updated: When tool responses are appended to assistant messages

## Indexes

### Performance Optimizations
- Conversation: Index on user_id for quick retrieval of user's conversations
- Message: Index on conversation_id for quick retrieval of conversation history
- Message: Composite index on conversation_id and timestamp for chronological ordering