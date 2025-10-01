# app/adapters/platforms/facebook_adapter.py
import subprocess
import json
import uuid
from pathlib import Path
import re
import requests


FB_DIR = Path("./temp_videos/facebook")
FB_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*]', "", filename)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:100]


def get_formats(url: str) -> list:
    # yt-dlp goi tuong ung
    command = ["yt-dlp", "-j", "--impersonate", "chrome", url]
    result = subprocess.run(
        command, capture_output=True, text=True, check=True, encoding="utf-8"
    )

    info = json.loads(result.stdout)
    return info.get("formats", [])


def download_and_merge(url: str, format_id: str) -> tuple[Path, str]:
    # 0. Preprocessing url for direction link
    response = requests.get(url)

    final_url = response.url

    # 1. info
    command = ["yt-dlp", "-j", final_url]
    result = subprocess.run(
        command, capture_output=True, text=True, check=True, encoding="utf-8"
    )
    info = json.loads(result.stdout)

    formats = info.get("formats", [])

    selected_format = next((f for f in formats if f["format_id"] == format_id), None)

    if not selected_format:
        raise ValueError("Format id khong hop le")

    # 2. get video
    selected_video_format = next(
        (f for f in formats if f.get("format_id") == format_id), None
    )

    if not selected_video_format:
        raise ValueError(f"Format ID '{format_id}' không hợp lệ hoặc không tìm thấy.")

    # 3. check format item have avcodec? if don't have, we must find item music in  format item another with best quality
    format_selector = format_id
    if selected_video_format.get("acodec") == "none":
        # find another format item
        audio_formats = [
            f
            for f in formats
            if f.get("vcodec") == "none" and f.get("acodec") != "none"
        ]

        # after have item audio, it's time find best audio qualitiy
        if audio_formats:
            best_audio = max(audio_formats, key=lambda f: f.get("abr", 0))
            best_audio_id = best_audio["format_id"]
            # tao selector de yt-dlp de ca hai merge va "video_id + audio_id"
            format_selector = f"{format_id}+{best_audio_id}"
            print(
                f"Đã chọn video-only. Tìm thấy audio tốt nhất: {best_audio_id}. Sử dụng format: '{format_selector}'"
            )

    # 4. prepare file name and path
    title = sanitize_filename(info.get("title", "video"))
    ext = info.get("ext", "mp4")

    session_id = str(uuid.uuid4())

    OUTPUT_DIR = FB_DIR

    final_filename = f"{title}.{ext}"
    output_path_template = OUTPUT_DIR / f"{session_id}.%(ext)s"

    # 5. download : download and merge
    download_command = [
        "yt-dlp",
        "-f",
        format_selector,
        "-o",
        str(output_path_template),
        "--merge-output-format",
        "mp4",
        final_url,
    ]

    print(f"Dang thuc thi lenh: {" ".join(download_command)}")
    subprocess.run(download_command, check=True)

    final_path = OUTPUT_DIR / f"{session_id}.mp4"

    if not final_path.exists():
        raise FileNotFoundError("Không tìm thấy file video sau khi tải và merge.")

    return final_path, final_filename
