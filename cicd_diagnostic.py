#!/usr/bin/env python3
"""
CI/CD Pipeline Diagnostic Tool
Identifies and fixes common GitHub Actions workflow failures
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def check_python_environment():
    """Check Python environment and dependencies"""
    print("🐍 Checking Python Environment...")

    try:
        # Check Python version
        result = subprocess.run(
            [sys.executable, "--version"], capture_output=True, text=True
        )
        print(f"✅ Python: {result.stdout.strip()}")

        # Check if pip is available
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"], capture_output=True, text=True
        )
        print(f"✅ Pip: {result.stdout.strip()}")

        return True
    except Exception as e:
        print(f"❌ Python environment issue: {e}")
        return False


def check_requirements():
    """Check if requirements files exist and are valid"""
    print("\n📦 Checking Requirements Files...")

    files_to_check = ["requirements.txt", "requirements-test.txt"]
    issues = []

    for req_file in files_to_check:
        if Path(req_file).exists():
            print(f"✅ Found: {req_file}")
            try:
                with open(req_file, "r") as f:
                    lines = f.readlines()
                    print(f"   📄 {len(lines)} dependencies listed")
            except Exception as e:
                issues.append(f"Error reading {req_file}: {e}")
                print(f"❌ Error reading {req_file}: {e}")
        else:
            issues.append(f"Missing required file: {req_file}")
            print(f"❌ Missing: {req_file}")

    return issues


def check_test_files():
    """Check if test files exist and are importable"""
    print("\n🧪 Checking Test Files...")

    test_files = [
        "test_autonomous_optimizer.py",
        "test_model_optimizer.py",
        "test_sota_integration.py",
        "test_azure_functions.py",
        "tests/test_venturi_batching.py",
    ]

    issues = []

    for test_file in test_files:
        if Path(test_file).exists():
            print(f"✅ Found: {test_file}")
            # Try to parse the file
            try:
                with open(test_file, "r") as f:
                    content = f.read()
                    if "import" in content and "def test_" in content:
                        print(f"   📝 Valid test structure")
                    else:
                        issues.append(f"{test_file} may not have proper test structure")
            except Exception as e:
                issues.append(f"Error reading {test_file}: {e}")
        else:
            issues.append(f"Missing test file: {test_file}")
            print(f"❌ Missing: {test_file}")

    return issues


def check_azure_dependencies():
    """Check Azure-specific dependencies and configurations"""
    print("\n☁️ Checking Azure Dependencies...")

    azure_files = [
        "azure_config.py",
        "azure_functions_config.py",
        "infra/main.bicep",
        "infra/main.parameters.json",
    ]

    issues = []

    for azure_file in azure_files:
        if Path(azure_file).exists():
            print(f"✅ Found: {azure_file}")
        else:
            issues.append(f"Missing Azure file: {azure_file}")
            print(f"❌ Missing: {azure_file}")

    return issues


def check_workflow_secrets():
    """Check if required GitHub secrets are properly configured"""
    print("\n🔐 Checking Workflow Configuration...")

    # Read workflow files and extract required secrets
    workflow_dir = Path(".github/workflows")
    required_secrets = set()

    if workflow_dir.exists():
        for workflow_file in workflow_dir.glob("*.yml"):
            print(f"📄 Analyzing: {workflow_file.name}")
            try:
                with open(workflow_file, "r") as f:
                    content = f.read()
                    # Extract secrets references
                    import re

                    secrets_found = re.findall(r"secrets\.([A-Z_]+)", content)
                    required_secrets.update(secrets_found)
            except Exception as e:
                print(f"❌ Error reading {workflow_file}: {e}")

    print(f"🔑 Required GitHub Secrets:")
    for secret in sorted(required_secrets):
        print(f"   - {secret}")

    return list(required_secrets)


def check_import_issues():
    """Check for common Python import issues"""
    print("\n🔍 Checking Import Issues...")

    python_files = list(Path(".").glob("*.py"))
    issues = []

    for py_file in python_files:
        if py_file.name.startswith("test_"):
            try:
                with open(py_file, "r") as f:
                    content = f.read()
                    # Check for imports
                    lines = content.split("\n")
                    for i, line in enumerate(lines, 1):
                        if line.strip().startswith("from ") or line.strip().startswith(
                            "import "
                        ):
                            # Check if it's importing a local module
                            if "from " in line and not any(
                                stdlib in line
                                for stdlib in [
                                    "sys",
                                    "os",
                                    "time",
                                    "json",
                                    "pathlib",
                                    "subprocess",
                                    "numpy",
                                    "pytest",
                                    "asyncio",
                                ]
                            ):
                                module = (
                                    line.split("from ")[1].split(" import")[0].strip()
                                )
                                if not Path(f"{module}.py").exists():
                                    issues.append(
                                        f"{py_file}:{i} - Missing module: {module}"
                                    )
            except Exception as e:
                issues.append(f"Error analyzing {py_file}: {e}")

    if issues:
        print("❌ Import Issues Found:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("✅ No obvious import issues detected")

    return issues


def generate_fix_suggestions(all_issues):
    """Generate specific fix suggestions based on identified issues"""
    print("\n🔧 Fix Suggestions:")
    print("=" * 50)

    if not all_issues:
        print("✅ No critical issues detected!")
        return

    fixes = []

    for issue in all_issues:
        if "Missing test file" in issue:
            fixes.append(f"Create missing test file: {issue.split(': ')[1]}")
        elif "Missing required file" in issue:
            fixes.append(f"Create missing file: {issue.split(': ')[1]}")
        elif "Missing module" in issue:
            module = issue.split("Missing module: ")[1]
            fixes.append(f"Create or fix import for module: {module}")
        elif "Missing Azure file" in issue:
            fixes.append(f"Create Azure configuration: {issue.split(': ')[1]}")

    for i, fix in enumerate(fixes, 1):
        print(f"{i}. {fix}")

    return fixes


def main():
    """Main diagnostic routine"""
    print("🔍 L.I.F.E. Platform CI/CD Diagnostic Tool")
    print("=" * 60)

    all_issues = []

    # Run all checks
    if not check_python_environment():
        print("❌ Critical: Python environment not properly configured")
        return 1

    all_issues.extend(check_requirements())
    all_issues.extend(check_test_files())
    all_issues.extend(check_azure_dependencies())
    all_issues.extend(check_import_issues())

    required_secrets = check_workflow_secrets()

    # Generate summary
    print(f"\n📊 Diagnostic Summary:")
    print(f"   🔍 Issues Found: {len(all_issues)}")
    print(f"   🔑 Required Secrets: {len(required_secrets)}")

    if all_issues:
        print(f"\n❌ Issues Detected:")
        for issue in all_issues:
            print(f"   • {issue}")

    # Generate fixes
    generate_fix_suggestions(all_issues)

    # Create action plan
    print(f"\n🎯 Action Plan:")
    print("1. Fix missing files and dependencies")
    print("2. Configure GitHub repository secrets")
    print("3. Test workflows locally before pushing")
    print("4. Monitor GitHub Actions for specific error messages")

    return 0 if not all_issues else 1


if __name__ == "__main__":
    sys.exit(main())
