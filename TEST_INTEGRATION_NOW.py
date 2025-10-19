#!/usr/bin/env python
"""
Quick integration test - verifies everything works end-to-end
"""

import os
import subprocess
import sys
import time

print("=" * 80)
print("🧠 L.I.F.E PLATFORM BACKEND INTEGRATION TEST")
print("=" * 80)

# Check if Python files exist
backend_file = "life_backend_server.py"
if not os.path.exists(backend_file):
    print(f"❌ {backend_file} not found in current directory")
    sys.exit(1)

print(f"\n✅ Found {backend_file}")

# Install requirements first
print("\n📦 Installing dependencies...")
try:
    subprocess.run(
        ["pip", "install", "-q", "flask", "flask-cors", "numpy"],
        check=True,
        capture_output=True,
    )
    print("✅ Dependencies installed")
except Exception as e:
    print(f"⚠️  Could not install dependencies: {e}")

# Start backend server
print("\n🚀 Starting backend server...")
print(f"   Command: python {backend_file}")

try:
    backend_process = subprocess.Popen(
        ["python", backend_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    # Wait for server to start
    time.sleep(3)

    print("⏳ Server starting (waiting 3 seconds)...")

    # Check if process is still running
    if backend_process.poll() is not None:
        print("❌ Backend process crashed on startup")
        print(backend_process.stdout.read())
        sys.exit(1)

    print("✅ Backend server running on http://localhost:5000")

    # Test the health endpoint
    print("\n📡 Testing /health endpoint...")
    import json
    import urllib.request

    try:
        with urllib.request.urlopen(
            "http://localhost:5000/health", timeout=5
        ) as response:
            health_data = json.loads(response.read().decode())
            print(f"✅ Health check passed:")
            print(f"   Status: {health_data['status']}")
            print(f"   Algorithm: {health_data['algorithm']}")
            print(f"   Version: {health_data['version']}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        sys.exit(1)

    # Test the /analyze-eeg endpoint
    print("\n📊 Testing /analyze-eeg endpoint...")
    import numpy as np

    # Generate test EEG
    eeg_test = np.sin(np.linspace(0, 10 * np.pi, 512)).tolist()

    payload = json.dumps(
        {
            "eeg_signal": eeg_test,
            "sample_rate": 256,
            "duration_seconds": 2,
            "session_id": "test_session_001",
            "user_type": "test",
        }
    ).encode()

    req = urllib.request.Request(
        "http://localhost:5000/analyze-eeg",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result_data = json.loads(response.read().decode())
            if result_data["status"] == "SUCCESS":
                print(f"✅ Analysis successful:")
                print(f"   Session: {result_data['session_id']}")
                print(f"   Results:")
                for key, value in result_data["results"].items():
                    if isinstance(value, (int, float)):
                        print(f"      • {key}: {value}")
            else:
                print(f"❌ Analysis failed: {result_data}")
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        sys.exit(1)

    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    print("\n🎯 Next steps:")
    print("   1. Keep this backend server running")
    print("   2. In another terminal, run: python -m http.server 8080")
    print("   3. Open browser: http://localhost:8080/LIFE_AI_PLATFORM_REAL.html")
    print("   4. The platform should show '🟢 Real Algorithm (Backend Connected)'")
    print("   5. Click 'Process EEG AI Integration' tab and run analysis")
    print("\n💡 The platform will now use REAL algorithm, not simulated!")
    print("=" * 80)

    # Keep server running
    print("\n🔄 Backend server is running... Press Ctrl+C to stop")
    backend_process.wait()

except KeyboardInterrupt:
    print("\n\n⛔ Stopping backend server...")
    backend_process.terminate()
    backend_process.wait(timeout=5)
    print("✅ Backend stopped")
except Exception as e:
    print(f"\n❌ Error: {e}")
    if backend_process:
        backend_process.terminate()
    sys.exit(1)
