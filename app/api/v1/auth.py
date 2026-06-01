"""Auth endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_auth_service
from app.services.auth_service import AuthService
from app.schemas.auth import UserLogin, UserRegister, TokenResponse
from app.core.security import create_access_token, create_refresh_token
from app.core.logger import AppLogger

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = AppLogger(__name__)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
)
async def register(
    user_data: UserRegister, auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user"""
    logger.info(f"Registration request received - email={user_data.email}")

    if user_data.password != user_data.confirm_password:
        logger.warning(
            f"Registration failed - passwords don't match - email={user_data.email}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
        )

    try:
        user = auth_service.register_user(user_data.email, user_data.password)
        logger.info(f"User registered successfully via API - email={user_data.email}")
        return {"message": "User registered successfully", "user": user}
    except ValueError as e:
        logger.warning(f"Registration failed - {str(e)} - email={user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
)
async def login(
    user_data: UserLogin, auth_service: AuthService = Depends(get_auth_service)
):
    """Login and get access token"""
    logger.info(f"Login request received - email={user_data.email}")

    try:
        # authenticate_user returns a dictionary with 'id' and 'email' keys
        user_dict = auth_service.authenticate_user(user_data.email, user_data.password)

        # Access email as dictionary key
        access_token = create_access_token(data={"sub": user_dict["email"]})
        refresh_token = create_refresh_token(data={"sub": user_dict["email"]})

        logger.info(f"User logged in successfully - email={user_data.email}")

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=1800,
        )
    except ValueError as e:
        logger.warning(f"Login failed - {str(e)} - email={user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e
