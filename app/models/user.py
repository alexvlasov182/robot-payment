"""Model for the User"""

from sqlalchemy import Boolean, Column, Integer, String  # type: ignore[reportMissingImports]  # pylint: disable=import-error

# from sqlalchemy.sql import func  # type: ignore[reportMissingImports]  # pylint: disable=import-error
from app.core.database import Base


class User(Base):
    """User model for authentication"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    # created_at = Column(DateTime(timezone=True), server_default=func.now())
