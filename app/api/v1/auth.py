"""Auth endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_auth_service
from app.services.auth_service import AuthService
from app.schemas.auth import UserLogin, UserRegister, TokenResponse
from app.core.security import create_access_token, create_refresh_token

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
        return {"message": "User registered successfully", "user": user}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
    description="Authenticate and get JWT tokens",
)
async def login(
    user_data: UserLogin, auth_service: AuthService = Depends(get_auth_service)
):
    """Login and get access token + refresh token"""
    try:
        # Authenticate user
        user = auth_service.authenticate_user(user_data.email, user_data.password)
        
        # Create both tokens
        access_token = create_access_token(data={"sub": user["email"]})
        refresh_token = create_refresh_token(data={"sub": user["email"]})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=1800
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e
