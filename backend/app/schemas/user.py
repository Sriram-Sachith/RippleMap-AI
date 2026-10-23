"""User schemas."""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from ..models.user import UserRole


class UserCreate(BaseModel):
    """User creation schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=255)
    full_name: Optional[str] = None
    role: UserRole = UserRole.VIEWER
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "analyst@ripplemap.ai",
                "username": "john_analyst",
                "password": "SecurePassword123!",
                "full_name": "John Analyst",
                "role": "analyst"
            }
        }


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    email: str
    username: str
    full_name: Optional[str]
    role: UserRole
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "analyst@ripplemap.ai",
                "username": "john_analyst",
                "full_name": "John Analyst",
                "role": "analyst",
                "is_active": True,
                "created_at": "2026-10-22T10:30:00",
                "last_login": "2026-10-22T14:00:00"
            }
        }


class UserUpdate(BaseModel):
    """User update schema."""
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Updated",
                "role": "analyst"
            }
        }


class TokenResponse(BaseModel):
    """Token response."""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600,
                "user": {}
            }
        }
