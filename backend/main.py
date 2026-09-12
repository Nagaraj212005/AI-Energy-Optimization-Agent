import sys
from pathlib import Path

from fastapi import FastAPI

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.app.database.database import Base, engine
from backend.app.database import models

from backend.app.routes.dashboard import router as dashboard_router
from backend.app.routes.forecast import router as forecast_router
from backend.app.routes.anomaly import router as anomaly_router
from backend.app.routes.recommendation import router as recommendation_router
from backend.app.routes.history import router as history_router
from backend.app.routes.report import router as report_router
from backend.app.routes.agent import router as agent_router
from backend.app.routes import recommendation
from backend.app.routes import agent

app = FastAPI(
    title="AI Energy Optimization Agent"
)

Base.metadata.create_all(bind=engine)

app.include_router(dashboard_router)
app.include_router(forecast_router)
app.include_router(anomaly_router)
app.include_router(recommendation_router)
app.include_router(history_router)
app.include_router(report_router)
app.include_router(agent_router)


@app.get("/")
def home():
    return {"message": "AI Energy Optimization Agent API"}