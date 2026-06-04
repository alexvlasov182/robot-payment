"""Auth endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_auth_service
from app.services.auth_service import AuthService
from app.schemas.auth import UserLogin, UserRegister, TokenResponse
from loguru import logger

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account",
)
async def register(
    user_data: UserRegister, auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user"""
    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
        )

    try:
        user = auth_service.register_user(user_data.email, user_data.password)
        logger.info(f"User registered successfully via API - email={user_data.email}")
        return {"message": "User registered successfully", "user": user}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
    description="Authenticate and get JWT token",
)
async def login(
    user_data: UserLogin, auth_service: AuthService = Depends(get_auth_service)
):
    """Login and get access token"""
    try:
        user = auth_service.authenticate_user(user_data.email, user_data.password)
        tokens = auth_service.get_tokens(user["email"])
        logger.info(f"User logged in successfully - email={user_data.email}")
        return TokenResponse(
            access_token=tokens["access_token"],
            token_type=tokens["token_type"],
            expires_in=tokens["expires_in"],
        )  # type: ignore
    except ValueError as e:
        logger.warning(f"Login failed - {str(e)} - email={user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh token",
    description="Get new access token using refresh token",
)
async def refresh_token(
    refresh_token: str, auth_service: AuthService = Depends(get_auth_service)
):
    """Refresh access token"""
    try:
        tokens = auth_service.refresh_token(refresh_token)
        return TokenResponse(
            access_token=tokens["access_token"],
            token_type=tokens["token_type"],
            expires_in=tokens["expires_in"],
        )  # type: ignore
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e


@router.post(
    "/logout",
    summary="Logout user",
    description="Invalidate current token",
)
async def logout(
    auth_service: AuthService = Depends(get_auth_service), token: str = None
):
    """Logout user"""
    result = auth_service.logout(token)
    return {"message": "Successfully logged out"}
