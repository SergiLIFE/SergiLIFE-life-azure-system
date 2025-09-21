#!/usr/bin/env python3
"""
🔐 Private Repository VS Code Sync
==================================

Simple manual sync tool for private .vscode repositories.
Handles authentication and provides step-by-step guidance.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path


def manual_sync_guide():
    """Provide step-by-step guide for manual sync from private repo."""
    print("🔐 Private Repository VS Code Sync Guide")
    print("=" * 50)
    print()

    workspace_dir = Path.cwd()
    vscode_dir = workspace_dir / ".vscode"

    print("📋 Manual Sync Steps for Private Repository:")
    print()

    print("1. 🌐 Open your private .vscode repository in browser:")
    print("   https://github.com/SergiLIFE/.vscode")
    print()

    print("2. 📁 Navigate to the files you want to sync:")
    print("   • settings.json")
    print("   • tasks.json")
    print("   • launch.json")
    print("   • extensions.json")
    print("   • Any .py development tools")
    print()

    print("3. 📥 For each file:")
    print("   • Click the file name")
    print("   • Click 'Raw' button")
    print("   • Copy the content (Ctrl+A, Ctrl+C)")
    print("   • I'll help you merge it safely")
    print()

    # Check what we already have
    if vscode_dir.exists():
        print("✅ Current .vscode directory contents:")
        for file_path in vscode_dir.iterdir():
            if file_path.is_file():
                print(f"   • {file_path.name}")
        print()
    else:
        print("📁 No .vscode directory found - will create fresh setup")
        vscode_dir.mkdir(exist_ok=True)
        print()

    return vscode_dir


def safe_merge_json(existing_file, new_content, file_name):
    """Safely merge JSON content with conflict resolution."""
    try:
        if existing_file.exists():
            with open(existing_file, "r") as f:
                existing_data = json.load(f)

            new_data = json.loads(new_content)

            print(f"🔀 Merging {file_name}...")

            if isinstance(existing_data, dict) and isinstance(new_data, dict):
                # Show conflicts
                conflicts = []
                for key, value in new_data.items():
                    if key in existing_data and existing_data[key] != value:
                        conflicts.append((key, existing_data[key], value))

                if conflicts:
                    print(f"⚠️  Found {len(conflicts)} conflicts in {file_name}:")
                    for key, old_val, new_val in conflicts:
                        print(f"   {key}:")
                        print(f"     Current: {old_val}")
                        print(f"     New:     {new_val}")

                    choice = input("Keep new values? (y/n/review): ").lower()
                    if choice == "review":
                        for key, old_val, new_val in conflicts:
                            keep = input(f"Keep new value for '{key}'? (y/n): ").lower()
                            if keep != "y":
                                new_data[key] = old_val
                    elif choice == "n":
                        for key, old_val, _ in conflicts:
                            new_data[key] = old_val

                # Merge
                merged_data = {**existing_data, **new_data}

                # Create backup
                backup_file = existing_file.with_suffix(".backup")
                shutil.copy2(existing_file, backup_file)
                print(f"📦 Backup created: {backup_file.name}")

                # Write merged content
                with open(existing_file, "w") as f:
                    json.dump(merged_data, f, indent=2)

                print(f"✅ {file_name} merged successfully")

            else:
                # Not both dicts, just replace
                choice = input(f"Replace {file_name} entirely? (y/n): ").lower()
                if choice == "y":
                    with open(existing_file, "w") as f:
                        json.dump(new_data, f, indent=2)
                    print(f"✅ {file_name} replaced")
        else:
            # New file
            new_data = json.loads(new_content)
            with open(existing_file, "w") as f:
                json.dump(new_data, f, indent=2)
            print(f"✅ {file_name} created")

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {file_name}: {e}")
        print("Please check the content and try again.")
        return False
    except Exception as e:
        print(f"❌ Error processing {file_name}: {e}")
        return False

    return True


def interactive_file_sync(vscode_dir):
    """Interactive file-by-file sync process."""
    config_files = ["settings.json", "tasks.json", "launch.json", "extensions.json"]

    print("🔄 Interactive File Sync")
    print("-" * 30)

    for file_name in config_files:
        print(f"\n📝 {file_name}:")
        print("1. Go to: https://github.com/SergiLIFE/.vscode")
        print(f"2. Click on: {file_name}")
        print("3. Click 'Raw' button")
        print("4. Copy all content (Ctrl+A, Ctrl+C)")

        choice = input(f"Ready to paste {file_name} content? (y/n/skip): ").lower()

        if choice == "y":
            print(
                f"Paste the {file_name} content below (press Ctrl+Z then Enter when done):"
            )
            print("-" * 40)

            # Read multi-line input
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass

            content = "\n".join(lines)

            if content.strip():
                file_path = vscode_dir / file_name
                success = safe_merge_json(file_path, content, file_name)
                if success:
                    print(f"🎉 {file_name} synced successfully!")
                else:
                    print(f"❌ Failed to sync {file_name}")
            else:
                print("⚠️  No content provided, skipping...")

        elif choice == "skip":
            print(f"⏭️  Skipping {file_name}")
        else:
            print("❌ Cancelled sync process")
            break

    print("\n✅ Interactive sync completed!")


def validate_setup(vscode_dir):
    """Validate the synced VS Code setup."""
    print("\n🔍 Validating VS Code Setup...")
    print("-" * 35)

    essential_files = ["settings.json", "tasks.json", "launch.json", "extensions.json"]
    valid_files = 0

    for file_name in essential_files:
        file_path = vscode_dir / file_name
        if file_path.exists():
            try:
                with open(file_path, "r") as f:
                    json.load(f)
                print(f"   ✅ {file_name}: Valid JSON")
                valid_files += 1
            except json.JSONDecodeError:
                print(f"   ❌ {file_name}: Invalid JSON")
        else:
            print(f"   ⚠️  {file_name}: Not found")

    print(f"\n📊 Validation Results: {valid_files}/{len(essential_files)} files valid")

    if valid_files == len(essential_files):
        print("🎉 All essential files are valid!")
        print("\n💡 Next steps:")
        print("   1. Restart VS Code")
        print("   2. Open your workspace")
        print("   3. Press F5 to test debugging")
        print("   4. Try Ctrl+Shift+P → 'Tasks: Run Task'")
    else:
        print("⚠️  Some issues found. Please review the files above.")

    return valid_files == len(essential_files)


def main():
    """Main entry point for private repository sync."""
    print("🔐 Starting Private Repository Sync...")
    print()

    try:
        # Guide user through manual sync
        vscode_dir = manual_sync_guide()

        # Choose sync method
        print("🔄 Sync Options:")
        print("1. Interactive file-by-file sync (recommended)")
        print("2. View current configuration only")
        print("3. Create minimal configuration")

        choice = input("Select option (1-3): ").strip()

        if choice == "1":
            interactive_file_sync(vscode_dir)
            validate_setup(vscode_dir)
        elif choice == "2":
            if vscode_dir.exists():
                print("\n📁 Current VS Code configuration:")
                for file_path in vscode_dir.iterdir():
                    if file_path.is_file() and file_path.suffix == ".json":
                        print(f"\n📄 {file_path.name}:")
                        try:
                            with open(file_path, "r") as f:
                                data = json.load(f)
                            print(f"   Keys: {list(data.keys())}")
                        except:
                            print("   Invalid JSON")
            else:
                print("❌ No .vscode directory found")
        elif choice == "3":
            from setup_vscode_repo import QuickVSCodeSetup

            setup = QuickVSCodeSetup()
            setup.create_essential_configs()
            validate_setup(vscode_dir)
        else:
            print("❌ Invalid choice")

    except KeyboardInterrupt:
        print("\n\n⚠️  Sync cancelled by user")
    except Exception as e:
        print(f"\n❌ Error during sync: {e}")


if __name__ == "__main__":
    main()
