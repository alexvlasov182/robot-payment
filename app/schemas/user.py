"""User schemas for request/response validation."""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    """Schema for creating a new user"""

    email: EmailStr = Field(..., description="User email address")
    hashed_password: str = Field(..., min_length=6, description="User password")


class UserUpdate(BaseModel):
    """Schema for updating an existing user."""

    email: Optional[EmailStr] = Field(None, description="User email address")
    is_active: Optional[bool] = Field(None, description="User active status")


class UserResponse(BaseModel):
    """Schema for user response."""

    id: int = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email address")
    is_active: bool = Field(..., description="User active status")

    model_config = ConfigDict(from_attributes=True)  # pylint: disable=invalid-name
