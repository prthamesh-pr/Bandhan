# Bandhan - Mobile Object Detection App

A mobile application for object detection using YOLOv8, built with Flutter frontend and Flask backend.

## Project Structure

```
BANDHAN/
├── BACKEND/
│   └── assis/
│       ├── main.py          # Flask backend with YOLOv8
│       ├── requirements.txt # Python dependencies
│       ├── render.yaml     # Render deployment config
│       └── yolov8n.pt     # YOLOv8 model file
└── FRONTEND/
    ├── lib/                # Flutter source code
    ├── android/           # Android specific files
    ├── ios/              # iOS specific files
    └── pubspec.yaml      # Flutter dependencies
```

## Backend Setup

### Prerequisites
- Python 3.9+
- pip (Python package manager)

### Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/prthamesh-pr/Bandhan.git
cd Bandhan/BACKEND/assis
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python main.py
```

The backend server will start on `http://localhost:5000`

### Backend API Endpoints

#### 1. Login
- **URL**: `/login`
- **Method**: `POST`
- **Body**:
```json
{
    "email": "test@example.com",
    "password": "123456"
}
```
- **Response**:
```json
{
    "token": "your-jwt-token",
    "email": "test@example.com"
}
```

#### 2. Predict
- **URL**: `/predict`
- **Method**: `POST`
- **Headers**:
  - `Authorization: Bearer your-jwt-token`
- **Body** (URL):
```json
{
    "url": "https://example.com/image.jpg"
}
```
- **Body** (File): `multipart/form-data` with key "file"
- **Response**:
```json
[
    {
        "class_id": 0,
        "class_name": "person",
        "confidence": 0.954,
        "bbox": {
            "x1": 100.25,
            "y1": 200.75,
            "x2": 300.50,
            "y2": 400.25
        }
    }
]
```

#### 3. Health Check
- **URL**: `/health`
- **Method**: `GET`
- **Response**:
```json
{
    "status": "healthy",
    "model_loaded": true,
    "config_dir": "/tmp/Ultralytics"
}
```

## Frontend Setup

### Prerequisites
- Flutter SDK 3.0+
- Android Studio / Xcode (for mobile development)

### Installation & Setup

1. Navigate to the frontend directory:
```bash
cd Bandhan/FRONTEND
```

2. Get Flutter dependencies:
```bash
flutter pub get
```

3. Run the app:
```bash
flutter run
```

## Test Credentials

For testing the application, use these hardcoded credentials:
- **Email**: `test@example.com`
- **Password**: `123456`

## Deployment

### Backend Deployment (Render)
The backend is configured to deploy on Render using the provided `render.yaml` file.

1. Fork/Clone the repository
2. Connect your Render account
3. Create a new Web Service using the repo
4. Render will automatically use the configuration from `render.yaml`

Current deployed URL: `https://bandhan-4dqo.onrender.com`

### Frontend Deployment
The Flutter app can be built for various platforms:

- Android:
```bash
flutter build apk --release
```

- iOS:
```bash
flutter build ios --release
```

## Dependencies

### Backend Dependencies
- Flask
- Flask-CORS
- YOLOv8 (ultralytics)
- OpenCV
- NumPy
- PyJWT
- python-dotenv
- waitress (production server)

### Frontend Dependencies
- Flutter SDK
- http package (API calls)
- image_picker (camera/gallery access)
- provider (state management)

## Features
- User authentication with JWT
- Image capture from camera
- Image selection from gallery
- Real-time object detection
- Display of detection results with confidence scores
- Error handling and loading states

## Contributing
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License
This project is licensed under the MIT License.
