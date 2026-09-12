from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.recommendation_service import generate_recommendations

router = APIRouter(
    prefix="/Recommendation",
    tags=["Recommendation"]
)


@router.get("/")
def get_recommendations(db: Session = Depends(get_db)):
    return generate_recommendations(db)