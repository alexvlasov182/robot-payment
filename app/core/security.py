"""Security configuration"""

from datetime import UTC, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2-SHA256"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithms)


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days)

    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithms)


def decode_access_token(token: str) -> str | None:
    """Decode JWT token and return subject (email)"""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithms]
        )
        # Check if it's an access token
        if payload.get("type") != "access":
            return None
        return payload.get("sub")
    except jwt.JWTError:  # type: ignore
        return None


def decode_refresh_token(token: str) -> str | None:
    """Decode refresh token and return subject (email)"""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithms]
        )
        # Check if it's a refresh token
        if payload.get("type") != "refresh":
            return None
        return payload.get("sub")
    except jwt.JWTError:  # type: ignore
        return None
