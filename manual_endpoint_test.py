"""
Manual Endpoint Test - L.I.F.E Platform
Tests the corrected health_simple endpoint
"""

import json
import urllib.error
import urllib.request


def test_health_endpoint():
    """Test the health_simple endpoint with proper error handling"""

    url = "https://life-functions-app-prod.azurewebsites.net/api/health_simple"

    print("=" * 60)
    print("L.I.F.E PLATFORM - CORRECTED ENDPOINT TEST")
    print("=" * 60)
    print(f"Testing URL: {url}")
    print()

    try:
        print("Making request...")
        response = urllib.request.urlopen(url, timeout=30)

        print(f"✅ Response Status: {response.getcode()}")
        print(f"✅ Response Headers: {dict(response.headers)}")

        content = response.read().decode("utf-8")
        print(f"✅ Raw Response: {content}")

        # Try to parse as JSON
        try:
            data = json.loads(content)
            print("✅ JSON Parsed Successfully:")
            for key, value in data.items():
                print(f"   {key}: {value}")

            print()
            print("🎉 SUCCESS! The health_simple endpoint is working correctly!")
            return True

        except json.JSONDecodeError as e:
            print(f"⚠️  Response is not valid JSON: {e}")
            return False

    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        try:
            error_content = e.read().decode("utf-8")
            print(f"Error Content: {error_content}")
        except Exception:
            pass
        return False

    except urllib.error.URLError as e:
        print(f"❌ URL Error: {e.reason}")
        return False

    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_health_endpoint()

    print()
    print("=" * 60)
    if success:
        print("✅ ENDPOINT VALIDATION: PASSED")
        print("The L.I.F.E Platform health endpoint is working correctly!")
    else:
        print("❌ ENDPOINT VALIDATION: FAILED")
        print("The endpoint is not responding correctly.")
    print("=" * 60)
