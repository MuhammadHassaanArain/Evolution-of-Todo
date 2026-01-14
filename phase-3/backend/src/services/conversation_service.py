from typing import List, Optional
from sqlmodel import Session, select
from ..models.conversation import Conversation
from ..models.message import Message
import uuid
from datetime import datetime


class ConversationService:
    """
    Service for managing conversations and messages
    """

    def create_conversation(self, db: Session, user_id: str, first_message: Optional[str] = None, thread_id: Optional[str] = None) -> Conversation:
        """
        Create a new conversation for a user with an auto-generated title
        """
        if not thread_id:
            # Generate a unique thread ID for OpenAI
            thread_id = f"thread_{uuid.uuid4().hex}"

        # Generate title based on first message or timestamp
        title = self.generate_conversation_title(first_message)

        conversation = Conversation(
            user_id=user_id,
            thread_id=thread_id,
            title=title,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    def generate_conversation_title(self, first_message: Optional[str]) -> str:
        """
        Generate a conversation title based on the first message or timestamp
        """
        if first_message:
            # Take first 50 characters of the first message
            title = first_message.strip()[:50]
            # Add ellipsis if the message was truncated
            if len(first_message.strip()) > 50:
                title += "..."
        else:
            # Use timestamp if no message is provided
            title = f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        return title

    def get_conversation_by_id(self, db: Session, conversation_id: int) -> Optional[Conversation]:
        """
        Get a conversation by its ID
        """
        return db.exec(select(Conversation).where(Conversation.id == conversation_id)).first()

    def get_conversation_by_thread_id(self, db: Session, thread_id: str) -> Optional[Conversation]:
        """
        Get a conversation by its thread ID
        """
        return db.exec(select(Conversation).where(Conversation.thread_id == thread_id)).first()

    def get_user_conversations(self, db: Session, user_id: str) -> List[Conversation]:
        """
        Get all conversations for a user
        """
        return db.exec(select(Conversation).where(Conversation.user_id == user_id)).all()

    def update_conversation_title(self, db: Session, conversation_id: int, title: str) -> Optional[Conversation]:
        """
        Update the title of a conversation
        """
        conversation = self.get_conversation_by_id(db, conversation_id)
        if conversation:
            conversation.title = title
            conversation.updated_at = datetime.utcnow()
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        return conversation

    def delete_conversation(self, db: Session, conversation_id: int) -> bool:
        """
        Delete a conversation and its messages
        """
        conversation = self.get_conversation_by_id(db, conversation_id)
        if conversation:
            # Delete associated messages first (due to foreign key constraint)
            messages = db.exec(select(Message).where(Message.conversation_id == conversation_id)).all()
            for message in messages:
                db.delete(message)

            # Then delete the conversation
            db.delete(conversation)
            db.commit()
            return True

        return False

    def get_messages_for_conversation(self, db: Session, conversation_id: int) -> List[Message]:
        """
        Get all messages for a specific conversation
        """
        return db.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        ).all()


# Global instance
conversation_service = ConversationService()