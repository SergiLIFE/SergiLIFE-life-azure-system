#!/usr/bin/env python
"""
🔍 L.I.F.E PLATFORM DIAGNOSTIC TOOL
Quick test to verify everything is set up correctly
"""

import os
import socket
import subprocess
import sys


def check_port_open(host, port, timeout=3):
    """Check if a port is open"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False


def main():
    print("\n" + "=" * 80)
    print("🔍 L.I.F.E PLATFORM DIAGNOSTIC TOOL")
    print("=" * 80 + "\n")

    # Check 1: Python installed
    print("✅ Check 1: Python installation")
    try:
        version = subprocess.check_output(
            [sys.executable, "--version"], stderr=subprocess.STDOUT, text=True
        ).strip()
        print(f"   ✅ Python found: {version}\n")
    except Exception as e:
        print(f"   ❌ Python not found: {e}\n")
        return False

    # Check 2: Dependencies installed
    print("✅ Check 2: Required packages")
    packages = ["flask", "flask_cors", "numpy"]
    for package in packages:
        try:
            __import__(package.replace("_", "-"))
            print(f"   ✅ {package} installed")
        except ImportError:
            print(f"   ❌ {package} NOT installed")
            print(f"      Fix: pip install {package}")
    print()

    # Check 3: Backend file exists
    print("✅ Check 3: Backend server file")
    if os.path.exists("life_backend_server.py"):
        size = os.path.getsize("life_backend_server.py")
        print(f"   ✅ life_backend_server.py found ({size} bytes)\n")
    else:
        print(f"   ❌ life_backend_server.py NOT found\n")
        return False

    # Check 4: Frontend files exist
    print("✅ Check 4: Frontend files")
    files = ["LIFE_AI_PLATFORM_REAL.html", "PLATFORM_BACKEND_INTEGRATION.js"]
    for f in files:
        if os.path.exists(f):
            size = os.path.getsize(f)
            print(f"   ✅ {f} found ({size} bytes)")
        else:
            print(f"   ❌ {f} NOT found")
    print()

    # Check 5: Ports available
    print("✅ Check 5: Port availability")
    if check_port_open("localhost", 5000):
        print("   ⚠️  Port 5000 already in use (something else running)")
    else:
        print("   ✅ Port 5000 available")

    if check_port_open("localhost", 8080):
        print("   ⚠️  Port 8080 already in use (something else running)")
    else:
        print("   ✅ Port 8080 available")
    print()

    print("=" * 80)
    print("📋 NEXT STEPS:")
    print("=" * 80)
    print(
        """
1. Install missing packages (if any):
   pip install flask flask-cors numpy

2. Terminal 1 - Start backend:
   python life_backend_server.py

3. Terminal 2 - Start HTTP server:
   python -m http.server 8080

4. Browser:
   http://localhost:8080/LIFE_AI_PLATFORM_REAL.html

5. Look for 🟢 Green status at top of page

6. Click "EEG AI Integration" tab

7. Click "Process EEG AI Integration" button

8. See REAL algorithm results!
"""
    )
    print("=" * 80 + "\n")

    return True


if __name__ == "__main__":
    main()
