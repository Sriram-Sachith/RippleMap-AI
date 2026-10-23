"""Common Pydantic schemas."""

from typing import Generic, TypeVar, List, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination parameters."""
    skip: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=1000)
    sort_by: Optional[str] = None
    sort_order: str = Field("asc", regex="^(asc|desc)$")


class StandardResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {},
                "message": "Operation completed successfully"
            }
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response with metadata."""
    success: bool = True
    data: List[T]
    pagination: dict = Field(default_factory=dict)
    message: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": [],
                "pagination": {
                    "total": 100,
                    "skip": 0,
                    "limit": 10,
                    "total_pages": 10
                },
                "message": "Data retrieved successfully"
            }
        }


class ErrorResponse(BaseModel):
    """Error response."""
    success: bool = False
    error: str
    detail: Optional[str] = None
    status_code: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Not found",
                "detail": "Resource not found",
                "status_code": 404
            }
        }


class LocationPoint(BaseModel):
    """Geographic point (latitude, longitude)."""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    
    class Config:
        json_schema_extra = {
            "example": {
                "latitude": 37.7749,
                "longitude": -122.4194
            }
        }


class BoundingBox(BaseModel):
    """Geographic bounding box (southwest to northeast)."""
    southwest: LocationPoint
    northeast: LocationPoint
    
    class Config:
        json_schema_extra = {
            "example": {
                "southwest": {"latitude": 37.0, "longitude": -122.5},
                "northeast": {"latitude": 38.0, "longitude": -121.5}
            }
        }
