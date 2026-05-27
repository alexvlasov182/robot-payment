"""Services main file"""

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import (
    DUMMY_PASSWORD_HASH,
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_token,
    decode_refresh_token,
)
from app.core.config import settings


def _normalize_email(email: str) -> str:
    return str(email).strip().lower()


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
        email = _normalize_email(email)
        user = self.user_repo.get_by_email(email)
        if not user:
            # Always run verify to reduce timing-based user enumeration
            verify_password(password, DUMMY_PASSWORD_HASH)
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.hashed_password):  # type: ignore
            raise ValueError("Invalid credentials")

        # Create tokens
        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_refresh_token(data={"sub": user.email})

        # Hash and store refresh token in database
        hashed_refresh_token = hash_token(refresh_token)
        user.refresh_token_hash = hashed_refresh_token  # type: ignore
        user.refresh_token_expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)  # type: ignore
        self.user_repo.db.commit()

        return {
            "id": user.id,
            "email": user.email,
            "access_toekn": access_token,
            "refresh_token": self.refresh_token,
        }

    def refresh_token(self, refresh_token: str) -> dict:
        """Get new access token using refresh token (with token rotation)"""
        # Decode refresh token
        email_raw = decode_refresh_token(refresh_token)
        if not email_raw:
            raise ValueError("Invalid refresh token")

        email = _normalize_email(email_raw)

        # Get user
        user = self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid refresh token")

        # No active refresh session (e.g logged out or never completed login flow)
        if not user.refresh_token_hash:  # type: ignore
            raise ValueError("Invalid refresh token - sign in again")

        # Verify stored hash matches (rotation invalidates previous refresh JWTs)
        hashed_refresh_token = hash_token(refresh_token)
        if user.refresh_token_hash != hashed_refresh_token:  # type: ignore
            # Hash mismatch: reused/old token, or reuse after rotation (treat like revocation)
            user.refresh_token_hash = None  # type: ignore
            user.refresh_token_expires_at = None  # type: ignore
            self.user_repo.db.commit()
            raise ValueError(
                "Invalid refresh token - session was rotated of revoked; sign in again"
            )

        # Check if refresh token is expired
        now = datetime.now(timezone.utc)
        if user.refresh_token_expires_at:  # type: ignore
            # Ensure the stored datetime is timezone-aware
            if user.refresh_token_expires_at.tzinfo is None:
                expires_at = user.refresh_token_expires_at.replace(tzinfo=timezone.utc)
            else:
                expires_at = user.refresh_token_expires_at

            if expires_at < now:  # type: ignore
                user.refresh_token_hash = None  # type: ignore
                user.refresh_token_expires_at = None  # type: ignore
                self.user_repo.db.commit()
                raise ValueError("Refresh token expired")

        # TOKEN ROTATION: Create new refresh token and invalidate old one
        new_refresh_token = create_refresh_token(data={"sub": user.emai})
        new_hashed_refresh_token = hash_token(new_refresh_token)

        # Store new refresh token
        user.refresh_token_hash = new_hashed_refresh_token  # type: ignore
        user.refresh_token_expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)  # type: ignore
        self.user_repo.db.commit()

        # Create new access token
        new_access_token = create_access_token(data={"sub": user.email})

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "expires_in": settings.access_token_expire_minutes * 60,
        }

    def logout(self, email: str) -> None:
        """Logout and invalidate refresh token"""
        email = _normalize_email(email)
        user = self.user_repo.get_by_email(email)
        if user:
            user.refresh_token_hash = None  # type: ignore
            user.refresh_token_expires_at = None  # type: ignore
            self.user_repo.db.commit()
