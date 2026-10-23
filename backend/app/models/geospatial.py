"""Geospatial data models."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from ..database import Base


class PopulationDensity(Base):
    """Population density grid data."""
    __tablename__ = "population_density"

    id = Column(Integer, primary_key=True, index=True)
    study_area_id = Column(Integer, ForeignKey("study_areas.id"), nullable=False, index=True)
    
    # Geometry (grid cells)
    geom = Column(Geometry("POLYGON", srid=4326), nullable=False, spatialindex=True)
    
    # Population data
    population_count = Column(Integer, default=0)
    density_per_km2 = Column(Float, default=0.0)
    
    # Demographics
    vulnerable_population = Column(Integer, default=0)  # Children, elderly, disabled
    vulnerable_percentage = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    study_area = relationship("StudyArea", back_populates="population_data")
    
    class Config:
        from_attributes = True


class Facility(Base):
    """Critical facility (hospital, fire station, police, etc.)."""
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    study_area_id = Column(Integer, ForeignKey("study_areas.id"), nullable=False, index=True)
    
    # Basic info
    name = Column(String(255), nullable=False, index=True)
    facility_type = Column(String(50), nullable=False, index=True)  # hospital, fire_station, police, school, etc.
    
    # Location
    geom = Column(Geometry("POINT", srid=4326), nullable=False, spatialindex=True)
    address = Column(String(500), nullable=True)
    
    # Capacity
    capacity = Column(Integer, nullable=True)
    current_occupancy = Column(Integer, default=0)
    
    # Coverage
    service_radius_km = Column(Float, default=5.0)
    population_served = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    study_area = relationship("StudyArea", back_populates="facilities")
    
    class Config:
        from_attributes = True

    def __repr__(self) -> str:
        return f"<Facility {self.name} ({self.facility_type})>"


class RoadNetwork(Base):
    """Road network segments for routing analysis."""
    __tablename__ = "road_network"

    id = Column(Integer, primary_key=True, index=True)
    study_area_id = Column(Integer, ForeignKey("study_areas.id"), nullable=False, index=True)
    
    # Geometry
    geom = Column(Geometry("LINESTRING", srid=4326), nullable=False, spatialindex=True)
    
    # Road properties
    road_name = Column(String(255), nullable=True)
    road_type = Column(String(50), nullable=False)  # highway, primary, secondary, tertiary
    surface_type = Column(String(50), nullable=True)  # asphalt, gravel, dirt
    
    # Network properties
    length_km = Column(Float, nullable=False)
    speed_limit_kmh = Column(Integer, default=50)
    lanes = Column(Integer, default=2)
    
    # Importance
    criticality_score = Column(Float, default=0.0)  # 0-100
    connectivity_index = Column(Float, default=0.0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_disrupted = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    study_area = relationship("StudyArea", back_populates="road_network")
    
    class Config:
        from_attributes = True

    def __repr__(self) -> str:
        return f"<RoadNetwork {self.road_name} ({self.length_km} km)>"
