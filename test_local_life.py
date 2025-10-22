"""
Local L.I.F.E Platform Test - Tests local development server
Updated to test localhost endpoints while Azure authorization is pending
"""

import json
import urllib.error
import urllib.request


def test_local_endpoints():
    """Test all local L.I.F.E Platform endpoints"""

    base_url = "http://localhost:5000"
    endpoints = [
        "/",
        "/api/health",
        "/api/health_simple",
        "/api/eeg_processor",
        "/api/platform_info",
    ]

    print("=" * 70)
    print("🧠 L.I.F.E PLATFORM - LOCAL DEVELOPMENT TEST")
    print("=" * 70)
    print("Testing local server while Azure authorization is pending...")
    print()

    results = {}

    for endpoint in endpoints:
        url = base_url + endpoint
        print(f"[Testing] {url}")

        try:
            response = urllib.request.urlopen(url, timeout=10)
            content = response.read().decode("utf-8")

            print(f"  ✅ Status: {response.getcode()}")

            try:
                data = json.loads(content)
                print(f"  📄 JSON Response: {data}")
                results[endpoint] = {"status": "success", "data": data}
            except json.JSONDecodeError:
                print(f"  📄 Text Response: {content[:100]}...")
                results[endpoint] = {"status": "success", "data": content}

        except urllib.error.URLError as e:
            print(f"  ❌ Failed: {e.reason}")
            results[endpoint] = {"status": "failed", "error": str(e.reason)}
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results[endpoint] = {"status": "failed", "error": str(e)}

        print()

    # Summary
    print("=" * 70)
    print("🎯 TEST SUMMARY")
    print("=" * 70)

    successful = sum(1 for r in results.values() if r["status"] == "success")
    total = len(results)

    print(f"Endpoints tested: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print()

    if successful == total:
        print("🎉 ALL ENDPOINTS WORKING!")
        print("✅ Local L.I.F.E Platform is fully operational")
        print("✅ Ready to continue development locally")
        print("⏳ Azure Functions deployment pending authorization")
    else:
        print("⚠️  Some endpoints failed")
        print("💡 Make sure the local server is running: python local_life_server.py")

    print()
    print("🌐 Access L.I.F.E Platform at: http://localhost:5000")
    print("=" * 70)

    return successful == total


if __name__ == "__main__":
    success = test_local_endpoints()

    if success:
        print("\n✅ LOCAL L.I.F.E PLATFORM: OPERATIONAL")
    else:
        print("\n❌ LOCAL L.I.F.E PLATFORM: ISSUES DETECTED")
