from __future__ import annotations

import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import yt_dlp

SUPPORTED_FORMATS = {"mp3", "mp4"}
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
}


@dataclass(frozen=True)
class DownloadRequest:
    url: str
    format: str

    def __post_init__(self) -> None:
        fmt = (self.format or "").lower().strip()
        if fmt not in SUPPORTED_FORMATS:
            raise ValueError("지원 형식은 mp3 또는 mp4입니다.")
        normalized_url = normalize_youtube_url(self.url)
        object.__setattr__(self, "format", fmt)
        object.__setattr__(self, "url", normalized_url)


def normalize_youtube_url(value: str) -> str:
    """Return a canonical single-video YouTube watch URL or raise ValueError."""
    raw = (value or "").strip()
    if not raw:
        raise ValueError("YouTube URL 또는 영상 ID가 필요합니다.")
    if VIDEO_ID_RE.fullmatch(raw):
        return f"https://www.youtube.com/watch?v={raw}"

    parsed = urlparse(raw)
    host = parsed.netloc.lower()
    if host not in YOUTUBE_HOSTS:
        raise ValueError("YouTube 링크만 사용할 수 있습니다.")

    video_id: str | None = None
    if host == "youtu.be":
        video_id = parsed.path.strip("/").split("/")[0]
    else:
        query = parse_qs(parsed.query)
        if query.get("v"):
            video_id = query["v"][0]
        else:
            parts = [part for part in parsed.path.split("/") if part]
            for marker in ("embed", "shorts", "live"):
                if marker in parts:
                    idx = parts.index(marker)
                    if idx + 1 < len(parts):
                        video_id = parts[idx + 1]
                        break

    if not video_id or not VIDEO_ID_RE.fullmatch(video_id):
        raise ValueError("유효한 YouTube 영상 ID를 찾지 못했습니다.")
    return f"https://www.youtube.com/watch?v={video_id}"


def build_yt_dlp_options(request: DownloadRequest, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    common: dict[str, Any] = {
        "outtmpl": str(output_dir / "%(title).200B-%(id)s.%(ext)s"),
        "noplaylist": True,
        "restrictfilenames": True,
        "quiet": True,
        "no_warnings": True,
        "max_filesize": 500 * 1024 * 1024,
    }

    if request.format == "mp3":
        return {
            **common,
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

    return {
        **common,
        "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best",
        "merge_output_format": "mp4",
    }


def download_media(request: DownloadRequest) -> tuple[Path, str, tempfile.TemporaryDirectory[str]]:
    """Download one video and return (file_path, display_title, tempdir_handle)."""
    tempdir = tempfile.TemporaryDirectory(prefix="ytbg-")
    output_dir = Path(tempdir.name)
    opts = build_yt_dlp_options(request, output_dir)

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(request.url, download=True)
            safe_info = ydl.sanitize_info(info)

        video_id = str(safe_info.get("id") or "")
        title = str(safe_info.get("title") or "youtube-download")
        candidates = sorted(
            output_dir.glob(f"*-{video_id}.{request.format}") if video_id else output_dir.glob(f"*.{request.format}"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        if not candidates:
            candidates = sorted(output_dir.glob(f"*.{request.format}"), key=lambda path: path.stat().st_mtime, reverse=True)
        if not candidates:
            raise RuntimeError("다운로드 결과 파일을 찾지 못했습니다.")
        return candidates[0], title, tempdir
    except Exception:
        tempdir.cleanup()
        raise
