from app.services.download_service import get_video_info


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
