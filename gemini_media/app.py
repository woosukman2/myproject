"""제미나이(Gemini) 사진 · 동영상 생성 웹앱 (Flask)

실행 전:
    pip install -r requirements.txt
    export GEMINI_API_KEY="발급받은_키"      # Windows: set GEMINI_API_KEY=발급받은_키
    python app.py
브라우저에서 http://localhost:5000 접속
"""
import os
import time
import uuid

from flask import Flask, jsonify, render_template, request
from google import genai
from google.genai import types

# 모델 이름은 바뀔 수 있으므로 환경변수로 바꿀 수 있게 둡니다.
IMAGE_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image")
VIDEO_MODEL = os.environ.get("GEMINI_VIDEO_MODEL", "veo-3.1-generate-preview")

app = Flask(__name__)
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# GEMINI_API_KEY 환경변수를 자동으로 읽습니다.
client = genai.Client()


@app.route("/")
def home():
    return render_template("index.html", image_model=IMAGE_MODEL, video_model=VIDEO_MODEL)


@app.route("/api/image", methods=["POST"])
def make_image():
    prompt = request.form.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "프롬프트를 입력하세요."}), 400

    try:
        response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=[prompt],
            config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
        )
    except Exception as e:  # API 키 오류, 모델 이름 오류 등
        return jsonify({"error": str(e)}), 500

    text, url = "", None
    for part in response.candidates[0].content.parts:
        if part.text:
            text += part.text
        elif part.inline_data:
            filename = f"img_{uuid.uuid4().hex[:8]}.png"
            with open(os.path.join(STATIC_DIR, filename), "wb") as f:
                f.write(part.inline_data.data)
            url = f"/static/{filename}"

    if not url:
        return jsonify({"error": "이미지가 생성되지 않았습니다.", "text": text}), 500
    return jsonify({"url": url, "text": text})


@app.route("/api/video", methods=["POST"])
def make_video():
    prompt = request.form.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "프롬프트를 입력하세요."}), 400

    try:
        # 동영상은 오래 걸리는 작업(operation)이라 완료될 때까지 기다려야 합니다 (보통 1~6분).
        operation = client.models.generate_videos(model=VIDEO_MODEL, prompt=prompt)
        while not operation.done:
            time.sleep(10)
            operation = client.operations.get(operation)

        if operation.error:
            return jsonify({"error": str(operation.error)}), 500

        video = operation.response.generated_videos[0]
        client.files.download(file=video.video)
        filename = f"vid_{uuid.uuid4().hex[:8]}.mp4"
        video.video.save(os.path.join(STATIC_DIR, filename))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"url": f"/static/{filename}"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
