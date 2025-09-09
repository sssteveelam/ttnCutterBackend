 🎯 Mục tiêu

Đây là backend prototype của hệ thống.
Nhiệm vụ của backend:

Quản lý user và log (metadata download/cut).

Không tải file, không cắt video (theo yêu cầu kiến trúc client-heavy).

Expose API để frontend gửi và lấy log.

🏗️ Công nghệ sử dụng

FastAPI (Python) – framework backend.

SQLite – database đơn giản cho prototype.

SQLAlchemy – ORM quản lý model.

Pydantic – schema validation.

📂 Cấu trúc thư mục
app/
 ├── main.py                # Entry point
 ├── api/
 │    └── routes_logs.py    # Endpoint POST/GET logs
 ├── models/
 │    └── log.py            # ORM model cho Log
 ├── schemas/
 │    └── log_schema.py     # Pydantic schema
 ├── services/
 │    └── log_service.py    # Business logic
 └── db.py                  # DB connection (SQLite)

🚀 Cách chạy
pip install -r requirements.txt
uvicorn app.main:app --reload


Chạy ở http://localhost:8000/docs

