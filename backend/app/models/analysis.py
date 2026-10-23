"""Analysis result models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean, JSON

from ..database import Base


class RiskAnalysis(Base):
    """Risk analysis results."""
    __tablename__ = "risk_analyses"

    id = Column(Integer, primary_key=True, index=True)
    
    # References (flexible foreign keys for different entity types)
    study_area_id = Column(Integer, nullable=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=True, index=True)
    
    # Risk metrics
    hazard_score = Column(Float, default=0.0)  # 0-100
    exposure_score = Column(Float, default=0.0)  # 0-100
    vulnerability_score = Column(Float, default=0.0)  # 0-100
    overall_risk = Column(Float, default=0.0)  # 0-100
    
    # Risk categories
    critical_risks = Column(JSON, default=[])  # List of critical risk areas
    moderate_risks = Column(JSON, default=[])
    low_risks = Column(JSON, default=[])
    
    # Affected entities
    affected_population = Column(Integer, default=0)
    affected_facilities = Column(Integer, default=0)
    affected_roads_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    class Config:
        from_attributes = True


class VulnerabilityScore(Base):
    """Vulnerability scoring for different asset types."""
    __tablename__ = "vulnerability_scores"

    id = Column(Integer, primary_key=True, index=True)
    
    # Entity reference
    entity_type = Column(String(50), nullable=False)  # facility, population_grid, road_network
    entity_id = Column(Integer, nullable=False)
    
    # Vulnerability factors
    physical_vulnerability = Column(Float, default=0.0)  # 0-100
    social_vulnerability = Column(Float, default=0.0)   # 0-100
    economic_vulnerability = Column(Float, default=0.0) # 0-100
    infrastructure_vulnerability = Column(Float, default=0.0)  # 0-100
    
    # Overall scores
    overall_vulnerability = Column(Float, default=0.0)  # 0-100
    vulnerability_category = Column(String(20), default="moderate")  # low, moderate, high, critical
    
    # Ranking
    percentile_rank = Column(Float, default=0.0)  # 0-100
    priority_level = Column(Integer, default=3)  # 1 (highest) to 5 (lowest)
    
    # Contributing factors
    contributing_factors = Column(JSON, default=[])  # List of main vulnerability drivers
    mitigation_recommendations = Column(JSON, default=[])
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    class Config:
        from_attributes = True


class AccessibilityMetrics(Base):
    """Accessibility metrics for essential services."""
    __tablename__ = "accessibility_metrics"

    id = Column(Integer, primary_key=True, index=True)
    
    # Entity reference
    population_grid_id = Column(Integer, nullable=False)
    facility_id = Column(Integer, nullable=False)
    
    # Distance metrics
    network_distance_km = Column(Float, nullable=False)
    euclidean_distance_km = Column(Float, nullable=False)
    
    # Time metrics
    travel_time_minutes = Column(Float, nullable=False)
    
    # Accessibility scoring
    is_accessible = Column(Boolean, default=True)
    accessibility_score = Column(Float, default=100.0)  # 0-100
    
    # Baseline and disrupted scenario
    baseline_travel_time = Column(Float, nullable=False)
    disrupted_travel_time = Column(Float, nullable=True)
    travel_time_increase_percentage = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    class Config:
        from_attributes = True
