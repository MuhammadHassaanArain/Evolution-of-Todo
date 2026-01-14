# Research Document: AI-Powered Todo Chatbot

**Feature**: 001-ai-chatbot
**Date**: 2026-01-14
**Status**: Completed

## Research Objectives

This document addresses the technical unknowns identified in the implementation plan for the AI-powered todo chatbot feature.

## 1. OpenAI Agents SDK Integration

### Decision: Use OpenAI Assistant API with RunExecutor
**Rationale**: The OpenAI Assistant API provides a managed way to run agents with memory and tool integration. The RunExecutor pattern allows for streaming responses and proper error handling.

**Implementation Details**:
- Use `openai.Assistant` to create the agent with MCP tools
- Use `openai.Thread` to maintain conversation context
- Use `openai.beta.threads.runs.RunExecutor` to process user input and execute tools

**Alternatives Considered**:
- Raw OpenAI Completions API: Requires more manual management of context and tool calls
- LangChain: Adds complexity with little benefit for this simple use case

## 2. MCP Server Setup

### Decision: Use Official MCP SDK with FastAPI-style endpoints
**Rationale**: The MCP SDK allows us to define tools that can call our existing FastAPI endpoints. This maintains the architecture constraint of reusing existing APIs.

**Implementation Details**:
- Create a standalone Python application using the official MCP SDK
- Define tools that map to existing CRUD endpoints
- Use HTTP client to call existing FastAPI endpoints from MCP tools
- Host MCP server separately but ensure it can access the main API

**Alternatives Considered**:
- Direct function calls: Would require duplicating business logic
- GraphQL schema: Overcomplicates the simple CRUD operations

## 3. Conversation State Management

### Decision: Use OpenAI Threads + Database Storage
**Rationale**: OpenAI's Thread system provides built-in conversation memory, while database storage ensures persistence across application restarts and enables conversation history viewing.

**Implementation Details**:
- Store OpenAI Thread ID in Conversation model
- Mirror messages in database for UI display
- Sync database messages with OpenAI Thread when needed
- Allow users to resume previous conversations by loading Thread ID

**Alternatives Considered**:
- Pure database approach: Loses OpenAI's context window benefits
- Pure OpenAI approach: No ability to display conversation history in UI

## 4. Rate Limiting & Costs

### Decision: Implement Usage Tracking and Basic Limits
**Rationale**: While we need to be mindful of costs, implementing basic usage tracking provides sufficient protection for a prototype without over-engineering.

**Implementation Details**:
- Track API usage per user in database
- Implement soft limits (warnings) and hard limits (denial)
- Monitor usage patterns to optimize prompts for efficiency
- Log costs per session for future analysis

**Alternatives Considered**:
- Complex subscription system: Too complex for prototype
- Per-minute billing: Not applicable to OpenAI's per-token model

## 5. OpenAI Model Selection

### Decision: Use gpt-4o for Balance of Capability and Cost
**Rationale**: GPT-4o provides excellent reasoning capabilities for interpreting natural language while being more cost-effective than older GPT-4 models.

**Implementation Details**:
- Default to gpt-4o model for assistant
- Configure temperature settings for deterministic tool usage
- Allow model to be configurable via environment variables

**Alternatives Considered**:
- GPT-3.5 Turbo: Less capable for complex natural language understanding
- GPT-4: More expensive with minimal benefit for this use case

## 6. Authentication Flow for AI Requests

### Decision: Pass User Context Through MCP Tools
**Rationale**: Maintain security by ensuring all MCP tool calls include proper user authentication context without exposing credentials to the AI.

**Implementation Details**:
- Extract user_id from JWT in the main API endpoint
- Pass user_id as parameter to MCP tools
- MCP tools validate user ownership when calling existing APIs
- Never expose user credentials to the AI system

**Alternatives Considered**:
- Direct database access from MCP: Would bypass API security layers
- Shared session tokens: Security risk to pass credentials to AI system

## 7. Error Handling Strategy

### Decision: Graceful Degradation with User-Friendly Messages
**Rationale**: AI systems can fail in unpredictable ways, so the system must handle errors gracefully while maintaining a good user experience.

**Implementation Details**:
- Catch and handle API errors from OpenAI
- Format errors appropriately for AI consumption
- Provide fallback responses when tools fail
- Log errors for debugging while protecting user privacy

**Alternatives Considered**:
- Fail fast approach: Would provide poor user experience
- Generic error messages: Would not be helpful for users