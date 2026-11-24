# ANIMAL PATH — Streamlit starter

## 실행 방법
1. Python 3.9 이상 설치
2. 터미널에서 프로젝트 폴더로 이동
3. 아래 명령 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 파일 구성
- `app.py`: 화면 흐름, UI, CSS 애니메이션
- `questions.py`: 질문과 선택지
- `results.py`: 성향 점수 계산 및 결과 유형
- `requirements.txt`: 필요한 패키지

## 참고
현재 버전은 이미지 파일 대신 이모지와 CSS로 숲/캐릭터의 기본 움직임을 표현한 프로토타입입니다.
실제 동물 일러스트와 스프라이트 애니메이션을 준비하면 `app.py`의 캐릭터 표시 부분을 이미지 기반으로 교체할 수 있습니다.
