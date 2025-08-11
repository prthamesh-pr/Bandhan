# Deployment instructions for Bandhan Backend

## Local Development

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   pip install flask-cors python-dotenv
   ```
2. Copy `.env.example` to `.env` and adjust as needed.
3. Run the server:
   ```sh
   python main.py
   ```
   The backend will be available at `http://localhost:5000` by default.

## Production Deployment

- Use a production WSGI server like Gunicorn or Waitress.
- Example (with Waitress):
  ```sh
  pip install waitress
  waitress-serve --host=0.0.0.0 --port=5000 main:app
  ```
- Set environment variables as needed (see `.env.example`).

## Notes
- Ensure CORS is restricted to your frontend domain in production for security.
- Place your model file (`yolov8n.pt`) in the same directory as `main.py`.
