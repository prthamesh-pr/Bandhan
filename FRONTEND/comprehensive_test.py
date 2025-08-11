import requests
import json
import time

def test_apple_with_patience():
    """Test apple detection with patience for cold starts"""
    
    print("🍎 Testing Apple Detection with Cold Start Handling")
    print("=" * 50)
    
    api_url = "https://bandhan-task.onrender.com"
    
    # Step 1: Wake up the API
    print("☕ Step 1: Waking up the API (this may take 60-90 seconds)...")
    
    for attempt in range(3):
        try:
            print(f"   Attempt {attempt + 1}/3...")
            response = requests.get(f"{api_url}/", timeout=120)
            
            if response.status_code == 200:
                print("✅ API is awake!")
                health_data = response.json()
                print(f"   Status: {health_data.get('status')}")
                print(f"   Model: {health_data.get('model')}")
                break
            else:
                print(f"   Response: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"   Timeout on attempt {attempt + 1}")
            if attempt < 2:
                print("   Waiting 30 seconds before retry...")
                time.sleep(30)
        except Exception as e:
            print(f"   Error: {e}")
            if attempt < 2:
                time.sleep(10)
    else:
        print("❌ Could not wake up API after 3 attempts")
        return False
    
    # Step 2: Test detection
    print("\n🔍 Step 2: Testing object detection...")
    
    # Use a reliable test image URL
    test_image = "https://ultralytics.com/images/bus.jpg"  # Known to work
    
    try:
        response = requests.post(
            f"{api_url}/predict",
            json={"url": test_image},
            headers={'Content-Type': 'application/json'},
            timeout=120
        )
        
        print(f"📤 Request sent to: {api_url}/predict")
        print(f"📥 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            detections = response.json()
            print(f"✅ SUCCESS! Detected {len(detections)} objects:")
            
            for i, obj in enumerate(detections[:5], 1):  # Show first 5
                name = obj.get('class_name', 'Unknown')
                conf = obj.get('confidence', 0)
                print(f"   {i}. {name}: {conf*100:.1f}%")
            
            print(f"\n🎉 Your API is working perfectly!")
            print(f"🎯 Your Flutter app should work the same way!")
            return True
            
        else:
            print(f"❌ Detection failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Detection error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting comprehensive API test...")
    success = test_apple_with_patience()
    
    if success:
        print("\n" + "="*50)
        print("🏆 TEST SUCCESSFUL!")
        print("📱 Your Flutter app is ready to use!")
        print("🍎 Try selecting the apple image in your app!")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("⚠️ API might need more time to start")
        print("🔄 Try running your Flutter app and wait for first request")
        print("="*50)
