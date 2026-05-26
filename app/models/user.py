"""Model for the User"""

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from app.core.database import Base


class User(Base):
    """User model for authentication"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    refresh_token_hash = Column(
        String(64), nullable=True
    )  # SHA256 hash of refresh token
    refresh_token_expires_at = Column(DateTime(timezone=True), nullable=True)  # type: ignore

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"

    # created_at = Column(DateTime(timezone=True), server_default=func.now())
