from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal
from backend.app.services.report_service import generate_report

router = APIRouter(prefix="/report", tags=["Report"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def report(db: Session = Depends(get_db)):
    return generate_report(db)