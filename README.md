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

## 팁

- 자주 듣는 영상 링크를 넣어두면 다음 접속 때 자동으로 기억됩니다.
- `미니모드`를 누르면 작은 플레이어로 화면에 유지할 수 있습니다.
- 화면을 다시 열었을 때 멈춰 있으면 `재생`을 한 번 더 눌러주세요.
- Samsung Internet의 브라우저 어시스턴트 기능을 같이 사용할 수 있습니다.
