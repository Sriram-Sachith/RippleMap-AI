"""Geospatial schemas."""

from typing import Optional, List
from pydantic import BaseModel, Field

from .common import LocationPoint, BoundingBox


class PopulationDensityResponse(BaseModel):
    """Population density response schema."""
    id: int
    study_area_id: int
    population_count: int
    density_per_km2: float
    vulnerable_population: int
    vulnerable_percentage: float
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "study_area_id": 1,
                "population_count": 5420,
                "density_per_km2": 2710.0,
                "vulnerable_population": 542,
                "vulnerable_percentage": 10.0
            }
        }


class FacilityCreate(BaseModel):
    """Facility creation schema."""
    name: str = Field(..., min_length=1, max_length=255)
    facility_type: str = Field(..., regex="^(hospital|fire_station|police|school|water_treatment|power_plant)$")
    location: LocationPoint
    address: Optional[str] = None
    capacity: Optional[int] = None
    current_occupancy: int = 0
    service_radius_km: float = Field(5.0, ge=0.5, le=50.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "UCSF Medical Center",
                "facility_type": "hospital",
                "location": {"latitude": 37.7625, "longitude": -122.4508},
                "address": "505 Parnassus Ave, San Francisco, CA 94143",
                "capacity": 700,
                "current_occupancy": 580,
                "service_radius_km": 10.0
            }
        }


class FacilityResponse(BaseModel):
    """Facility response schema."""
    id: int
    name: str
    facility_type: str
    address: Optional[str]
    capacity: Optional[int]
    current_occupancy: int
    service_radius_km: float
    population_served: int
    is_active: bool
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "UCSF Medical Center",
                "facility_type": "hospital",
                "address": "505 Parnassus Ave, San Francisco, CA 94143",
                "capacity": 700,
                "current_occupancy": 580,
                "service_radius_km": 10.0,
                "population_served": 245_000,
                "is_active": True
            }
        }


class RoadNetworkResponse(BaseModel):
    """Road network response schema."""
    id: int
    study_area_id: int
    road_name: Optional[str]
    road_type: str
    surface_type: Optional[str]
    length_km: float
    speed_limit_kmh: int
    lanes: int
    criticality_score: float
    connectivity_index: float
    is_active: bool
    is_disrupted: bool
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 101,
                "study_area_id": 1,
                "road_name": "Bay Bridge",
                "road_type": "highway",
                "surface_type": "asphalt",
                "length_km": 4.5,
                "speed_limit_kmh": 80,
                "lanes": 4,
                "criticality_score": 95.0,
                "connectivity_index": 0.92,
                "is_active": True,
                "is_disrupted": False
            }
        }


class SpatialQueryRequest(BaseModel):
    """Spatial query request."""
    query_type: str = Field(..., regex="^(intersection|within|contains|distance)$")
    bounds: BoundingBox
    resource_types: List[str] = Field(default_factory=list)  # facilities, roads, population, etc.
    
    class Config:
        json_schema_extra = {
            "example": {
                "query_type": "within",
                "bounds": {
                    "southwest": {"latitude": 37.0, "longitude": -122.5},
                    "northeast": {"latitude": 38.0, "longitude": -121.5}
                },
                "resource_types": ["facilities", "roads", "population"]
            }
        }


class LayerResponse(BaseModel):
    """GIS layer metadata and features."""
    layer_id: str
    layer_name: str
    layer_type: str  # facilities, roads, population, terrain, etc.
    feature_count: int
    bounds: BoundingBox
    style_config: dict = Field(default_factory=dict)
    is_visible: bool = True
    opacity: float = Field(1.0, ge=0.0, le=1.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "layer_id": "hospitals_001",
                "layer_name": "Hospitals",
                "layer_type": "facilities",
                "feature_count": 42,
                "bounds": {
                    "southwest": {"latitude": 37.0, "longitude": -122.5},
                    "northeast": {"latitude": 38.0, "longitude": -121.5}
                },
                "style_config": {
                    "color": "#FF0000",
                    "icon": "hospital"
                },
                "is_visible": True,
                "opacity": 1.0
            }
        }
