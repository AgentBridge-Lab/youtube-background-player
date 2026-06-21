from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = (ROOT / "index.html").read_text(encoding="utf-8")


def test_homepage_has_no_default_youtube_video():
    assert "const DEFAULT_VIDEO = 'dQw4w9WgXcQ';" not in INDEX_HTML
    assert "https://www.youtube.com/watch?v=' + currentVideo" not in INDEX_HTML


def test_homepage_only_saves_video_when_one_is_selected():
    assert "if (currentVideo) {" in INDEX_HTML
    assert "saveCurrent(currentVideo, els.input.value);" in INDEX_HTML
    assert "주소를 넣고 불러오기를 눌러주세요." in INDEX_HTML
