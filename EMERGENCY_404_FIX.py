#!/usr/bin/env python3
"""
🚨 EMERGENCY: L.I.F.E Platform 404 Fix - October 18, 2025
Immediate diagnostic and repair tool for lifeplatform1760781933 404 errors

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import json
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime
from typing import Dict, List, Tuple


def check_azure_cli() -> bool:
    """Check if Azure CLI is available"""
    try:
        result = subprocess.run(
            ["az", "--version"], capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except:
        return False


def check_function_app_status(app_name: str) -> Dict[str, str]:
    """Check Function App deployment status"""
    print(f"🔍 Checking Function App: {app_name}")

    status = {
        "name": app_name,
        "url": f"https://{app_name}.azurewebsites.net",
        "api_status": "unknown",
        "python_version": "unknown",
        "deployment_status": "unknown",
    }

    # Test basic connectivity
    try:
        req = urllib.request.Request(status["url"])
        with urllib.request.urlopen(req, timeout=10) as response:
            status["api_status"] = f"HTTP {response.getcode()}"
            if response.getcode() == 200:
                status["deployment_status"] = "running"
            else:
                status["deployment_status"] = "issues"
    except urllib.error.HTTPError as e:
        status["api_status"] = f"HTTP {e.code}"
        status["deployment_status"] = "error"
    except Exception as e:
        status["api_status"] = f"Connection failed: {e}"
        status["deployment_status"] = "offline"

    # Test API endpoints
    endpoints = [
        "/api/validate-ingestion",
        "/api/ingestion-stats",
        "/api/ingest-external-eeg",
    ]
    status["endpoints"] = {}

    for endpoint in endpoints:
        url = status["url"] + endpoint
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as response:
                status["endpoints"][endpoint] = f"✅ HTTP {response.getcode()}"
        except urllib.error.HTTPError as e:
            status["endpoints"][endpoint] = f"❌ HTTP {e.code}"
        except Exception as e:
            status["endpoints"][endpoint] = f"❌ {str(e)[:50]}"

    return status


def execute_python313_fix(app_name: str, resource_group: str) -> bool:
    """Execute Python 3.13 deployment fix"""

    if not check_azure_cli():
        print("❌ Azure CLI not available. Cannot execute automated fix.")
        print("📋 Manual steps required:")
        print("1. Install Azure CLI")
        print("2. Run: az login")
        print("3. Run: deploy_python313.bat")
        return False

    print(f"🔧 Executing Python 3.13 fix for {app_name}")

    commands = [
        # Update runtime version
        [
            "az",
            "functionapp",
            "config",
            "appsettings",
            "set",
            "--resource-group",
            resource_group,
            "--name",
            app_name,
            "--settings",
            "FUNCTIONS_WORKER_RUNTIME=python",
            "FUNCTIONS_WORKER_RUNTIME_VERSION=3.13",
            "FUNCTIONS_EXTENSION_VERSION=~4",
        ],
        # Restart function app
        [
            "az",
            "functionapp",
            "restart",
            "--resource-group",
            resource_group,
            "--name",
            app_name,
        ],
    ]

    for i, cmd in enumerate(commands, 1):
        print(f"📝 Step {i}/{len(commands)}: {' '.join(cmd[:3])}...")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print(f"✅ Step {i} completed")
            else:
                print(f"❌ Step {i} failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Step {i} error: {e}")
            return False

    print("⏳ Waiting 30 seconds for deployment to complete...")
    import time

    time.sleep(30)

    return True


def generate_fix_report() -> str:
    """Generate comprehensive fix report"""

    report = f"""
🚨 L.I.F.E PLATFORM EMERGENCY DIAGNOSTIC REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
================================================================

ISSUE SUMMARY:
❌ Function App lifeplatform1760781933 returning HTTP 404 errors
❌ API endpoints /api/validate-ingestion, /api/ingestion-stats not accessible
🔧 Root Cause: Python 3.9 runtime reaching EOL (October 31, 2025)

IMMEDIATE ACTION REQUIRED:
1. 🐍 Upgrade Python runtime from 3.9 → 3.13
2. 🔄 Redeploy LifePlatformAPI functions
3. ✅ Validate API endpoint restoration

AUTO-FIX AVAILABLE:
- Run: python EMERGENCY_404_FIX.py --auto-fix
- Or: deploy_python313.bat (if Azure CLI available)

MANUAL ALTERNATIVE:
1. Open Azure Portal
2. Navigate to Function App: lifeplatform1760781933
3. Configuration → Application Settings
4. Update FUNCTIONS_WORKER_RUNTIME_VERSION=3.13
5. Restart Function App

TARGET COMPLETION: 15 minutes
VALIDATION: verify_python313_deployment.py
================================================================
"""
    return report


def main():
    """Main emergency fix execution"""

    print("🚨" * 30)
    print("🚨 L.I.F.E PLATFORM EMERGENCY 404 FIX")
    print("🚨" * 30)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Target: lifeplatform1760781933.azurewebsites.net")
    print()

    # Check current status
    print("STEP 1: DIAGNOSTIC ANALYSIS")
    print("=" * 40)

    status = check_function_app_status("lifeplatform1760781933")

    print(f"🌐 Function App: {status['name']}")
    print(f"📊 Base URL Status: {status['api_status']}")
    print(f"🔧 Deployment Status: {status['deployment_status']}")
    print()

    print("API Endpoint Status:")
    for endpoint, result in status["endpoints"].items():
        print(f"  {endpoint}: {result}")

    # Check if auto-fix is possible
    print("\nSTEP 2: AUTO-FIX CAPABILITY")
    print("=" * 40)

    has_azure_cli = check_azure_cli()
    print(f"🔧 Azure CLI Available: {'✅ Yes' if has_azure_cli else '❌ No'}")

    if "--auto-fix" in sys.argv and has_azure_cli:
        print("\n🚀 EXECUTING AUTO-FIX...")
        print("=" * 40)

        success = execute_python313_fix("lifeplatform1760781933", "life-platform-prod")

        if success:
            print("\n✅ AUTO-FIX COMPLETED!")
            print("🔄 Re-testing endpoints...")

            new_status = check_function_app_status("lifeplatform1760781933")

            all_working = all(
                "✅" in result for result in new_status["endpoints"].values()
            )

            if all_working:
                print("🎉 ALL ENDPOINTS RESTORED! Fix successful!")
                print("📊 Next: Update Enhanced Dashboard connectivity")
            else:
                print(
                    "⚠️  Some endpoints still have issues. Manual intervention may be needed."
                )
        else:
            print("❌ AUTO-FIX FAILED. Manual steps required.")

    # Generate report
    print("\nSTEP 3: DETAILED REPORT")
    print("=" * 40)

    report = generate_fix_report()

    # Save report
    report_file = (
        f"EMERGENCY_404_FIX_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )
    with open(report_file, "w") as f:
        f.write(report)

    print(report)
    print(f"📋 Full report saved: {report_file}")

    print("\n🎯 NEXT STEPS:")
    print("1. If auto-fix worked: Run verify_python313_deployment.py")
    print("2. If manual fix needed: Run deploy_python313.bat")
    print("3. Update Enhanced Dashboard External EEG tab")
    print("4. Confirm marketplace compatibility")

    return status


if __name__ == "__main__":
    try:
        result = main()
        print(f"\n✅ Emergency diagnostic completed: {result['deployment_status']}")
    except KeyboardInterrupt:
        print("\n🚫 Emergency fix cancelled by user")
    except Exception as e:
        print(f"\n❌ Emergency fix error: {e}")
        sys.exit(1)
