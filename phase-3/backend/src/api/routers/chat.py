from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Session
from ..deps import get_current_user
from ...database.connection import get_session
from ...services.conversation_service import conversation_service
from ...services.message_service import message_service
from ...services.ai_service import ai_service
import json
from datetime import datetime
from ...models import User
from ...models.message import RoleEnum


router = APIRouter(tags=["chat"])


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
    role: RoleEnum
    content: str
    created_at: str
    
@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Process natural language chat message and return AI response
    using the new Gemini Agent SDK.
    """
    user_id = str(current_user.id)

    # Get or create conversation
    if request.conversation_id:
        conversation = conversation_service.get_conversation_by_id(db, request.conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        if conversation.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
    else:
        conversation = conversation_service.create_conversation(db, user_id, request.message)

    # Save user message to database
    message_service.create_message(
        db=db,
        user_id=user_id,
        conversation_id=conversation.id,
        role=RoleEnum.user,
        content=request.message
    )

    # Run the Gemini agent
    response_text = await ai_service.run_async(request.message)

    # Save assistant response to database
    message_service.create_message(
        db=db,
        user_id=user_id,
        conversation_id=conversation.id,
        role=RoleEnum.assistant,
        content=response_text
    )

    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    db.add(conversation)
    db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        response=response_text,
        tool_calls=[]  # no tool_calls tracking yet for Gemini agent
    )





@router.get("/conversations", response_model=list[ConversationsResponse])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    List all conversations for the authenticated user
    """
    user_id = str(current_user.id)  # Convert to string to match expected format
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
async def get_conversation_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Get all messages for a specific conversation
    """
    user_id = str(current_user.id)  # Convert to string to match expected format

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