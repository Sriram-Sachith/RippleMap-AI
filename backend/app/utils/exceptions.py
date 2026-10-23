"""Custom exception classes."""

from fastapi import HTTPException, status
from typing import Optional, Dict, Any


class RippleMapException(Exception):
    """Base exception for RippleMap application."""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Optional[str] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail or message
        super().__init__(self.message)


class NotFoundError(RippleMapException):
    """Resource not found error."""
    
    def __init__(self, resource: str, resource_id: Any = None):
        message = f"{resource} not found"
        if resource_id:
            message += f" (ID: {resource_id})"
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class ValidationError(RippleMapException):
    """Validation error."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        full_message = message
        if field:
            full_message = f"Validation error in {field}: {message}"
        super().__init__(full_message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UnauthorizedError(RippleMapException):
    """Unauthorized access error."""
    
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(RippleMapException):
    """Forbidden access error."""
    
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)


class ConflictError(RippleMapException):
    """Conflict error (e.g., duplicate resource)."""
    
    def __init__(self, message: str, resource: Optional[str] = None):
        full_message = message
        if resource:
            full_message = f"{resource}: {message}"
        super().__init__(full_message, status_code=status.HTTP_409_CONFLICT)


class AnalysisError(RippleMapException):
    """Error during analysis execution."""
    
    def __init__(self, message: str, scenario_id: Optional[int] = None):
        full_message = message
        if scenario_id:
            full_message = f"Analysis error for scenario {scenario_id}: {message}"
        super().__init__(full_message, status_code=status.HTTP_400_BAD_REQUEST)


class DatabaseError(RippleMapException):
    """Database operation error."""
    
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExternalServiceError(RippleMapException):
    """Error communicating with external service."""
    
    def __init__(self, service: str, message: str):
        full_message = f"Error from {service}: {message}"
        super().__init__(full_message, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
