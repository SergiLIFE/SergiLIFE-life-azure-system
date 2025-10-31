#!/usr/bin/env python3
"""
L.I.F.E. Repository Protection System
Advanced backup and corruption prevention for the LIFE platform
"""

import datetime
import hashlib
import json
import shutil
import subprocess
import time
from pathlib import Path


class RepositoryProtector:
    def __init__(self):
        self.repo_path = Path(
            "c:/Users/Sergio Paya Borrull/.azure/SergiLIFE-life-azure-system/.git/hooks/SergiLIFE-life-azure-system"
        )
        self.desktop_backup = Path.home() / "Desktop" / "LIFE_Repository_Backups"
        self.config_file = self.desktop_backup / "protection_config.json"

        # Create backup directory structure
        self.create_backup_structure()
        self.load_config()

    def create_backup_structure(self):
        """Create organized backup directory structure"""
        directories = [
            self.desktop_backup / "daily",
            self.desktop_backup / "weekly",
            self.desktop_backup / "monthly",
            self.desktop_backup / "git_bundles",
            self.desktop_backup / "health_reports",
            self.desktop_backup / "recovery_kits",
            self.desktop_backup / "checksums",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def load_config(self):
        """Load or create protection configuration"""
        default_config = {
            "backup_schedule": {
                "daily": "23:00",
                "weekly": "Sunday at 22:00",
                "health_check": "every 2 hours",
            },
            "retention": {"daily": 7, "weekly": 4, "monthly": 12, "bundles": 30},
            "monitoring": {
                "check_interval": 2,
                "alert_on_corruption": True,
                "auto_repair": True,
            },
        }

        if not self.config_file.exists():
            with open(self.config_file, "w") as f:
                json.dump(default_config, f, indent=4)

        with open(self.config_file, "r") as f:
            self.config = json.load(f)

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
            print(f"Error: {e.stderr if capture_output else e}")
            return None

    def health_check(self):
        """Comprehensive repository health check"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = (
            self.desktop_backup / "health_reports" / f"health_{timestamp}.json"
        )

        print("🔍 Running repository health check...")

        health_report = {
            "timestamp": timestamp,
            "checks": {},
            "status": "unknown",
            "issues": [],
        }

        # Git fsck check
        fsck_result = self.run_git_command(["git", "fsck", "--full", "--strict"])
        health_report["checks"]["fsck"] = "pass" if fsck_result is not None else "fail"
        if fsck_result is None:
            health_report["issues"].append("Repository corruption detected by fsck")

        # Check for zero-byte refs
        refs_path = self.repo_path / ".git" / "refs"
        zero_byte_refs = []
        if refs_path.exists():
            for ref_file in refs_path.rglob("*"):
                if ref_file.is_file() and ref_file.stat().st_size == 0:
                    zero_byte_refs.append(str(ref_file))

        health_report["checks"]["zero_byte_refs"] = (
            "pass" if not zero_byte_refs else "fail"
        )
        if zero_byte_refs:
            health_report["issues"].append(f"Zero-byte refs found: {zero_byte_refs}")

        # Check git status
        status_result = self.run_git_command(["git", "status", "--porcelain"])
        health_report["checks"]["git_status"] = (
            "pass" if status_result is not None else "fail"
        )

        # Check remotes connectivity
        remote_result = self.run_git_command(["git", "remote", "-v"])
        health_report["checks"]["remotes"] = (
            "pass" if remote_result is not None else "fail"
        )

        # Overall status
        all_checks_pass = all(
            check == "pass" for check in health_report["checks"].values()
        )
        health_report["status"] = "healthy" if all_checks_pass else "issues_detected"

        # Save report
        with open(report_file, "w") as f:
            json.dump(health_report, f, indent=4)

        # Alert if issues found
        if health_report["status"] == "issues_detected":
            print("⚠️  Repository issues detected!")
            for issue in health_report["issues"]:
                print(f"   - {issue}")

            if self.config["monitoring"]["auto_repair"]:
                print("🔧 Attempting auto-repair...")
                self.auto_repair()
        else:
            print("✅ Repository is healthy")

        return health_report

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
            print(f"📋 Checksum saved: {checksum_file.name}")
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

    def create_file_backup(self, backup_type="daily"):
        """Create file system backup excluding unnecessary files"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.desktop_backup / backup_type / f"life_repo_{timestamp}"

        print(f"📁 Creating {backup_type} file backup...")

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
            ".pytest_cache",
            "*.pyc",
            ".coverage",
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
        print("🔧 Starting automatic repair sequence...")

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

    def cleanup_old_backups(self):
        """Clean up old backups according to retention policy"""
        print("🧹 Cleaning up old backups...")

        retention = self.config["retention"]
        now = datetime.datetime.now()

        cleanup_dirs = {
            "daily": retention["daily"],
            "weekly": retention["weekly"],
            "monthly": retention["monthly"],
        }

        for backup_type, days_to_keep in cleanup_dirs.items():
            backup_dir = self.desktop_backup / backup_type
            if backup_dir.exists():
                for item in backup_dir.iterdir():
                    if item.is_dir():
                        # Extract timestamp from directory name
                        try:
                            dir_timestamp = (
                                item.name.split("_")[-2]
                                + "_"
                                + item.name.split("_")[-1]
                            )
                            dir_date = datetime.datetime.strptime(
                                dir_timestamp, "%Y%m%d_%H%M%S"
                            )
                            if (now - dir_date).days > days_to_keep:
                                shutil.rmtree(item)
                                print(
                                    f"   🗑️  Removed old {backup_type} backup: {item.name}"
                                )
                        except (ValueError, IndexError):
                            continue

        # Clean old bundles
        bundle_dir = self.desktop_backup / "git_bundles"
        if bundle_dir.exists():
            for bundle in bundle_dir.glob("*.bundle"):
                try:
                    bundle_timestamp = (
                        bundle.stem.split("_")[-2] + "_" + bundle.stem.split("_")[-1]
                    )
                    bundle_date = datetime.datetime.strptime(
                        bundle_timestamp, "%Y%m%d_%H%M%S"
                    )
                    if (now - bundle_date).days > retention["bundles"]:
                        bundle.unlink()
                        # Also remove corresponding checksum
                        checksum_file = (
                            self.desktop_backup / "checksums" / f"{bundle.name}.sha256"
                        )
                        if checksum_file.exists():
                            checksum_file.unlink()
                        print(f"   🗑️  Removed old bundle: {bundle.name}")
                except (ValueError, IndexError):
                    continue

    def full_backup(self, backup_type="daily"):
        """Perform complete backup (bundle + files)"""
        print(f"\n🛡️  Starting {backup_type} backup sequence...")
        print(f"⏰ Time: {datetime.datetime.now()}")

        # Health check first
        health = self.health_check()

        # Create backups
        bundle = self.create_git_bundle()
        files = self.create_file_backup(backup_type)

        # Cleanup old backups
        self.cleanup_old_backups()

        # Create backup summary
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": backup_type,
            "health_status": health["status"],
            "bundle_created": bundle is not None,
            "files_backed_up": files is not None,
            "bundle_path": str(bundle) if bundle else None,
            "files_path": str(files) if files else None,
        }

        summary_file = self.desktop_backup / "last_backup.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=4)

        print(f"\n✅ {backup_type.title()} backup complete!")
        print(f"📍 Backup location: {self.desktop_backup}")

        return summary

    def setup_scheduled_backups(self):
        """Setup automated backup schedule"""
        print("⏰ Setting up backup schedule...")

        # Daily backup
        schedule.every().day.at(self.config["backup_schedule"]["daily"]).do(
            self.full_backup, "daily"
        )

        # Weekly backup (Sunday)
        schedule.every().sunday.at("22:00").do(self.full_backup, "weekly")

        # Monthly backup (1st of month)
        schedule.every().day.at("21:00").do(
            lambda: (
                self.full_backup("monthly")
                if datetime.datetime.now().day == 1
                else None
            )
        )

        # Health checks
        schedule.every(self.config["monitoring"]["check_interval"]).hours.do(
            self.health_check
        )

        print("✅ Backup schedule configured")
        print(f"   📅 Daily backups: {self.config['backup_schedule']['daily']}")
        print(f"   📅 Weekly backups: Sunday 22:00")
        print(
            f"   🔍 Health checks: Every {self.config['monitoring']['check_interval']} hours"
        )

    def run_protection_service(self):
        """Run continuous protection service"""
        print("🛡️  Starting L.I.F.E. Repository Protection Service")
        print("   Press Ctrl+C to stop")

        self.setup_scheduled_backups()

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n🛑 Protection service stopped")


def main():
    protector = RepositoryProtector()

    print("🛡️  L.I.F.E. Repository Protection System")
    print("=" * 50)
    print("1. Run immediate backup")
    print("2. Run health check")
    print("3. Start protection service (continuous)")
    print("4. Auto-repair repository")
    print("5. Show backup status")

    choice = input("\nSelect option (1-5): ").strip()

    if choice == "1":
        protector.full_backup()
    elif choice == "2":
        protector.health_check()
    elif choice == "3":
        protector.run_protection_service()
    elif choice == "4":
        protector.auto_repair()
    elif choice == "5":
        summary_file = protector.desktop_backup / "last_backup.json"
        if summary_file.exists():
            with open(summary_file) as f:
                summary = json.load(f)
            print(f"\n📊 Last backup: {summary['timestamp']}")
            print(f"   Type: {summary['type']}")
            print(f"   Health: {summary['health_status']}")
            print(f"   Bundle: {'✅' if summary['bundle_created'] else '❌'}")
            print(f"   Files: {'✅' if summary['files_backed_up'] else '❌'}")
        else:
            print("No backup history found")


if __name__ == "__main__":
    main()
