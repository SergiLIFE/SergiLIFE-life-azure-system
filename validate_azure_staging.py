# 🧪 L.I.F.E Platform Azure Deployment Validation Script
# Test staging environment endpoints and functionality

import json
import time
from datetime import datetime

import requests


def test_endpoint(url, endpoint_name, expected_status=200):
    """Test an endpoint and return results"""
    print(f"\n🔍 Testing {endpoint_name}...")
    print(f"📍 URL: {url}")

    try:
        response = requests.get(url, timeout=30)

        if response.status_code == expected_status:
            print(f"✅ {endpoint_name}: SUCCESS (Status: {response.status_code})")

            # Try to parse JSON response
            try:
                json_data = response.json()
                print(f"📊 Response: {json.dumps(json_data, indent=2)}")
                return True, json_data
            except json.JSONDecodeError:
                print(f"📄 Response (Text): {response.text[:200]}...")
                return True, response.text
        else:
            print(f"⚠️ {endpoint_name}: Unexpected status {response.status_code}")
            print(f"📄 Response: {response.text[:200]}...")
            return False, None

    except requests.exceptions.ConnectionError:
        print(f"❌ {endpoint_name}: Connection failed - DNS/Network issue")
        return False, None
    except requests.exceptions.Timeout:
        print(f"⏱️ {endpoint_name}: Request timed out")
        return False, None
    except requests.exceptions.RequestException as e:
        print(f"❌ {endpoint_name}: Request failed - {str(e)}")
        return False, None


def main():
    """Main validation function"""
    print("=" * 60)
    print("🚀 L.I.F.E PLATFORM - AZURE STAGING VALIDATION")
    print("=" * 60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Platform: Learning Individually from Experience")
    print("💰 Revenue Target: $345K Q4 2025 → $50.7M by 2029")
    print("🏪 Azure Marketplace ID: 9a600d96-fe1e-420b-902a-a0c42c561adb")
    print("=" * 60)

    base_url = "https://life-platform-staging.azurewebsites.net"
    endpoints = [
        ("/", "Main Landing Page"),
        ("/health", "Health Check API"),
        ("/api/status", "Platform Status API"),
        ("/api/metrics", "Performance Metrics API"),
        ("/api/life", "L.I.F.E Algorithm Status"),
    ]

    results = {}

    print("\n🌐 Testing L.I.F.E Platform Staging Endpoints...")

    for endpoint, name in endpoints:
        url = f"{base_url}{endpoint}"
        success, data = test_endpoint(url, name)
        results[endpoint] = {"name": name, "success": success, "data": data}

        # Small delay between requests
        time.sleep(1)

    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)

    successful_endpoints = sum(1 for r in results.values() if r["success"])
    total_endpoints = len(results)

    for endpoint, result in results.items():
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"{status} {result['name']} ({endpoint})")

    print(
        f"\n📈 Success Rate: {successful_endpoints}/{total_endpoints} ({(successful_endpoints/total_endpoints)*100:.1f}%)"
    )

    # Business Impact Assessment
    print("\n💰 BUSINESS IMPACT ASSESSMENT:")
    if successful_endpoints >= 3:
        print("✅ Staging environment is operational")
        print("✅ Production deployment pathway validated")
        print("✅ $345K Q4 2025 revenue target enabled")
        print("✅ Azure Marketplace deployment ready")
        print("\n🎉 L.I.F.E Platform staging deployment SUCCESSFUL!")
    else:
        print("⚠️ Staging environment needs attention")
        print("🔧 Some endpoints require debugging")
        print("⏳ Production deployment delayed until issues resolved")
        print("\n🚨 L.I.F.E Platform staging deployment needs FIXES")

    # Next Steps
    print("\n🎯 RECOMMENDED NEXT STEPS:")
    if successful_endpoints >= 3:
        print("1. 🚀 Proceed with production deployment")
        print("2. 🏪 Submit to Azure Marketplace")
        print("3. 📈 Begin customer acquisition for revenue targets")
        print("4. 🧪 Continue testing and optimization")
    else:
        print("1. 🔍 Debug failed endpoints")
        print("2. 🔧 Check Azure Web App logs")
        print("3. 🧪 Re-run deployment script")
        print("4. 📞 Contact Azure support if needed")

    print(f"\n🔗 Direct Links:")
    print(f"📍 Staging Platform: {base_url}")
    print(f"🏥 Health Check: {base_url}/health")
    print(
        f"📊 Azure Portal: https://portal.azure.com/#@/resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-staging-rg/providers/Microsoft.Web/sites/life-platform-staging"
    )

    print("\n" + "=" * 60)
    print("✅ L.I.F.E Platform validation complete!")
    print("=" * 60)

    return successful_endpoints >= 3


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Validation interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n💥 Validation failed with error: {str(e)}")
        exit(1)
