from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.format_service import get_formats


router = APIRouter()


class FormatRequest(BaseModel):
    url: str
    impersonate_client: str | None = None


@router.post("/formats")
def list_formats(data: FormatRequest):
    try:
        print(data)
        return get_formats(data.url, data.impersonate_client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))