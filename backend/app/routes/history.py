from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal
from backend.app.services.history_service import get_history

router = APIRouter(
    prefix="/history",
    tags=["History"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def history(db: Session = Depends(get_db)):
    return get_history(db)