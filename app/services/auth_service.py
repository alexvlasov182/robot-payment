"""Services main file"""

from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)


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
        """Authenticate user and return user data"""
        user = self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        # Return dictionary, not SQLAlchemy object
        return {"id": user.id, "email": user.email}

    def get_tokens(self, email: str) -> dict:
        """Get access and refresh tokens"""
        access_token = create_access_token(data={"sub": email})
        refresh_token = create_refresh_token(data={"sub": email})
        return {"access_token": access_token, "refresh_token": refresh_token}

    def refresh_token(self, refresh_token: str) -> dict:
        """Refresh access token"""
        from app.core.security import decode_refresh_token

        email = decode_refresh_token(refresh_token)
        if not email:
            raise ValueError("Invalid refresh token")

        user = self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("User not found")

        return self.get_tokens(user.email)

    def logout(self, email: str) -> None:
        """Logout user"""
        pass
