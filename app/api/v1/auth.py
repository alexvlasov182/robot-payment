"""Auth endpoints"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.api.dependencies import get_auth_service, get_current_user
from app.services.auth_service import AuthService
from app.schemas.auth import RefreshTokenRequest, UserLogin, UserRegister, TokenResponse

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
    description="Authenticate and get JWT token",
)
async def login(
    user_data: UserLogin, auth_service: AuthService = Depends(get_auth_service)
):
    """Login and get access token + refresh token"""
    try:
        result = auth_service.authenticate_user(user_data.email, user_data.password)
        return TokenResponse(
            access_token=result["access_token"], refresh_token=result["refresh_token"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e


@router.post(
    "/token",
    response_model=TokenResponse,
    summary="OAuth2-compatible login (form)",
    description=(
        "Same as /login but accepts `application/x-www-form-urlencoded`"
        "as used by OAuth2PasswordRequestFrom. Use your **emial** in the `username` field."
    ),
)
async def login_oauth2_form(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(get_auth_service),
):
    """Loign via OAuth2 password flow (Swagger 'Authorize' compatible)."""
    try:
        result = auth_service.authenticate_user(form_data.username, form_data.password)
        return TokenResponse(
            access_token=result["access_token"], refresh_token=result["refresh_token"]
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Get new access token using refresh token (implements token rotation)"""
    try:
        result = auth_service.refresh_token(refresh_data.refresh_token)
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout user",
)
async def logout(
    current_user: dict = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Logout and invalidate refresh token"""
    auth_service.logout(current_user["email"])
    return None
