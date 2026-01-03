from sqlmodel import Session, select
from typing import Optional
from ..models.user import User, UserCreate, UserUpdate, UserWithPassword
from .auth_service import auth_service
from ..utils.logging import log_auth_event


class UserService:
    def create_user(self, session: Session, user_create: UserCreate) -> User:
        """
        Create a new user with hashed password
        """
        # Check if user with this email already exists
        existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            log_auth_event("registration_failed", user=existing_user, success=False, details={"reason": "email_already_exists"})
            raise ValueError("Email already registered")

        # Hash the password
        hashed_password = auth_service.get_password_hash(user_create.password)

        # Create the user
        db_user = User(
            email=user_create.email,
            name=user_create.name,
            hashed_password=hashed_password
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        log_auth_event("user_created", user=db_user, success=True)
        return db_user

    def get_user_by_id(self, session: Session, user_id: str) -> Optional[User]:
        """
        Get a user by ID
        """
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        if user:
            log_auth_event("user_retrieved", user=user, success=True)
        else:
            log_auth_event("user_not_found", user_id=user_id, success=False)
        return user

    def get_user_by_email(self, session: Session, email: str) -> Optional[User]:
        """
        Get a user by email
        """
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if user:
            log_auth_event("user_retrieved_by_email", user=user, success=True)
        else:
            log_auth_event("user_not_found_by_email", user_id=email, success=False)
        return user

    def update_user(self, session: Session, user_id: str, user_update: UserUpdate) -> Optional[User]:
        """
        Update user information
        """
        db_user = self.get_user_by_id(session, user_id)
        if not db_user:
            log_auth_event("user_update_failed", user_id=user_id, success=False, details={"reason": "user_not_found"})
            return None

        # Update the fields that were provided
        if user_update.name is not None:
            db_user.name = user_update.name
        if user_update.email is not None:
            # Check if the new email is already taken by another user
            existing_user = session.exec(
                select(User).where(User.email == user_update.email, User.id != user_id)
            ).first()
            if existing_user:
                log_auth_event("user_update_failed", user=db_user, success=False, details={"reason": "email_already_exists"})
                raise ValueError("Email already registered by another user")
            db_user.email = user_update.email

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        log_auth_event("user_updated", user=db_user, success=True)
        return db_user

    def delete_user(self, session: Session, user_id: str) -> bool:
        """
        Delete a user by ID
        """
        db_user = self.get_user_by_id(session, user_id)
        if not db_user:
            log_auth_event("user_delete_failed", user_id=user_id, success=False, details={"reason": "user_not_found"})
            return False

        session.delete(db_user)
        session.commit()
        log_auth_event("user_deleted", user=db_user, success=True)
        return True

    def list_users(self, session: Session, offset: int = 0, limit: int = 100) -> list[User]:
        """
        List users with pagination
        """
        statement = select(User).offset(offset).limit(limit)
        users = session.exec(statement).all()
        log_auth_event("users_listed", success=True, details={"count": len(users)})
        return users

    def get_user_with_password(self, session: Session, user_id: str) -> Optional[UserWithPassword]:
        """
        Get a user with password (for internal use)
        """
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        if user:
            log_auth_event("user_with_password_retrieved", user=user, success=True)
            return UserWithPassword.from_orm(user) if hasattr(UserWithPassword, 'from_orm') else UserWithPassword(
                id=user.id,
                email=user.email,
                name=user.name,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                hashed_password=user.hashed_password
            )
        log_auth_event("user_with_password_not_found", user_id=user_id, success=False)
        return None


# Create a singleton instance of the UserService
user_service = UserService()