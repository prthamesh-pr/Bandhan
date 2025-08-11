import requests
import json
import base64
from io import BytesIO

# Test the deployed API with the apple image
API_URL = "https://bandhan-task.onrender.com"

def test_apple_detection():
    print("🍎 Testing Apple Image Detection")
    print("=" * 40)
    
    # Test with URL approach (using a publicly available apple image)
    test_image_url = "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=500"
    
    try:
        print("🔄 Testing API health first...")
        health_response = requests.get(f"{API_URL}/", timeout=30)
        print(f"✅ Health Check: {health_response.status_code}")
        print(f"Response: {health_response.json()}")
        
        print("\n🍎 Testing apple detection...")
        
        # Test with URL
        response = requests.post(
            f"{API_URL}/predict",
            json={"url": test_image_url},
            headers={'Content-Type': 'application/json'},
            timeout=120
        )
        
        print(f"📤 Request sent to: {API_URL}/predict")
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            detections = response.json()
            print(f"✅ Detection successful!")
            print(f"🔍 Found {len(detections)} objects:")
            
            for i, detection in enumerate(detections, 1):
                name = detection.get('class_name', 'Unknown')
                confidence = detection.get('confidence', 0)
                bbox = detection.get('bbox', {})
                
                print(f"  {i}. {name} - {confidence*100:.1f}% confidence")
                if bbox:
                    print(f"     Location: [{bbox.get('x1', 0):.1f}, {bbox.get('y1', 0):.1f}, {bbox.get('x2', 0):.1f}, {bbox.get('y2', 0):.1f}]")
                    
            return True
        else:
            print(f"❌ Detection failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - API might be sleeping (cold start)")
        print("💡 Try again in a few minutes")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_apple_detection()
    
    if success:
        print("\n🎉 Test completed successfully!")
        print("Your Flutter app should work the same way!")
    else:
        print("\n⚠️ Test failed. Check API status.")
        print("If API is sleeping, try opening: https://bandhan-task.onrender.com")
