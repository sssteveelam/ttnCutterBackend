from fastapi import APIRouter, HTTPException, FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.thumb_service import get_facebook_thumbnail, get_titkok_thumbnail

router = APIRouter()


class ThumbnailRequest(BaseModel):
    url: str


@router.post("/get-facebook-thumbnail")
async def facebook_thumb(request: ThumbnailRequest, background_tasks: BackgroundTasks):
    try:
        thumb_url = await get_facebook_thumbnail(request.url)
        return {"thumbnailUrl": thumb_url}
    except Exception as e:
        print(f"Lỗi trong quá trình get facbook thumbails : {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-tiktok-thumbnail")
async def tiktok_thumb(request: ThumbnailRequest, background_tasks: BackgroundTasks):
    try:
        thumb_object = await get_titkok_thumbnail(request.url)
        return thumb_object
    except Exception as e:
        print(f"Lỗi trong quá trình get tiktok thumbails : {e}")
        raise HTTPException(status_code=500, detail=str(e))
