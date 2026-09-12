from fastapi import FastAPI

from app.database.database import engine, Base
import app.database.models
from app.routes.dashboard import router as dashboard_router
from app.routes.forecast import router as forecast_router
from app.routes.anomaly import router as anomaly_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Energy Optimization Agent",
    version="1.0.0",
    description="Backend APIs for Energy Forecasting, Anomaly Detection and AI Recommendations"
)

app.include_router(dashboard_router)
app.include_router(forecast_router)
app.include_router(anomaly_router)

@app.get("/")
def home():
    return {"message": "Backend Running Successfully"}