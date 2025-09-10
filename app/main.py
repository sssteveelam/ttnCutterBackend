from fastapi import FastAPI
from app.api.routes_logs import router as logs_router
from app.db import Base, engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Tạo bảng trong DB khi khởi động
Base.metadata.create_all(bind=engine)

app.include_router(logs_router, prefix="/api")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies and other credentials
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def root():
    return {"message": "Backend is running"}
