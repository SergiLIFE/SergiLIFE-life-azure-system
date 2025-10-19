"""
🧪 Quick API Endpoint Test for Python 3.13 Deployment
Test the deployed Azure Function App endpoints
"""

import json
from datetime import datetime

import requests

# Function App details
FUNC_APP_NAME = "lifeplatform1760781933"
BASE_URL = f"https://{FUNC_APP_NAME}.azurewebsites.net"

def test_endpoint(endpoint, method="GET", data=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"\n🔍 Testing: {method} {url}")
    print("-" * 50)
    
    try:
        if method.upper() == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            response = requests.get(url, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS")
            try:
                json_data = response.json()
                print("Response:")
                print(json.dumps(json_data, indent=2))
                return True
            except:
                print("Response (text):")
                print(response.text[:500])
                return True
        else:
            print(f"❌ FAILED - Status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ TIMEOUT - Request took longer than 30 seconds")
        return False
    except requests.exceptions.RequestException as e:
        print(f"🚨 ERROR - {str(e)}")
        return False

def main():
    """Main test function"""
    
    print("=" * 60)
    print("🧪 L.I.F.E Platform API Endpoint Testing")
    print("=" * 60)
    print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Function App: {FUNC_APP_NAME}")
    print(f"🌐 Base URL: {BASE_URL}")
    
    # Test endpoints
    tests = [
        ("Root API", "/", "GET", None),
        ("Validate Ingestion", "/api/validate-ingestion", "GET", None),
        ("Ingestion Stats", "/api/ingestion-stats", "GET", None),
        ("External EEG Ingestion", "/api/ingest-external-eeg", "POST", {"mode": "full_cycle"})
    ]
    
    results = []
    
    for test_name, endpoint, method, data in tests:
        print(f"\n🧪 Test: {test_name}")
        success = test_endpoint(endpoint, method, data)
        results.append((test_name, success))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\n📈 Overall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! Python 3.13 deployment successful!")
        print("\n🔗 Ready to update Enhanced Dashboard with working endpoints!")
    else:
        print("🚨 Some tests failed. Check Azure Function App logs.")
    
    print("\n🎯 Next Steps:")
    print("1. Update Enhanced Dashboard to use these endpoints")
    print("2. Test External EEG Ingestion tab functionality")
    print("3. Monitor Azure Function App performance")

if __name__ == "__main__":
    main()    main()