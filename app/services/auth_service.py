"""Authentication service."""

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class AuthService:
    """Authentication service with dependency injection."""

    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register_user(
        self,
        email: str,
        password: str,
    ) -> dict:
        """Register a new user."""

        if self.user_repo.exists_by_email(email):
            raise ValueError("Email already registered")

        hashed_password = hash_password(password)

        user_data = UserCreate(
            email=email,
            hashed_password=hashed_password,
        )

        user = self.user_repo.create(user_data)

        return {
            "id": user.id,
            "email": user.email,
        }

    def authenticate_user(self, email: str, password: str) -> dict:
        """Authenticate user"""

        user = self.user_repo.get_by_email(email)

        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        return {
            "id": user.id,
            "email": user.email,
        }

    def get_tokens(
        self,
        email: str,
    ) -> dict:
        """Generate access and refresh JWT tokens."""

        access_token = create_access_token(
            data={"sub": email},
        )

        refresh_token = create_refresh_token(
            data={"sub": email},
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60,
        }

    def refresh_token(
        self,
        refresh_token: str,
    ) -> dict:
        """Create a new access token from refresh token."""

        email = decode_refresh_token(refresh_token)

        if not email:
            raise ValueError("Invalid refresh token")

        access_token = create_access_token(
            data={"sub": email},
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60,
        }

    def logout(
        self,
        token: str,
    ) -> bool:
        """
        Logout user.

        JWT access tokens are stateless.
        Refresh token invalidation can be implemented
        using database storage or token blacklist.
        """

        return True
