from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.services.agent_service import ai_agent_summary

router = APIRouter(
    prefix="/agent",
    tags=["AI Agent"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def agent(db: Session = Depends(get_db)):
    return ai_agent_summary(db)