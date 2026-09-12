from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal
from backend.app.services.recommendation_service import detect_recommendations

router = APIRouter(
    prefix="/recommendation",
    tags=["Recommendation"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_recommendations(db: Session = Depends(get_db)):
    return detect_recommendations(db)