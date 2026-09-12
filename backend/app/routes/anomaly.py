from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.services.anomaly_service import detect_anomalies

router = APIRouter(
    prefix="/anomaly",
    tags=["Anomaly"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_anomalies(db: Session = Depends(get_db)):
    return detect_anomalies(db)