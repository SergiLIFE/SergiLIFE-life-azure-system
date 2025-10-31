#!/usr/bin/env python3
"""
L.I.F.E. Repository Protection System
Simple backup and corruption prevention (no external dependencies)
"""

import datetime
import hashlib
import json
import shutil
import subprocess
import time
from pathlib import Path


class SimpleRepositoryProtector:
    def __init__(self):
        self.repo_path = Path(
            "c:/Users/Sergio Paya Borrull/.azure/SergiLIFE-life-azure-system/.git/hooks/SergiLIFE-life-azure-system"
        )
        self.desktop_backup = Path.home() / "Desktop" / "LIFE_Repository_Backups"
        self.create_backup_structure()

    def create_backup_structure(self):
        """Create organized backup directory structure"""
        directories = [
            self.desktop_backup / "daily",
            self.desktop_backup / "git_bundles",
            self.desktop_backup / "health_reports",
            self.desktop_backup / "checksums",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def run_git_command(self, cmd, capture_output=True):
        """Run git command safely with error handling"""
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=capture_output,
                text=True,
                check=True,
            )
            return result.stdout if capture_output else True
        except subprocess.CalledProcessError as e:
            print(f"Git command failed: {' '.join(cmd)}")
            if capture_output and e.stderr:
                print(f"Error: {e.stderr}")
            return None

    def health_check(self):
        """Comprehensive repository health check"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        print("🔍 Running repository health check...")

        issues = []

        # Git fsck check
        fsck_result = self.run_git_command(["git", "fsck", "--full"])
        if fsck_result is None:
            issues.append("Repository corruption detected by fsck")

        # Check for zero-byte refs
        refs_path = self.repo_path / ".git" / "refs"
        zero_byte_refs = []
        if refs_path.exists():
            for ref_file in refs_path.rglob("*"):
                if ref_file.is_file() and ref_file.stat().st_size == 0:
                    zero_byte_refs.append(str(ref_file))

        if zero_byte_refs:
            issues.append(f"Zero-byte refs found: {zero_byte_refs}")

        # Check git status
        status_result = self.run_git_command(["git", "status", "--porcelain"])
        if status_result is None:
            issues.append("Git status check failed")

        # Check remotes connectivity
        remote_result = self.run_git_command(["git", "remote", "-v"])
        if remote_result is None:
            issues.append("Remote connectivity check failed")

        if issues:
            print("⚠️  Repository issues detected!")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("✅ Repository is healthy")
            return True

    def create_git_bundle(self):
        """Create complete git bundle backup"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        bundle_file = (
            self.desktop_backup / "git_bundles" / f"life_repo_{timestamp}.bundle"
        )

        print(f"📦 Creating git bundle: {bundle_file.name}")

        result = self.run_git_command(
            ["git", "bundle", "create", str(bundle_file), "--all"], capture_output=False
        )

        if result:
            # Create checksum for integrity verification
            checksum = self.calculate_checksum(bundle_file)
            checksum_file = (
                self.desktop_backup / "checksums" / f"{bundle_file.name}.sha256"
            )
            with open(checksum_file, "w") as f:
                f.write(f"{checksum}  {bundle_file.name}\n")

            print(f"✅ Bundle created successfully: {bundle_file.name}")
            return bundle_file
        else:
            print("❌ Bundle creation failed")
            return None

    def calculate_checksum(self, file_path):
        """Calculate SHA256 checksum for file integrity"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    def create_file_backup(self):
        """Create file system backup excluding unnecessary files"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.desktop_backup / "daily" / f"life_repo_{timestamp}"

        print("📁 Creating file backup...")

        # Files and directories to exclude
        exclude_patterns = [
            "__pycache__",
            ".mypy_cache",
            ".venv",
            "node_modules",
            ".git/objects/tmp",
            "*.tmp",
            "*.log",
            "thumbcache*",
        ]

        try:
            shutil.copytree(
                self.repo_path,
                backup_dir,
                ignore=shutil.ignore_patterns(*exclude_patterns),
            )
            print(f"✅ File backup created: {backup_dir.name}")
            return backup_dir
        except Exception as e:
            print(f"❌ File backup failed: {e}")
            return None

    def auto_repair(self):
        """Attempt automatic repository repair"""
        print("🔧 Starting automatic repair...")

        repairs_applied = []

        # Remove zero-byte refs
        refs_path = self.repo_path / ".git" / "refs"
        if refs_path.exists():
            for ref_file in refs_path.rglob("*"):
                if ref_file.is_file() and ref_file.stat().st_size == 0:
                    try:
                        ref_file.unlink()
                        repairs_applied.append(f"Removed zero-byte ref: {ref_file}")
                    except Exception as e:
                        print(f"Failed to remove {ref_file}: {e}")

        # Fetch from remotes
        fetch_result = self.run_git_command(["git", "fetch", "--all", "--prune"])
        if fetch_result is not None:
            repairs_applied.append("Successfully fetched from remotes")

        # Garbage collection
        gc_result = self.run_git_command(["git", "gc", "--prune=now"])
        if gc_result is not None:
            repairs_applied.append("Garbage collection completed")

        print(f"🔧 Repairs applied: {len(repairs_applied)}")
        for repair in repairs_applied:
            print(f"   ✅ {repair}")

        return repairs_applied

    def full_backup(self):
        """Perform complete backup (bundle + files)"""
        print("\n🛡️  Starting backup sequence...")

        # Health check first
        is_healthy = self.health_check()

        # Create backups
        bundle = self.create_git_bundle()
        files = self.create_file_backup()

        # Create backup summary
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "health_status": "healthy" if is_healthy else "issues_detected",
            "bundle_created": bundle is not None,
            "files_backed_up": files is not None,
            "bundle_path": str(bundle) if bundle else None,
            "files_path": str(files) if files else None,
        }

        summary_file = self.desktop_backup / "last_backup.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=4)

        print("\n✅ Backup complete!")
        print(f"📍 Backup location: {self.desktop_backup}")

        return summary


def main():
    protector = SimpleRepositoryProtector()

    print("🛡️  L.I.F.E. Repository Protection System")
    print("=" * 50)
    print("1. Run immediate backup")
    print("2. Run health check")
    print("3. Auto-repair repository")
    print("4. Show backup status")

    choice = input("\nSelect option (1-4): ").strip()

    if choice == "1":
        protector.full_backup()
    elif choice == "2":
        protector.health_check()
    elif choice == "3":
        protector.auto_repair()
    elif choice == "4":
        summary_file = protector.desktop_backup / "last_backup.json"
        if summary_file.exists():
            with open(summary_file) as f:
                summary = json.load(f)
            print(f"\n📊 Last backup: {summary['timestamp']}")
            print(f"   Health: {summary['health_status']}")
            print(f"   Bundle: {'✅' if summary['bundle_created'] else '❌'}")
            print(f"   Files: {'✅' if summary['files_backed_up'] else '❌'}")
        else:
            print("No backup history found")


if __name__ == "__main__":
    main()
