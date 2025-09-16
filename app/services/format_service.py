import yt_dlp


def get_formats(url: str) -> list[dict]:
    ydl_opts = {
        "skip_download": True,
        "forcejson": True,
        "simulate": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        formats = []
        for f in info.get("formats", []):

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
