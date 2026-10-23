"""User and authentication models."""

from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import Column, String, DateTime, Boolean, Enum as SQLEnum, Integer
from sqlalchemy.orm import relationship

from ..database import Base


class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


class User(Base):
    """User model for authentication and authorization."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    scenarios = relationship("Scenario", back_populates="created_by", foreign_keys="Scenario.created_by_id")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    class Config:
        from_attributes = True

    def __repr__(self) -> str:
        return f"<User {self.username} ({self.role})>"
