
## Deploying to Render

1. Create a new **Web Service** on Render and connect this repository.
2. Set the **Build Command** to `pip install -r requirements.txt`.
3. Set the **Start Command** to `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Add a `DATABASE_URL` environment variable. For SQLite you can leave it empty (the
   application falls back to `sqlite:///./logs.db`), but when using a Render PostgreSQL
   instance paste the connection string provided by Render.
5. (Optional) Add a **Persistent Disk** if you plan on keeping the generated
   `temp_videos` or SQLite database file between deployments.

The application automatically creates the `temp_videos` directory on startup so the
static files route works in the Render container filesystem.
