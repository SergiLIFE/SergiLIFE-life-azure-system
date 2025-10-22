import urllib.error
import urllib.request

print("🔍 Function App Connectivity Test")
print("=" * 40)

# Test different endpoints
test_urls = [
    "https://life-functions-app.azurewebsites.net",
    "https://life-functions-app.azurewebsites.net/api",
    "https://life-functions-app.scm.azurewebsites.net/api/deployments",
]

for url in test_urls:
    print(f"\nTesting: {url}")
    try:
        response = urllib.request.urlopen(url, timeout=10)
        print(f"  ✅ Response: {response.status} - {len(response.read())} bytes")
    except urllib.error.HTTPError as e:
        print(f"  ⚠️ HTTP Error: {e.code} - {e.reason}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n" + "=" * 40)
