from typing import List, Optional, Union
from sqlmodel import Session, select
from ..models.message import Message, RoleEnum
from datetime import datetime


class MessageService:
    """
    Service for managing messages in conversations
    """

    def create_message(self, db: Session, user_id: str, conversation_id: int, role: Union[RoleEnum, str], content: str, tool_calls: Optional[str] = None) -> Message:
        """
        Create a new message in a conversation
        """
        # Ensure role is converted to string if it's an enum
        role_value = role.value if isinstance(role, RoleEnum) else role

        message = Message(
            user_id=user_id,
            conversation_id=conversation_id,
            role=role_value,
            content=content,
            tool_calls=tool_calls,
            created_at=datetime.utcnow()
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    def get_message_by_id(self, db: Session, message_id: int) -> Optional[Message]:
        """
        Get a message by its ID
        """
        return db.exec(select(Message).where(Message.id == message_id)).first()

    def get_messages_by_conversation(self, db: Session, conversation_id: int) -> List[Message]:
        """
        Get all messages for a conversation, ordered by creation time
        """
        return db.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        ).all()

    def get_latest_messages(self, db: Session, conversation_id: int, limit: int = 10) -> List[Message]:
        """
        Get the latest messages for a conversation
        """
        return db.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        ).all()

    def update_message_content(self, db: Session, message_id: int, content: str) -> Optional[Message]:
        """
        Update the content of a message (should rarely be needed)
        """
        message = self.get_message_by_id(db, message_id)
        if message:
            message.content = content
            db.add(message)
            db.commit()
            db.refresh(message)

        return message

    def delete_message(self, db: Session, message_id: int) -> bool:
        """
        Delete a message
        """
        message = self.get_message_by_id(db, message_id)
        if message:
            db.delete(message)
            db.commit()
            return True

        return False


# Global instance
message_service = MessageService()