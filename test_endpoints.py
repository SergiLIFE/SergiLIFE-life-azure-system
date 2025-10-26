"""
Quick endpoint test for L.I.F.E Platform Azure Function
"""

import json
import subprocess
import urllib.request


def test_endpoint(url, name):
    """Test a single endpoint"""
    print(f"\n[Testing {name}]")
    print(f"URL: {url}")
    try:
        response = urllib.request.urlopen(url, timeout=15)
        data = response.read().decode("utf-8")
        print(f"✅ SUCCESS - Status: {response.getcode()}")
        try:
            json_data = json.loads(data)
            print(f"📄 JSON Response: {json_data}")
        except json.JSONDecodeError:
            print(f"📄 Raw Response: {data}")
        return True
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def list_deployed_functions():
    """List currently deployed functions"""
    print("\n[Checking Deployed Functions]")
    try:
        result = subprocess.run(
            [
                "az",
                "functionapp",
                "function",
                "list",
                "--name",
                "life-functions-app-prod",
                "--resource-group",
                "life-platform-prod",
                "--output",
                "table",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            print("📋 Deployed Functions:")
            print(result.stdout)
        else:
            print(f"❌ Error listing functions: {result.stderr}")
    except Exception as e:
        print(f"❌ Failed to list functions: {e}")


def main():
    print("=" * 60)
    print("L.I.F.E PLATFORM - ENDPOINT STATUS CHECK")
    print("=" * 60)

    base_url = "https://life-functions-app-prod.azurewebsites.net"

    # Test base URL
    test_endpoint(base_url, "Base Function App URL")

    # Test health endpoints
    test_endpoint(f"{base_url}/api/health", "Health Endpoint")
    test_endpoint(f"{base_url}/api/health_simple", "Simple Health Endpoint")

    # List deployed functions
    list_deployed_functions()

    print("\n" + "=" * 60)
    print("STATUS CHECK COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
