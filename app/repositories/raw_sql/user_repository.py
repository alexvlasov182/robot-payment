"""User Repositories"""

from typing import TypeVar

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import Base
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate, UserUpdate

ModelTypeT = TypeVar("ModelTypeT", bound=Base)  # type: ignore


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """Repository for User entity"""

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> User | None:
        """Get user by email address"""
        normalized = str(email).strip().lower()
        sql = text("SELECT * FROM users WHERE email = :email")
        row = self.db.execute(sql, {"email": normalized}).mappings().first()
        if not row:
            return None
        return self._row_to_model(row)

    def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email"""
        normalized = str(email).strip().lower()
        sql = text("SELECT 1 FROM users WHERE email = :email LIMIT 1")
        row = self.db.execute(sql, {"email": normalized}).first()
        return row is not None

    def _row_to_model(self, row) -> ModelTypeT:  # type: ignore
        """Convert a raw SQL row (mapping) back to a SQLAlchemy model instance"""
        obj = self.model(**dict(row))
        # Mark as "persistent" so SQLAlchemy knows it exists in DB
        self.db.enable_relationship_loading(obj)
        return obj
