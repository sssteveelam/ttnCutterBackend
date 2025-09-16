# services.py
import subprocess
import json
import uuid
from pathlib import Path

VIDEO_DIR = Path("./temp_videos")
VIDEO_DIR.mkdir(exist_ok=True)


def get_video_info(url: str) -> dict:
    command = ["yt-dlp", "-j", str(url)]
    result = subprocess.run(
        command, capture_output=True, text=True, check=True, encoding="utf-8"
    )
    return json.loads(result.stdout)


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

    video_info = get_video_info(url)
    formats = video_info.get("formats", [])

    selected_format = next((f for f in formats if f["format_id"] == format_id), None)

    if not selected_format:
        raise ValueError("Format ID không hợp lệ.")

    has_video = selected_format.get("vcodec") != "none"
    has_audio = selected_format.get("acodec") != "none"

    video_title = video_info.get("title", "video")
    safe_filename = "".join(
        [c for c in video_title if c.isalpha() or c.isdigit() or c.isspace()]
    ).rstrip()
    final_ext = "mp3" if not has_video and has_audio else "mp4"
    final_filename = f"{safe_filename}.{final_ext}"

    session_id = str(uuid.uuid4())

    if (has_video and has_audio) or (not has_video and has_audio):
        output_path = VIDEO_DIR / f"{session_id}.{selected_format.get('ext', 'tmp')}"
        command = ["yt-dlp", "-f", format_id, "-o", str(output_path), str(url)]
        subprocess.run(command, check=True)
        if not has_video and has_audio and final_ext == "mp3":
            final_output_path = VIDEO_DIR / f"{session_id}.mp3"
            ffmpeg_cmd = [
                "ffmpeg",
                "-i",
                str(output_path),
                "-vn",
                "-acodec",
                "libmp3lame",
                str(final_output_path),
            ]
            subprocess.run(ffmpeg_cmd, check=True)
            # output_path.unlink()
            return final_output_path, final_filename
        return output_path, final_filename

    elif has_video and not has_audio:
        best_audio_id = find_best_audio_format_id(formats)
        if not best_audio_id:
            raise RuntimeError("Không tìm thấy luồng audio phù hợp để ghép.")

        video_path = VIDEO_DIR / f"{session_id}_video.tmp"
        audio_path = VIDEO_DIR / f"{session_id}_audio.tmp"
        final_output_path = VIDEO_DIR / f"{session_id}.mp4"

        subprocess.run(
            ["yt-dlp", "-f", format_id, "-o", str(video_path), str(url)], check=True
        )
        subprocess.run(
            ["yt-dlp", "-f", best_audio_id, "-o", str(audio_path), str(url)], check=True
        )

        ffmpeg_cmd = [
            "ffmpeg",
            "-i",
            str(video_path),
            "-i",
            str(audio_path),
            "-c",
            "copy",
            str(final_output_path),
        ]
        subprocess.run(ffmpeg_cmd, check=True)

        video_path.unlink()
        audio_path.unlink()

        return final_output_path, final_filename

    else:
        raise ValueError("Format không hợp lệ (không có cả video và audio).")
