# YOLOv8 Object Detection API

This project provides a simple REST API for object detection using YOLOv8 (Ultralytics). Users can either upload an image file or provide a URL to an image, and the API returns detected objects in JSON format.

---

## 🔧 Setup

### 1. Clone the repository and install dependencies:

```bash

pip install -r requirements.txt

```

### 2.Activate ENV:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Run the code:

```bash

python main.py

```

### 4. API Request:

```bash

curl -X POST -H "Content-Type: application/json" \
     -d '{"url": "https://c.pxhere.com/photos/10/ab/highway_travel_ride_reindeer_autos_traffic_vehicles_motor_vehicles_multi_track-1393510.jpg!d"}' \
     http://127.0.0.1:5000/predict

```

## Output:

```bash

[
  {
    "bbox": {
      "x1": 610.82,
      "x2": 833.53,
      "y1": 700.59,
      "y2": 881.39
    },
    "class_id": 2,
    "class_name": "car",
    "confidence": 0.931
  },
  
]

```

