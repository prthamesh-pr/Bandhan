from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from functools import wraps
import cv2
import numpy as np
import requests
import os
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configure JWT
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your-secret-key-here")

# Configure YOLO
try:
    # First try the temp directory
    yolo_config_dir = "/tmp/Ultralytics"
    os.environ["YOLO_CONFIG_DIR"] = yolo_config_dir
    if not os.path.exists(yolo_config_dir):
        os.makedirs(yolo_config_dir, mode=0o777, exist_ok=True)
except Exception as e:
    print(f"Failed to create directory in /tmp: {str(e)}")
    # Fallback to current working directory
    yolo_config_dir = os.path.join(os.getcwd(), "Ultralytics")
    os.environ["YOLO_CONFIG_DIR"] = yolo_config_dir
    if not os.path.exists(yolo_config_dir):
        os.makedirs(yolo_config_dir, mode=0o777, exist_ok=True)

print(f"Using YOLO config directory: {yolo_config_dir}")

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Mock user database
USERS = {
    "test@example.com": {
        "password": "123456"
    }
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].replace("Bearer ", "")
        
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = USERS.get(data["email"])
            if not current_user:
                return jsonify({"error": "Invalid token"}), 401
        except:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def read_image_from_url(url):
    resp = requests.get(url, stream=True).raw
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    return cv2.imdecode(image, cv2.IMREAD_COLOR)

def read_image_from_file(file):
    npimg = np.frombuffer(file.read(), np.uint8)
    return cv2.imdecode(npimg, cv2.IMREAD_COLOR)

def predict_objects(image):
    try:
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
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return None

@app.route("/login", methods=["POST"])
def login():
    auth = request.json
    if not auth or not auth.get("email") or not auth.get("password"):
        return jsonify({"error": "Missing credentials"}), 401
    
    user = USERS.get(auth["email"])
    if not user or user["password"] != auth["password"]:
        return jsonify({"error": "Invalid credentials"}), 401
    
    token = jwt.encode({
        "email": auth["email"],
        "exp": datetime.utcnow() + timedelta(hours=24)
    }, app.config["SECRET_KEY"])
    
    return jsonify({
        "token": token,
        "email": auth["email"]
    })

@app.route("/predict", methods=["POST", "OPTIONS"])
@token_required
def predict():
    if request.method == "OPTIONS":
        return "", 200
    
    try:
        if "file" in request.files:
            image = read_image_from_file(request.files["file"])
        elif request.is_json and "url" in request.json:
            image = read_image_from_url(request.json["url"])
        else:
            return jsonify({"error": "No image provided. Send file or url."}), 400

        detections = predict_objects(image)
        if detections is None:
            return jsonify({"error": "Error processing image"}), 500

        return jsonify(detections)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", os.getenv("BACKEND_PORT", 5000)))
    debug = os.getenv("BACKEND_DEBUG", "False").lower() == "true"
    app.run(host=host, port=port, debug=debug)
