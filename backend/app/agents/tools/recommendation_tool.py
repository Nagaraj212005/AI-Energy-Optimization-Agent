from backend.app.database.database import SessionLocal
from backend.app.services.recommendation_service import get_recommendations


def run_recommendation():
    db = SessionLocal()

    try:
        return get_recommendations(db)
    finally:
        db.close()