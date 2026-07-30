"""Security configuration."""

from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing configuration
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """Hash password using PBKDF2-SHA256."""

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Verify password against hash."""

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    """Create JWT access token."""

    to_encode = data.copy()

    expire = (
        datetime.now(UTC) + expires_delta
        if expires_delta
        else datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    )

    to_encode.update(
        {
            "exp": expire,
            "type": "access",
        }
    )

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithms,
    )


def create_refresh_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    """Create JWT refresh token."""

    to_encode = data.copy()

    expire = (
        datetime.now(UTC) + expires_delta
        if expires_delta
        else datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days)
    )

    to_encode.update(
        {
            "exp": expire,
            "type": "refresh",
        }
    )

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithms,
    )


def _decode_token(
    token: str,
    token_type: str,
) -> str | None:
    """Decode JWT token and validate type."""

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithms],
        )

        if payload.get("type") != token_type:
            return None

        subject = payload.get("sub")

        if not isinstance(subject, str):
            return None

        return subject

    except JWTError:
        return None


def decode_access_token(
    token: str,
) -> str | None:
    """Decode access token."""

    return _decode_token(
        token,
        "access",
    )


def decode_refresh_token(
    token: str,
) -> str | None:
    """Decode refresh token."""

    return _decode_token(
        token,
        "refresh",
    )
