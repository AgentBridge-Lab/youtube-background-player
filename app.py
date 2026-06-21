from __future__ import annotations

import re
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from downloader import DownloadRequest, download_media, normalize_youtube_url

ROOT = Path(__file__).resolve().parent

app = FastAPI(title="YouTube Background Player API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

_SAFE_FILENAME_RE = re.compile(r"[^A-Za-z0-9가-힣._ -]+")


def safe_download_name(title: str, fmt: str) -> str:
    cleaned = _SAFE_FILENAME_RE.sub(" ", title).strip().strip(".")
    cleaned = re.sub(r"\s+", " ", cleaned)[:120] or "youtube-download"
    return f"{cleaned}.{fmt}"


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"ok": "true"}


@app.post("/api/info")
async def info(request: Request) -> dict[str, str]:
    payload = await request.json()
    try:
        return {"url": normalize_youtube_url(str(payload.get("url", "")))}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/download")
async def download(request: Request, background_tasks: BackgroundTasks) -> FileResponse:
    payload = await request.json()
    try:
        download_request = DownloadRequest(
            url=str(payload.get("url", "")),
            format=str(payload.get("format", "")).lower(),
        )
        file_path, title, tempdir = download_media(download_request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"다운로드 처리에 실패했습니다: {exc}") from exc

    background_tasks.add_task(tempdir.cleanup)
    return FileResponse(
        path=file_path,
        media_type="audio/mpeg" if download_request.format == "mp3" else "video/mp4",
        filename=safe_download_name(title, download_request.format),
        background=background_tasks,
    )


app.mount("/", StaticFiles(directory=ROOT, html=True), name="static")
