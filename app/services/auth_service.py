"""Services main file"""

from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password


class AuthService:
    """Authentication service with dependency injection"""

    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register_user(self, email: str, password: str) -> dict:
        """Register a new user"""

        if self.user_repo.exists_by_email(email):
            raise ValueError("Email already registered")

        hashed = hash_password(password)
        user_data = UserCreate(email=email, hashed_password=hashed)
        user = self.user_repo.create(user_data)

        return {"id": user.id, "email": user.email}

    def authenticate_user(self, email: str, password: str) -> dict:
        """Authenticaticate user and return user data"""
        user = self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.hashed_password):  # type: ignore
            raise ValueError("Invalid credentials")

        return {"id": user.id, "email": user.email}
