"""
Quick Server Test - Check if L.I.F.E Platform is responding
"""

import json
import urllib.error
import urllib.request


def test_server():
    """Test if the local server is responding"""

    base_url = "http://127.0.0.1:5000"

    print("🧠 L.I.F.E PLATFORM - SERVER TEST")
    print("=" * 40)

    try:
        # Test main endpoint
        response = urllib.request.urlopen(base_url, timeout=5)
        content = response.read().decode("utf-8")
        data = json.loads(content)

        print("✅ Server is RUNNING!")
        print(f"✅ Status: {response.getcode()}")
        print(f"✅ Platform: {data.get('platform', 'Unknown')}")
        print(f"✅ Message: {data.get('message', 'No message')}")

        # Test health endpoint
        health_url = base_url + "/api/health_simple"
        health_response = urllib.request.urlopen(health_url, timeout=5)
        health_data = json.loads(health_response.read().decode("utf-8"))

        print(f"✅ Health endpoint: {health_data.get('status', 'Unknown')}")
        print()
        print("🎉 SUCCESS! L.I.F.E Platform is working locally!")
        print(f"🌐 Access at: {base_url}")
        print(f"🏥 Health check: {health_url}")

        return True

    except urllib.error.URLError as e:
        print("❌ Server NOT running!")
        print(f"❌ Error: {e.reason}")
        print("💡 Try running: START_SIMPLE_SERVER.bat")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False


if __name__ == "__main__":
    test_server()
