from pathlib import Path

from fastapi import FastAPI
from app.api.routes_logs import router as logs_router
from app.db import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_download import router as download_router
from app.api.routes_formats import router as format_router
from fastapi.staticfiles import StaticFiles


TEMP_VIDEO_DIR = Path("temp_videos")
TEMP_VIDEO_DIR.mkdir(parents=True, exist_ok=True)


app = FastAPI()

Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.include_router(logs_router, prefix="/api")
app.include_router(download_router, prefix="/api")
app.include_router(format_router, prefix="/api")
app.mount("/videos", StaticFiles(directory=TEMP_VIDEO_DIR), name="videos")
