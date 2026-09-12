from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal
from backend.app.agents.energy_agent import ask_agent

router = APIRouter(
    prefix="/agent",
    tags=["AI Agent"]
)


class Question(BaseModel):
    question: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def chat(question: Question, db: Session = Depends(get_db)):
    return ask_agent(question.question, db)