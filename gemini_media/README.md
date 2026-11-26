# 제미나이 사진 · 동영상 생성기

Gemini API로 **사진(Nano Banana)** 과 **동영상(Veo)** 을 만드는 Flask 웹앱입니다.

## 1. API 키 발급
1. https://aistudio.google.com/apikey 접속 → 구글 계정 로그인
2. **Create API key** 클릭 → 키 복사
3. 동영상(Veo)은 **유료(결제 등록) 프로젝트**에서만 됩니다. 사진은 무료 등급에서도 사용량 제한 안에서 가능합니다.

> 키는 코드에 직접 쓰지 말고 환경변수로 넣으세요. GitHub에 올리면 유출됩니다.

## 2. 설치 및 실행
```bash
cd gemini_media
pip install -r requirements.txt

# macOS / Linux
export GEMINI_API_KEY="발급받은_키"
# Windows (cmd)
set GEMINI_API_KEY=발급받은_키

python app.py
```
브라우저에서 http://localhost:5000 접속 → 프롬프트 입력 → 버튼 클릭.
생성된 파일은 `static/` 폴더에 저장됩니다.

## 3. 핵심 코드
```python
from google import genai
from google.genai import types
client = genai.Client()  # GEMINI_API_KEY 자동 사용

# 사진
res = client.models.generate_content(
    model="gemini-3.1-flash-image",
    contents=["우주복 입은 고양이"],
    config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
)

# 동영상 (오래 걸리는 작업 → 완료될 때까지 기다림)
op = client.models.generate_videos(model="veo-3.1-generate-preview", prompt="달리는 강아지")
while not op.done:
    time.sleep(10)
    op = client.operations.get(op)
```

## 4. 모델 바꾸기
모델 이름은 자주 바뀝니다. 최신 목록: https://ai.google.dev/gemini-api/docs/models
```bash
export GEMINI_IMAGE_MODEL="gemini-3-pro-image"        # 고품질 사진 (Nano Banana Pro)
export GEMINI_VIDEO_MODEL="veo-3.1-lite-generate-preview"  # 저렴한 동영상
```

## 자주 나는 오류
| 오류 | 원인 |
|---|---|
| `API key not valid` | 키가 틀렸거나 환경변수가 설정되지 않음 |
| `404 model not found` | 모델 이름이 바뀜 → 위 4번 참고 |
| `429 RESOURCE_EXHAUSTED` | 무료 사용량 초과 / 동영상은 결제 등록 필요 |
