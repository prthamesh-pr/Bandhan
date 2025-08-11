# Deployment instructions for Bandhan Frontend (Flutter)

## Local Development

1. Ensure the backend is running locally (see backend instructions).
2. The app uses `http://localhost:5000` for API calls in debug mode (see `lib/services/app_config.dart`).
3. Run the app:
   ```sh
   flutter run
   ```

## Production Build

1. Update `prodBackend` in `lib/services/app_config.dart` with your deployed backend URL.
2. Build the app for release:
   ```sh
   flutter build apk   # For Android
   flutter build ios   # For iOS
   flutter build web   # For Web
   ```
3. Deploy the built app as per platform requirements.

## Notes
- For web, ensure CORS is enabled on the backend for your deployed frontend domain.
- For mobile, if testing on a real device, use your computer's LAN IP instead of `localhost` in `localBackend`.
