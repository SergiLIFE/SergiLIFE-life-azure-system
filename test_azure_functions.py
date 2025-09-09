#!/usr/bin/env python3
"""
🚀 Quick Azure Functions Test
============================

Quick test of the Azure Functions enterprise workflow.
"""

import subprocess
import sys
from pathlib import Path


def test_azure_functions_workflow():
    """Test the Azure Functions workflow."""
    print("🧪 Testing Azure Functions Enterprise Workflow")
    print("=" * 50)

    # Check if workflow exists
    workflow_file = Path("azure_functions_workflow.py")
    if not workflow_file.exists():
        print("❌ Azure Functions workflow file not found")
        return False

    # Test workflow help
    try:
        result = subprocess.run(
            ["python", "azure_functions_workflow.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            print("✅ Workflow help accessible")
            print("📋 Available options:")
            print(result.stdout)
            return True
        else:
            print("❌ Workflow help failed")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main():
    """Main test function."""
    if test_azure_functions_workflow():
        print("\n🎉 Azure Functions workflow is ready to use!")
        print("\n🚀 To start the workflow:")
        print("   python azure_functions_workflow.py")
        print("\n📋 Example with options:")
        print(
            "   python azure_functions_workflow.py --language python --project-name my-functions"
        )
    else:
        print("\n❌ Azure Functions workflow test failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
