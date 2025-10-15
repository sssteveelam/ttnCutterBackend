# app/adapters/platforms/youtube_adapter.py
import subprocess
import json
import uuid
from pathlib import Path
import re
from app.services.download_service import get_video_info


YOUTUBE_DIR = Path("./temp_videos/youtube")
YOUTUBE_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*]', "", filename)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:100]


def get_formats(url: str, impersonate_client: str | None = None) -> list[dict]:
    video_info = get_video_info(url, impersonate_client)

    formats = []
    for f in video_info.get("formats", []):
        formats.append(
            {
                "format_id": f["format_id"],
                "ext": f["ext"],
                "vcodec": f["vcodec"],
                "acodec": f["acodec"],
                "resolution": f.get("resolution") or f.get("height"),
                "note": f.get("format_note", ""),
                "filesize": f.get("filesize") or 0,
            }
        )

    return formats


def find_best_audio_format_id(formats: list) -> str | None:
    best_audio = None
    for f in formats:
        if f.get("acodec") != "none" and f.get("vcodec") == "none":
            if f.get("ext") == "m4a":
                return f["format_id"]
            if best_audio is None:
                best_audio = f
    return best_audio["format_id"] if best_audio else None


def download_and_merge(url: str, format_id: str) -> tuple[Path, str]:
    # 1. Lấy metadata
    command = ["yt-dlp", "-j", url]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    info = json.loads(result.stdout)

    formats = info.get("formats", [])
    selected_format = next((f for f in formats if f["format_id"] == format_id), None)
    if not selected_format:
        raise ValueError("Format ID không hợp lệ.")

    has_video = selected_format.get("vcodec") != "none"
    has_audio = selected_format.get("acodec") != "none"

    title = sanitize_filename(info.get("title", "video"))
    ext = selected_format.get("ext", "mp4")
    final_ext = "mp3" if not has_video and has_audio else ext

    session_id = str(uuid.uuid4())
    final_filename = f"{title}.{final_ext}"

    if has_video and has_audio or (not has_video and has_audio):
        output_path = YOUTUBE_DIR / f"{session_id}.{ext}"
        subprocess.run(
            ["yt-dlp", "-f", format_id, "-o", str(output_path), url], check=True
        )

        # Nếu chỉ audio thì chuyển sang mp3
        if not has_video and has_audio and final_ext == "mp3":
            mp3_path = YOUTUBE_DIR / f"{session_id}.mp3"
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    str(output_path),
                    "-vn",
                    "-acodec",
                    "libmp3lame",
                    str(mp3_path),
                ],
                check=True,
            )
            output_path.unlink()
            return mp3_path, final_filename

        return output_path, final_filename

    elif has_video and not has_audio:
        # Ghép audio nếu thiếu
        best_audio_id = find_best_audio_format_id(formats)
        if not best_audio_id:
            raise RuntimeError("Không tìm thấy audio phù hợp để ghép.")

        video_path = YOUTUBE_DIR / f"{session_id}_video.tmp"
        audio_path = YOUTUBE_DIR / f"{session_id}_audio.tmp"
        merged_path = YOUTUBE_DIR / f"{session_id}_merged.mp4"

        subprocess.run(
            ["yt-dlp", "-f", format_id, "-o", str(video_path), url], check=True
        )
        subprocess.run(
            ["yt-dlp", "-f", best_audio_id, "-o", str(audio_path), url], check=True
        )

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                str(video_path),
                "-i",
                str(audio_path),
                "-c",
                "copy",
                str(merged_path),
            ],
            check=True,
        )

        video_path.unlink()
        audio_path.unlink()
        return merged_path, final_filename

    else:
        raise ValueError("Format không hợp lệ (không có video/audio).")
