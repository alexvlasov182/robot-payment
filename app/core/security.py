"""Scurity configuration"""

from datetime import datetime, timedelta, timezone
from jose import jwt  # type: ignore[reportMissingImports]  # pylint: disable=import-error
from passlib.context import CryptContext  # type: ignore[reportMissingImports]  # pylint: disable=import-error
from app.core.config import settings

pwd_context = CryptContext(shcemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    """The hash the password"""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    """Create an access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
