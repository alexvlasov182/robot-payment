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
from app.core.logger import AppLogger

# Create logger instance
logger = AppLogger(__name__)


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

        logger.info(f"User registered successfully - user_id={user.id}, email={email}")
        return {"id": user.id, "email": user.email}

    def authenticate_user(self, email: str, password: str) -> dict:
        """Authenticate user and return user data"""
        logger.info(f"Login attempt - email={email}")

        user = self.user_repo.get_by_email(email)
        if not user:
            logger.warning(f"Login failed - user not found - email={email}")
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.hashed_password):  # type: ignore
            logger.warning(f"Login failed - invalid password - email={email}")
            raise ValueError("Invalid credentials")

        logger.info(
            f"User authenticated successfully - user_id={user.id}, email={email}"
        )
        # Return dictionary, not SQLAlchemy object
        return {"id": user.id, "email": user.email}

    def get_tokens(self, email: str) -> dict:
        """Get access and refresh tokens"""
        logger.info(f"Generating tokens for - email={email}")
        access_token = create_access_token(data={"sub": email})
        refresh_token = create_refresh_token(data={"sub": email})
        return {"access_token": access_token, "refresh_token": refresh_token}

    def refresh_token(self, refresh_token: str) -> dict:
        """Refresh access token"""
        from app.core.security import decode_refresh_token

        logger.info("Token refresh attempt")

        email = decode_refresh_token(refresh_token)
        if not email:
            logger.warning("Token refresh failed - invalid refresh token")
            raise ValueError("Invalid refresh token")

        user = self.user_repo.get_by_email(email)
        if not user:
            logger.warning(f"Token refresh failed - user not found - email={email}")
            raise ValueError("User not found")

        logger.info(f"Token refreshed successfully - email={email}")
        return self.get_tokens(user.email)  # type: ignore

    def logout(self, email: str) -> None:
        """Logout user"""
        logger.info(f"User logged out - email={email}")
