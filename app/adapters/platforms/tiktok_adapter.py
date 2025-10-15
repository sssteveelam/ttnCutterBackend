import subprocess
import json
import uuid
from pathlib import Path
import re
from app.services.download_service import get_video_info

TT_DIR = Path("./temp_videos/tiktok")
TT_DIR.mkdir(parents=True, exist_ok=True)


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


def download_and_merge(url: str, format_id: str) -> tuple[Path, str]:
    try:
        # 1. Lấy metadata video
        info_command = [
            "yt-dlp",
            "-j",
            url,
        ]
        result = subprocess.run(
            info_command, capture_output=True, text=True, check=True, encoding="utf-8"
        )

        info = json.loads(result.stdout)
        formats = info.get("formats", [])
        selected_format = next(
            (f for f in formats if f["format_id"] == format_id), None
        )

        if not selected_format:
            raise ValueError("Format id không hợp lệ.")

        format_selector = format_id

        # 2. Nếu chỉ có video thì ghép audio
        if selected_format.get("acodec") == "none":
            audio_formats = [
                f
                for f in formats
                if f.get("vcodec") == "none" and f.get("acodec") != "none"
            ]
            if audio_formats:
                best_audio = max(audio_formats, key=lambda f: f.get("abr", 0))
                best_audio_id = best_audio["format_id"]
                format_selector = f"{format_id}+{best_audio_id}"
                print(f"Chọn thêm audio: {best_audio_id} → merge: {format_selector}")

        # 3. Tạo tên và đường dẫn file
        title = sanitize_filename(info.get("title", "video"))
        ext = info.get("ext", "mp4")
        session_id = str(uuid.uuid4())
        final_filename = f"{title}.{ext}"
        output_path_template = TT_DIR / f"{session_id}.%(ext)s"
        final_path = TT_DIR / f"{session_id}.mp4"

        # 4. Tải và merge video
        download_command = [
            "yt-dlp",
            "--impersonate",
            "chrome",
            "--limit-rate",
            "2M",
            "--throttled-rate",
            "500K",
            "--http-chunk-size",
            "1M",
            "--sleep-interval",
            "1",
            "--max-sleep-interval",
            "3",
            "-f",
            format_selector,
            "-o",
            str(output_path_template),
            "--merge-output-format",
            "mp4",
            url,
        ]

        print("▶️ Lệnh tải video:")
        print(" ".join(download_command))

        subprocess.run(download_command, check=True)

        if not final_path.exists():
            raise FileNotFoundError("Không tìm thấy file video sau khi tải và merge.")

        return final_path, final_filename

    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi yt-dlp (exit code {e.returncode}):")
        print(e.stderr)
        raise RuntimeError("Lỗi khi tải video từ TikTok.")
