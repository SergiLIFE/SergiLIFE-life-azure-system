"""Quick path diagnostic and directory creation test"""

import os
import sys

print("=" * 60)
print("PATH DIAGNOSTIC TEST")
print("=" * 60)

# Get current info
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
current_dir = os.getcwd()

print(f"\nCurrent working directory:")
print(f"  {current_dir}")
print(f"\nScript location:")
print(f"  {script_path}")
print(f"\nScript directory:")
print(f"  {script_dir}")

# Test directory creation
print("\n" + "=" * 60)
print("TESTING DIRECTORY CREATION")
print("=" * 60)

test_dirs = ["logs", "results"]

for dir_name in test_dirs:
    full_path = os.path.join(current_dir, dir_name)
    print(f"\nTrying to create: {dir_name}")
    print(f"Full path: {full_path}")

    try:
        if not os.path.exists(full_path):
            os.mkdir(full_path)  # Use mkdir instead of makedirs
            print(f"  ✅ SUCCESS - Created {dir_name}")
        else:
            print(f"  ℹ️  Already exists")
    except Exception as e:
        print(f"  ❌ FAILED: {e}")

# List what we have now
print("\n" + "=" * 60)
print("CURRENT DIRECTORY CONTENTS")
print("=" * 60)
try:
    items = os.listdir(current_dir)
    for item in sorted(items):
        if os.path.isdir(os.path.join(current_dir, item)):
            print(f"  📁 {item}")
    print(f"\nTotal items: {len(items)}")
except Exception as e:
    print(f"  ❌ Could not list directory: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
