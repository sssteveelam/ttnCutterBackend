from sqlalchemy.orm import Session
from app.models.log import LogModel
from app.schemas.log_schema import LogSchema


def create_log_service(db: Session, log: LogSchema):
    new_log = LogModel(**log.dict())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log


def get_logs_service(db: Session, userId: str):
    return db.query(LogModel).filter(LogModel.userId == userId).all()
