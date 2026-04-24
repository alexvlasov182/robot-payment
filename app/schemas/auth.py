"""Main file fot the Auth Schemas"""

from pydantic import BaseModel, EmailStr  # type: ignore[reportMissingImports]  # pylint: disable=import-error


class UserRegister(BaseModel):
    """Schema for the User Regestration"""

    email: EmailStr
    password: str
    confirm_password: str


class UserLogin(BaseModel):
    """Shema for the User Login"""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for the Token"""

    access_token: str
    token_type: str = "bearer"
