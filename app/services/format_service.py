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


def get_formats(url: str, impersonate_client: str) -> list[dict]:
    platform = detect_platform(url)
    print(platform)
    if platform == "youtube":
        return youtube_adapter.get_formats(url,impersonate_client)
    elif platform == "facebook":
        return facebook_adapter.get_formats(url,impersonate_client)
    elif platform == "tiktok":
        return tiktok_adapter.get_formats(url,impersonate_client)
    else:
        raise ValueError("Nền tảng chưa được hỗ trợ")
