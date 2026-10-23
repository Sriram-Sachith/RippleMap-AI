"""Audit logging models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class AuditLog(Base):
    """Audit log for tracking user actions."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # User information
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Action details
    action = Column(String(100), nullable=False, index=True)  # create, update, delete, view, etc.
    resource_type = Column(String(100), nullable=False)  # scenario, study_area, facility, etc.
    resource_id = Column(Integer, nullable=True)
    
    # Details
    details = Column(Text, nullable=True)  # JSON string with change details
    
    # IP and user agent
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    # Status
    status = Column(String(20), default="success")  # success, failure
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    class Config:
        from_attributes = True

    def __repr__(self) -> str:
        return f"<AuditLog {self.user_id} {self.action} {self.resource_type}>"
