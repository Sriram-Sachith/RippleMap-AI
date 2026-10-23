# RippleMap AI - API Specification (v1.0)

**Base URL**: `/api/v1`  
**Content-Type**: `application/json`  
**Versioning**: `/api/v1` (future: `/api/v2`, etc.)

---

## 1. Authentication Endpoints

### `POST /auth/register`
Register a new user account.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe",
  "organization": "Urban Planning Department"
}
```

**Response** (201):
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "analyst",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### `POST /auth/login`
Authenticate and obtain access token.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response** (200):
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLC...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLC...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

## 2. Study Area Endpoints

### `GET /study-areas`
List available study areas with metadata.

**Query Parameters**:
- `skip` (int, default=0): Pagination offset
- `limit` (int, default=10): Items per page

**Response** (200):
```json
{
  "data": [
    {
      "id": "study-area-001",
      "name": "Bangalore Urban District",
      "country": "India",
      "region_code": "KA",
      "boundary": { "type": "Feature", "geometry": {...} },
      "population_total": 1850000,
      "road_segments_count": 12450,
      "facilities_count": 245,
      "data_last_updated": "2024-01-10T00:00:00Z",
      "coverage_status": "complete"
    }
  ],
  "total": 15,
  "page": 1
}
```

---

### `GET /study-areas/{id}/summary`
Get baseline summary for a study area.

**Response** (200):
```json
{
  "study_area_id": "study-area-001",
  "baseline_metrics": {
    "population_total": 1850000,
    "population_with_access_to_hospitals": 1802500,
    "average_access_distance_km": 4.2,
    "facilities_accessible_from_population_center_percent": 98.5,
    "no_access_population": 47500,
    "no_access_population_percent": 2.5
  },
  "roads": {
    "total_length_km": 8423.4,
    "primary_roads_count": 234,
    "secondary_roads_count": 1045,
    "tertiary_roads_count": 5670
  },
  "dataset_versions": {
    "roads": "OpenStreetMap 2024-01-10",
    "population": "WorldPop 2023",
    "facilities": "Geofabrik 2024-01-10"
  }
}
```

---

## 3. Scenario Endpoints

### `POST /scenarios`
Create a new disruption scenario.

**Request**:
```json
{
  "study_area_id": "study-area-001",
  "name": "Monsoon Road Closure - August 2024",
  "scenario_type": "road_closure",
  "affected_road_ids": ["road-101", "road-102"],
  "parameters": {
    "population_year": 2024,
    "access_metric": "shortest_network_distance",
    "max_access_distance_km": 20
  }
}
```

**Response** (201):
```json
{
  "id": "scenario-abc123",
  "study_area_id": "study-area-001",
  "name": "Monsoon Road Closure - August 2024",
  "scenario_type": "road_closure",
  "status": "draft",
  "created_at": "2024-01-15T10:30:00Z",
  "created_by": "user-uuid"
}
```

---

### `GET /scenarios`
List scenarios for current user.

**Query Parameters**:
- `study_area_id` (string, required): Filter by study area
- `skip`, `limit`: Pagination

**Response** (200):
```json
{
  "data": [
    {
      "id": "scenario-abc123",
      "name": "Monsoon Road Closure - August 2024",
      "status": "draft",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 5
}
```

---

### `POST /scenarios/{id}/run`
Execute scenario simulation.

**Request**:
```json
{
  "parameters": {
    "simulation_mode": "accessibility_loss",
    "include_alternative_routes": true
  }
}
```

**Response** (202):
```json
{
  "job_id": "job_scenario-abc123_1705315800",
  "scenario_id": "scenario-abc123",
  "status": "queued",
  "estimated_completion_seconds": 45
}
```

---

## 4. Results & Analysis Endpoints

### `GET /jobs/{job_id}`
Check simulation job status.

**Response** (200):
```json
{
  "job_id": "job_scenario-abc123_1705315800",
  "status": "completed",
  "progress_percent": 100,
  "started_at": "2024-01-15T10:31:00Z",
  "completed_at": "2024-01-15T10:32:30Z"
}
```

---

### `GET /scenarios/{id}/results`
Retrieve completed scenario results.

**Response** (200):
```json
{
  "scenario_id": "scenario-abc123",
  "job_id": "job_scenario-abc123_1705315800",
  "completion_timestamp": "2024-01-15T10:32:30Z",
  "algorithm_version": "v1.0.0",
  "baseline_metrics": {
    "population_with_access": 1802500,
    "average_access_distance_km": 4.2
  },
  "disrupted_metrics": {
    "population_with_access": 1720300,
    "average_access_distance_km": 6.8,
    "newly_unreachable_population": 82200,
    "affected_population_percent": 4.4
  },
  "aggregate_impact": {
    "total_access_loss_person_km": 450230,
    "average_additional_distance_km": 5.6,
    "accessibility_loss_ratio": 0.044
  }
}
```

---

### `GET /scenarios/{id}/vulnerable-areas`
Get ranked vulnerability analysis.

**Response** (200):
```json
{
  "scenario_id": "scenario-abc123",
  "ranking_method": "composite_vulnerability_index",
  "weight_definitions": {
    "distance_impact": 0.25,
    "population_exposure": 0.35,
    "unreachability": 0.25,
    "baseline_disadvantage": 0.15
  },
  "areas": [
    {
      "area_id": "cell-001",
      "area_name": "Slum Colony A",
      "vulnerability_score": 0.87,
      "rank": 1,
      "population": 12450,
      "baseline_access_km": 3.2,
      "disrupted_access_km": 18.5,
      "newly_unreachable": false,
      "baseline_disadvantage_score": 0.6
    }
  ]
}
```

---

## 5. Routes & Service Access Endpoints

### `POST /routes/compare`
Compare routes under different scenarios.

**Request**:
```json
{
  "origin_geometry": {"type": "Point", "coordinates": [75.34, 13.12]},
  "destination_facility_id": "facility-005",
  "scenario_id": "scenario-abc123"
}
```

**Response** (200):
```json
{
  "baseline_route": {
    "distance_m": 4200,
    "estimated_time_minutes": 12,
    "path_geometry": {"type": "LineString", "coordinates": [...]}
  },
  "disrupted_route": {
    "distance_m": 8400,
    "estimated_time_minutes": 24,
    "path_geometry": {"type": "LineString", "coordinates": [...]}
  },
  "comparison": {
    "distance_increase_percent": 100,
    "time_increase_percent": 100,
    "uses_affected_roads": true
  }
}
```

---

## 6. Map Layers & Filtering Endpoints

### `GET /map/layers`
List available geographic layers.

**Response** (200):
```json
{
  "layers": [
    {
      "id": "roads",
      "name": "Road Network",
      "description": "Road segments with accessibility status",
      "geometry_type": "LineString",
      "visible_by_default": true
    },
    {
      "id": "facilities",
      "name": "Healthcare Facilities",
      "description": "Hospitals and clinics",
      "geometry_type": "Point",
      "visible_by_default": true
    },
    {
      "id": "population",
      "name": "Population Grid",
      "description": "Population estimates by cell",
      "geometry_type": "Polygon",
      "visible_by_default": false
    },
    {
      "id": "risk",
      "name": "Vulnerability Score",
      "description": "Composite vulnerability ranking",
      "geometry_type": "Polygon",
      "visible_by_default": false
    }
  ]
}
```

---

### `GET /map/features`
Retrieve geospatial features filtered by area and layer.

**Query Parameters**:
- `layer_id` (string, required): Layer to query
- `study_area_id` (string, required): Study area
- `scenario_id` (string, optional): For scenario-specific data
- `bounds` (string): Bounding box for map viewport filtering

**Response** (200):
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "road-101",
      "geometry": {"type": "LineString", "coordinates": [[...]]},
      "properties": {
        "road_class": "primary",
        "length_m": 2345,
        "status": "affected",
        "baseline_accessibility": 0.95,
        "disrupted_accessibility": 0.45
      }
    }
  ]
}
```

---

## 7. Reporting & Export Endpoints

### `POST /reports`
Generate a scenario report.

**Request**:
```json
{
  "scenario_id": "scenario-abc123",
  "format": "pdf",
  "include_sections": ["summary", "methodology", "results", "recommendations"],
  "include_charts": true
}
```

**Response** (202):
```json
{
  "report_id": "report-xyz789",
  "format": "pdf",
  "status": "generating",
  "estimated_completion_seconds": 30
}
```

---

### `GET /reports/{report_id}/download`
Download generated report.

**Response** (200):
- Content-Type: `application/pdf`
- Body: PDF file stream

---

## 8. Data Sources & Transparency Endpoints

### `GET /data-sources`
Retrieve data source metadata and provenance.

**Response** (200):
```json
{
  "study_area_id": "study-area-001",
  "sources": [
    {
      "id": "source-roads",
      "name": "OpenStreetMap",
      "data_type": "road_network",
      "coverage": "Bangalore Urban District",
      "version": "2024-01-10",
      "licence": "ODbL 1.0",
      "last_update": "2024-01-10T00:00:00Z",
      "attribution": "© OpenStreetMap contributors",
      "known_limitations": "Minor discrepancies in secondary roads"
    },
    {
      "id": "source-population",
      "name": "WorldPop",
      "data_type": "population_estimates",
      "coverage": "Global 100m grid",
      "version": "2023",
      "licence": "CC BY 4.0",
      "last_update": "2023-12-01T00:00:00Z",
      "citation": "WorldPop (2023)"
    }
  ]
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message",
  "error_code": "INVALID_INPUT",
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "req-abc123"
}
```

**Common Status Codes**:
- `400`: Invalid input or validation error
- `401`: Unauthorized (missing/invalid token)
- `403`: Forbidden (insufficient permissions)
- `404`: Resource not found
- `409`: Conflict (e.g., duplicate scenario)
- `422`: Unprocessable entity
- `429`: Rate limit exceeded
- `500`: Internal server error
- `503`: Service unavailable

---

## Rate Limiting

All endpoints are rate-limited:
- **Default**: 100 requests per 60 seconds per user
- **Simulations**: 20 concurrent jobs per user
- **Exports**: 10 concurrent exports per user

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 89
X-RateLimit-Reset: 1705315860
```

---

## Pagination

List endpoints support:
- `skip` (default: 0)
- `limit` (default: 10, max: 100)

Response includes:
```json
{
  "data": [...],
  "total": 150,
  "skip": 0,
  "limit": 10,
  "page": 1,
  "pages": 15
}
```

---

## Status Codes & Meanings

| Status | Meaning |
|--------|---------|
| `draft` | Scenario created, not run |
| `queued` | Simulation job waiting to execute |
| `running` | Simulation in progress |
| `completed` | Simulation finished successfully |
| `failed` | Simulation encountered an error |
| `generating` | Report generation in progress |
| `ready` | Report ready for download |

---

**Last Updated**: January 2024  
**Version**: 1.0.0  
**Contact**: api-support@ripplemap.ai
