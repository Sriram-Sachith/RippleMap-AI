"""Scenario models for disruption analysis."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum, ForeignKey, Float, Boolean, JSON
from sqlalchemy.orm import relationship

from ..database import Base


class ScenarioStatus(str, Enum):
    """Scenario status enumeration."""
    DRAFT = "draft"
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


class Scenario(Base):
    """Disruption scenario for analysis."""
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Foreign keys
    study_area_id = Column(Integer, ForeignKey("study_areas.id"), nullable=False, index=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Scenario configuration
    disruption_type = Column(String(50), nullable=False)  # road_closure, accident, flooding, etc.
    severity_level = Column(Integer, default=1)  # 1-5
    affected_roads = Column(JSON, default=[])  # List of road IDs or coordinates
    
    # Status
    status = Column(SQLEnum(ScenarioStatus), default=ScenarioStatus.DRAFT, nullable=False, index=True)
    
    # Duration
    duration_minutes = Column(Integer, default=60)  # Expected duration of disruption
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    execution_started = Column(DateTime, nullable=True)
    execution_completed = Column(DateTime, nullable=True)
    
    # Relationships
    study_area = relationship("StudyArea", back_populates="scenarios")
    created_by = relationship("User", back_populates="scenarios", foreign_keys=[created_by_id])
    results = relationship("ScenarioResult", back_populates="scenario", cascade="all, delete-orphan")
    
    class Config:
        from_attributes = True

    def __repr__(self) -> str:
        return f"<Scenario {self.name} ({self.status})>"


class ScenarioResult(Base):
    """Results from scenario analysis execution."""
    __tablename__ = "scenario_results"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False, index=True)
    
    # Impact metrics
    affected_population = Column(Integer, default=0)
    affected_facilities = Column(Integer, default=0)
    critical_services_at_risk = Column(Integer, default=0)
    
    # Network metrics
    average_delay_minutes = Column(Float, default=0.0)
    detour_distance_km = Column(Float, default=0.0)
    network_efficiency_reduction = Column(Float, default=0.0)  # Percentage
    
    # Accessibility
    accessibility_score_before = Column(Float, default=0.0)  # 0-100
    accessibility_score_after = Column(Float, default=0.0)   # 0-100
    population_with_reduced_access = Column(Integer, default=0)
    
    # Risk
    overall_risk_score = Column(Float, default=0.0)  # 0-100
    vulnerability_score = Column(Float, default=0.0)  # 0-100
    resilience_score = Column(Float, default=0.0)    # 0-100
    
    # Recommendations
    recommendations = Column(JSON, default=[])  # List of intervention recommendations
    
    # Execution details
    execution_duration_seconds = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    scenario = relationship("Scenario", back_populates="results")
    
    class Config:
        from_attributes = True

    def __repr__(self) -> str:
        return f"<ScenarioResult scenario_id={self.scenario_id} score={self.overall_risk_score}>"
