"""
Geospatial simulation engine
Handles disruption simulation and accessibility calculations
"""

import logging
import asyncio
from typing import Dict, List, Any
import networkx as nx
from geopandas import GeoDataFrame
import numpy as np

logger = logging.getLogger(__name__)


class SimulationEngine:
    """
    Main simulation engine for RippleMap AI
    Handles road network disruption and accessibility analysis
    """
    
    def __init__(self):
        self.graph: nx.DiGraph = None
        self.population_cells: GeoDataFrame = None
        self.facilities: GeoDataFrame = None
        
    async def queue_simulation(self, scenario_id: str, parameters: Dict[str, Any]) -> str:
        """Queue a simulation for async processing"""
        # In production, this would use Celery or similar
        job_id = f"job_{scenario_id}_{int(asyncio.get_event_loop().time())}"
        return job_id
    
    def construct_road_network(self, road_segments: List[Dict]) -> nx.DiGraph:
        """
        Construct a directed graph from road segment data
        
        Parameters:
        - road_segments: List of road segment objects with geometry
        
        Returns:
        - networkx.DiGraph: Directed graph representation
        """
        G = nx.DiGraph()
        
        for segment in road_segments:
            segment_id = segment.get('id')
            start_node = segment.get('start_node')
            end_node = segment.get('end_node')
            length_m = segment.get('length_m', 0)
            road_class = segment.get('road_class')
            
            # Add edge with attributes
            G.add_edge(
                start_node, 
                end_node,
                weight=length_m,
                segment_id=segment_id,
                road_class=road_class
            )
        
        logger.info(f"Road network constructed: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        return G
    
    def calculate_baseline_accessibility(
        self, 
        graph: nx.DiGraph,
        population_cells: GeoDataFrame,
        facilities: GeoDataFrame
    ) -> Dict[str, Any]:
        """
        Calculate baseline accessibility metrics
        
        Returns:
        - Dict with accessibility scores per population cell
        """
        accessibility_metrics = {}
        
        for cell_id, cell_row in population_cells.iterrows():
            # Find nearest facility
            nearest_facility = self._find_nearest_facility(
                cell_row.geometry,
                facilities
            )
            
            if nearest_facility:
                # Calculate shortest path distance
                try:
                    path_length = nx.shortest_path_length(
                        graph,
                        cell_row['node_id'],
                        nearest_facility['node_id'],
                        weight='weight'
                    )
                    
                    accessibility_metrics[cell_id] = {
                        'baseline_distance': path_length,
                        'facility_id': nearest_facility['id'],
                        'reachable': True
                    }
                except nx.NetworkXNoPath:
                    accessibility_metrics[cell_id] = {
                        'baseline_distance': np.inf,
                        'facility_id': None,
                        'reachable': False
                    }
        
        return accessibility_metrics
    
    def simulate_disruption(
        self,
        graph: nx.DiGraph,
        affected_segment_ids: List[str],
        action_type: str = 'closure'
    ) -> nx.DiGraph:
        """
        Create a modified graph with disrupted segments
        
        Parameters:
        - graph: Original network graph
        - affected_segment_ids: Segments to disrupt
        - action_type: 'closure' or 'partial_degradation'
        
        Returns:
        - Modified graph (original left unchanged)
        """
        disrupted_graph = graph.copy()
        
        if action_type == 'closure':
            # Remove affected edges
            for u, v, data in graph.edges(data=True):
                if data.get('segment_id') in affected_segment_ids:
                    disrupted_graph.remove_edge(u, v)
        
        elif action_type == 'partial_degradation':
            # Increase weight (travel time) for affected edges
            for u, v, data in graph.edges(data=True):
                if data.get('segment_id') in affected_segment_ids:
                    # Multiply weight by 2 (slower traversal)
                    disrupted_graph[u][v]['weight'] *= 2
        
        logger.info(f"Disruption simulated: {action_type} for {len(affected_segment_ids)} segments")
        return disrupted_graph
    
    def calculate_disruption_impact(
        self,
        original_accessibility: Dict,
        disrupted_graph: nx.DiGraph,
        population_cells: GeoDataFrame,
        facilities: GeoDataFrame
    ) -> Dict[str, Any]:
        """
        Calculate impact of disruption
        
        Returns:
        - Dict with impact metrics per cell
        """
        impact_metrics = {}
        
        for cell_id, cell_row in population_cells.iterrows():
            if cell_id not in original_accessibility:
                continue
            
            original = original_accessibility[cell_id]
            
            # Calculate new distance in disrupted network
            try:
                new_distance = nx.shortest_path_length(
                    disrupted_graph,
                    cell_row['node_id'],
                    facilities.loc[original['facility_id'], 'node_id'],
                    weight='weight'
                )
                reachable_after = True
            except (nx.NetworkXNoPath, KeyError):
                new_distance = np.inf
                reachable_after = False
            
            # Calculate access loss
            if original['reachable'] and reachable_after:
                distance_increase = new_distance - original['baseline_distance']
                access_loss = distance_increase / original['baseline_distance'] if original['baseline_distance'] > 0 else 0
            elif original['reachable'] and not reachable_after:
                access_loss = 1.0  # Complete loss of access
            else:
                access_loss = 0  # No change
            
            impact_metrics[cell_id] = {
                'baseline_distance': original['baseline_distance'],
                'disrupted_distance': new_distance,
                'distance_increase': distance_increase if reachable_after else np.inf,
                'access_loss_ratio': access_loss,
                'reachable_before': original['reachable'],
                'reachable_after': reachable_after,
                'newly_unreachable': original['reachable'] and not reachable_after
            }
        
        return impact_metrics
    
    def calculate_vulnerability_score(
        self,
        impact_metrics: Dict,
        population_data: GeoDataFrame
    ) -> Dict[str, float]:
        """
        Calculate vulnerability scores using weighted formula
        
        Score = (w_A × A_i) + (w_P × P_i) + (w_U × U_i) + (w_B × B_i)
        """
        # Weights (must sum to 1.0, documented)
        weights = {
            'distance_impact': 0.25,      # A_i
            'population_exposure': 0.35,  # P_i
            'unreachability': 0.25,       # U_i
            'baseline_disadvantage': 0.15 # B_i
        }
        
        vulnerability_scores = {}
        
        for cell_id, impact in impact_metrics.items():
            # Normalize components to 0-1 scale
            a_i = min(impact['access_loss_ratio'], 1.0)  # Capped at 1
            p_i = population_data.loc[cell_id, 'population'] / population_data['population'].max() if cell_id in population_data.index else 0
            u_i = 1.0 if impact['newly_unreachable'] else 0
            b_i = population_data.loc[cell_id, 'baseline_disadvantage_score'] if cell_id in population_data.index else 0
            
            # Calculate score
            score = (
                weights['distance_impact'] * a_i +
                weights['population_exposure'] * p_i +
                weights['unreachability'] * u_i +
                weights['baseline_disadvantage'] * b_i
            )
            
            vulnerability_scores[cell_id] = score
        
        return vulnerability_scores
    
    def _find_nearest_facility(self, geometry, facilities_gdf):
        """Find nearest facility to a geometry"""
        distances = facilities_gdf.geometry.distance(geometry)
        nearest_idx = distances.idxmin()
        return facilities_gdf.loc[nearest_idx].to_dict() if len(distances) > 0 else None
