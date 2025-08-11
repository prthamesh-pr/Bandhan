import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:bandhan/main.dart';

void main() {
  testWidgets('App launches with splash screen', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const ObjectDetectionApp());

    // Verify that the splash screen is shown with the app title.
    expect(find.text('Object Detection App'), findsOneWidget);
    expect(find.byType(CircularProgressIndicator), findsOneWidget);

    // Wait for splash screen navigation timer to complete and pump frames
    await tester.pump(const Duration(seconds: 3));

    // After splash, we should see the login screen
    await tester.pumpAndSettle();

    // Check if login screen elements are present
    expect(find.text('Login'), findsOneWidget);
    expect(find.text('Email'), findsOneWidget);
    expect(find.text('Password'), findsOneWidget);
  });
}
