# app/services/download_service.py
import yt_dlp
import os


VIDEO_DIR = "videos_temp"


def download_youtube_video(url: str, media_type: str = "video") -> dict:
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)

    ydl_opts = {
        "outtmpl": f"{VIDEO_DIR}/%(id)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
    }

    if media_type == "audio":
        ydl_opts.update(
            {"format": "bestaudio", "extract_audio": True, "audio_format": mp3}
        )
    else:
        ydl_opts.update({"format": "mp4"})

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        return {
            "title": info.get("title"),
            "id": info.get("id"),
            "ext": info.get("ext"),
            "filename": f"{info.get("id")}.{info.get("ext")}",
            "duration": info.get("duration"),
            "download_url": f"http://localhost:8000/videos/{info.get('id')}.{info.get('ext')}",
        }
