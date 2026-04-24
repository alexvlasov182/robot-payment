"""Configuration for the connection to the database"""

from sqlalchemy import create_engine  # type: ignore[reportMissingImports]  # pylint: disable=import-error
from sqlalchemy.orm import declarative_base, sessionmaker  # type: ignore[reportMissingImports]  # pylint: disable=import-error
from app.core.config import settings

# Use sync engine (psycopg2) - simpler for our sync endpoints
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Get database connection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
