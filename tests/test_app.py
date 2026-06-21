from pathlib import Path

from fastapi.testclient import TestClient

import app as app_module


def test_health_endpoint():
    client = TestClient(app_module.app)

    response = client.get('/api/health')

    assert response.status_code == 200
    assert response.json() == {'ok': 'true'}


def test_info_endpoint_normalizes_video_id():
    client = TestClient(app_module.app)

    response = client.post('/api/info', json={'url': 'dQw4w9WgXcQ'})

    assert response.status_code == 200
    assert response.json() == {'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}


def test_info_endpoint_rejects_non_youtube_url():
    client = TestClient(app_module.app)

    response = client.post('/api/info', json={'url': 'https://example.com/video'})

    assert response.status_code == 400
    assert 'YouTube' in response.json()['detail']


def test_download_endpoint_returns_generated_file(monkeypatch, tmp_path):
    output = tmp_path / 'sample.mp3'
    output.write_bytes(b'audio-data')

    class DummyTempDir:
        def __init__(self):
            self.cleaned = False

        def cleanup(self):
            self.cleaned = True

    dummy_tempdir = DummyTempDir()

    def fake_download_media(download_request):
        assert download_request.url == 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        assert download_request.format == 'mp3'
        return Path(output), 'Sample Title', dummy_tempdir

    monkeypatch.setattr(app_module, 'download_media', fake_download_media)
    client = TestClient(app_module.app)

    response = client.post('/api/download', json={'url': 'dQw4w9WgXcQ', 'format': 'mp3'})

    assert response.status_code == 200
    assert response.content == b'audio-data'
    assert response.headers['content-type'].startswith('audio/mpeg')
    assert 'Sample%20Title.mp3' in response.headers['content-disposition']
    assert dummy_tempdir.cleaned is True
