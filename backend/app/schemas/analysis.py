"""Analysis schemas."""

from typing import Optional, List
from pydantic import BaseModel, Field


class RiskAnalysisResponse(BaseModel):
    """Risk analysis response schema."""
    id: int
    study_area_id: Optional[int]
    scenario_id: Optional[int]
    hazard_score: float = Field(..., ge=0, le=100)
    exposure_score: float = Field(..., ge=0, le=100)
    vulnerability_score: float = Field(..., ge=0, le=100)
    overall_risk: float = Field(..., ge=0, le=100)
    affected_population: int
    affected_facilities: int
    affected_roads_count: int
    critical_risks: List[dict]
    moderate_risks: List[dict]
    low_risks: List[dict]
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "study_area_id": 1,
                "scenario_id": None,
                "hazard_score": 85.0,
                "exposure_score": 72.0,
                "vulnerability_score": 68.0,
                "overall_risk": 75.0,
                "affected_population": 245_000,
                "affected_facilities": 18,
                "affected_roads_count": 12,
                "critical_risks": [
                    {
                        "location": "Bay Bridge",
                        "type": "critical_route_closure",
                        "potential_impact": "245000 people isolated"
                    }
                ],
                "moderate_risks": [],
                "low_risks": []
            }
        }


class VulnerabilityScoreResponse(BaseModel):
    """Vulnerability score response schema."""
    id: int
    entity_type: str
    entity_id: int
    physical_vulnerability: float = Field(..., ge=0, le=100)
    social_vulnerability: float = Field(..., ge=0, le=100)
    economic_vulnerability: float = Field(..., ge=0, le=100)
    infrastructure_vulnerability: float = Field(..., ge=0, le=100)
    overall_vulnerability: float = Field(..., ge=0, le=100)
    vulnerability_category: str  # low, moderate, high, critical
    percentile_rank: float = Field(..., ge=0, le=100)
    priority_level: int = Field(..., ge=1, le=5)
    contributing_factors: List[str]
    mitigation_recommendations: List[str]
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "entity_type": "facility",
                "entity_id": 5,
                "physical_vulnerability": 45.0,
                "social_vulnerability": 62.0,
                "economic_vulnerability": 58.0,
                "infrastructure_vulnerability": 71.0,
                "overall_vulnerability": 59.0,
                "vulnerability_category": "high",
                "percentile_rank": 78.5,
                "priority_level": 2,
                "contributing_factors": [
                    "Located in flood zone",
                    "Limited backup power",
                    "High dependent population"
                ],
                "mitigation_recommendations": [
                    "Install emergency backup generator",
                    "Implement flood mitigation measures",
                    "Establish evacuation protocols"
                ]
            }
        }


class AccessibilityMetricsResponse(BaseModel):
    """Accessibility metrics response schema."""
    id: int
    population_grid_id: int
    facility_id: int
    network_distance_km: float
    euclidean_distance_km: float
    travel_time_minutes: float
    is_accessible: bool
    accessibility_score: float = Field(..., ge=0, le=100)
    baseline_travel_time: float
    disrupted_travel_time: Optional[float]
    travel_time_increase_percentage: float
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "population_grid_id": 42,
                "facility_id": 5,
                "network_distance_km": 3.2,
                "euclidean_distance_km": 2.8,
                "travel_time_minutes": 8.5,
                "is_accessible": True,
                "accessibility_score": 92.0,
                "baseline_travel_time": 8.5,
                "disrupted_travel_time": 24.3,
                "travel_time_increase_percentage": 185.9
            }
        }


class AccessibilityReportRequest(BaseModel):
    """Request for accessibility report generation."""
    study_area_id: int
    facility_type: Optional[str] = None
    include_baseline: bool = True
    include_scenario_comparison: bool = False
    scenario_id: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "study_area_id": 1,
                "facility_type": "hospital",
                "include_baseline": True,
                "include_scenario_comparison": True,
                "scenario_id": 42
            }
        }
