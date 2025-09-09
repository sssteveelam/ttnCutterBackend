from fastapi import FastAPI
from app.api.routes_logs import router as logs_router

app = FastAPI(title="Video Cutter TTN")

app.include_router(logs_router, prefix="/api", tags=["logs"])


@app.get("/")
def root():
    return {"message": "Backend is running"}
