#!/usr/bin/env python3
"""
Wake up and test the deployed Bandhan API on Render
"""

import requests
import time

API_URL = "https://bandhan-task.onrender.com"

def wake_up_service():
    """Wake up the sleeping Render service"""
    print("🔄 Waking up the Render service...")
    print("This may take 30-60 seconds for cold start...")
    
    try:
        # Try health check with longer timeout
        response = requests.get(f"{API_URL}/", timeout=120)
        print(f"✅ Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Service is awake and healthy!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"⚠️ Service responded with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.Timeout:
        print("❌ Service took too long to respond (timeout)")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_prediction():
    """Test the prediction endpoint"""
    print("\n🧪 Testing object detection...")
    
    test_data = {
        "url": "https://ultralytics.com/images/bus.jpg"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=test_data,
            timeout=120,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            predictions = response.json()
            print(f"✅ Detected {len(predictions)} objects:")
            for i, pred in enumerate(predictions[:5]):
                print(f"  {i+1}. {pred.get('class_name', 'Unknown')} (confidence: {pred.get('confidence', 0)})")
            return True
        else:
            print(f"❌ Prediction failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Bandhan API on Render")
    print(f"URL: {API_URL}")
    print("=" * 50)
    
    # Wake up service
    health_ok = wake_up_service()
    
    if health_ok:
        # Test prediction
        prediction_ok = test_prediction()
        
        print("\n" + "=" * 50)
        print("📊 Final Results:")
        print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
        print(f"Object Detection: {'✅ PASS' if prediction_ok else '❌ FAIL'}")
        
        if health_ok and prediction_ok:
            print("\n🎉 Your API is fully operational!")
            print("Your Flutter app should now work with the live API!")
        else:
            print("\n⚠️ Some issues detected. Check Render logs for details.")
    else:
        print("\n❌ Service health check failed.")
        print("💡 Troubleshooting tips:")
        print("1. Check Render dashboard for deployment logs")
        print("2. Verify build completed successfully")
        print("3. Try again in a few minutes (cold start issues)")
        print("4. Check if service is sleeping due to inactivity")
