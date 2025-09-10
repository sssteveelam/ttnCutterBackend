from pydantic import BaseModel
from uuid import uuid4


class LogSchema(BaseModel):
    logId: str = str(uuid4())
    userId: str
    action: str
    status: str

    class Config:
        orm_mode = True
