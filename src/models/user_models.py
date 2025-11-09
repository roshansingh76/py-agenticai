from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserResponse(BaseModel):
    """Response model for user information"""
    user_id: str = Field(..., description="User identifier")
    email: Optional[str] = Field(None, description="User email address")
    username: Optional[str] = Field(None, description="Username")


class LoginRequest(BaseModel):
    """Request model for user login"""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="User password")


class LoginResponse(BaseModel):
    """Response model for login"""
    user_id: str = Field(..., description="User identifier")
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
