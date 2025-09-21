#!/usr/bin/env python3
"""
🚀 VS Code Repository Quick Setup
================================

Quick setup script to fetch VS Code configurations from your .vscode repository
and other common VS Code configuration sources.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb

This script will:
1. Backup your current .vscode settings
2. Fetch configurations from specified repositories
3. Merge settings intelligently to avoid conflicts
4. Install recommended extensions
5. Validate the final configuration

Usage:
    python setup_vscode_repo.py
    python setup_vscode_repo.py --repo https://github.com/SergiLIFE/.vscode
    python setup_vscode_repo.py --quick-setup
"""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class QuickVSCodeSetup:
    """Quick VS Code repository synchronization for L.I.F.E. platform."""

    def __init__(self):
        self.workspace_dir = Path.cwd()
        self.vscode_dir = self.workspace_dir / ".vscode"
        self.backup_dir = (
            self.workspace_dir
            / "backups"
            / f"vscode_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        # Common VS Code repositories to sync from
        self.known_repos = {
            "SergiLIFE/.vscode": "https://github.com/SergiLIFE/.vscode",
            "microsoft/vscode-samples": "https://github.com/microsoft/vscode-samples",
            "microsoft/vscode-python": "https://github.com/microsoft/vscode-python",
            "microsoft/vscode-extension-samples": "https://github.com/microsoft/vscode-extension-samples",
        }

        # Essential extensions for L.I.F.E. development
        self.essential_extensions = [
            "ms-python.python",
            "ms-python.pylint",
            "ms-python.black-formatter",
            "ms-vscode.azure-account",
            "ms-azuretools.vscode-azureresourcegroups",
            "ms-azuretools.vscode-azurefunctions",
            "ms-vscode.vscode-json",
            "redhat.vscode-yaml",
            "ms-vscode.powershell",
            "github.copilot",
            "github.copilot-chat",
        ]

    def create_backup(self):
        """Create backup of existing VS Code configuration."""
        if self.vscode_dir.exists():
            print(f"📦 Creating backup: {self.backup_dir}")
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copytree(self.vscode_dir, self.backup_dir / ".vscode")
            return True
        return False

    def quick_setup_from_github(self, repo_name="SergiLIFE/.vscode"):
        """Quick setup from a specific GitHub repository."""
        print(f"🔄 Quick setup from {repo_name}")

        if repo_name in self.known_repos:
            repo_url = self.known_repos[repo_name]
        else:
            repo_url = f"https://github.com/{repo_name}"

        # Use git to clone temporarily
        temp_dir = self.workspace_dir / "temp_vscode_sync"

        try:
            # Clone repository
            print(f"📥 Cloning {repo_url}...")
            subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, str(temp_dir)],
                check=True,
                capture_output=True,
            )

            # Copy .vscode directory if it exists
            source_vscode = temp_dir / ".vscode"
            if source_vscode.exists():
                self.vscode_dir.mkdir(exist_ok=True)

                for file_path in source_vscode.iterdir():
                    if file_path.is_file():
                        target_path = self.vscode_dir / file_path.name

                        if file_path.suffix == ".json" and target_path.exists():
                            # Merge JSON files
                            self.merge_json_file(file_path, target_path)
                        else:
                            shutil.copy2(file_path, target_path)

                        print(f"✅ Synced: {file_path.name}")

            # Copy development tools
            for file_path in temp_dir.iterdir():
                if file_path.is_file() and file_path.suffix == ".py":
                    if any(
                        keyword in file_path.name.lower()
                        for keyword in [
                            "setup",
                            "tool",
                            "dev",
                            "monitor",
                            "test",
                            "vscode",
                        ]
                    ):
                        target_path = self.workspace_dir / file_path.name
                        if not target_path.exists():
                            shutil.copy2(file_path, target_path)
                            print(f"🛠️  Added tool: {file_path.name}")

            print("✅ Repository sync completed!")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Git clone failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False
        finally:
            # Cleanup
            if temp_dir.exists():
                shutil.rmtree(temp_dir)

    def merge_json_file(self, source_path, target_path):
        """Merge JSON configuration files."""
        try:
            with open(source_path, "r") as f:
                source_data = json.load(f)

            with open(target_path, "r") as f:
                target_data = json.load(f)

            # Simple merge strategy
            if isinstance(source_data, dict) and isinstance(target_data, dict):
                merged_data = {**target_data, **source_data}

                with open(target_path, "w") as f:
                    json.dump(merged_data, f, indent=2)

                print(f"🔀 Merged: {target_path.name}")
            else:
                # Replace if not dictionaries
                shutil.copy2(source_path, target_path)

        except Exception as e:
            print(f"❌ Failed to merge {target_path.name}: {e}")
            # Fallback to copy
            shutil.copy2(source_path, target_path)

    def install_extensions(self):
        """Install essential VS Code extensions."""
        print("🔌 Installing VS Code extensions...")

        installed_count = 0
        for extension in self.essential_extensions:
            try:
                result = subprocess.run(
                    ["code", "--install-extension", extension],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode == 0:
                    print(f"   ✅ {extension}")
                    installed_count += 1
                else:
                    print(f"   ⚠️  {extension}: {result.stderr.strip()}")

            except subprocess.TimeoutExpired:
                print(f"   ⏱️  {extension}: Timeout")
            except FileNotFoundError:
                print("❌ VS Code CLI not found. Install extensions manually.")
                break
            except Exception as e:
                print(f"   ❌ {extension}: {e}")

        print(
            f"📊 Installed {installed_count}/{len(self.essential_extensions)} extensions"
        )
        return installed_count > 0

    def create_essential_configs(self):
        """Create essential VS Code configuration files."""
        self.vscode_dir.mkdir(exist_ok=True)

        # Essential settings.json
        settings = {
            "python.defaultInterpreterPath": "python",
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": True,
            "python.formatting.provider": "black",
            "files.autoSave": "afterDelay",
            "editor.formatOnSave": True,
            "git.autofetch": True,
            "terminal.integrated.defaultProfile.windows": "PowerShell",
            "azure.cloud": "AzureCloud",
            "files.associations": {"*.yaml": "yaml", "*.yml": "yaml"},
        }

        settings_file = self.vscode_dir / "settings.json"
        if settings_file.exists():
            with open(settings_file, "r") as f:
                existing_settings = json.load(f)
            settings = {**existing_settings, **settings}

        with open(settings_file, "w") as f:
            json.dump(settings, f, indent=2)

        print("✅ Created essential settings.json")

        # Essential extensions.json
        extensions = {"recommendations": self.essential_extensions}

        with open(self.vscode_dir / "extensions.json", "w") as f:
            json.dump(extensions, f, indent=2)

        print("✅ Created extensions.json")

        # Basic tasks.json
        tasks = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "🐍 Run Python File",
                    "type": "shell",
                    "command": "python",
                    "args": ["${file}"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                    },
                },
                {
                    "label": "🧪 Run Tests",
                    "type": "shell",
                    "command": "python",
                    "args": ["-m", "pytest", "-v"],
                    "group": "test",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                    },
                },
            ],
        }

        with open(self.vscode_dir / "tasks.json", "w") as f:
            json.dump(tasks, f, indent=2)

        print("✅ Created tasks.json")

    def validate_setup(self):
        """Validate the VS Code setup."""
        print("🔍 Validating VS Code setup...")

        essential_files = ["settings.json", "extensions.json", "tasks.json"]
        all_good = True

        for file_name in essential_files:
            file_path = self.vscode_dir / file_name
            if file_path.exists():
                try:
                    with open(file_path, "r") as f:
                        json.load(f)
                    print(f"   ✅ {file_name}: Valid")
                except json.JSONDecodeError:
                    print(f"   ❌ {file_name}: Invalid JSON")
                    all_good = False
            else:
                print(f"   ⚠️  {file_name}: Missing")
                all_good = False

        if all_good:
            print("✅ VS Code setup validation passed!")
        else:
            print("⚠️  Some issues found in VS Code setup")

        return all_good

    def run_interactive_setup(self):
        """Run interactive setup process."""
        print("🚀 VS Code Repository Setup for L.I.F.E. Platform")
        print("=" * 50)

        # Create backup
        self.create_backup()

        print("\n📋 Setup Options:")
        print("1. Quick setup from SergiLIFE/.vscode repository")
        print("2. Setup from custom GitHub repository")
        print("3. Create minimal configuration only")
        print("4. Install extensions only")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":
            # Quick setup from SergiLIFE/.vscode
            success = self.quick_setup_from_github("SergiLIFE/.vscode")
            if not success:
                print("⚠️  GitHub sync failed, creating minimal config...")
                self.create_essential_configs()

        elif choice == "2":
            # Custom repository
            repo_input = input(
                "Enter GitHub repository (owner/repo or full URL): "
            ).strip()
            if "/" in repo_input:
                if repo_input.startswith("https://"):
                    # Extract owner/repo from URL
                    parts = repo_input.split("/")
                    repo_name = f"{parts[-2]}/{parts[-1].replace('.git', '')}"
                else:
                    repo_name = repo_input

                success = self.quick_setup_from_github(repo_name)
                if not success:
                    print("⚠️  Repository sync failed, creating minimal config...")
                    self.create_essential_configs()
            else:
                print("❌ Invalid repository format")
                return False

        elif choice == "3":
            # Minimal configuration
            self.create_essential_configs()

        elif choice == "4":
            # Extensions only
            self.install_extensions()
            return True

        else:
            print("❌ Invalid choice")
            return False

        # Install extensions
        if input("\nInstall VS Code extensions? (y/n): ").lower() == "y":
            self.install_extensions()

        # Validate setup
        self.validate_setup()

        print("\n🎉 VS Code setup completed!")
        print("💡 Restart VS Code to apply all changes.")

        return True


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="VS Code Repository Setup")
    parser.add_argument("--repo", help="GitHub repository to sync from")
    parser.add_argument(
        "--quick-setup", action="store_true", help="Quick setup from SergiLIFE/.vscode"
    )
    parser.add_argument(
        "--extensions-only", action="store_true", help="Install extensions only"
    )

    args = parser.parse_args()

    setup = QuickVSCodeSetup()

    if args.quick_setup:
        setup.create_backup()
        setup.quick_setup_from_github("SergiLIFE/.vscode")
        setup.install_extensions()
        setup.validate_setup()
    elif args.repo:
        setup.create_backup()
        setup.quick_setup_from_github(args.repo)
        setup.install_extensions()
        setup.validate_setup()
    elif args.extensions_only:
        setup.install_extensions()
    else:
        setup.run_interactive_setup()


if __name__ == "__main__":
    main()
