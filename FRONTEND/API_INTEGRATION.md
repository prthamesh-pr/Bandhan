# API Integration Guide

## YOLOv8 API Integration

### Required API Endpoint
The app is designed to work with the YOLOv8 Flask API from: https://github.com/PlanetDestroyyer/assis

### API Configuration

1. **Update the API URL** in `lib/services/object_detection_service.dart`:
```dart
static const String baseUrl = 'https://your-actual-api-url.com';
```

2. **Expected API Behavior**:
   - **Endpoint**: `POST /predict`
   - **Content-Type**: `multipart/form-data`
   - **Request Body**: Image file with key `image`
   - **Response**: JSON with detected objects

### Expected Response Formats

#### Format 1 (Preferred):
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

#### Format 2 (Alternative):
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

## Mock Data

When the API is unavailable, the app will show mock detection results:
- Person (95% confidence)
- Car (87% confidence)
- Dog (78% confidence)

## Error Handling

The app gracefully handles:
- Network connectivity issues
- API server errors
- Invalid API responses
- Permission denials for camera/gallery access

## Testing the Integration

1. **With Mock Data**: The app works immediately with sample detection results
2. **With Real API**: Update the `baseUrl` and deploy the Flask API
3. **Error Scenarios**: Test without internet connection or with invalid API URL

## Development Tips

1. **Debug API Calls**: Check Flutter logs for HTTP request/response details
2. **Test Image Formats**: The API should handle JPEG, PNG formats
3. **Response Validation**: Ensure API returns expected JSON structure
4. **Error Messages**: App shows user-friendly error messages for API failures

## Production Deployment

1. **API Security**: Use HTTPS and proper authentication if needed
2. **Rate Limiting**: Consider API rate limits for production use
3. **Caching**: Implement local caching for better performance
4. **Monitoring**: Add analytics for API success/failure rates
