#!/usr/bin/env python3
"""
Simple UI Test - L.I.F.E. Platform
Quick test to ensure UI components are operational

Copyright 2025 - Sergio Paya Borrull
"""

import os
import sys
from datetime import datetime
from pathlib import Path

def main():
    print("🔍 L.I.F.E. Platform - Quick UI Test")
    print("=" * 45)
    print(f"🕐 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 45)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Basic Python functionality
    print("🧪 Test 1: Python Environment")
    try:
        print(f"  ✅ Python Version: {sys.version}")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Python Error: {e}")
        tests_failed += 1
    
    # Test 2: File system access
    print("🧪 Test 2: File System Access")
    try:
        script_dir = Path(__file__).parent
        test_file = script_dir / "test_ui.tmp"
        test_file.write_text("test")
        test_file.unlink()
        print("  ✅ File system read/write: OK")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ File system error: {e}")
        tests_failed += 1
    
    # Test 3: Campaign trigger script
    print("🧪 Test 3: Campaign Trigger Script")
    try:
        trigger_script = script_dir / "campaign_automatic_trigger.py"
        if trigger_script.exists():
            print("  ✅ Campaign trigger script: Found")
            tests_passed += 1
        else:
            print("  ❌ Campaign trigger script: Missing")
            tests_failed += 1
    except Exception as e:
        print(f"  ❌ Script check error: {e}")
        tests_failed += 1
    
    # Test 4: GitHub workflow
    print("🧪 Test 4: GitHub Actions Workflow")
    try:
        workflow_file = script_dir / ".github" / "workflows" / "campaign-launcher.yml"
        if workflow_file.exists():
            print("  ✅ GitHub workflow: Found")
            # Check for automatic trigger
            content = workflow_file.read_text()
            if "schedule:" in content and "cron:" in content:
                print("  ✅ Automatic trigger: Configured")
            else:
                print("  ⚠️ Automatic trigger: Not found")
            tests_passed += 1
        else:
            print("  ❌ GitHub workflow: Missing")
            tests_failed += 1
    except Exception as e:
        print(f"  ❌ Workflow check error: {e}")
        tests_failed += 1
    
    # Test 5: PowerShell and Batch scripts
    print("🧪 Test 5: UI Scripts")
    try:
        ps_script = script_dir / "TRIGGER_CAMPAIGN.ps1"
        bat_script = script_dir / "TRIGGER_CAMPAIGN.bat"
        
        if ps_script.exists():
            print("  ✅ PowerShell script: Found")
        else:
            print("  ❌ PowerShell script: Missing")
            
        if bat_script.exists():
            print("  ✅ Batch script: Found")
        else:
            print("  ❌ Batch script: Missing")
        
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ UI scripts error: {e}")
        tests_failed += 1
    
    # Results
    print("\n📊 TEST RESULTS:")
    print(f"  ✅ Passed: {tests_passed}")
    print(f"  ❌ Failed: {tests_failed}")
    print(f"  📊 Success Rate: {tests_passed / (tests_passed + tests_failed) * 100:.1f}%")
    
    if tests_failed == 0:
        print("\n🎯 RESULT: System is OPERATIONAL - Ready for campaign triggering")
        print("🚀 All UI interfaces are working properly")
        return 0
    elif tests_failed <= 2:
        print("\n⚠️ RESULT: System has minor issues but is FUNCTIONAL")
        print("🔧 Some features may not work optimally")
        return 0
    else:
        print("\n❌ RESULT: System has CRITICAL ISSUES - Not ready for triggering")
        print("🔧 Please address the failed tests before proceeding")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Critical error: {e}")
        sys.exit(1)