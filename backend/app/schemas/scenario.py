"""Scenario schemas."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from ..models.scenario import ScenarioStatus


class ScenarioCreate(BaseModel):
    """Scenario creation schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    study_area_id: int
    disruption_type: str = Field(..., min_length=1, max_length=50)
    severity_level: int = Field(1, ge=1, le=5)
    affected_roads: List[int] = Field(default_factory=list)
    duration_minutes: int = Field(60, ge=1, le=10080)  # Max 1 week
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Bay Bridge Closure Scenario",
                "description": "Analysis of Bay Bridge complete closure for 4 hours",
                "study_area_id": 1,
                "disruption_type": "road_closure",
                "severity_level": 5,
                "affected_roads": [101, 102, 103],
                "duration_minutes": 240
            }
        }


class ScenarioResponse(BaseModel):
    """Scenario response schema."""
    id: int
    name: str
    description: Optional[str]
    study_area_id: int
    disruption_type: str
    severity_level: int
    status: ScenarioStatus
    duration_minutes: int
    affected_roads: List[int]
    created_at: datetime
    updated_at: datetime
    execution_started: Optional[datetime] = None
    execution_completed: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 42,
                "name": "Bay Bridge Closure Scenario",
                "description": "Analysis of Bay Bridge complete closure for 4 hours",
                "study_area_id": 1,
                "disruption_type": "road_closure",
                "severity_level": 5,
                "status": "completed",
                "duration_minutes": 240,
                "affected_roads": [101, 102, 103],
                "created_at": "2026-10-22T10:00:00",
                "updated_at": "2026-10-22T10:15:30",
                "execution_started": "2026-10-22T10:05:00",
                "execution_completed": "2026-10-22T10:15:30"
            }
        }


class ScenarioUpdate(BaseModel):
    """Scenario update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    severity_level: Optional[int] = Field(None, ge=1, le=5)
    affected_roads: Optional[List[int]] = None
    duration_minutes: Optional[int] = Field(None, ge=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "severity_level": 4,
                "duration_minutes": 180
            }
        }


class ScenarioResultResponse(BaseModel):
    """Scenario result response schema."""
    id: int
    scenario_id: int
    affected_population: int
    affected_facilities: int
    critical_services_at_risk: int
    average_delay_minutes: float
    detour_distance_km: float
    network_efficiency_reduction: float
    accessibility_score_before: float
    accessibility_score_after: float
    population_with_reduced_access: int
    overall_risk_score: float
    vulnerability_score: float
    resilience_score: float
    recommendations: List[str]
    execution_duration_seconds: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "scenario_id": 42,
                "affected_population": 245_000,
                "affected_facilities": 18,
                "critical_services_at_risk": 4,
                "average_delay_minutes": 28.5,
                "detour_distance_km": 12.3,
                "network_efficiency_reduction": 34.2,
                "accessibility_score_before": 95.0,
                "accessibility_score_after": 67.3,
                "population_with_reduced_access": 145_000,
                "overall_risk_score": 78.5,
                "vulnerability_score": 72.1,
                "resilience_score": 68.9,
                "recommendations": [
                    "Deploy emergency response from local fire stations",
                    "Establish alternative routing via 101 North",
                    "Increase transit service frequency"
                ],
                "execution_duration_seconds": 42.3,
                "created_at": "2026-10-22T10:15:30"
            }
        }


class ScenarioExecutionRequest(BaseModel):
    """Request to execute a scenario analysis."""
    include_recommendations: bool = True
    detailed_output: bool = False
    
    class Config:
        json_schema_extra = {
            "example": {
                "include_recommendations": True,
                "detailed_output": False
            }
        }
