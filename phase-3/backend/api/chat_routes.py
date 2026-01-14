from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Session
from backend.database import get_session
from backend.middleware.chat_auth import chat_auth
from backend.services.conversation_service import conversation_service
from backend.services.message_service import message_service
from backend.services.ai_service import ai_service
from sqlalchemy import func
import json
from datetime import datetime


router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: list = []


class ConversationsResponse(BaseModel):
    id: int
    title: Optional[str]
    created_at: str
    updated_at: str


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request, db: Session = Depends(get_session)):
    """
    Process natural language chat message and return AI response with tool execution
    """
    # Authenticate the request and get user_id
    user_id = await chat_auth.authenticate_request(req)

    # Get or create conversation
    if request.conversation_id:
        # Get existing conversation
        conversation = conversation_service.get_conversation_by_id(db, request.conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Verify that the conversation belongs to the user
        if conversation.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        thread_id = conversation.thread_id
    else:
        # Create new conversation
        conversation = conversation_service.create_conversation(db, user_id)
        thread_id = conversation.thread_id

    # Add user message to database
    message_service.create_message(
        db=db,
        user_id=user_id,
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )

    # Add user message to OpenAI thread
    ai_service.add_message_to_thread(thread_id, request.message, "user")

    # Run the assistant
    result = ai_service.run_assistant(thread_id, user_id)

    # Add assistant message to database
    message_service.create_message(
        db=db,
        user_id=user_id,
        conversation_id=conversation.id,
        role="assistant",
        content=result["response"],
        tool_calls=json.dumps(result["tool_calls"]) if result["tool_calls"] else None
    )

    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    db.add(conversation)
    db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        response=result["response"],
        tool_calls=result["tool_calls"]
    )


@router.get("/conversations", response_model=list[ConversationsResponse])
async def get_conversations(req: Request, db: Session = Depends(get_session)):
    """
    List all conversations for the authenticated user
    """
    # Authenticate the request and get user_id
    user_id = await chat_auth.authenticate_request(req)

    conversations = conversation_service.get_user_conversations(db, user_id)

    return [
        ConversationsResponse(
            id=conv.id,
            title=conv.title,
            created_at=conv.created_at.isoformat(),
            updated_at=conv.updated_at.isoformat()
        )
        for conv in conversations
    ]


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageResponse])
async def get_conversation_messages(conversation_id: int, req: Request, db: Session = Depends(get_session)):
    """
    Get all messages for a specific conversation
    """
    # Authenticate the request and get user_id
    user_id = await chat_auth.authenticate_request(req)

    # Verify that the conversation belongs to the user
    conversation = conversation_service.get_conversation_by_id(db, conversation_id)
    if not conversation or conversation.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    messages = message_service.get_messages_by_conversation(db, conversation_id)

    return [
        MessageResponse(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at.isoformat()
        )
        for msg in messages
    ]