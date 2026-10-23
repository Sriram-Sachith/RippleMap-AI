"""Study area models for managing geographic regions."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from ..database import Base


class StudyArea(Base):
    """Geographic study area for analysis."""
    __tablename__ = "study_areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Geographic bounds (WGS84)
    bounds_geom = Column(Geometry("POLYGON", srid=4326), nullable=False)
    
    # Metrics
    area_km2 = Column(Float, nullable=False)
    population = Column(Integer, nullable=True)
    primary_facilities_count = Column(Integer, default=0)
    road_network_km = Column(Float, default=0.0)
    
    # Configuration
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    scenarios = relationship("Scenario", back_populates="study_area")
    population_data = relationship("PopulationDensity", back_populates="study_area")
    facilities = relationship("Facility", back_populates="study_area")
    road_network = relationship("RoadNetwork", back_populates="study_area")
    
    class Config:
        from_attributes = True

    def __repr__(self) -> str:
        return f"<StudyArea {self.name} ({self.area_km2} km²)>"
