from app.adapters.platforms import youtube_adapter, facebook_adapter, tiktok_adapter
from pathlib import Path


def detect_platform(url: str) -> str:
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "tiktok.com" in url:
        return "tiktok"
    elif "facebook.com" in url or "fb.watch" in url:
        return "facebook"
    return "unknown"


def download_and_merge(url: str, format_id: str) -> tuple[Path, str]:
    platform = detect_platform(url)
    if platform == "youtube":
        return youtube_adapter.download_and_merge(url, format_id)
    elif platform == "facebook":
        return facebook_adapter.download_and_merge(url, format_id)
    elif platform == "tiktok":
        return tiktok_adapter.download_and_merge(url, format_id)
    else:
        raise ValueError("Nền tảng chưa được hỗ trợ")
