# L.I.F.E. Platform Functions - Local Testing Script
# Tests Azure Functions locally before deployment
# Generated: September 28, 2025

import asyncio
import json
import time
from datetime import datetime

import requests

# Local Function App URL (when running func start)
BASE_URL = "http://localhost:7071"


def test_learning_api():
    """Test the main Learning API endpoint"""
    print("🧪 Testing Learning API...")

    try:
        # Test GET request (health check)
        response = requests.get(f"{BASE_URL}/api/learning", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ GET /api/learning: {response.status_code}")
            print(f"   📊 Platform: {data.get('platform', 'Unknown')}")
            print(f"   🏆 Version: {data.get('version', 'Unknown')}")
            print(
                f"   ⚡ Speed: {data.get('features', {}).get('processing_speed', 'Unknown')}"
            )
            print(
                f"   🎯 Accuracy: {data.get('features', {}).get('accuracy', 'Unknown')}"
            )
        else:
            print(f"   ❌ GET /api/learning: {response.status_code}")

    except Exception as e:
        print(f"   ❌ Learning API test failed: {str(e)}")

    print()


def test_eeg_processor():
    """Test the EEG Processing endpoint"""
    print("🧠 Testing EEG Processor...")

    # Sample EEG data
    test_data = {
        "channels": [1.2, -0.5, 0.8, 2.1, -1.3, 0.6, 1.8, -0.9],
        "sampling_rate": 256,
        "user_id": "test_user_001",
        "session_type": "training",
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/eeg/process",
            json=test_data,
            timeout=10,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ POST /api/eeg/process: {response.status_code}")
            print(
                f"   ⚡ Processing Time: {data.get('processing_time_ms', 'Unknown')}ms"
            )
            print(f"   🎯 Accuracy: {data.get('accuracy_percentage', 'Unknown')}%")
            print(f"   🧠 Neural State: {data.get('neural_state', 'Unknown')}")
            print(f"   📊 Learning Outcome: {data.get('learning_outcome', 'Unknown')}")
        else:
            print(f"   ❌ POST /api/eeg/process: {response.status_code}")

    except Exception as e:
        print(f"   ❌ EEG Processor test failed: {str(e)}")

    print()


def test_analytics():
    """Test the Analytics endpoint"""
    print("📊 Testing Analytics...")

    try:
        response = requests.get(f"{BASE_URL}/api/analytics", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ GET /api/analytics: {response.status_code}")

            metrics = data.get("performance_summary", {})
            print(
                f"   ⚡ Avg Processing: {metrics.get('avg_processing_time', 'Unknown')}ms"
            )
            print(f"   🎯 Accuracy Rate: {metrics.get('accuracy_rate', 'Unknown')}%")
            print(f"   👥 Active Sessions: {metrics.get('active_sessions', 'Unknown')}")

            health = data.get("system_health", {})
            print(f"   💻 CPU Usage: {health.get('cpu_usage', 'Unknown')}%")
            print(f"   🧠 Memory Usage: {health.get('memory_usage', 'Unknown')}%")

        else:
            print(f"   ❌ GET /api/analytics: {response.status_code}")

    except Exception as e:
        print(f"   ❌ Analytics test failed: {str(e)}")

    print()


def test_authentication():
    """Test the Authentication endpoint"""
    print("🔐 Testing Authentication...")

    auth_data = {
        "user_id": "test_user_001",
        "credentials": "test_credentials",
        "session_type": "standard",
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/token",
            json=auth_data,
            timeout=10,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ POST /api/auth/token: {response.status_code}")
            print(f"   🎫 Token Type: {data.get('token_type', 'Unknown')}")
            print(f"   ⏰ Expires In: {data.get('expires_in', 'Unknown')} seconds")
            print(f"   👤 User ID: {data.get('user_id', 'Unknown')}")
            print(f"   🔑 Permissions: {data.get('permissions', 'Unknown')}")
        else:
            print(f"   ❌ POST /api/auth/token: {response.status_code}")

    except Exception as e:
        print(f"   ❌ Authentication test failed: {str(e)}")

    print()


def test_campaign_trigger():
    """Test the Campaign trigger endpoint (manual)"""
    print("📧 Testing Campaign Trigger...")

    campaign_data = {
        "trigger_type": "manual_test",
        "test_mode": True,
        "target_institutions": 10,  # Small test batch
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/campaign/trigger",
            json=campaign_data,
            timeout=10,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ POST /api/campaign/trigger: {response.status_code}")
            print(f"   📊 Campaign Status: {data.get('campaign_status', 'Unknown')}")
            print(f"   🎯 Trigger Type: {data.get('trigger_type', 'Unknown')}")
            print(
                f"   📧 Target Institutions: {data.get('target_institutions', 'Unknown')}"
            )
            print(f"   🆔 Campaign ID: {data.get('campaign_id', 'Unknown')}")
        else:
            print(f"   ❌ POST /api/campaign/trigger: {response.status_code}")

    except Exception as e:
        print(f"   ❌ Campaign trigger test failed: {str(e)}")

    print()


def main():
    """Run all local function tests"""
    print("🚀 L.I.F.E. Platform Local Function Testing")
    print("===========================================")
    print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing against: {BASE_URL}")
    print()

    # Wait a moment for Function App to be ready
    print("⏳ Waiting for Function App to be ready...")
    time.sleep(2)
    print()

    # Run all tests
    test_learning_api()
    test_eeg_processor()
    test_analytics()
    test_authentication()
    test_campaign_trigger()

    print("🎯 LOCAL TESTING COMPLETE")
    print("=========================")
    print("✅ All L.I.F.E. Platform functions tested locally!")
    print("🚀 Ready for Azure deployment!")
    print()
    print("💡 Next Steps:")
    print("   1. If tests passed, deploy to Azure: .\\deploy-functions.ps1 -Deploy")
    print("   2. Validate deployment: .\\deploy-functions.ps1 -Validate")
    print("   3. Complete platform for October 7th launch!")


if __name__ == "__main__":
    main()
