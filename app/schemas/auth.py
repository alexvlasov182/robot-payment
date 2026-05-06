"""Main file fot the Auth Schemas"""

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """Request schema for user registration"""

    email: EmailStr = Field(..., description="User eamil address")
    password: str = Field(..., min_length=6, description="User passwrod")
    confirm_password: str = Field(..., description="Confirm password")


class UserLogin(BaseModel):
    """Request schema for user login"""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    """Response schema for login"""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(default=1800, description="Token expiration in seconds")
