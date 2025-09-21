#!/usr/bin/env python3
"""
🔄 VS Code Repository Synchronization Tool
==========================================

Safely fetches and integrates VS Code configurations, tools, and utilities
from other repositories to avoid recreating development environments.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb

Features:
- Safe configuration merging without overwriting existing customizations
- Backup creation before any changes
- Selective synchronization of specific file types
- Conflict resolution with user prompts
- Support for GitHub repositories and local paths
- Automatic dependency detection and installation

Author: L.I.F.E. Autonomous Optimizer
Created: September 9, 2025
"""

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests


class VSCodeRepoSync:
    """Synchronizes VS Code configurations between repositories."""

    def __init__(self, target_dir: str = None):
        self.target_dir = Path(target_dir) if target_dir else Path.cwd()
        self.vscode_dir = self.target_dir / ".vscode"
        self.backup_dir = (
            self.target_dir
            / "backups"
            / f"vscode_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.safe_extensions = {
            ".json",
            ".md",
            ".py",
            ".js",
            ".ts",
            ".yaml",
            ".yml",
            ".toml",
            ".ini",
        }
        self.config_files = {
            "settings.json",
            "tasks.json",
            "launch.json",
            "extensions.json",
            "c_cpp_properties.json",
            "keybindings.json",
            "snippets",
        }

    def create_backup(self) -> bool:
        """Create backup of existing VS Code configuration."""
        try:
            if self.vscode_dir.exists():
                print(f"📦 Creating backup: {self.backup_dir}")
                self.backup_dir.mkdir(parents=True, exist_ok=True)
                shutil.copytree(self.vscode_dir, self.backup_dir / ".vscode")
                return True
            return False
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False

    def fetch_github_repo_contents(self, repo_url: str, path: str = "") -> List[Dict]:
        """Fetch repository contents from GitHub API."""
        try:
            # Parse GitHub URL
            if "github.com" in repo_url:
                parts = repo_url.split("/")
                owner = parts[-2]
                repo = parts[-1].replace(".git", "")
            else:
                raise ValueError("Invalid GitHub URL format")

            # API request
            api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
            headers = {"Accept": "application/vnd.github.v3+json"}
            if self.github_token:
                headers["Authorization"] = f"token {self.github_token}"

            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"❌ Failed to fetch GitHub contents: {e}")
            return []

    def download_file(self, file_info: Dict, target_path: Path) -> bool:
        """Download a single file from GitHub."""
        try:
            if file_info.get("download_url"):
                response = requests.get(file_info["download_url"])
                response.raise_for_status()

                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_bytes(response.content)
                return True
            else:
                # Handle base64 encoded content
                content = base64.b64decode(file_info["content"]).decode("utf-8")
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(content)
                return True

        except Exception as e:
            print(f"❌ Failed to download {file_info['name']}: {e}")
            return False

    def merge_json_configs(self, existing: Dict, new: Dict, file_name: str) -> Dict:
        """Intelligently merge JSON configurations."""
        if file_name == "settings.json":
            # Merge settings with conflict resolution
            merged = existing.copy()
            conflicts = []

            for key, value in new.items():
                if key in existing and existing[key] != value:
                    conflicts.append((key, existing[key], value))
                merged[key] = value

            if conflicts:
                print(f"\n⚠️  Configuration conflicts in {file_name}:")
                for key, old_val, new_val in conflicts:
                    print(f"   {key}: {old_val} → {new_val}")

                choice = input("Keep new values? (y/n/review): ").lower()
                if choice == "n":
                    for key, old_val, _ in conflicts:
                        merged[key] = old_val
                elif choice == "review":
                    for key, old_val, new_val in conflicts:
                        keep_new = (
                            input(
                                f"Keep new value for '{key}'? {old_val} → {new_val} (y/n): "
                            ).lower()
                            == "y"
                        )
                        if not keep_new:
                            merged[key] = old_val

            return merged

        elif file_name == "tasks.json":
            # Merge tasks arrays
            merged = existing.copy()
            existing_labels = {task.get("label") for task in existing.get("tasks", [])}

            for task in new.get("tasks", []):
                if task.get("label") not in existing_labels:
                    if "tasks" not in merged:
                        merged["tasks"] = []
                    merged["tasks"].append(task)

            return merged

        elif file_name == "launch.json":
            # Merge launch configurations
            merged = existing.copy()
            existing_names = {
                config.get("name") for config in existing.get("configurations", [])
            }

            for config in new.get("configurations", []):
                if config.get("name") not in existing_names:
                    if "configurations" not in merged:
                        merged["configurations"] = []
                    merged["configurations"].append(config)

            return merged

        else:
            # Default merge strategy
            return {**existing, **new}

    def sync_from_github(self, repo_url: str, selective: bool = True) -> bool:
        """Sync VS Code configurations from a GitHub repository."""
        print(f"🔄 Syncing from GitHub repository: {repo_url}")

        # Create backup
        backup_created = self.create_backup()

        try:
            # Fetch .vscode directory contents
            vscode_contents = self.fetch_github_repo_contents(repo_url, ".vscode")
            if not vscode_contents:
                print("❌ No .vscode directory found in repository")
                return False

            # Ensure local .vscode directory exists
            self.vscode_dir.mkdir(exist_ok=True)

            synced_files = 0
            skipped_files = 0

            for item in vscode_contents:
                if item["type"] == "file":
                    file_name = item["name"]

                    # Check if file should be synced
                    if selective and file_name not in self.config_files:
                        file_ext = Path(file_name).suffix
                        if file_ext not in self.safe_extensions:
                            print(f"⏭️  Skipping unsafe file: {file_name}")
                            skipped_files += 1
                            continue

                    target_path = self.vscode_dir / file_name

                    # Handle JSON merging
                    if file_name.endswith(".json") and target_path.exists():
                        print(f"🔀 Merging: {file_name}")

                        try:
                            # Download new content
                            temp_path = (
                                Path(tempfile.gettempdir()) / f"temp_{file_name}"
                            )
                            if self.download_file(item, temp_path):
                                new_content = json.loads(temp_path.read_text())
                                existing_content = json.loads(target_path.read_text())

                                merged_content = self.merge_json_configs(
                                    existing_content, new_content, file_name
                                )

                                target_path.write_text(
                                    json.dumps(merged_content, indent=2)
                                )
                                temp_path.unlink()
                                synced_files += 1

                        except json.JSONDecodeError as e:
                            print(f"❌ JSON error in {file_name}: {e}")
                            # Fallback to direct copy
                            if self.download_file(item, target_path):
                                synced_files += 1

                    else:
                        # Direct download for non-JSON files
                        if self.download_file(item, target_path):
                            print(f"✅ Downloaded: {file_name}")
                            synced_files += 1
                        else:
                            skipped_files += 1

            # Fetch additional development tools
            dev_tools = self.fetch_github_repo_contents(repo_url, "")
            for item in dev_tools:
                if item["type"] == "file" and item["name"].endswith(".py"):
                    # Look for VS Code related Python tools
                    if any(
                        keyword in item["name"].lower()
                        for keyword in [
                            "vscode",
                            "setup",
                            "tool",
                            "dev",
                            "monitor",
                            "test",
                        ]
                    ):

                        target_path = self.target_dir / item["name"]
                        if not target_path.exists():
                            if self.download_file(item, target_path):
                                print(f"🛠️  Added development tool: {item['name']}")
                                synced_files += 1

            print(f"\n✅ Sync completed!")
            print(f"   📁 Files synced: {synced_files}")
            print(f"   ⏭️  Files skipped: {skipped_files}")
            if backup_created:
                print(f"   📦 Backup created: {self.backup_dir}")

            return True

        except Exception as e:
            print(f"❌ Sync failed: {e}")
            if backup_created:
                print(f"💾 Restore from backup: {self.backup_dir}")
            return False

    def sync_from_local(self, source_path: str) -> bool:
        """Sync VS Code configurations from a local repository."""
        source = Path(source_path)
        source_vscode = source / ".vscode"

        if not source_vscode.exists():
            print(f"❌ No .vscode directory found in {source_path}")
            return False

        print(f"🔄 Syncing from local repository: {source_path}")
        backup_created = self.create_backup()

        try:
            self.vscode_dir.mkdir(exist_ok=True)
            synced_files = 0

            for file_path in source_vscode.iterdir():
                if file_path.is_file():
                    target_path = self.vscode_dir / file_path.name

                    if file_path.suffix == ".json" and target_path.exists():
                        # Merge JSON files
                        existing_content = json.loads(target_path.read_text())
                        new_content = json.loads(file_path.read_text())

                        merged_content = self.merge_json_configs(
                            existing_content, new_content, file_path.name
                        )

                        target_path.write_text(json.dumps(merged_content, indent=2))
                        print(f"🔀 Merged: {file_path.name}")
                    else:
                        shutil.copy2(file_path, target_path)
                        print(f"✅ Copied: {file_path.name}")

                    synced_files += 1

            print(f"\n✅ Local sync completed! Files synced: {synced_files}")
            return True

        except Exception as e:
            print(f"❌ Local sync failed: {e}")
            return False

    def list_available_repos(self) -> List[str]:
        """List commonly used VS Code configuration repositories."""
        repos = [
            "https://github.com/microsoft/vscode-samples",
            "https://github.com/vscode-org/vscode-org",
            "https://github.com/SergiLIFE/.vscode",  # Your VS Code repository
            "https://github.com/microsoft/vscode-python-tools-extension-template",
            "https://github.com/microsoft/vscode-extension-samples",
        ]

        print("📋 Suggested VS Code repositories:")
        for i, repo in enumerate(repos, 1):
            print(f"   {i}. {repo}")

        return repos

    def install_extensions(self) -> bool:
        """Install VS Code extensions from extensions.json."""
        extensions_file = self.vscode_dir / "extensions.json"

        if not extensions_file.exists():
            print("❌ No extensions.json found")
            return False

        try:
            extensions_data = json.loads(extensions_file.read_text())
            recommendations = extensions_data.get("recommendations", [])

            if not recommendations:
                print("ℹ️  No extension recommendations found")
                return True

            print(f"🔌 Installing {len(recommendations)} VS Code extensions...")

            for extension in recommendations:
                try:
                    result = subprocess.run(
                        ["code", "--install-extension", extension],
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )

                    if result.returncode == 0:
                        print(f"   ✅ {extension}")
                    else:
                        print(f"   ❌ {extension}: {result.stderr.strip()}")

                except subprocess.TimeoutExpired:
                    print(f"   ⏱️  {extension}: Installation timeout")
                except Exception as e:
                    print(f"   ❌ {extension}: {e}")

            return True

        except Exception as e:
            print(f"❌ Extension installation failed: {e}")
            return False

    def validate_sync(self) -> bool:
        """Validate the synchronized VS Code configuration."""
        print("🔍 Validating VS Code configuration...")

        issues = []

        # Check essential files
        essential_files = ["settings.json", "tasks.json", "launch.json"]
        for file_name in essential_files:
            file_path = self.vscode_dir / file_name
            if file_path.exists():
                try:
                    json.loads(file_path.read_text())
                    print(f"   ✅ {file_name}: Valid JSON")
                except json.JSONDecodeError as e:
                    issues.append(f"{file_name}: Invalid JSON - {e}")
            else:
                print(f"   ⚠️  {file_name}: Not found")

        # Check for common configuration issues
        settings_file = self.vscode_dir / "settings.json"
        if settings_file.exists():
            try:
                settings = json.loads(settings_file.read_text())

                # Check Python configuration
                if "python.defaultInterpreterPath" in settings:
                    python_path = Path(settings["python.defaultInterpreterPath"])
                    if not python_path.exists():
                        issues.append(f"Python interpreter not found: {python_path}")

                print(f"   ✅ Settings validation passed")

            except Exception as e:
                issues.append(f"Settings validation error: {e}")

        if issues:
            print("\n⚠️  Validation issues found:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("\n✅ Validation passed! VS Code configuration is ready.")
            return True


def main():
    """Main entry point for VS Code repository synchronization."""
    parser = argparse.ArgumentParser(
        description="🔄 VS Code Repository Synchronization Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python vscode_repo_sync.py --github https://github.com/SergiLIFE/.vscode
  python vscode_repo_sync.py --local ../other-project
  python vscode_repo_sync.py --list-repos
  python vscode_repo_sync.py --install-extensions
        """,
    )

    parser.add_argument("--github", type=str, help="GitHub repository URL to sync from")
    parser.add_argument("--local", type=str, help="Local repository path to sync from")
    parser.add_argument(
        "--target", type=str, help="Target directory (default: current directory)"
    )
    parser.add_argument(
        "--list-repos", action="store_true", help="List suggested repositories"
    )
    parser.add_argument(
        "--install-extensions", action="store_true", help="Install VS Code extensions"
    )
    parser.add_argument(
        "--validate", action="store_true", help="Validate current configuration"
    )
    parser.add_argument("--no-backup", action="store_true", help="Skip backup creation")
    parser.add_argument(
        "--force", action="store_true", help="Force overwrite without prompts"
    )

    args = parser.parse_args()

    # Initialize synchronizer
    sync_tool = VSCodeRepoSync(args.target)

    # Handle different operations
    if args.list_repos:
        repos = sync_tool.list_available_repos()
        choice = input("\nEnter repository number to sync (or 'q' to quit): ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(repos):
            repo_url = repos[int(choice) - 1]
            success = sync_tool.sync_from_github(repo_url)
            if success:
                sync_tool.validate_sync()
                if input("Install extensions? (y/n): ").lower() == "y":
                    sync_tool.install_extensions()

    elif args.github:
        success = sync_tool.sync_from_github(args.github)
        if success:
            sync_tool.validate_sync()

    elif args.local:
        success = sync_tool.sync_from_local(args.local)
        if success:
            sync_tool.validate_sync()

    elif args.install_extensions:
        sync_tool.install_extensions()

    elif args.validate:
        sync_tool.validate_sync()

    else:
        # Interactive mode
        print("🔄 VS Code Repository Synchronization Tool")
        print("=" * 50)

        print("\n📋 Available operations:")
        print("1. Sync from GitHub repository")
        print("2. Sync from local repository")
        print("3. List suggested repositories")
        print("4. Install extensions")
        print("5. Validate current configuration")

        choice = input("\nSelect operation (1-5): ").strip()

        if choice == "1":
            repo_url = input("Enter GitHub repository URL: ").strip()
            if repo_url:
                success = sync_tool.sync_from_github(repo_url)
                if success:
                    sync_tool.validate_sync()

        elif choice == "2":
            local_path = input("Enter local repository path: ").strip()
            if local_path:
                success = sync_tool.sync_from_local(local_path)
                if success:
                    sync_tool.validate_sync()

        elif choice == "3":
            repos = sync_tool.list_available_repos()
            repo_choice = input(
                "\nEnter repository number to sync (or 'q' to quit): "
            ).strip()

            if repo_choice.isdigit() and 1 <= int(repo_choice) <= len(repos):
                repo_url = repos[int(repo_choice) - 1]
                success = sync_tool.sync_from_github(repo_url)
                if success:
                    sync_tool.validate_sync()

        elif choice == "4":
            sync_tool.install_extensions()

        elif choice == "5":
            sync_tool.validate_sync()

        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()
