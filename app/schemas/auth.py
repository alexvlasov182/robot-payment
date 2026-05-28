"""Main file fot the Auth Schemas"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    """Request schema for user registration"""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")
    confirm_password: str = Field(..., description="Confirm password")

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        """Require a minumum bar beyond length"""
        if not any(ch.isalpha() for ch in value):
            raise ValueError("Password must contain at least one letter")
        if not any(ch.isdigit() for ch in value):
            raise ValueError("Password must contain at least one digit")
        return value


class UserLogin(BaseModel):
    """Request schema for user login"""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    """Response schema for login"""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: Optional[str] = Field(None, description="Refresh token (optional)")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(default=1800, description="Token expiration in seconds")


class RefreshTokenRequest(BaseModel):
    """Request schema for toekn refresh"""

    refresh_token: str = Field(..., description="Refresh token")


class RefreshTokenResponse(BaseModel):
    """Response schema for token refresh"""

    access_token: str = Field(..., description="New JWT access token")
    refresh_token: str = Field(..., description="New JWT refresh token")
