"""Quick test to verify Azure CLI connectivity"""

import json
import subprocess

print("=" * 60)
print("Testing Azure CLI Connection")
print("=" * 60)

try:
    # Test Azure CLI
    print("\n1. Checking Azure CLI version...")
    result = subprocess.run(["az", "version"], capture_output=True, text=True)
    if result.returncode == 0:
        print("   ✅ Azure CLI is installed")
    else:
        print("   ❌ Azure CLI not found")
        exit(1)

    # Test authentication
    print("\n2. Checking Azure authentication...")
    result = subprocess.run(["az", "account", "show"], capture_output=True, text=True)
    if result.returncode == 0:
        account = json.loads(result.stdout)
        print(f"   ✅ Authenticated")
        print(f"   Subscription: {account['name']}")
        print(f"   ID: {account['id']}")
        print(f"   State: {account['state']}")
    else:
        print("   ❌ Not authenticated")
        print("   Please run: az login")
        exit(1)

    print("\n" + "=" * 60)
    print("✅ Azure CLI is ready for deployment!")
    print("=" * 60)
    print("\nYou can now run: python DEPLOY_LIFE_AZURE_STAGING.py")

except Exception as e:
    print(f"\n❌ Error: {e}")
    exit(1)
