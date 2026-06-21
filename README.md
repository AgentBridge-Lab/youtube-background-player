# YouTube Background Player

Samsung Internet 모바일앱에서 YouTube 영상을 백그라운드로 들을 수 있게 만든 간단한 웹 플레이어입니다.

삼성브라우저에서 YouTube 웹사이트를 직접 열면 백그라운드 재생이 막혀 있어 불편한 경우가 있습니다. 이 페이지는 그런 상황에서 휴대폰으로 다른 앱을 쓰는 동안에도 YouTube 영상을 계속 듣기 위해 만들었습니다.

Samsung Internet의 브라우저 어시스턴트 기능도 함께 이용할 수 있습니다.

## 접속

GitHub Pages 주소:

```text
https://agentbridge-lab.github.io/youtube-background-player/
```

로컬에서 실행하려면:

```bash
cd /Users/ldh/youtube-background-player
python3 -m http.server 8088
```

브라우저에서:

```text
http://localhost:8088
```

같은 Wi-Fi의 휴대폰에서 테스트하려면 Mac의 로컬 IP를 확인한 뒤:

```bash
ipconfig getifaddr en0
```

휴대폰 Samsung Internet에서:

```text
http://<Mac의 IP>:8088
```

## 사용법

1. Samsung Internet에서 사이트를 엽니다.
2. YouTube URL 또는 11자리 영상 ID를 입력합니다.
3. `불러오기`를 누릅니다.
4. 영상이 보이면 `재생`을 직접 누릅니다.
5. 홈 화면으로 나가거나 다른 앱을 열어 YouTube 소리가 계속 재생되는지 확인합니다.

## MP3 / MP4 다운로드 기능

다운로드 기능은 [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)를 사용하는 FastAPI 백엔드가 필요합니다. GitHub Pages는 정적 호스팅만 지원하므로, Pages 주소만으로는 다운로드 API가 실행되지 않습니다.

로컬에서 플레이어와 다운로드 API를 함께 실행하려면:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8088
```

브라우저에서:

```text
http://localhost:8088
```

같은 Wi-Fi의 휴대폰에서 테스트하려면 Mac의 로컬 IP를 확인한 뒤:

```bash
ipconfig getifaddr en0
```

휴대폰 Samsung Internet에서:

```text
http://<Mac의 IP>:8088
```

### API

- `GET /api/health`: 다운로드 API 상태 확인
- `POST /api/info`: YouTube URL/영상 ID 정규화
- `POST /api/download`: MP3 또는 MP4 파일 생성 후 반환

요청 예시:

```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "format": "mp3"
}
```

지원 형식은 `mp3`, `mp4`입니다. 서버 남용을 줄이기 위해 현재 구현은 단일 영상만 처리하며 재생목록 다운로드는 비활성화되어 있습니다.

## 주의

본인이 권리를 보유했거나 다운로드가 허용된 콘텐츠에만 사용하세요. 공개 서비스로 운영할 경우 저작권, YouTube 이용약관, 트래픽 비용, 서버 남용 방지 정책을 별도로 검토해야 합니다.

## 팁

- 자주 듣는 영상 링크를 넣어두면 다음 접속 때 자동으로 기억됩니다.
- `미니모드`를 누르면 작은 플레이어로 화면에 유지할 수 있습니다.
- 화면을 다시 열었을 때 멈춰 있으면 `재생`을 한 번 더 눌러주세요.
- Samsung Internet의 브라우저 어시스턴트 기능을 같이 사용할 수 있습니다.
- GitHub Pages 화면에서 별도 다운로드 서버를 연결하려면 브라우저 콘솔에서 `localStorage.setItem('ytbg:apiBase', 'https://다운로드서버주소')`를 설정한 뒤 새로고침하세요.
