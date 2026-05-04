"""Dependency Injection"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token

from app.services.auth_service import AuthService
from app.services.robot_service import RobotService
from app.services.terminal_services import TerminalService

# Security
security = HTTPBearer()


# Service factories
def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Get AuthService instance"""
    return AuthService(db)


def get_robot_service(db: Session = Depends(get_db)) -> RobotService:
    """Get RobotService instance"""
    return RobotService(db)


def get_terminal_service() -> TerminalService:
    """Get TerminalService instance"""
    return TerminalService()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> dict:
    """Get current authenticated user"""
    token = credentials.credentials
    email = decode_access_token(token)

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    auth_service = AuthService(db)
    return {"email": email, "auth_service": auth_service}
