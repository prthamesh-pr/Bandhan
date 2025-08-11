import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

class CrossPlatformImage extends StatelessWidget {
  final XFile imageFile;
  final double? width;
  final double? height;
  final BoxFit fit;

  const CrossPlatformImage({
    super.key,
    required this.imageFile,
    this.width,
    this.height,
    this.fit = BoxFit.cover,
  });

  @override
  Widget build(BuildContext context) {
    if (kIsWeb) {
      // For web platform, use Image.network with the blob URL
      return FutureBuilder<Uint8List>(
        future: imageFile.readAsBytes(),
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            return Image.memory(
              snapshot.data!,
              width: width,
              height: height,
              fit: fit,
            );
          } else if (snapshot.hasError) {
            return Container(
              width: width,
              height: height,
              color: Colors.grey[300],
              child: const Center(child: Icon(Icons.error)),
            );
          } else {
            return Container(
              width: width,
              height: height,
              color: Colors.grey[200],
              child: const Center(child: CircularProgressIndicator()),
            );
          }
        },
      );
    } else {
      // For mobile platforms, use Image.file
      return Image.file(
        File(imageFile.path),
        width: width,
        height: height,
        fit: fit,
      );
    }
  }
}
