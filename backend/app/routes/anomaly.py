from fastapi import APIRouter

from backend.app.services.anomaly_service import detect_anomalies

router = APIRouter(
    prefix="/anomaly",
    tags=["Anomaly"],
)


@router.get("/")
def get_anomalies():
    return detect_anomalies()