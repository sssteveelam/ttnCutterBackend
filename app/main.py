from fastapi import FastAPI
from app.api.routes_logs import router as logs_router
from app.db import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_download import router as download_router
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Tạo bảng trong DB khi khởi động
Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho tất cả origin (FE)
    allow_credentials=True,
    allow_methods=["*"],  # Cho mọi phương thức (GET, POST,...)
    allow_headers=["*"],  # Cho mọi header
)

app.include_router(logs_router, prefix="/api")
app.include_router(download_router, prefix="/api")
app.mount("/videos", StaticFiles(directory="videos_temp"), name="videos")
