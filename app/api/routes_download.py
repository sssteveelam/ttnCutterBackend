# app/api/routes_download.py
from fastapi import APIRouter, HTTPException, FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import urllib.parse
from pydantic import BaseModel
from app.services.download_service import download_and_merge
from app.services import download_service as services
import os
from urllib.parse import urlparse
from pydantic import BaseModel, field_validator

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

        # print("file_path, final_filename = ", file_path, final_filename)

        background_tasks.add_task(file_path.unlink)

        file_size = os.path.getsize(file_path)
        encoded_filename = urllib.parse.quote(final_filename)
        headers = {
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}",
            "Content-Length": str(file_size),
        }
        return FileResponse(
            path=file_path,
            filename=final_filename,
            media_type="application/octet-stream",
            headers=headers,
        )

    except Exception as e:
        print(f"Lỗi trong quá trình download/merge: {e}")
        raise HTTPException(status_code=500, detail=str(e))
