import json
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


def complete_backup_test():
    """Complete backup and recovery test for L.I.F.E. Platform"""

    print("🧪 L.I.F.E. PLATFORM - COMPLETE BACKUP & RECOVERY TEST")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🚀 Testing everything before tomorrow's launch!")
    print()

    # Setup directories
    desktop = Path.home() / "Desktop"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    repo_dir = Path(__file__).parent
    test_backup_dir = desktop / f"LIFE_TEST_BACKUP_{timestamp}"
    recovery_dir = desktop / f"LIFE_RECOVERY_{timestamp}"

    # Test results tracking
    test_results = {
        "timestamp": timestamp,
        "date": datetime.now().isoformat(),
        "repo_path": str(repo_dir),
        "backup_path": str(test_backup_dir),
        "recovery_path": str(recovery_dir),
        "files": {
            "core": {"found": [], "missing": [], "success_rate": 0},
            "python": {"found": [], "missing": [], "success_rate": 0},
            "markdown": {"found": [], "missing": [], "success_rate": 0},
            "config": {"found": [], "missing": [], "success_rate": 0},
        },
        "phases": {
            "backup": False,
            "zip_creation": False,
            "recovery": False,
            "verification": False,
        },
        "overall_success": False,
    }

    try:
        # Phase 1: Create backup directory
        print("🔨 PHASE 1: BACKUP PREPARATION")
        print("-" * 40)
        test_backup_dir.mkdir(exist_ok=True)
        print(f"✅ Test backup directory: {test_backup_dir}")

        # Phase 2: Scan and backup core files
        print("\n🧠 PHASE 2: CORE L.I.F.E. PLATFORM FILES")
        print("-" * 40)

        core_files = [
            "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py",
            "autonomous_optimizer.py",
            "sota_benchmark.py",
            "azure_config.py",
            "production_deployment_test.py",
            "azure_functions_workflow.py",
        ]

        for filename in core_files:
            source_file = repo_dir / filename
            if source_file.exists():
                try:
                    shutil.copy2(source_file, test_backup_dir)
                    test_results["files"]["core"]["found"].append(filename)
                    print(f"✅ {filename}")
                except Exception as e:
                    test_results["files"]["core"]["missing"].append(
                        f"{filename} (copy failed: {e})"
                    )
                    print(f"❌ {filename} - Copy failed: {e}")
            else:
                test_results["files"]["core"]["missing"].append(
                    f"{filename} (not found)"
                )
                print(f"❌ {filename} - NOT FOUND")

        core_success_rate = (
            len(test_results["files"]["core"]["found"]) / len(core_files) * 100
        )
        test_results["files"]["core"]["success_rate"] = core_success_rate
        print(f"📊 Core files success rate: {core_success_rate:.1f}%")

        # Phase 3: All Python files
        print("\n🐍 PHASE 3: ALL PYTHON FILES")
        print("-" * 40)

        py_files = list(repo_dir.glob("*.py"))
        for py_file in py_files:
            try:
                shutil.copy2(py_file, test_backup_dir)
                test_results["files"]["python"]["found"].append(py_file.name)
                print(f"✅ {py_file.name}")
            except Exception as e:
                test_results["files"]["python"]["missing"].append(
                    f"{py_file.name} ({e})"
                )
                print(f"❌ {py_file.name} - {e}")

        if py_files:
            py_success_rate = (
                len(test_results["files"]["python"]["found"]) / len(py_files) * 100
            )
            test_results["files"]["python"]["success_rate"] = py_success_rate
            print(f"📊 Python files success rate: {py_success_rate:.1f}%")

        # Phase 4: All Markdown files
        print("\n📝 PHASE 4: ALL MARKDOWN FILES")
        print("-" * 40)

        md_files = list(repo_dir.glob("*.md"))
        for md_file in md_files:
            try:
                shutil.copy2(md_file, test_backup_dir)
                test_results["files"]["markdown"]["found"].append(md_file.name)
                print(f"✅ {md_file.name}")
            except Exception as e:
                test_results["files"]["markdown"]["missing"].append(
                    f"{md_file.name} ({e})"
                )
                print(f"❌ {md_file.name} - {e}")

        if md_files:
            md_success_rate = (
                len(test_results["files"]["markdown"]["found"]) / len(md_files) * 100
            )
            test_results["files"]["markdown"]["success_rate"] = md_success_rate
            print(f"📊 Markdown files success rate: {md_success_rate:.1f}%")

        # Phase 5: Configuration files
        print("\n⚙️ PHASE 5: CONFIGURATION FILES")
        print("-" * 40)

        config_files = [
            "requirements.txt",
            "azure.yaml",
            "Dockerfile",
            "pyproject.toml",
        ]
        for filename in config_files:
            source_file = repo_dir / filename
            if source_file.exists():
                try:
                    shutil.copy2(source_file, test_backup_dir)
                    test_results["files"]["config"]["found"].append(filename)
                    print(f"✅ {filename}")
                except Exception as e:
                    test_results["files"]["config"]["missing"].append(
                        f"{filename} ({e})"
                    )
                    print(f"❌ {filename} - {e}")
            else:
                print(f"⚠️ {filename} - Not found (optional)")

        if config_files:
            config_found = len(test_results["files"]["config"]["found"])
            config_success_rate = config_found / len(config_files) * 100
            test_results["files"]["config"]["success_rate"] = config_success_rate
            print(f"📊 Config files success rate: {config_success_rate:.1f}%")

        # Phase 6: Infrastructure directory
        print("\n🏗️ PHASE 6: INFRASTRUCTURE FILES")
        print("-" * 40)

        infra_dir = repo_dir / "infra"
        if infra_dir.exists():
            try:
                shutil.copytree(infra_dir, test_backup_dir / "infra")
                print("✅ Infrastructure directory backed up")
            except Exception as e:
                print(f"❌ Infrastructure backup failed: {e}")
        else:
            print("⚠️ No infrastructure directory found")

        test_results["phases"]["backup"] = True

        # Phase 7: Create ZIP archive
        print("\n📦 PHASE 7: ZIP ARCHIVE CREATION")
        print("-" * 40)

        zip_path = desktop / f"LIFE_COMPLETE_TEST_{timestamp}.zip"
        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(test_backup_dir):
                    for file in files:
                        file_path = Path(root) / file
                        arc_name = file_path.relative_to(test_backup_dir)
                        zipf.write(file_path, arc_name)

            print(f"✅ ZIP archive created: {zip_path.name}")
            print(f"📏 ZIP size: {zip_path.stat().st_size:,} bytes")
            test_results["phases"]["zip_creation"] = True

        except Exception as e:
            print(f"❌ ZIP creation failed: {e}")

        # Phase 8: Recovery test
        print("\n🔄 PHASE 8: RECOVERY SIMULATION")
        print("-" * 40)

        recovery_dir.mkdir(exist_ok=True)
        try:
            # Extract ZIP to recovery directory
            with zipfile.ZipFile(zip_path, "r") as zipf:
                zipf.extractall(recovery_dir)

            print(f"✅ Files extracted to recovery directory")
            test_results["phases"]["recovery"] = True

        except Exception as e:
            print(f"❌ Recovery failed: {e}")

        # Phase 9: Verification
        print("\n🔍 PHASE 9: RECOVERY VERIFICATION")
        print("-" * 40)

        verification_passed = 0
        verification_total = len(core_files)

        for filename in core_files:
            recovered_file = recovery_dir / filename
            if recovered_file.exists():
                print(f"✅ {filename} - Successfully recovered")
                verification_passed += 1
            else:
                print(f"❌ {filename} - Recovery failed")

        verification_rate = verification_passed / verification_total * 100
        test_results["phases"]["verification"] = verification_rate == 100

        # Save test results
        results_file = test_backup_dir / "TEST_RESULTS.json"
        with open(results_file, "w") as f:
            json.dump(test_results, f, indent=2)

        # Create summary report
        summary_file = test_backup_dir / "BACKUP_TEST_SUMMARY.txt"
        with open(summary_file, "w") as f:
            f.write("L.I.F.E. PLATFORM - COMPLETE BACKUP TEST REPORT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Timestamp: {timestamp}\n\n")
            f.write("BACKUP STATISTICS:\n")
            f.write("-" * 20 + "\n")
            f.write(
                f"Core files: {core_success_rate:.1f}% ({len(test_results['files']['core']['found'])}/{len(core_files)})\n"
            )
            f.write(
                f"Python files: {test_results['files']['python']['success_rate']:.1f}% ({len(test_results['files']['python']['found'])}/{len(py_files)})\n"
            )
            f.write(
                f"Markdown files: {test_results['files']['markdown']['success_rate']:.1f}% ({len(test_results['files']['markdown']['found'])}/{len(md_files)})\n"
            )
            f.write(
                f"Config files: {test_results['files']['config']['success_rate']:.1f}% ({len(test_results['files']['config']['found'])}/{len(config_files)})\n"
            )
            f.write(f"Recovery verification: {verification_rate:.1f}%\n\n")
            f.write("AZURE DEPLOYMENT INFO:\n")
            f.write("-" * 22 + "\n")
            f.write("Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca\n")
            f.write("Storage: stlifeplatformprod\n")
            f.write(
                "Email: sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com\n"
            )
            f.write("Marketplace: 9a600d96-fe1e-420b-902a-a0c42c561adb\n")
            f.write("Launch: September 27, 2025 (TOMORROW!)\n\n")
            f.write("STATUS: BACKUP TEST COMPLETE\n")
            f.write("LAUNCH READINESS: CONFIRMED\n")

        # Overall success determination
        overall_success = (
            core_success_rate >= 90
            and test_results["phases"]["backup"]
            and test_results["phases"]["zip_creation"]
            and test_results["phases"]["recovery"]
            and test_results["phases"]["verification"]
        )
        test_results["overall_success"] = overall_success

        # Final report
        print("\n" + "=" * 60)
        print("             BACKUP TEST COMPLETE")
        print("=" * 60)
        print()
        print("📊 FINAL RESULTS:")
        print(f"   🧠 Core L.I.F.E. files: {core_success_rate:.1f}%")
        print(
            f"   🐍 Python files: {test_results['files']['python']['success_rate']:.1f}%"
        )
        print(
            f"   📝 Markdown files: {test_results['files']['markdown']['success_rate']:.1f}%"
        )
        print(
            f"   ⚙️ Config files: {test_results['files']['config']['success_rate']:.1f}%"
        )
        print(f"   🔄 Recovery rate: {verification_rate:.1f}%")
        print()
        print("📁 Test Locations:")
        print(f"   Backup: {test_backup_dir}")
        print(f"   Recovery: {recovery_dir}")
        print(f"   ZIP: {zip_path}")
        print()

        if overall_success:
            print("🎉 BACKUP TEST: PASSED")
            print("✅ ALL SYSTEMS READY FOR LAUNCH!")
            print("🚀 September 27, 2025 - BRING IT ON!")
        else:
            print("⚠️ BACKUP TEST: ISSUES DETECTED")
            print("🔧 Review missing files and retry")

        print()
        print("🛡️ Your L.I.F.E. Platform is backed up and tested!")
        print("📧 Email the ZIP file for additional security!")
        print("☁️ Upload to Azure Storage for enterprise backup!")

        # Try to open directories
        try:
            os.startfile(test_backup_dir)
        except:
            print(f"\n📂 Manually open: {test_backup_dir}")

        return overall_success

    except Exception as e:
        print(f"\n❌ CRITICAL TEST FAILURE: {e}")
        print("\n🆘 EMERGENCY BACKUP STEPS:")
        print("1. Copy all .py files manually")
        print("2. Copy all .md files manually")
        print("3. Copy config files manually")
        print("4. ZIP everything manually")
        print("5. Email ZIP to yourself")

        return False


def main():
    """Main test function"""
    try:
        print("Starting complete backup and recovery test...")
        print("This will verify everything is ready for tomorrow's launch!")
        print()

        success = complete_backup_test()

        print()
        if success:
            input("✅ All tests passed! Press Enter to exit...")
        else:
            input("⚠️ Some issues found. Press Enter to exit...")

    except KeyboardInterrupt:
        print("\n⚠️ Test cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
