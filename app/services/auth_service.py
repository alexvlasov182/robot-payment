"""Services main file"""

from sqlalchemy.orm import Session  # type: ignore[reportMissingImports]  # pylint: disable=import-error
from app.models.user import User
from app.core.security import hash_password, verify_password


def get_user_by_email(db: Session, email: str):
    """Get the user by email"""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, password: str):
    """Add the user to the database"""
    hashed = hash_password(password)
    user = User(email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    """Authentication for user into database"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):  # type: ignore
        return None
    return user
