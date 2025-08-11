# Object Detection Mobile App

A Flutter mobile application that uses YOLOv8-powered API for real-time object detection with user authentication.

## Features

- **User Authentication**: Simple login/signup with hardcoded credentials
- **Image Capture/Upload**: Take photos with camera or select from gallery
- **Object Detection**: Analyze images using YOLOv8 API
- **Results Display**: View detected objects with confidence scores
- **Clean UI**: Modern, intuitive user interface

## Screenshots

### Login Screen
- Clean authentication interface
- Demo credentials displayed for easy testing
- Form validation and loading states

### Detection Screen
- Image preview before analysis
- Camera and gallery selection options
- Real-time analysis with loading indicators
- Detailed results with confidence scores

## Setup Instructions

### Prerequisites

1. **Flutter SDK**: Install Flutter (latest stable version)
   ```bash
   flutter --version
   ```

2. **Development Environment**: 
   - Android Studio or VS Code with Flutter extension
   - Android SDK for Android development
   - Xcode for iOS development (Mac only)

### Installation

1. **Clone and Navigate**:
   ```bash
   git clone <repository-url>
   cd bandhan
   ```

2. **Install Dependencies**:
   ```bash
   flutter pub get
   ```

3. **Run the App**:
   ```bash
   # For Android
   flutter run

   # For iOS (Mac only)
   flutter run -d ios
   
   # For a specific device
   flutter devices
   flutter run -d <device-id>
   ```

### Configuration

#### API Integration
To connect to your YOLOv8 API, update the `baseUrl` in `lib/services/object_detection_service.dart`:

```dart
static const String baseUrl = 'https://your-api-url.com';
```

**Note**: The app currently includes mock data for testing when the API is not available.

#### Authentication
The app uses hardcoded credentials for demo purposes:
- **Email**: `test@example.com`
- **Password**: `123456`

To modify credentials, edit `lib/services/auth_service.dart`:

```dart
static const String validEmail = 'your-email@example.com';
static const String validPassword = 'your-password';
```

## Dependencies

### Core Dependencies
- `flutter`: SDK framework
- `http`: HTTP requests for API communication
- `image_picker`: Camera and gallery access
- `shared_preferences`: Local storage for authentication
- `path_provider`: File system access

### Dev Dependencies
- `flutter_test`: Testing framework
- `flutter_lints`: Code quality and style

## Project Structure

```
lib/
├── main.dart                 # App entry point and splash screen
├── services/                 # Business logic and API services
│   ├── auth_service.dart    # Authentication management
│   └── object_detection_service.dart  # API communication
└── screens/                  # UI screens
    ├── login_screen.dart    # Authentication interface
    └── detection_screen.dart # Main detection interface
```

## API Integration

### Expected API Format

The app expects the YOLOv8 API to accept:
- **Method**: POST
- **Endpoint**: `/predict`
- **Content-Type**: `multipart/form-data`
- **Body**: Image file with key `image`

### Expected Response Format

```json
{
  "detections": [
    {
      "class": "person",
      "confidence": 0.95
    },
    {
      "class": "car", 
      "confidence": 0.87
    }
  ]
}
```

Alternative format (array directly):
```json
[
  {
    "name": "person",
    "confidence": 0.95
  },
  {
    "name": "car",
    "confidence": 0.87
  }
]
```

## Login Credentials

For testing purposes, use these hardcoded credentials:
- **Email**: `test@example.com`
- **Password**: `123456`

## Testing

### Manual Testing
1. **Authentication**: Test login with correct/incorrect credentials
2. **Image Selection**: Test camera and gallery functionality  
3. **Detection**: Test image analysis with various image types
4. **Error Handling**: Test without internet connection

### Unit Testing
```bash
flutter test
```

## Troubleshooting

### Common Issues

1. **Camera Permission Denied**
   - Ensure camera permissions are granted in device settings
   - Check `android/app/src/main/AndroidManifest.xml` for Android
   - Check `ios/Runner/Info.plist` for iOS

2. **Network Issues**
   - Verify internet connection
   - Check API endpoint URL
   - Review API key/authentication if required

3. **Build Errors**
   - Run `flutter clean` and `flutter pub get`
   - Update Flutter SDK: `flutter upgrade`
   - Check platform-specific setup

### Platform Permissions

#### Android (`android/app/src/main/AndroidManifest.xml`)
```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.INTERNET" />
```

#### iOS (`ios/Runner/Info.plist`)
```xml
<key>NSCameraUsageDescription</key>
<string>This app needs access to camera to take photos for object detection.</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>This app needs access to photo library to select images for object detection.</string>
```

## Demo Video

Record a demo showing:
1. App launch and splash screen
2. Login process
3. Image selection (camera/gallery)
4. Object detection analysis
5. Results display
6. Logout functionality

## Future Enhancements

- Real backend authentication
- Image history/favorites
- Offline detection capability
- Advanced filtering and search
- Social sharing features
- Multi-language support

## License

This project is developed for evaluation purposes.

## Support

For issues or questions:
1. Check troubleshooting section
2. Review Flutter documentation
3. Check API documentation
4. Test with mock data first
