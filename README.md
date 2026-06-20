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

## 제한

- YouTube 공식 IFrame API만 사용합니다.
- 영상/음성 다운로드, 추출, 우회 재생은 하지 않습니다.
- 백그라운드 재생 지속 여부는 Samsung Internet, Android, YouTube 정책에 따라 달라질 수 있습니다.
- 모바일 브라우저 정책상 자동재생은 제한되므로 사용자의 직접 터치가 필요합니다.
