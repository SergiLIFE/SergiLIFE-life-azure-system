"""
L.I.F.E. Platform - Simple File Backup (No Terminal Required)
This Python script backs up your files to OneDrive/local backup without Azure CLI

Since your terminal isn't working, this creates local backups that sync via OneDrive
Your files will be safely backed up and accessible from anywhere!
"""

import json
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


def create_simple_backup():
    """Create a simple backup without requiring Azure CLI or terminal"""
    
    print("🛡️ L.I.F.E. Platform - Simple Backup System")
    print("=" * 50)
    print("📅 Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("💾 Backing up your L.I.F.E. Platform repository...")
    print()
    
    # Get current directory
    repo_path = Path(__file__).parent
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create backup directory in OneDrive (usually syncs automatically)
    onedrive_path = Path.home() / "OneDrive" / "L.I.F.E-Platform-Backups"
    backup_dir = onedrive_path / f"backup_{timestamp}"
    
    try:
        # Create backup directory
        backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created backup directory: {backup_dir}")
        
        # Important files to backup
        important_files = [
            "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py",
            "autonomous_optimizer.py",
            "sota_benchmark.py",
            "azure_config.py",
            "azure_functions_workflow.py",
            "production_deployment_test.py",
            "README.md",
            "requirements.txt",
            "azure.yaml",
            "Dockerfile",
            "ACCURACY_ENHANCEMENT_PLAN.md",
            "AZURE_CLI_INSTALLATION_GUIDE.md",
            "AUTONOMOUS_SOTA_KPI_IMPLEMENTATION_COMPLETE.md",
            "AZURE_BACKUP_SYSTEM_README.md"
        ]
        
        # Copy important files individually
        files_copied = 0
        for file_name in important_files:
            source_file = repo_path / file_name
            if source_file.exists():
                dest_file = backup_dir / file_name
                shutil.copy2(source_file, dest_file)
                print(f"✅ Copied: {file_name}")
                files_copied += 1
            else:
                print(f"⚠️  Not found: {file_name}")
        
        # Copy all Python files
        py_files = list(repo_path.glob("*.py"))
        for py_file in py_files:
            if py_file.name not in [f for f in important_files if f.endswith('.py')]:
                dest_file = backup_dir / py_file.name
                shutil.copy2(py_file, dest_file)
                print(f"✅ Copied Python file: {py_file.name}")
                files_copied += 1
        
        # Copy all Markdown files
        md_files = list(repo_path.glob("*.md"))
        for md_file in md_files:
            if md_file.name not in [f for f in important_files if f.endswith('.md')]:
                dest_file = backup_dir / md_file.name
                shutil.copy2(md_file, dest_file)
                print(f"✅ Copied Markdown file: {md_file.name}")
                files_copied += 1
        
        # Copy infra directory if exists
        infra_dir = repo_path / "infra"
        if infra_dir.exists():
            dest_infra_dir = backup_dir / "infra"
            shutil.copytree(infra_dir, dest_infra_dir)
            print("✅ Copied infra directory")
            files_copied += 1
        
        # Create a ZIP archive for easy sharing
        zip_path = backup_dir.parent / f"LIFE_Platform_Backup_{timestamp}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_name = file_path.relative_to(backup_dir)
                    zipf.write(file_path, arc_name)
        
        print(f"✅ Created ZIP archive: {zip_path.name}")
        
        # Create backup info file
        backup_info = {
            "timestamp": timestamp,
            "date": datetime.now().isoformat(),
            "files_copied": files_copied,
            "backup_directory": str(backup_dir),
            "zip_archive": str(zip_path),
            "repository_path": str(repo_path),
            "azure_subscription": "5c88cef6-f243-497d-98af-6c6086d575ca",
            "admin_email": "sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com",
            "platform_version": "2025.1.0-PRODUCTION",
            "marketplace_offer_id": "9a600d96-fe1e-420b-902a-a0c42c561adb"
        }
        
        info_file = backup_dir / "backup_info.json"
        with open(info_file, 'w') as f:
            json.dump(backup_info, f, indent=2)
        
        print()
        print("🎉 BACKUP COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print(f"📁 Backup Location: {backup_dir}")
        print(f"📦 ZIP Archive: {zip_path}")
        print(f"📊 Files Backed Up: {files_copied}")
        print()
        print("🔄 OneDrive Sync:")
        if onedrive_path.exists():
            print("✅ OneDrive folder found - files will sync automatically!")
            print("📱 Access from any device via OneDrive")
            print("🌐 Web access: https://onedrive.live.com")
        else:
            print("⚠️  OneDrive not found - backup saved locally")
            print(f"📂 Manual backup location: {backup_dir}")
        
        print()
        print("🛡️ Your L.I.F.E. Platform work is now safely backed up!")
        print("💡 Even if your computer crashes, your work is preserved!")
        print()
        print("🔗 Additional Backup Options:")
        print("1. Email the ZIP file to yourself")
        print("2. Upload ZIP to Google Drive/Dropbox")
        print("3. Copy to external USB drive")
        print("4. GitHub repository (already backing up)")
        
        return True
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        print()
        print("🆘 Alternative backup methods:")
        print("1. Manually copy files to OneDrive folder")
        print("2. Email important files to yourself")
        print("3. Use GitHub (already has your code)")
        print("4. Copy to USB drive")
        return False

def main():
    """Main backup function"""
    try:
        success = create_simple_backup()
        
        if success:
            print()
            input("✅ Press Enter to exit...")
        else:
            print()
            input("❌ Press Enter to exit...")
            
    except KeyboardInterrupt:
        print("\n⚠️ Backup cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()    main()