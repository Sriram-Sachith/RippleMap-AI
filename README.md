> [!NOTE]
> **Viewing Large Documentation Files on GitHub**
> 
> Some large documentation files (such as `API_SPEC.md`, `DEPLOYMENT.md`, and `LOCAL_DEVELOPMENT.md`) may show a `"Large diffs are not rendered by default"` or `"The contents of the file couldn't be loaded"` notice when viewed inside commit history pages.

#### 💡 Instructions to view file contents:
1. Navigate directly to the repository's main **Code** view page.
2. Click on the file directly from the file list to open and view its full contents.
3. Alternatively, clone or open the repository locally in **VS Code** to view all files without limitations.

Sorry For the Inconvenience


# 🌍 RippleMap AI - Geospatial Intelligence Platform

**See the impact. Find the vulnerable. Plan the response.**

RippleMap AI is a cutting-edge geospatial analytics and decision-support platform that helps urban planners, disaster-preparedness teams, and communities understand how road disruptions affect essential service accessibility. By combining geographic data, road-network analysis, population estimates, and rainfall analytics into a single interactive application, RippleMap AI empowers stakeholders to make data-driven decisions.

## 🎯 Problem Statement

When a road becomes inaccessible, the impact spreads far beyond that single road. Communities may lose convenient access to hospitals, travel distances may increase, and alternative routes may become overloaded or unavailable. RippleMap AI addresses this critical gap by:

- **Calculating accessibility impacts** with precision
- **Identifying vulnerable communities** most affected by disruptions
- **Simulating scenarios** before they happen
- **Recommending interventions** backed by data

## ✨ Key Features

### 1. **Interactive Map Workspace**
- Zoom, pan, and reset controls
- Multiple layer toggles (roads, hospitals, population, risk)
- Real-time geographic filtering
- Professional cartography with semantic coloring

### 2. **Disruption Simulation Engine**
- Create custom road-closure scenarios
- Simulate accessibility changes instantly
- Compare before-and-after metrics
- Track affected population counts

### 3. **Risk & Vulnerability Explorer**
- Ranked vulnerability analysis by geographic area
- Population exposure metrics
- Disruption impact categorization
- Sensitivity-based prioritization

### 4. **Alternative Routes & Service Access**
- Route comparison under simulated closures
- Travel time and distance analysis
- Service facility impact assessment
- Network resilience evaluation

### 5. **Advanced Reporting**
- CSV and PDF exports
- Scenario comparisons
- Research methodology transparency
- Uncertainty documentation

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User's Browser (HTTPS)                   │
│              React + TypeScript Frontend (React Query)      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│               Frontend Hosting (CDN + TLS)                  │
│          Static Assets, Domain, HTTPS Configuration         │
└─────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│          Backend API Service (FastAPI + Python)            │
│  Authentication • Validation • Orchestration • Business Logic│
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │   Analysis   │  │ Object Store │
│   + PostGIS  │  │    Engine    │  │     (S3)     │
│   Database   │  │  (Geospatial)│  │   Reports    │
└──────────────┘  └──────────────┘  └──────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+ with PostGIS
- Docker & Docker Compose

### Installation

```bash
# Clone the repository
git clone https://github.com/ripplemap-ai/ripplemap-ai.git
cd ripplemap-ai

# Frontend setup
cd frontend
npm install
npm start

# Backend setup (in another terminal)
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Database setup
docker-compose up -d

# Run migrations
python backend/app/migrations/run.py
```

Visit `http://localhost:3000` to access the application.

## 📊 Data Sources

| Source | Data Type | Usage | Notes |
|--------|-----------|-------|-------|
| **Geofabrik** | Road networks, healthcare facilities | Network construction, facility mapping | Regional extracts, attribution required |
| **IMD** | Historical rainfall observations | Rainfall analysis, extreme-event study | Download & preprocess supported formats |
| **WorldPop** | Population estimates | Baseline accessibility, vulnerability scoring | Compatible raster data or API |
| **OpenRouteService** | Routing comparison (optional) | Route validation, cost-benefit analysis | API key, usage limits apply |
| **OpenStreetMap** | Background map tiles | Context visualization | Comply with attribution policy |

## 📐 Core Algorithms

### Accessibility Calculation
RippleMap AI calculates three distinct accessibility metrics:

1. **Baseline Network Distance** - Shortest path in undisrupted network
2. **Disruption-Adjusted Distance** - Recalculated paths after road closures
3. **Access Loss Score** - Normalized increase in travel distance or unreachability

### Vulnerability Ranking
```
Risk Score = (w_A × A_i) + (w_P × P_i) + (w_U × U_i) + (w_B × B_i)

Where:
  A_i = Additional travel distance impact
  P_i = Population exposure
  U_i = Increase in unreachability
  B_i = Baseline service-access disadvantage
  w_* = Documented, adjustable weights (sum = 1.0)
```

**Important**: This is a *prioritization index*, not a calibrated disaster prediction. Component definitions, weights, and sensitivities are fully documented and transparent.

## 🔐 Security & Privacy

- ✅ Passwords hashed with bcrypt (never stored plaintext)
- ✅ HTTPS-only communication with secure cookies
- ✅ Input validation on all endpoints
- ✅ Role-based access control (RBAC)
- ✅ Audit logging for administrative actions
- ✅ No public exposure of sensitive infrastructure paths

## 🧪 Testing & Validation

```bash
# Run backend tests
pytest backend/tests/ -v

# Run frontend tests
npm run test

# Integration tests
pytest backend/tests/integration/ -v
```

**Performance targets**:
- Normal API reads: p95 < 500ms
- Small simulations: < 10 seconds
- Dashboard load: < 3 seconds
- Map responsiveness: Zoom/pan < 100ms

## 📖 Documentation

- **[User Guide](docs/USER_GUIDE.md)** - How to use every feature
- **[API Specification](docs/API_SPECIFICATION.md)** - Complete endpoint reference
- **[Data Dictionary](docs/DATA_DICTIONARY.md)** - Field definitions and data provenance
- **[Research Methodology](docs/RESEARCH_METHODOLOGY.md)** - Scientific foundations
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production setup & operations

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 👥 Initial Target Users

- 🏛️ Urban and district planners
- 🚨 Disaster-preparedness and emergency-response teams
- 🌱 NGOs working on community resilience
- 🔬 Researchers studying transport and public-service accessibility
- 🏢 Infrastructure analysts and public-interest organizations

## 📊 First Release Scope

**Included in the 12-week MVP:**
- One selected district/study area
- Road-network accessibility analysis
- Simulated road closures
- Historical rainfall analysis
- Population-weighted vulnerability ranking
- Healthcare facility accessibility
- Scenario comparisons and basic intervention optimization
- Interactive web application and API
- Data exports (CSV/PDF) and full documentation

**Not required for first release:**
- Nationwide coverage
- Live traffic prediction
- Certified flood-warning system
- Accurate road-failure predictions without labels

## 🌱 Future Roadmap

- Expansion to additional districts and regions
- Machine learning models for disruption prediction
- Mobile applications (iOS/Android)
- Advanced intervention optimization algorithms
- Integration with live traffic and weather feeds
- Community-contributed scenario sharing

---

**Built with ❤️ for better disaster preparedness and community resilience.**

For questions or support, visit [support.ripplemap.ai](https://support.ripplemap.ai)
