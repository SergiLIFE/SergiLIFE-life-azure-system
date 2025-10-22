#!/usr/bin/env python3
"""
Azure Function App Status Check
Checks if the Function App exists and what its status is
"""
import json
import subprocess
import sys


def run_az_command(command):
    """Run Azure CLI command and return result"""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def main():
    print("=" * 60)
    print("AZURE FUNCTION APP STATUS CHECK")
    print("=" * 60)

    func_app_name = "life-functions-app-prod"
    resource_group = "life-platform-prod"

    print(f"Checking Function App: {func_app_name}")
    print(f"Resource Group: {resource_group}")
    print()

    # Check if Function App exists
    print("[1] Checking if Function App exists...")
    cmd = f'az functionapp show --name {func_app_name} --resource-group {resource_group} --query "{{name:name, state:state, kind:kind}}" --output json'

    returncode, stdout, stderr = run_az_command(cmd)

    if returncode == 0:
        try:
            data = json.loads(stdout)
            print("✅ Function App EXISTS!")
            print(f"   Name: {data.get('name', 'Unknown')}")
            print(f"   State: {data.get('state', 'Unknown')}")
            print(f"   Kind: {data.get('kind', 'Unknown')}")

            # Check deployed functions
            print()
            print("[2] Checking deployed functions...")
            cmd_functions = f"az functionapp function list --name {func_app_name} --resource-group {resource_group} --output json"

            returncode2, stdout2, stderr2 = run_az_command(cmd_functions)

            if returncode2 == 0:
                try:
                    functions = json.loads(stdout2)
                    if functions:
                        print(f"✅ Found {len(functions)} deployed functions:")
                        for func in functions:
                            print(f"   - {func.get('name', 'Unknown')}")
                    else:
                        print("❌ NO FUNCTIONS DEPLOYED!")
                        print(
                            "   This explains the 404 error - no functions are deployed."
                        )
                        print(
                            "   Solution: Need to deploy functions to the Function App."
                        )
                except json.JSONDecodeError:
                    print("⚠️  Could not parse functions list")
            else:
                print(f"❌ Error checking functions: {stderr2}")

        except json.JSONDecodeError:
            print("⚠️  Could not parse Function App data")

    else:
        print("❌ Function App does NOT exist!")
        print("   This explains the 404 error.")
        print(f"   Error: {stderr}")
        print()
        print("📝 SOLUTION:")
        print(f"   1. Create Function App: {func_app_name}")
        print(f"   2. In Resource Group: {resource_group}")
        print("   3. Deploy functions to it")
        return False

    print()
    print("=" * 60)

    return True


if __name__ == "__main__":
    exists = main()
    if not exists:
        print(
            "🔧 Would you like me to create the Function App? (This will be done in the next step)"
        )
    else:
        print("🎯 Function App exists - checking why endpoints return 404...")
