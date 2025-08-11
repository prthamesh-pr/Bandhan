import 'dart:convert';
import 'package:http/http.dart' as http;
import 'app_config.dart';

class ApiService {
  static Future<List<dynamic>> predictFromFile(String filePath) async {
    var request = http.MultipartRequest('POST', Uri.parse('${AppConfig.backendUrl}/predict'));
    request.files.add(await http.MultipartFile.fromPath('file', filePath));
    var response = await request.send();
    if (response.statusCode == 200) {
      final respStr = await response.stream.bytesToString();
      return jsonDecode(respStr);
    } else {
      throw Exception('Failed to get prediction');
    }
  }

  static Future<List<dynamic>> predictFromUrl(String imageUrl) async {
    final response = await http.post(
      Uri.parse('${AppConfig.backendUrl}/predict'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'url': imageUrl}),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to get prediction');
    }
  }
}
