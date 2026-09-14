from backend.app.database.database import SessionLocal
from backend.app.services.dashboard_service import get_dashboard_summary

def run_dashboard():
    db = SessionLocal()
    try:
        return get_dashboard_summary(db)
    finally:
        db.close()