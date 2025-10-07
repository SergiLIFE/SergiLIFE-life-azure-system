"""
L.I.F.E. Platform - Repository Analysis and Backup Test Report
This script analyzes your repository and creates a detailed report
"""

import os
from datetime import datetime
from pathlib import Path


def analyze_repository():
    """Analyze the L.I.F.E. Platform repository and create a detailed report"""

    print("🔍 L.I.F.E. PLATFORM - REPOSITORY ANALYSIS")
    print("=" * 60)
    print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🚀 Pre-Launch Repository Health Check")
    print()

    # Get repository directory
    repo_dir = Path(__file__).parent
    print(f"📂 Repository Path: {repo_dir}")
    print()

    # Analysis results
    analysis = {
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "date": datetime.now().isoformat(),
        "repo_path": str(repo_dir),
        "core_files": {"found": [], "missing": [], "total": 0},
        "python_files": {"found": [], "missing": [], "total": 0},
        "markdown_files": {"found": [], "missing": [], "total": 0},
        "config_files": {"found": [], "missing": [], "total": 0},
        "directories": {"found": [], "missing": [], "total": 0},
        "total_size": 0,
        "launch_ready": False,
    }

    # Core L.I.F.E. Platform files (critical for launch)
    print("🧠 CORE L.I.F.E. PLATFORM FILES:")
    print("-" * 40)

    core_files = [
        "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py",
        "autonomous_optimizer.py",
        "sota_benchmark.py",
        "azure_config.py",
        "production_deployment_test.py",
        "azure_functions_workflow.py",
        "azure_deployment_manager.py",
    ]

    analysis["core_files"]["total"] = len(core_files)

    for filename in core_files:
        file_path = repo_dir / filename
        if file_path.exists():
            file_size = file_path.stat().st_size
            analysis["core_files"]["found"].append(
                {"name": filename, "size": file_size, "path": str(file_path)}
            )
            analysis["total_size"] += file_size
            print(f"✅ {filename} ({file_size:,} bytes)")
        else:
            analysis["core_files"]["missing"].append(filename)
            print(f"❌ {filename} - MISSING!")

    core_success = len(analysis["core_files"]["found"]) / len(core_files) * 100
    print(f"📊 Core Files Success Rate: {core_success:.1f}%")
    print()

    # All Python files
    print("🐍 ALL PYTHON FILES:")
    print("-" * 40)

    py_files = list(repo_dir.glob("*.py"))
    analysis["python_files"]["total"] = len(py_files)

    for py_file in py_files:
        if py_file.exists():
            file_size = py_file.stat().st_size
            analysis["python_files"]["found"].append(
                {"name": py_file.name, "size": file_size, "path": str(py_file)}
            )
            analysis["total_size"] += file_size
            print(f"✅ {py_file.name} ({file_size:,} bytes)")
        else:
            analysis["python_files"]["missing"].append(py_file.name)
            print(f"❌ {py_file.name}")

    py_success = (
        len(analysis["python_files"]["found"]) / len(py_files) * 100 if py_files else 0
    )
    print(
        f"📊 Python Files Success Rate: {py_success:.1f}% ({len(analysis['python_files']['found'])}/{len(py_files)})"
    )
    print()

    # All Markdown files
    print("📝 ALL MARKDOWN FILES:")
    print("-" * 40)

    md_files = list(repo_dir.glob("*.md"))
    analysis["markdown_files"]["total"] = len(md_files)

    for md_file in md_files:
        if md_file.exists():
            file_size = md_file.stat().st_size
            analysis["markdown_files"]["found"].append(
                {"name": md_file.name, "size": file_size, "path": str(md_file)}
            )
            analysis["total_size"] += file_size
            print(f"✅ {md_file.name} ({file_size:,} bytes)")
        else:
            analysis["markdown_files"]["missing"].append(md_file.name)
            print(f"❌ {md_file.name}")

    md_success = (
        len(analysis["markdown_files"]["found"]) / len(md_files) * 100
        if md_files
        else 0
    )
    print(
        f"📊 Markdown Files Success Rate: {md_success:.1f}% ({len(analysis['markdown_files']['found'])}/{len(md_files)})"
    )
    print()

    # Configuration files
    print("⚙️ CONFIGURATION FILES:")
    print("-" * 40)

    config_files = [
        "requirements.txt",
        "azure.yaml",
        "Dockerfile",
        "pyproject.toml",
        "setup.py",
    ]
    analysis["config_files"]["total"] = len(config_files)

    for filename in config_files:
        file_path = repo_dir / filename
        if file_path.exists():
            file_size = file_path.stat().st_size
            analysis["config_files"]["found"].append(
                {"name": filename, "size": file_size, "path": str(file_path)}
            )
            analysis["total_size"] += file_size
            print(f"✅ {filename} ({file_size:,} bytes)")
        else:
            analysis["config_files"]["missing"].append(filename)
            print(f"⚠️ {filename} - Not found (may be optional)")

    config_success = (
        len(analysis["config_files"]["found"]) / len(config_files) * 100
        if config_files
        else 0
    )
    print(f"📊 Config Files Success Rate: {config_success:.1f}%")
    print()

    # Important directories
    print("📁 IMPORTANT DIRECTORIES:")
    print("-" * 40)

    important_dirs = ["infra", "logs", "results", "bci_data", ".github"]
    analysis["directories"]["total"] = len(important_dirs)

    for dirname in important_dirs:
        dir_path = repo_dir / dirname
        if dir_path.exists() and dir_path.is_dir():
            # Count files in directory
            files_in_dir = list(dir_path.rglob("*"))
            file_count = len([f for f in files_in_dir if f.is_file()])

            analysis["directories"]["found"].append(
                {"name": dirname, "file_count": file_count, "path": str(dir_path)}
            )
            print(f"✅ {dirname}/ ({file_count} files)")
        else:
            analysis["directories"]["missing"].append(dirname)
            print(f"⚠️ {dirname}/ - Not found")

    dirs_success = (
        len(analysis["directories"]["found"]) / len(important_dirs) * 100
        if important_dirs
        else 0
    )
    print(f"📊 Directories Success Rate: {dirs_success:.1f}%")
    print()

    # Launch readiness assessment
    print("🚀 LAUNCH READINESS ASSESSMENT:")
    print("-" * 40)

    # Critical requirements for launch
    critical_files = [
        "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py",
        "autonomous_optimizer.py",
        "azure_config.py",
        "README.md",
    ]

    critical_found = 0
    for filename in critical_files:
        if (repo_dir / filename).exists():
            critical_found += 1
            print(f"✅ {filename} - READY")
        else:
            print(f"❌ {filename} - MISSING (CRITICAL!)")

    critical_success = critical_found / len(critical_files) * 100
    analysis["launch_ready"] = critical_success >= 90

    print()
    print("=" * 60)
    print("                REPOSITORY ANALYSIS SUMMARY")
    print("=" * 60)
    print()
    print("📊 DETAILED STATISTICS:")
    print(
        f"   🧠 Core L.I.F.E. files: {core_success:.1f}% ({len(analysis['core_files']['found'])}/{analysis['core_files']['total']})"
    )
    print(
        f"   🐍 Python files: {py_success:.1f}% ({len(analysis['python_files']['found'])}/{analysis['python_files']['total']})"
    )
    print(
        f"   📝 Markdown files: {md_success:.1f}% ({len(analysis['markdown_files']['found'])}/{analysis['markdown_files']['total']})"
    )
    print(
        f"   ⚙️ Config files: {config_success:.1f}% ({len(analysis['config_files']['found'])}/{analysis['config_files']['total']})"
    )
    print(
        f"   📁 Directories: {dirs_success:.1f}% ({len(analysis['directories']['found'])}/{analysis['directories']['total']})"
    )
    print(
        f"   📏 Total repository size: {analysis['total_size']:,} bytes ({analysis['total_size']/1024/1024:.1f} MB)"
    )
    print()

    # Overall assessment
    overall_health = (
        core_success + py_success + md_success + config_success + dirs_success
    ) / 5

    print("🎯 OVERALL REPOSITORY HEALTH:")
    if overall_health >= 90:
        print(f"   ✅ EXCELLENT ({overall_health:.1f}%) - Ready for launch!")
    elif overall_health >= 75:
        print(f"   ⚠️ GOOD ({overall_health:.1f}%) - Minor issues to address")
    elif overall_health >= 50:
        print(f"   🔧 NEEDS WORK ({overall_health:.1f}%) - Several files missing")
    else:
        print(f"   ❌ CRITICAL ISSUES ({overall_health:.1f}%) - Major files missing!")

    print()
    print("🚀 MARKETPLACE LAUNCH STATUS:")
    if analysis["launch_ready"]:
        print("   ✅ READY FOR LAUNCH - September 27, 2025!")
        print("   🎉 All critical components are present")
    else:
        print("   ❌ NOT READY - Missing critical files!")
        print("   🔧 Address missing files before launch")

    print()
    print("💾 BACKUP RECOMMENDATIONS:")
    if overall_health >= 80:
        print("   ✅ Repository is healthy - standard backup sufficient")
        print("   📦 Create ZIP archive of entire repository")
        print("   ☁️ Upload to Azure Storage or cloud service")
    else:
        print("   ⚠️ Repository has issues - immediate backup needed!")
        print("   🚨 Manually copy all existing files to safe location")
        print("   📧 Email critical files to yourself")

    print()
    print("📋 AZURE DEPLOYMENT INFO:")
    print("   🔗 Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca")
    print("   💾 Storage: stlifeplatformprod")
    print("   📧 Admin: sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com")
    print("   🏪 Marketplace: 9a600d96-fe1e-420b-902a-a0c42c561adb")
    print("   📅 Launch: September 27, 2025 (TOMORROW!)")

    # Save analysis to file
    desktop = Path.home() / "Desktop"
    report_file = desktop / f"LIFE_Repository_Analysis_{analysis['timestamp']}.txt"

    try:
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("L.I.F.E. PLATFORM - REPOSITORY ANALYSIS REPORT\n")
            f.write("=" * 60 + "\n")
            f.write(f"Analysis Date: {datetime.now()}\n")
            f.write(f"Repository: {repo_dir}\n\n")

            f.write("CORE FILES FOUND:\n")
            for file_info in analysis["core_files"]["found"]:
                f.write(f"  ✅ {file_info['name']} ({file_info['size']:,} bytes)\n")

            f.write("\nPYTHON FILES FOUND:\n")
            for file_info in analysis["python_files"]["found"]:
                f.write(f"  ✅ {file_info['name']} ({file_info['size']:,} bytes)\n")

            f.write("\nMARKDOWN FILES FOUND:\n")
            for file_info in analysis["markdown_files"]["found"]:
                f.write(f"  ✅ {file_info['name']} ({file_info['size']:,} bytes)\n")

            f.write(f"\nOVERALL HEALTH: {overall_health:.1f}%\n")
            f.write(f"LAUNCH READY: {'YES' if analysis['launch_ready'] else 'NO'}\n")
            f.write(f"TOTAL SIZE: {analysis['total_size']:,} bytes\n")

            f.write("\nAZURE INFO:\n")
            f.write("Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca\n")
            f.write("Storage: stlifeplatformprod\n")
            f.write("Launch: September 27, 2025\n")

        print(f"\n📄 Analysis report saved: {report_file}")

    except Exception as e:
        print(f"\n⚠️ Could not save report: {e}")

    print("\n🛡️ ANALYSIS COMPLETE!")
    print("📋 Review the results above to understand your repository status")
    print("💾 Use this information to plan your backup strategy")
    print("🚀 Ensure all critical files are present for tomorrow's launch!")

    return analysis


if __name__ == "__main__":
    try:
        print("Starting L.I.F.E. Platform repository analysis...")
        print("This will check all your files and provide a detailed report.")
        print()

        analysis = analyze_repository()

        print()
        input("📊 Analysis complete! Press Enter to exit...")

    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        print("\n🆘 Manual check required:")
        print("1. Verify your core Python files exist")
        print("2. Check README.md and documentation")
        print("3. Confirm azure_config.py is present")
        print("4. Backup any existing files immediately")
        input("Press Enter to exit...")
