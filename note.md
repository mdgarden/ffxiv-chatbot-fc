# Dev / Production 환경변수 분리

## 상황

- Production용 라인 챗봇과 Dev용 라인 챗봇이 따로 있음
- 서로 다른 챗봇이기 때문에 다른 환경변수를 이용할 필요가 있음
- 특히나 dev의 경우, ngrok를 사용하기 때문에 변수가 자주 바뀜. 반드시 분리를 해야 원활하게 테스트를 진행하며 개발을 할 수 있음.

## 문제

- 일반적인 flask의 템플릿을 따르지 않고 있기 때문에 인터넷의 샘플 코드들을 따라하기가 어려움
- 애초에 flask와 그를 포함한 다른 프레임워크들이 어떻게 dev/production을 구분하는지 모르겠음

## 해결법

- 조사중

# TODO

- Procfile, Pipfile, runtime.txt, requirements.txt 정리
- 대대적 리모델링
  - 트위터 업뎃기능
  - 각종 이슈 처리 등등
