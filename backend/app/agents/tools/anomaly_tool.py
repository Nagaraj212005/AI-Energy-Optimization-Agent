from backend.app.database.database import SessionLocal
from backend.app.services.anomaly_service import detect_anomalies

def run_anomaly():
    return detect_anomalies()
