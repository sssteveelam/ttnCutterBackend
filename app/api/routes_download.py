# app/api/routes_download.py
from fastapi import APIRouter, HTTPException, FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import urllib.parse
from pydantic import BaseModel
from app.services.download_service import download_and_merge
from app.services import download_service as services

router = APIRouter()


class DownloadRequest(BaseModel):
    url: str
    format_id: str = None


@router.post("/download")
async def download_video(request: DownloadRequest, background_tasks: BackgroundTasks):
    try:
        file_path, final_filename = services.download_and_merge(
            request.url, request.format_id
        )

        background_tasks.add_task(file_path.unlink)

        encoded_filename = urllib.parse.quote(final_filename)
        headers = {
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
        }
        return FileResponse(
            path=file_path, media_type="application/octet-stream", headers=headers
        )

    except Exception as e:
        print(f"Lỗi trong quá trình download/merge: {e}")
        raise HTTPException(status_code=500, detail=str(e))
