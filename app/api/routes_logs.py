from fastapi import APIRouter

router = APIRouter()


@router.post("/logs")
def create_log(log: dict):
    return {
        "message": "Log received",
    }   


@router.get("/logs")
def get_logs(userId: str):

    return [
        {"logId": "1", "userId": userId, "action": "download", "status": "completed"},
        {"logId": "2", "userId": userId, "action": "cut", "status": "failed"},
    ]
