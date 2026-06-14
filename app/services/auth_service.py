"""Services main file"""

from loguru import logger
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
    """Authentication service with dependency injection"""

    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        logger.info("AuthService initialized")

    def register_user(self, email: str, password: str) -> dict:
        """Register a new user"""
        logger.info(f"Registration attempt - email={email}")

        if self.user_repo.exists_by_email(email):
            logger.warning(
                f"Registration failed - email already exists - email={email}"
            )
            raise ValueError("Email already registered")

        hashed = hash_password(password)
        user_data = UserCreate(email=email, hashed_password=hashed)
        user = self.user_repo.create(user_data)

        logger.info(
            f"User registered successfully - user_id={user.id}, email={user.email}"
        )
        return {"id": user.id, "email": user.email}

    def authenticate_user(self, email: str, password: str) -> dict:
        """Authenticate user and return user data"""
        logger.info(f"Login attempt - email={email}")

        user = self.user_repo.get_by_email(email)
        if not user:
            logger.warning(f"Login failed - user not found - email={email}")
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.hashed_password):  # type: ignore
            logger.warning(f"Login failed - wrong password - email={email}")
            raise ValueError("Invalid credentials")

        logger.info(
            f"User authenticated successfully - user_id={user.id}, email={user.email}"
        )
        return {"id": user.id, "email": user.email}

    def get_tokens(self, email: str) -> dict:
        """Generate access and refresh tokens"""
        logger.info(f"Generating tokens for - email={email}")
        access_token = create_access_token(data={"sub": email})
        refresh_token = create_refresh_token(data={"sub": email})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60,
        }

    def refresh_token(self, refresh_token: str) -> dict:
        """Refresh access token using refresh token"""

        logger.info("Refreshing token")

        email = decode_refresh_token(refresh_token)
        if not email:
            raise ValueError("Invalid refresh token")

        new_access_token = create_access_token(data={"sub": email})
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60,
        }

    def logout(self, token: str) -> bool:
        """Logout user (in production, add token to blacklist)"""
        logger.info("Logout requested")
        # In production, you would add token to a blacklist in Redis
        return True
