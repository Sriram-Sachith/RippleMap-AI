"""Data export service for generating reports in various formats."""

import json
import csv
from io import StringIO, BytesIO
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataExportService:
    """Service for exporting data in various formats."""
    
    @staticmethod
    def to_json(data: Any, pretty: bool = True) -> str:
        """Export data as JSON."""
        try:
            if pretty:
                return json.dumps(data, indent=2, default=str)
            return json.dumps(data, default=str)
        except Exception as e:
            logger.error(f"Error converting to JSON: {str(e)}")
            raise
    
    @staticmethod
    def to_csv(data: List[Dict[str, Any]]) -> str:
        """Export data as CSV."""
        if not data:
            return ""
        
        try:
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            return output.getvalue()
        except Exception as e:
            logger.error(f"Error converting to CSV: {str(e)}")
            raise
    
    @staticmethod
    def to_geojson(features: List[Dict[str, Any]]) -> str:
        """Export data as GeoJSON."""
        try:
            geojson = {
                "type": "FeatureCollection",
                "features": features,
            }
            return json.dumps(geojson, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error converting to GeoJSON: {str(e)}")
            raise
    
    @staticmethod
    def scenario_result_to_dict(result: Any) -> Dict[str, Any]:
        """Convert scenario result to dictionary."""
        return {
            "id": result.id,
            "scenario_id": result.scenario_id,
            "affected_population": result.affected_population,
            "affected_facilities": result.affected_facilities,
            "critical_services_at_risk": result.critical_services_at_risk,
            "average_delay_minutes": result.average_delay_minutes,
            "detour_distance_km": result.detour_distance_km,
            "network_efficiency_reduction": result.network_efficiency_reduction,
            "accessibility_score_before": result.accessibility_score_before,
            "accessibility_score_after": result.accessibility_score_after,
            "population_with_reduced_access": result.population_with_reduced_access,
            "overall_risk_score": result.overall_risk_score,
            "vulnerability_score": result.vulnerability_score,
            "resilience_score": result.resilience_score,
            "created_at": result.created_at.isoformat() if result.created_at else None,
        }
    
    @staticmethod
    def facility_to_geojson_feature(facility: Any) -> Dict[str, Any]:
        """Convert facility to GeoJSON feature."""
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [facility.longitude, facility.latitude],  # GeoJSON uses [lon, lat]
            },
            "properties": {
                "id": facility.id,
                "name": facility.name,
                "type": facility.facility_type,
                "capacity": facility.capacity,
                "occupancy": facility.current_occupancy,
                "service_radius_km": facility.service_radius_km,
                "population_served": facility.population_served,
            },
        }
    
    @staticmethod
    def generate_summary_report(
        study_area: Any,
        scenario_results: List[Any],
    ) -> Dict[str, Any]:
        """Generate summary report from analysis."""
        if not scenario_results:
            avg_risk = 0
            avg_delay = 0
            total_affected = 0
        else:
            avg_risk = sum(r.overall_risk_score for r in scenario_results) / len(scenario_results)
            avg_delay = sum(r.average_delay_minutes for r in scenario_results) / len(scenario_results)
            total_affected = sum(r.affected_population for r in scenario_results)
        
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "study_area": {
                "id": study_area.id,
                "name": study_area.name,
                "area_km2": study_area.area_km2,
                "population": study_area.population,
            },
            "scenarios_analyzed": len(scenario_results),
            "summary_metrics": {
                "average_overall_risk_score": avg_risk,
                "average_delay_minutes": avg_delay,
                "total_population_affected": total_affected,
            },
            "scenarios": [
                DataExportService.scenario_result_to_dict(r)
                for r in scenario_results
            ],
        }
