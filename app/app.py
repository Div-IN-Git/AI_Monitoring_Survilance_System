from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import cv2, asyncio
from ultralytics import YOLO

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", "r") as f:
        return f.read()

# Load models
fire = YOLO("models/fire/best.pt")
smoke = YOLO("models/smoke/best.pt")
helmet = YOLO("models/helmet/best.pt")
accident = YOLO("models/accident/best.pt")

MODELS = [fire, smoke, helmet, accident]

@app.get("/webcam")
def webcam():

    async def stream():
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            for model in MODELS:
                results = model(frame, verbose=False)
                frame = results[0].plot()

            _, jpeg = cv2.imencode(".jpg", frame)

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + jpeg.tobytes() +
                b"\r\n"
            )

            await asyncio.sleep(0.03)

    return StreamingResponse(
        stream(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )