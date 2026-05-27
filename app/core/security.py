"""Security configuration"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
import hashlib
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Constant-time path for failed lookups (mitigate user enumeration via timing)
_DUMMY_TIMING_PLAIN = "\x00jwt_login_timing_dummy\x00"
DUMMY_PASSWORD_HASH: str = pwd_context.hash(_DUMMY_TIMING_PLAIN)


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2-SHA256"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def hash_token(token: str) -> str:
    """Hash a token for secure storage (SHA256)"""
    return hashlib.sha256(token.encode()).hexdigest()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    # python-jose expects `exp` as Unix timestamp (seconds)
    to_encode.update(
        {"exp": int(expire.timestamp()), "type": "access"}
    )  # Fixed: "access" not "refresh"
    return jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )  # Fixed: algorithm not algorithms


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expire_days
        )

    to_encode.update({"exp": int(expire.timestamp()), "type": "refresh"})
    return jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )  # Fixed: algorithm not algorithms


def decode_access_token(token: str) -> Optional[str]:
    """Decode JWT token and return subject (email)"""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],  # Fixed: use settings.algorithm in list
        )
        # Verify it's an access token
        if payload.get("type") != "access":
            return None
        return payload.get("sub")
    except jwt.JWTError:  # type: ignore
        return None


def decode_refresh_token(token: str) -> Optional[str]:
    """Decode refresh token and return subject (email)"""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],  # Fixed: use settings.algorithm in list
        )
        # Verify it's a refresh token
        if payload.get("type") != "refresh":
            return None
        return payload.get("sub")
    except jwt.JWTError:  # type: ignore
        return None
