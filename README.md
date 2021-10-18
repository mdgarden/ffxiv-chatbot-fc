## LINE ChatBot for FFXIV FreeCompany⚔

### 20/10/03 ~ in progress

#### 🎨Features layout

- [x] Search Items in FFXIV DB
- [ ] Notice Maintenance, Mog Station Updates, Events, forums, etc.
- [x] Get personal schedule and information by Lodestone

#### 테스트 방법

1. 반드시 현재 브랜치가 **linkshell_dev**인지 확인할 것
2. app.py 실행
3. **ngrok http 9000** 실행 _app.py의 PORT주소와 맞출 것_
4. 라인 개발자 콘솔  → 테스트봇 웹훅 주소에 "Forwarding 주소"+"/callback" 입력
5. ngrok 서버 유효시간 1시간
6. app.py / config.py는 커밋하지말 것

#### 모하지리스트

- dev브랜치 분리방법찾기
