"""Study area schemas."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from .common import BoundingBox


class StudyAreaCreate(BaseModel):
    """Study area creation schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    bounds: BoundingBox
    population: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "San Francisco Bay Area",
                "description": "Critical infrastructure analysis for Bay Area",
                "bounds": {
                    "southwest": {"latitude": 37.0, "longitude": -122.5},
                    "northeast": {"latitude": 38.0, "longitude": -121.5}
                },
                "population": 7_700_000
            }
        }


class StudyAreaResponse(BaseModel):
    """Study area response schema."""
    id: int
    name: str
    description: Optional[str]
    area_km2: float
    population: Optional[int]
    primary_facilities_count: int
    road_network_km: float
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "San Francisco Bay Area",
                "description": "Critical infrastructure analysis for Bay Area",
                "area_km2": 17662.0,
                "population": 7700000,
                "primary_facilities_count": 245,
                "road_network_km": 28450.5,
                "is_active": True,
                "created_at": "2026-10-22T10:00:00",
                "updated_at": "2026-10-22T10:00:00"
            }
        }


class StudyAreaUpdate(BaseModel):
    """Study area update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    population: Optional[int] = None
    is_active: Optional[bool] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Study Area",
                "population": 8_000_000
            }
        }


class StudyAreaWithMetrics(StudyAreaResponse):
    """Study area with additional analysis metrics."""
    average_population_density: float = Field(0.0, description="Population per km²")
    average_facility_coverage: float = Field(0.0, description="% of population with 5km facility access")
    network_efficiency_score: float = Field(0.0, description="0-100 network connectivity score")
