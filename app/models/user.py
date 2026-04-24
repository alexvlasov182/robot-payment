"""Model for the User"""

from sqlalchemy import Column, Integer, String, DateTime  # type: ignore[reportMissingImports]  # pylint: disable=import-error
from sqlalchemy.sql import func  # type: ignore[reportMissingImports]  # pylint: disable=import-error
from app.core.database import Base


class User(Base):
    """Base model for the Users"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
