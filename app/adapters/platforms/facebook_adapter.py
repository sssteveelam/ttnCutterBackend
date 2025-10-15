"""Helpers for downloading Facebook videos with yt-dlp."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable

FACEBOOK_DOMAINS: tuple[str, ...] = (
    "facebook.com",
    "fb.watch",
    "fb.com",
)


def supports(url: str) -> bool:
    """Return True when the url looks like a Facebook video link."""
    lowered = url.lower()
    return any(domain in lowered for domain in FACEBOOK_DOMAINS)


def build_download_command(url: str, output_path: Path, format_id: str | None = None) -> list[str]:
    """Compose the yt-dlp command used to download a Facebook video."""
    command: list[str] = ["yt-dlp", url, "-o", str(output_path)]
    if format_id:
        command.extend(["-f", format_id])
    return command


def run_download(command: Iterable[str]) -> None:
    """Execute the given download command."""
    printable = " ".join(str(part) for part in command)
    print(f"Dang thuc thi lenh: {printable}")
    subprocess.run(list(command), check=True)


def download_video(url: str, output_path: Path, format_id: str | None = None) -> Path:
    """Download a Facebook video to ``output_path`` and return the path."""
    command = build_download_command(url, output_path, format_id)
    run_download(command)
    return output_path


__all__ = [
    "supports",
    "build_download_command",
    "run_download",
    "download_video",
]
