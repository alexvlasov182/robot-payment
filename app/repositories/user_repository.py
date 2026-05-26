"""User Repositories"""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """Repository for User entity"""

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address"""
        normalized = str(email).strip().lower()
        return self.db.query(User).filter(User.email == normalized).first()

    def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email"""
        return self.get_by_email(email) is not None
