# app/api/routes_download.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.download_service import download_youtube_video

router = APIRouter()


class DownloadRequest(BaseModel):
    url: str
    type: str = "video"  # hoac video


@router.post("/download")
def download_video(data: DownloadRequest):
    try:
        result = download_youtube_video(data.url, data.type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
