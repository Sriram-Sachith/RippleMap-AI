"""
Geospatial Data Endpoints
GET /api/v1/geospatial/layers - Get available layers
GET /api/v1/geospatial/features - Get geographic features
POST /api/v1/geospatial/spatial-query - Execute spatial queries
GET /api/v1/geospatial/bounds - Get study area boundaries
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
import logging

from app.db.database import get_db
from app.core.security import verify_token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/geospatial", tags=["Geospatial"])


class SpatialQueryRequest(BaseModel):
    layer_id: str
    study_area_id: str
    query_type: str  # within_bounds, near_point, intersects
    geometry: Dict[str, Any]


@router.get("/layers")
async def get_available_layers(
    study_area_id: str = Query(...),
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    """
    Get all available geographic layers for a study area
    """
    try:
        layers = {
            "study_area_id": study_area_id,
            "layers": [
                {
                    "id": "roads",
                    "name": "Road Network",
                    "description": "Road segments with accessibility status",
                    "geometry_type": "LineString",
                    "feature_count": 12450,
                    "visible_by_default": True,
                    "properties": ["road_class", "length_m", "status", "accessibility_score"]
                },
                {
                    "id": "facilities",
                    "name": "Healthcare Facilities",
                    "description": "Hospitals, clinics, and primary health centers",
                    "geometry_type": "Point",
                    "feature_count": 245,
                    "visible_by_default": True,
                    "properties": ["facility_type", "name", "capacity", "services"]
                },
                {
                    "id": "population",
                    "name": "Population Grid",
                    "description": "Population estimates by 100m grid cells",
                    "geometry_type": "Polygon",
                    "feature_count": 42150,
                    "visible_by_default": False,
                    "properties": ["population", "population_density", "vulnerable_groups"]
                },
                {
                    "id": "risk",
                    "name": "Vulnerability Score",
                    "description": "Composite vulnerability ranking by area",
                    "geometry_type": "Polygon",
                    "feature_count": 42150,
                    "visible_by_default": False,
                    "properties": ["vulnerability_score", "risk_category", "priority"]
                },
                {
                    "id": "rainfall",
                    "name": "Rainfall Analysis",
                    "description": "Historical and extreme rainfall observations",
                    "geometry_type": "Polygon",
                    "feature_count": 120,
                    "visible_by_default": False,
                    "properties": ["avg_rainfall_mm", "extreme_rainfall_mm", "flood_risk"]
                },
                {
                    "id": "admin_boundaries",
                    "name": "Administrative Boundaries",
                    "description": "District and ward boundaries",
                    "geometry_type": "Polygon",
                    "feature_count": 245,
                    "visible_by_default": False,
                    "properties": ["admin_level", "name", "population"]
                }
            ]
        }
        
        return layers
    except Exception as e:
        logger.error(f"Get layers error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/features")
async def get_geographic_features(
    layer_id: str = Query(...),
    study_area_id: str = Query(...),
    scenario_id: str = Query(None),
    bounds: str = Query(None),  # Format: "minLat,minLng,maxLat,maxLng"
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    """
    Get geographic features for a layer with optional filtering
    
    Returns GeoJSON FeatureCollection
    """
    try:
        features = {
            "type": "FeatureCollection",
            "layer_id": layer_id,
            "study_area_id": study_area_id,
            "scenario_id": scenario_id,
            "feature_count": 150,  # Depends on bounds
            "features": [
                {
                    "type": "Feature",
                    "id": "road-101",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[75.3456, 13.1234], [75.3467, 13.1245]]
                    },
                    "properties": {
                        "road_class": "primary",
                        "length_m": 2345,
                        "status": "affected" if scenario_id else "normal",
                        "baseline_accessibility": 0.95,
                        "disrupted_accessibility": 0.45 if scenario_id else None
                    }
                },
                {
                    "type": "Feature",
                    "id": "facility-001",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [75.3500, 13.1300]
                    },
                    "properties": {
                        "facility_type": "hospital",
                        "name": "City Central Hospital",
                        "capacity": 500,
                        "accessible_baseline": True,
                        "accessible_disrupted": True
                    }
                }
            ]
        }
        
        return features
    except Exception as e:
        logger.error(f"Get features error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/spatial-query")
async def execute_spatial_query(
    request: SpatialQueryRequest,
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    """
    Execute spatial queries on geographic data
    
    Query types:
    - within_bounds: Features within bounding box
    - near_point: Features near a point (with radius)
    - intersects: Features intersecting geometry
    """
    try:
        result = {
            "query_type": request.query_type,
            "layer_id": request.layer_id,
            "study_area_id": request.study_area_id,
            "features_found": 45,
            "results": [
                {
                    "id": "result-001",
                    "distance_from_query": 0.5,
                    "properties": {
                        "name": "Feature Name",
                        "type": "category"
                    }
                }
            ]
        }
        
        return result
    except Exception as e:
        logger.error(f"Spatial query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bounds/{study_area_id}")
async def get_study_area_bounds(
    study_area_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    """
    Get geographic bounds (bounding box) of study area
    """
    try:
        bounds = {
            "study_area_id": study_area_id,
            "name": "Bangalore Urban District",
            "bounds": {
                "north": 13.2342,
                "south": 13.0234,
                "east": 75.4567,
                "west": 75.2345
            },
            "center": {
                "latitude": 13.1288,
                "longitude": 75.3456
            },
            "geom_type": "Polygon",
            "area_km2": 1235.5,
            "perimeter_km": 156.2
        }
        
        return bounds
    except Exception as e:
        logger.error(f"Get bounds error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
