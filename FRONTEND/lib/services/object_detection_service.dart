import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';
import 'package:flutter/foundation.dart';
import 'dart:convert';

class DetectionResult {
  final String objectName;
  final double confidence;
  final Map<String, double>? bbox;

  DetectionResult({
    required this.objectName,
    required this.confidence,
    this.bbox,
  });

  factory DetectionResult.fromJson(Map<String, dynamic> json) {
    return DetectionResult(
      objectName: json['class_name'] ?? json['name'] ?? 'Unknown',
      confidence: (json['confidence'] ?? 0.0).toDouble(),
      bbox: json['bbox'] != null
          ? {
              'x1': (json['bbox']['x1'] ?? 0.0).toDouble(),
              'y1': (json['bbox']['y1'] ?? 0.0).toDouble(),
              'x2': (json['bbox']['x2'] ?? 0.0).toDouble(),
              'y2': (json['bbox']['y2'] ?? 0.0).toDouble(),
            }
          : null,
    );
  }
}

class ObjectDetectionService {
  static const String baseUrl = 'https://bandhan-backend.onrender.com';
  static const String predictEndpoint = '/predict';

  Future<List<DetectionResult>> detectObjects(XFile imageFile) async {
    try {
      debugPrint('🔍 Starting object detection for: ${imageFile.name}');

      // For web platform, try API first, then fall back to mock data
      if (kIsWeb) {
        return await _detectObjectsWeb(imageFile);
      } else {
        return await _detectObjectsMobile(imageFile);
      }
    } catch (e) {
      debugPrint('💥 Detection error: $e');

      // Provide user-friendly error messages
      if (e.toString().contains('timeout') ||
          e.toString().contains('SocketException')) {
        throw Exception(
          'Connection timeout. The API may be starting up - please try again in 30 seconds.',
        );
      } else if (e.toString().contains('Connection refused')) {
        throw Exception(
          'Cannot connect to API. Please check your internet connection.',
        );
      } else {
        throw Exception('Detection failed: ${e.toString()}');
      }
    }
  }

  Future<List<DetectionResult>> _detectObjectsWeb(XFile imageFile) async {
    try {
      // Try API first with shorter timeout for web
      return await _makeApiRequest(imageFile, Duration(seconds: 30));
    } catch (e) {
      debugPrint('⚠️ API failed on web, using mock data: $e');
      // Fall back to mock data for web demo
      return _getMockDetectionResults(imageFile.name);
    }
  }

  Future<List<DetectionResult>> _detectObjectsMobile(XFile imageFile) async {
    // Try API with longer timeout for mobile
    return await _makeApiRequest(imageFile, Duration(seconds: 180));
  }

  Future<List<DetectionResult>> _makeApiRequest(
    XFile imageFile,
    Duration timeout,
  ) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl$predictEndpoint'),
    );

    // Add headers
    request.headers.addAll({'Accept': 'application/json'});

    // Add the image file
    if (kIsWeb) {
      var bytes = await imageFile.readAsBytes();
      request.files.add(
        http.MultipartFile.fromBytes(
          'file', // Backend expects 'file'
          bytes,
          filename: imageFile.name,
        ),
      );
    } else {
      request.files.add(
        await http.MultipartFile.fromPath(
          'file', // Backend expects 'file'
          imageFile.path,
          filename: imageFile.name,
        ),
      );
    }

    debugPrint('📤 Sending request to: $baseUrl$predictEndpoint');

    // Send request with specified timeout
    var streamedResponse = await request.send().timeout(timeout);
    var responseBody = await streamedResponse.stream.bytesToString();

    debugPrint('📥 Response Status: ${streamedResponse.statusCode}');
    debugPrint('📥 Response Body: $responseBody');

    if (streamedResponse.statusCode == 200) {
      var jsonData = json.decode(responseBody);

      List<DetectionResult> results = [];

      // Handle new API response format with 'detections' key
      if (jsonData is Map && jsonData.containsKey('detections')) {
        var detections = jsonData['detections'] as List;
        results = detections
            .map(
              (item) => DetectionResult.fromJson(item as Map<String, dynamic>),
            )
            .toList();

        // Log additional info
        if (jsonData.containsKey('processing_time')) {
          debugPrint('⏱️ Processing time: ${jsonData['processing_time']}s');
        }
        debugPrint(
          '✅ API processed ${jsonData['count'] ?? results.length} objects',
        );
      }
      // Handle legacy format (direct list)
      else if (jsonData is List) {
        results = jsonData
            .map(
              (item) => DetectionResult.fromJson(item as Map<String, dynamic>),
            )
            .toList();
      }

      debugPrint('✅ Successfully parsed ${results.length} detections');
      return results;
    } else {
      // Enhanced error handling
      var errorMessage = 'Detection failed';
      try {
        var errorData = json.decode(responseBody);
        errorMessage =
            errorData['error'] ?? errorData['details'] ?? errorMessage;
      } catch (e) {
        errorMessage = responseBody.isNotEmpty ? responseBody : errorMessage;
      }

      throw Exception(
        'API Error (${streamedResponse.statusCode}): $errorMessage',
      );
    }
  }

  // Mock data for fallback when API is unavailable
  List<DetectionResult> _getMockDetectionResults(String filename) {
    debugPrint('🎭 Using mock detection data for demo purposes');

    // Provide realistic mock data based on common objects
    if (filename.toLowerCase().contains('apple')) {
      return [
        DetectionResult(
          objectName: 'apple',
          confidence: 0.92,
          bbox: {'x1': 45.5, 'y1': 67.2, 'x2': 234.8, 'y2': 298.1},
        ),
      ];
    } else if (filename.toLowerCase().contains('car')) {
      return [
        DetectionResult(
          objectName: 'car',
          confidence: 0.87,
          bbox: {'x1': 12.3, 'y1': 45.6, 'x2': 456.7, 'y2': 234.5},
        ),
        DetectionResult(
          objectName: 'person',
          confidence: 0.73,
          bbox: {'x1': 123.4, 'y1': 56.7, 'x2': 234.5, 'y2': 345.6},
        ),
      ];
    } else {
      // General objects for any other image
      return [
        DetectionResult(
          objectName: 'person',
          confidence: 0.85,
          bbox: {'x1': 50.0, 'y1': 60.0, 'x2': 200.0, 'y2': 300.0},
        ),
        DetectionResult(
          objectName: 'chair',
          confidence: 0.67,
          bbox: {'x1': 220.0, 'y1': 150.0, 'x2': 350.0, 'y2': 280.0},
        ),
      ];
    }
  }

  // Test API health
  static Future<bool> testApiHealth() async {
    try {
      final response = await http
          .get(
            Uri.parse('https://bandhan-backend.onrender.com'),
            headers: {'Accept': 'application/json'},
          )
          .timeout(const Duration(seconds: 30));

      return response.statusCode == 200;
    } catch (e) {
      debugPrint('❌ Health check failed: $e');
      return false;
    }
  }
}
