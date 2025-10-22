#!/usr/bin/env python3
"""
L.I.F.E Platform - Stage 3 Real Deployment Validation
Tests the actual Azure deployment we just completed
"""

import json
import time
import urllib.error
import urllib.request
from datetime import datetime


def test_actual_deployment():
    """Test the real Azure Functions deployment"""

    print("🔥" * 50)
    print("🚀 L.I.F.E PLATFORM - STAGE 3 REAL DEPLOYMENT TEST")
    print("🔥" * 50)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Testing: Direct Azure ZIP deployment results")
    print("=" * 70)
    print()

    # Test endpoints
    endpoints = [
        {
            "name": "Health Check",
            "url": "https://life-functions-app.azurewebsites.net/api/health_check",
            "method": "GET",
            "auth": "Anonymous",
            "expected": "status: healthy",
        },
        {
            "name": "EEG Processor",
            "url": "https://life-functions-app.azurewebsites.net/api/eeg_processor",
            "method": "POST",
            "auth": "Function Key",
            "expected": "EEG processing response",
        },
        {
            "name": "Analytics Monitor",
            "url": "https://life-functions-app.azurewebsites.net/api/analytics_monitor",
            "method": "GET",
            "auth": "Function Key",
            "expected": "Analytics data",
        },
        {
            "name": "Learning API",
            "url": "https://life-functions-app.azurewebsites.net/api/learning_api",
            "method": "GET",
            "auth": "Function Key",
            "expected": "Learning metrics",
        },
        {
            "name": "Campaign Automation",
            "url": "https://life-functions-app.azurewebsites.net/api/campaign_automation",
            "method": "POST",
            "auth": "Function Key",
            "expected": "Campaign response",
        },
    ]

    results = []

    print("🧪 TESTING DEPLOYED ENDPOINTS")
    print("=" * 40)
    print()

    # Test 1: Health Check (most important)
    print("🔍 Test 1/5: Health Check Endpoint")
    print(f"   URL: {endpoints[0]['url']}")
    print("   Testing...")

    try:
        response = urllib.request.urlopen(endpoints[0]["url"], timeout=10)
        data = json.loads(response.read())

        if data.get("status") == "healthy":
            print("   ✅ PASSED - Health endpoint is responding!")
            print(f"   📊 Platform: {data.get('platform', 'N/A')}")
            print(f"   📊 Version: {data.get('version', 'N/A')}")
            print(f"   📊 Services: {len(data.get('services', {}))} operational")
            results.append(("Health Check", True, 100, "Health endpoint operational"))
        else:
            print(
                f"   ⚠️ PARTIAL - Response received but status is: {data.get('status')}"
            )
            results.append(("Health Check", False, 60, f"Status: {data.get('status')}"))

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("   ❌ FAILED - 404 Not Found (deployment issue)")
            results.append(("Health Check", False, 0, "404 Not Found"))
        else:
            print(f"   ❌ FAILED - HTTP Error {e.code}")
            results.append(("Health Check", False, 20, f"HTTP {e.code}"))
    except Exception as e:
        print(f"   ❌ FAILED - {str(e)}")
        results.append(("Health Check", False, 10, str(e)))

    print()

    # Test 2-5: Other endpoints (quick connectivity check)
    for i, endpoint in enumerate(endpoints[1:], 2):
        print(f"🔍 Test {i}/5: {endpoint['name']}")
        print(f"   URL: {endpoint['url']}")
        print("   Testing connectivity...")

        try:
            # Just test if endpoint exists (will likely get 401/403 without auth)
            urllib.request.urlopen(endpoint["url"], timeout=5)
            print("   ✅ PASSED - Endpoint is accessible")
            results.append((endpoint["name"], True, 90, "Endpoint accessible"))
        except urllib.error.HTTPError as e:
            if e.code in [401, 403]:
                print("   ✅ PASSED - Endpoint exists (requires auth)")
                results.append((endpoint["name"], True, 85, "Requires authentication"))
            elif e.code == 404:
                print("   ❌ FAILED - 404 Not Found")
                results.append((endpoint["name"], False, 0, "404 Not Found"))
            else:
                print(f"   ⚠️ PARTIAL - HTTP {e.code}")
                results.append((endpoint["name"], False, 40, f"HTTP {e.code}"))
        except Exception as e:
            print(f"   ❌ FAILED - {str(e)}")
            results.append((endpoint["name"], False, 20, str(e)))

        print()
        time.sleep(0.5)

    # Calculate results
    passed_tests = sum(1 for _, passed, _, _ in results if passed)
    total_score = sum(score for _, _, score, _ in results) / len(results)
    pass_rate = (passed_tests / len(results)) * 100

    print("=" * 70)
    print("📊 STAGE 3 DEPLOYMENT VALIDATION RESULTS")
    print("=" * 70)
    print(f"✅ Tests Passed: {passed_tests}/{len(results)} ({pass_rate:.1f}%)")
    print(f"⭐ Average Score: {total_score:.1f}%")
    print(f"🎯 Pass Threshold: 60% (Minimum for Stage 3)")
    print()

    if pass_rate >= 80:
        print("🎉 OUTSTANDING: Stage 3 deployment is EXCELLENT!")
        print("   🚀 Ready for full production testing")
        print("   🎯 Proceed to Stage 4: Full Integration Tests")
    elif pass_rate >= 60:
        print("🌟 GOOD: Stage 3 deployment is SUCCESSFUL!")
        print("   ✅ Basic deployment working")
        print("   🔧 May need authentication setup for full functionality")
    else:
        print("⚠️ NEEDS WORK: Stage 3 deployment has issues")
        print("   🔧 Check deployment logs and retry")

    print()
    print("🔧 DEPLOYMENT STATUS:")
    for test_name, passed, score, details in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} {test_name}: {details}")

    print()
    print("🎯 NEXT ACTIONS:")
    if pass_rate >= 60:
        print("   1. ✅ Stage 3 Complete - Deployment successful!")
        print("   2. 🔑 Set up function keys for authenticated endpoints")
        print("   3. 🧪 Run full integration test suite")
        print("   4. 🚀 Proceed to production readiness validation")
    else:
        print("   1. 🔧 Check Azure deployment logs")
        print("   2. 🔄 Retry deployment with DEPLOY_DIRECT.bat")
        print("   3. 🧪 Re-run Stage 3 validation")

    print()
    print("🏆 STAGE 3 VALIDATION COMPLETE! 🏆")
    print("=" * 70)


def main():
    """Main function"""
    test_actual_deployment()


if __name__ == "__main__":
    main()
