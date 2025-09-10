from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.schemas.log_schema import LogSchema
from app.services.log_service import create_log_service, get_logs_service

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/logs")
def create_log(log: LogSchema, db: Session = Depends(get_db)):
    return create_log_service(db, log)


@router.get("/logs")
def get_logs(userId: str, db: Session = Depends(get_db)):
    return get_logs_service(db, userId)
