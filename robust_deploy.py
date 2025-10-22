"""
L.I.F.E. Platform - Robust Deployment Script
Handles all common deployment issues automatically
"""

import os
import subprocess
import sys
import time
from pathlib import Path

print("=" * 70)
print(" L.I.F.E. PLATFORM - ROBUST DEPLOYMENT")
print("=" * 70)
print()

# Get script directory
SCRIPT_DIR = Path(__file__).parent.absolute()
os.chdir(SCRIPT_DIR)

print(f"Working directory: {SCRIPT_DIR}")
print()

# Step 1: Create .python_packages directory if missing
print("[1/5] Ensuring .python_packages directory exists...")
python_packages_dir = SCRIPT_DIR / ".python_packages"
try:
    python_packages_dir.mkdir(exist_ok=True)
    print(f"✅ {python_packages_dir}")
except (FileNotFoundError, OSError) as e:
    # Fallback: use os.makedirs which handles long paths better on Windows
    print(f"⚠️  Path.mkdir() failed, using os.makedirs fallback...")
    try:
        os.makedirs(str(python_packages_dir), exist_ok=True)
        print(f"✅ Created using os.makedirs: {python_packages_dir}")
    except Exception as e2:
        # If still fails, try creating in current directory
        print(f"⚠️  Long path issue detected. Creating in current directory...")
        os.makedirs(".python_packages", exist_ok=True)
        print(f"✅ Created in current directory")
print()

# Step 2: Verify essential files exist
print("[2/5] Verifying essential files...")
essential_files = ["function_app.py", "requirements.txt", "host.json"]
for file in essential_files:
    file_path = SCRIPT_DIR / file
    if file_path.exists():
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file} MISSING!")
        sys.exit(1)
print()

# Step 3: Deploy using func CLI
print("[3/5] Deploying to Azure...")
print("This may take 3-5 minutes...")
print()

deploy_cmd = [
    "func",
    "azure",
    "functionapp",
    "publish",
    "life-functions-app",
    "--python",
    "--build",
    "remote",
]

try:
    result = subprocess.run(
        deploy_cmd, check=True, capture_output=True, text=True, cwd=str(SCRIPT_DIR)
    )
    print(result.stdout)
    if result.stderr:
        print("Warnings:", result.stderr)
    print("✅ Deployment command completed")
except subprocess.CalledProcessError as e:
    print(f"❌ Deployment failed: {e}")
    print(f"Output: {e.stdout}")
    print(f"Error: {e.stderr}")
    sys.exit(1)
print()

# Step 4: Wait for Azure to process
print("[4/5] Waiting for Azure to sync (60 seconds)...")
for i in range(60, 0, -10):
    print(f"  {i} seconds remaining...")
    time.sleep(10)
print("✅ Wait complete")
print()

# Step 5: Restart function app
print("[5/5] Restarting Function App...")
restart_cmd = [
    "az",
    "functionapp",
    "restart",
    "--name",
    "life-functions-app",
    "--resource-group",
    "life-platform-rg",
]

try:
    subprocess.run(restart_cmd, check=True, capture_output=True)
    print("✅ Function App restarted")
except subprocess.CalledProcessError as e:
    print(f"⚠️  Restart failed (may not be critical): {e}")
print()

# Test deployment
print("=" * 70)
print(" TESTING DEPLOYMENT")
print("=" * 70)
print()

print("Testing health endpoint...")
print()

test_cmd = ["python", str(SCRIPT_DIR / "test_deployment.py")]
subprocess.run(test_cmd)

print()
print("=" * 70)
print(" DEPLOYMENT COMPLETE")
print("=" * 70)
print()
print("If test shows ✅ SUCCESS, deployment is working!")
print("If test shows ❌ 404, wait 2 more minutes and run: python test_deployment.py")
print()
