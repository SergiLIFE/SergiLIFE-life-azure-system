"""
Simple API Test - Post Python 3.13 Deployment
Run this after deploying the Python 3.13 fix to verify endpoints work
"""

import json
import urllib.request


def test_api():
    """Quick test of the fixed API endpoints"""
    
    base_url = "https://lifeplatform1760781933.azurewebsites.net"
    
    endpoints = [
        "/api/validate-ingestion",
        "/api/ingestion-stats"
    ]
    
    print("Python 3.13 API Endpoint Verification")
    print("=" * 40)
    
    all_good = True
    
    for endpoint in endpoints:
        url = base_url + endpoint
        print(f"\nTesting: {url}")
        
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    python_version = data.get('python_version', 'unknown')
                    print(f"✅ SUCCESS - Python {python_version}")
                else:
                    print(f"❌ FAILED - Status {response.getcode()}")
                    all_good = False
        except Exception as e:
            print(f"❌ ERROR - {e}")
            all_good = False
    
    print("\n" + "=" * 40)
    if all_good:
        print("🎉 All endpoints working! Python 3.13 deployment successful!")
        print("✅ Ready to update Enhanced Dashboard")
    else:
        print("🚨 Issues found. Check deployment or try manual commands.")
    
    return all_good

if __name__ == "__main__":
    test_api()    test_api()