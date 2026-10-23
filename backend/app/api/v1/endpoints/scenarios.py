"""
Scenario management endpoints
POST /api/v1/scenarios - Create scenario
GET /api/v1/scenarios - List scenarios
GET /api/v1/scenarios/{id} - Get scenario
PATCH /api/v1/scenarios/{id} - Update scenario
POST /api/v1/scenarios/{id}/run - Execute scenario simulation
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import logging

from app.db.database import get_db
from app.schemas.scenario import (
    ScenarioCreate,
    ScenarioUpdate,
    ScenarioResponse,
    ScenarioRunRequest
)
from app.models.scenario import Scenario
from app.services.simulation_engine import SimulationEngine
from app.core.security import verify_token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/scenarios", tags=["Scenarios"])


@router.post("", response_model=ScenarioResponse)
async def create_scenario(
    scenario: ScenarioCreate,
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    """
    Create a new disruption scenario
    
    Parameters:
    - study_area_id: ID of the study area
    - name: Scenario name
    - scenario_type: 'road_closure', 'flooding', etc.
    - affected_road_ids: List of road segment IDs
    - parameters: Additional simulation parameters
    """
    try:
        db_scenario = Scenario(
            study_area_id=scenario.study_area_id,
            owner_id=current_user.id,
            name=scenario.name,
            scenario_type=scenario.scenario_type,
            affected_road_ids=scenario.affected_road_ids,
            parameters=scenario.parameters,
            status="draft",
            created_at=datetime.utcnow()
        )
        db.add(db_scenario)
        db.commit()
        db.refresh(db_scenario)
        logger.info(f"Scenario created: {db_scenario.id}")
        return db_scenario
    except Exception as e:
        logger.error(f"Error creating scenario: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create scenario")


@router.get("", response_model=List[ScenarioResponse])
async def list_scenarios(
    study_area_id: str = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    """
    List all scenarios for a study area
    """
    scenarios = db.query(Scenario).filter(
        Scenario.study_area_id == study_area_id,
        Scenario.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return scenarios


@router.get("/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(
    scenario_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    """
    Retrieve a specific scenario
    """
    scenario = db.query(Scenario).filter(
        Scenario.id == scenario_id,
        Scenario.owner_id == current_user.id
    ).first()
    
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario


@router.patch("/{scenario_id}", response_model=ScenarioResponse)
async def update_scenario(
    scenario_id: str,
    updates: ScenarioUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    """
    Update a scenario (draft only)
    """
    scenario = db.query(Scenario).filter(
        Scenario.id == scenario_id,
        Scenario.owner_id == current_user.id
    ).first()
    
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    if scenario.status != "draft":
        raise HTTPException(status_code=400, detail="Can only update draft scenarios")
    
    update_data = updates.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(scenario, field, value)
    
    db.commit()
    db.refresh(scenario)
    return scenario


@router.post("/{scenario_id}/run")
async def run_scenario(
    scenario_id: str,
    request: ScenarioRunRequest,
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    """
    Execute a scenario simulation
    Returns job ID for async processing
    """
    scenario = db.query(Scenario).filter(
        Scenario.id == scenario_id,
        Scenario.owner_id == current_user.id
    ).first()
    
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    try:
        # Queue simulation job
        simulation_engine = SimulationEngine()
        job_id = await simulation_engine.queue_simulation(
            scenario_id=scenario.id,
            parameters=request.parameters
        )
        
        logger.info(f"Simulation queued: {job_id}")
        return {
            "job_id": job_id,
            "scenario_id": scenario.id,
            "status": "queued"
        }
    except Exception as e:
        logger.error(f"Error running simulation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to run simulation")
