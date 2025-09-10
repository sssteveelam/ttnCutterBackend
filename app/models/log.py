from sqlalchemy import Column, String, Integer
from app.db import Base


class LogModel(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String, index=True)
    action = Column(String)
    status = Column(String)
