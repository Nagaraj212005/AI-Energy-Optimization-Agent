# AI Energy Optimization Agent

An end-to-end energy intelligence platform for monitoring consumption, forecasting demand, detecting anomalous usage, and identifying opportunities to reduce energy waste.

The project was developed for the **Smart Energy Consumption Optimization** use case proposed by Cognizant for Smart India Hackathon. It combines a FastAPI backend, a SQLite data layer, trained machine learning models, and a responsive React dashboard.

## Problem Statement

### Smart Energy Consumption Optimization Agent

Buildings, campuses, and factories need to reduce energy usage and optimize cost without disrupting critical operations. Energy demand varies by time, occupancy, weather, and usage pattern.

## Objective

Build an energy optimization agent that forecasts peak consumption, detects anomalies, and recommends energy-saving actions with estimated impact.

## Our Solution

The AI Energy Optimization Agent is an end-to-end intelligent analytics platform built to address this challenge. It processes energy consumption records and converts them into operational insights that can support better planning and faster intervention.

The platform combines:

- Machine learning for forecasting, anomaly detection, and recommendations
- Agentic workflows for natural-language access to analytics modules
- FastAPI services for structured data access
- A responsive dashboard for monitoring and exploration
- SQLite storage for local, reproducible development

The current dataset contains more than one million energy consumption records across multiple regions. The system transforms this data into forecasts, anomaly signals, optimization recommendations, historical views, and operational reports.

### Key Capabilities

- Interactive energy dashboard
- 24-hour energy consumption forecasting
- Machine learning-based anomaly detection
- AI-generated energy optimization recommendations
- Historical consumption analytics with search, filters, pagination, and CSV export
- Automated energy reports
- Conversational AI assistant for natural-language queries

## System Overview

```text
Processed energy data
	|
	v
SQLite database (energy.db)
	|
	+--> Dashboard summary
	+--> 24-hour forecast model
	+--> Anomaly detection model
	+--> Recommendation model
	+--> History and report services
	+--> Conversational agent
	|
	v
FastAPI backend  <---- Axios / Vite proxy ---->  React dashboard
```

## Technology Stack

### Backend and data

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pandas and NumPy
- Scikit-learn
- Joblib

### Frontend

- React with Vite
- JavaScript
- Tailwind CSS
- React Router
- Axios
- Recharts
- Lucide React
- Framer Motion
- React Hook Form

## Project Structure

```text
.
├── backend/
│   ├── main.py                         # FastAPI application entry point
│   ├── requirements.txt                # Python dependencies
│   └── app/
│       ├── agents/                     # Conversational energy agent
│       ├── database/                   # SQLite connection, models, and loader
│       ├── models/                     # API/domain model definitions
│       ├── routes/                     # FastAPI route modules
│       ├── services/                   # Application and ML service logic
│       └── utils/                      # Data preparation utilities
├── data/
│   ├── raw/                            # Source regional datasets
│   └── processed/                      # Prepared data used by the loader
├── docs/                               # Architecture and project documentation
├── frontend/
│   ├── src/
│   │   ├── components/                 # Shared UI components
│   │   ├── hooks/                      # Data-fetching hooks
│   │   ├── layouts/                    # Application shell
│   │   ├── pages/                      # Dashboard views
│   │   ├── routes/                     # React Router configuration
│   │   ├── services/                   # Axios API services
│   │   ├── utils/                      # Shared frontend utilities
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── ml/
│   ├── anomaly/                        # Anomaly model and training script
│   ├── forecasting/                    # Forecast model and training script
│   ├── recommendation/                 # Recommendation model and training script
│   └── trained_models/                 # Saved Joblib artifacts
├── tests/                              # Backend and service tests
├── energy.db                           # Local SQLite database after loading data
└── README.md
```

## Setup

### Prerequisites

- Python 3.10 or newer
- Node.js 18 or newer
- npm

### 1. Create and activate a Python environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Load the processed dataset

The loader creates `energy.db`, creates the `energy_consumption` table, and inserts records from `data/processed/processed_energy_data.csv`.

Run it from the repository root:

```bash
python -m backend.app.database.load_data
```

The load operation is intended for initial database setup. Running it repeatedly will insert duplicate rows into the current SQLite database.

### 4. Start the backend

From the repository root:

```bash
uvicorn backend.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

Interactive API documentation is available at:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

### 5. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The dashboard will be available at `http://localhost:5173`.

During local development, Vite proxies frontend requests from `/api` to `http://localhost:8000`, allowing the browser to call the existing backend without changing its API contracts.

## API Reference

All routes are served by the FastAPI application.

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | API health response |
| `GET` | `/dashboard/summary` | Consumption totals, average, peak, and record count |
| `GET` | `/forecast/` | Next 24 predicted consumption values |
| `GET` | `/anomaly/` | Detected anomalies and anomaly scores |
| `GET` | `/recommendation/` | Ranked energy optimization recommendations |
| `GET` | `/history/` | Latest 100 consumption records |
| `GET` | `/report/` | Dataset and operational summary |
| `POST` | `/agent/` | Natural-language query interface |

### Agent request example

```json
{
  "question": "Show dashboard summary"
}
```

The agent routes supported questions to the dashboard, forecast, anomaly, recommendation, report, and history services.

## Machine Learning Workflows

The repository includes three model pipelines:

### Forecasting

The forecasting model predicts the next hour of consumption using consumption history and time-based features. The API rolls the model forward to produce a 24-hour forecast.

```bash
python ml/forecasting/train_forecast.py
```

### Anomaly detection

The anomaly pipeline uses a scaled Isolation Forest model to identify unusual consumption records and returns the highest-priority anomaly signals.

```bash
python ml/anomaly/train_anomaly.py
```

### Recommendations

The recommendation pipeline uses a scaled Random Forest regressor and region encoding to estimate recommended consumption, savings, savings percentage, and priority.

```bash
python ml/recommendation/train_recommendation.py
```

Training scripts expect the SQLite database to exist and contain populated `energy_consumption` records. Saved artifacts are written to `ml/trained_models/`.

## Testing and Validation

Run the backend test suite from the repository root:

```bash
pytest
```

Build the frontend:

```bash
cd frontend
npm run build
```

For a quick service check, verify the API root and dashboard summary:

```bash
curl http://localhost:8000/
curl http://localhost:8000/dashboard/summary
```

## Current Scope

The application currently focuses on analytics and decision support. It does not directly control building equipment or execute energy-saving actions. Recommendation savings are model estimates and should be reviewed against operational constraints before implementation.

The frontend displays only data supplied by the existing backend contracts. Features such as cost impact, carbon reduction, confidence intervals, PDF generation, and server-side history filters require corresponding backend fields or endpoints before they can be represented as authoritative product metrics.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Project plan](docs/PROJECT_PLAN.md)
- [API contract](docs/API_CONTRACT.md)
