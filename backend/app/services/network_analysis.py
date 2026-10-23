"""Advanced network analysis algorithms."""

import networkx as nx
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class NetworkAnalyzer:
    """Analyzer for road network connectivity and efficiency."""
    
    def __init__(self):
        """Initialize network analyzer."""
        self.graph = nx.MultiDiGraph()
    
    def add_road(
        self,
        road_id: int,
        from_node: Tuple[float, float],
        to_node: Tuple[float, float],
        length_km: float,
        speed_limit: int = 50,
        criticality: float = 0.5,
    ) -> None:
        """
        Add a road segment to the network.
        
        Args:
            road_id: Unique road identifier
            from_node: Starting coordinates (lat, lon)
            to_node: Ending coordinates (lat, lon)
            length_km: Road length in kilometers
            speed_limit: Speed limit in km/h
            criticality: Criticality score (0-1)
        """
        travel_time_min = (length_km / speed_limit) * 60  # Convert to minutes
        
        self.graph.add_edge(
            from_node,
            to_node,
            road_id=road_id,
            length_km=length_km,
            travel_time_min=travel_time_min,
            speed_limit=speed_limit,
            criticality=criticality,
        )
    
    def calculate_shortest_path(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        metric: str = "travel_time_min",
    ) -> Tuple[List[Tuple[float, float]], float]:
        """
        Calculate shortest path between two points.
        
        Args:
            start: Starting coordinates (lat, lon)
            end: Ending coordinates (lat, lon)
            metric: Weight metric ('travel_time_min' or 'length_km')
        
        Returns:
            Tuple of (path nodes, total distance/time)
        """
        try:
            path = nx.shortest_path(
                self.graph,
                start,
                end,
                weight=metric,
            )
            total_weight = nx.shortest_path_length(
                self.graph,
                start,
                end,
                weight=metric,
            )
            return path, total_weight
        except nx.NetworkXNoPath:
            logger.warning(f"No path found between {start} and {end}")
            return [], 0
    
    def find_alternative_routes(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        num_routes: int = 3,
    ) -> List[Dict[str, any]]:
        """
        Find multiple alternative routes.
        
        Args:
            start: Starting coordinates
            end: Ending coordinates
            num_routes: Number of alternative routes to find
        
        Returns:
            List of route dictionaries with path, distance, and time
        """
        try:
            paths = []
            for i in range(num_routes):
                try:
                    path = nx.shortest_path(
                        self.graph,
                        start,
                        end,
                        weight="travel_time_min",
                    )
                    length = sum(
                        self.graph[path[j]][path[j+1]][0].get("length_km", 0)
                        for j in range(len(path) - 1)
                    )
                    travel_time = nx.shortest_path_length(
                        self.graph,
                        start,
                        end,
                        weight="travel_time_min",
                    )
                    
                    paths.append({
                        "route_number": i + 1,
                        "path": path,
                        "distance_km": length,
                        "travel_time_minutes": travel_time,
                    })
                except nx.NetworkXNoPath:
                    break
            
            return paths
        except Exception as e:
            logger.error(f"Error finding alternative routes: {str(e)}")
            return []
    
    def identify_critical_roads(
        self,
        threshold: float = 0.7,
    ) -> List[Dict[str, any]]:
        """
        Identify critical roads that would cause significant disruption if closed.
        
        Args:
            threshold: Criticality threshold (0-1)
        
        Returns:
            List of critical roads with impact scores
        """
        critical_roads = []
        
        for u, v, key, data in self.graph.edges(keys=True, data=True):
            criticality = data.get("criticality", 0)
            if criticality >= threshold:
                critical_roads.append({
                    "road_id": data.get("road_id"),
                    "from": u,
                    "to": v,
                    "length_km": data.get("length_km", 0),
                    "criticality_score": criticality,
                })
        
        # Sort by criticality
        critical_roads.sort(key=lambda x: x["criticality_score"], reverse=True)
        return critical_roads
    
    def calculate_network_resilience(self) -> Dict[str, any]:
        """
        Calculate overall network resilience metrics.
        
        Returns:
            Dictionary with resilience metrics
        """
        num_nodes = self.graph.number_of_nodes()
        num_edges = self.graph.number_of_edges()
        
        if num_nodes < 2:
            return {"resilience_score": 0, "connectivity": 0}
        
        try:
            # Calculate connectivity coefficient
            strongly_connected_components = nx.number_strongly_connected_components(self.graph)
            connectivity = num_nodes / (strongly_connected_components + 1) if strongly_connected_components else 0
            
            # Normalize connectivity to 0-1 range
            connectivity_normalized = min(connectivity / num_nodes, 1.0)
            
            # Calculate density (how interconnected the network is)
            density = nx.density(self.graph)
            
            # Combined resilience score
            resilience_score = (connectivity_normalized * 0.6) + (density * 0.4)
            
            return {
                "resilience_score": round(resilience_score * 100, 2),
                "connectivity": round(connectivity_normalized * 100, 2),
                "network_density": round(density * 100, 2),
                "nodes": num_nodes,
                "edges": num_edges,
            }
        except Exception as e:
            logger.error(f"Error calculating resilience: {str(e)}")
            return {"resilience_score": 0, "connectivity": 0}
    
    def simulate_disruption(
        self,
        disrupted_roads: List[int],
    ) -> Dict[str, any]:
        """
        Simulate network disruption by removing specified roads.
        
        Args:
            disrupted_roads: List of road IDs to disrupt
        
        Returns:
            Impact assessment including affected paths and detours
        """
        # Create a copy of the graph for simulation
        temp_graph = self.graph.copy()
        
        # Remove disrupted roads
        removed_count = 0
        for u, v, key, data in list(temp_graph.edges(keys=True, data=True)):
            if data.get("road_id") in disrupted_roads:
                temp_graph.remove_edge(u, v, key)
                removed_count += 1
        
        # Calculate impact
        original_edges = self.graph.number_of_edges()
        remaining_edges = temp_graph.number_of_edges()
        
        return {
            "roads_disrupted": removed_count,
            "network_efficiency_reduction": ((original_edges - remaining_edges) / original_edges * 100) if original_edges > 0 else 0,
            "remaining_connectivity": nx.density(temp_graph) if temp_graph.number_of_edges() > 0 else 0,
        }
