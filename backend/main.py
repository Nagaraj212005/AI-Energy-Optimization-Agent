from fastapi import FastAPI

from app.database.database import Base, engine

# Import models so SQLAlchemy registers them
from app.database import models

from app.routes.dashboard import router as dashboard_router
from app.routes.forecast import router as forecast_router
from app.routes.anomaly import router as anomaly_router
from app.routes.recommendation import router as recommendation_router
from app.routes.history import router as history_router
from app.routes.report import router as report_router
from app.routes.agent import router as agent_router

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