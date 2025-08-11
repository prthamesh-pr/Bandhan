import 'package:flutter/foundation.dart';

class AppConfig {
  static const String localBackend = 'http://localhost:5000';
  static const String prodBackend = 'https://your-production-backend-url.com';

  static String get backendUrl => kReleaseMode ? prodBackend : localBackend;
}