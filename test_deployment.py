"""
L.I.F.E Platform - Simple Deployment Tester
Tests health endpoint without PowerShell dependency
"""

import json
import sys
import urllib.error
import urllib.request

print("=" * 60)
print(" L.I.F.E PLATFORM - DEPLOYMENT TEST")
print("=" * 60)
print()

# Test health endpoint
url = "https://life-functions-app.azurewebsites.net/api/health"
print(f"Testing: {url}")
print()

try:
    response = urllib.request.urlopen(url, timeout=10)
    data = json.loads(response.read())

    print("✅ SUCCESS! Function App is responding")
    print()
    print("Response:")
    print(json.dumps(data, indent=2))
    print()

    # Verify response content
    if data.get("status") == "healthy":
        print("=" * 60)
        print(" 🎉 DEPLOYMENT SUCCESSFUL!")
        print("=" * 60)
        print()
        print("Your L.I.F.E Platform is LIVE on Azure!")
        print()
        print("Available endpoints:")
        print(
            "  - Health Check: https://life-functions-app.azurewebsites.net/api/health"
        )
        print(
            "  - Process EEG:  https://life-functions-app.azurewebsites.net/api/process_eeg"
        )
        print(
            "  - Analyze Learning: https://life-functions-app.azurewebsites.net/api/analyze_learning"
        )
        print()
        sys.exit(0)
    else:
        print("⚠️ Function responded but status is not 'healthy'")
        sys.exit(1)

except urllib.error.HTTPError as e:
    print(f"❌ HTTP Error {e.code}: {e.reason}")
    print()
    if e.code == 404:
        print("Possible causes:")
        print("  1. Deployment still in progress (wait 1-2 minutes)")
        print("  2. Functions not synced properly")
        print("  3. Health endpoint not deployed")
        print()
        print("Solutions:")
        print("  - Wait 1-2 minutes and run this test again")
        print(
            "  - Restart Function App: az functionapp restart --name life-functions-app --resource-group life-platform-rg"
        )
        print(
            "  - Check deployment: func azure functionapp list-functions life-functions-app"
        )
    elif e.code == 503:
        print("Function App is starting up or experiencing issues")
        print()
        print("Solutions:")
        print("  - Wait 30 seconds and try again")
        print(
            "  - Check logs: az webapp log tail --name life-functions-app --resource-group life-platform-rg"
        )
    sys.exit(1)

except urllib.error.URLError as e:
    print(f"❌ Connection Error: {e.reason}")
    print()
    print("Possible causes:")
    print("  - No internet connection")
    print("  - Function App URL is incorrect")
    print("  - Azure service is down (rare)")
    sys.exit(1)

except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    sys.exit(1)
