# YouTube Background Player

Samsung Internet 모바일앱에서 YouTube iframe 재생을 백그라운드로 전환해볼 수 있는 정적 HTML 사이트입니다.

## 실행

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

1. YouTube URL 또는 11자리 영상 ID를 입력합니다.
2. `불러오기`를 누릅니다.
3. 영상이 보이면 `재생`을 사용자가 직접 누릅니다.
4. 홈 화면으로 나가거나 화면을 꺼서 백그라운드 재생 여부를 확인합니다.

## 팁

- 자주 듣는 영상 링크를 넣어두면 다음 접속 때 자동으로 기억됩니다.
- `미니모드`를 누르면 작은 플레이어로 화면에 유지할 수 있습니다.
- 화면을 다시 열었을 때 멈춰 있으면 `재생`을 한 번 더 눌러주세요.
