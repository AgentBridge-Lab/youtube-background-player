import pytest

from downloader import DownloadRequest, build_yt_dlp_options, normalize_youtube_url


def test_normalize_youtube_url_accepts_video_id():
    assert normalize_youtube_url("dQw4w9WgXcQ") == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def test_normalize_youtube_url_accepts_standard_youtube_url():
    assert normalize_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=abc") == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def test_normalize_youtube_url_accepts_short_url():
    assert normalize_youtube_url("https://youtu.be/dQw4w9WgXcQ?t=10") == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def test_normalize_youtube_url_rejects_non_youtube_url():
    with pytest.raises(ValueError, match="YouTube"):
        normalize_youtube_url("https://example.com/watch?v=dQw4w9WgXcQ")


def test_download_request_rejects_unsupported_format():
    with pytest.raises(ValueError, match="mp3 또는 mp4"):
        DownloadRequest(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", format="wav")


def test_build_mp3_options_extracts_audio(tmp_path):
    request = DownloadRequest(url="dQw4w9WgXcQ", format="mp3")

    opts = build_yt_dlp_options(request, tmp_path)

    assert opts["format"] == "bestaudio/best"
    assert opts["noplaylist"] is True
    assert opts["postprocessors"][0]["key"] == "FFmpegExtractAudio"
    assert opts["postprocessors"][0]["preferredcodec"] == "mp3"


def test_build_mp4_options_limits_to_single_video(tmp_path):
    request = DownloadRequest(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=playlist", format="mp4")

    opts = build_yt_dlp_options(request, tmp_path)

    assert opts["format"] == "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best"
    assert opts["merge_output_format"] == "mp4"
    assert opts["noplaylist"] is True
    assert str(tmp_path) in opts["outtmpl"]
