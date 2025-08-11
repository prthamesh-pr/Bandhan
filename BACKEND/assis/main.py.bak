from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import numpy as np
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

def read_image_from_url(url):
    resp = requests.get(url, stream=True).raw
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    return cv2.imdecode(image, cv2.IMREAD_COLOR)

def read_image_from_file(file):
    npimg = np.frombuffer(file.read(), np.uint8)
    return cv2.imdecode(npimg, cv2.IMREAD_COLOR)

def predict_objects(image):
    results = model.predict(source=image)
    json_output = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()

            json_output.append({
                "class_id": class_id,
                "class_name": model.names[class_id],
                "confidence": round(conf, 3),
                "bbox": {
                    "x1": round(xyxy[0], 2),
                    "y1": round(xyxy[1], 2),
                    "x2": round(xyxy[2], 2),
                    "y2": round(xyxy[3], 2)
                }
            })
    return json_output

@app.route("/predict", methods=["POST"])
def predict():
    if "file" in request.files:
        image = read_image_from_file(request.files["file"])
    elif "url" in request.json:
        image = read_image_from_url(request.json["url"])
    else:
        return jsonify({"error": "No image provided. Send 'file' or 'url'."}), 400

    detections = predict_objects(image)
    return jsonify(detections)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", 5000))
    debug = os.getenv("BACKEND_DEBUG", "True") == "True"
    app.run(host=host, port=port, debug=debug)
