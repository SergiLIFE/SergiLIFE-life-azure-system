import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


def emergency_backup():
    print("🚨 EMERGENCY BACKUP - L.I.F.E. Platform")
    print("=" * 50)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🛡️ Protecting your work before launch day!")
    print()
    
    # Simple backup to Desktop
    desktop = Path.home() / "Desktop" 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = desktop / f"LIFE_EMERGENCY_BACKUP_{timestamp}"
    
    try:
        backup_dir.mkdir(exist_ok=True)
        print(f"✅ Backup folder: {backup_dir}")
        
        # Get all files from current directory
        current_dir = Path(__file__).parent
        files_copied = 0
        
        # Copy Python files
        for py_file in current_dir.glob("*.py"):
            try:
                shutil.copy2(py_file, backup_dir)
                print(f"✅ {py_file.name}")
                files_copied += 1
            except:
                print(f"❌ {py_file.name}")
        
        # Copy Markdown files  
        for md_file in current_dir.glob("*.md"):
            try:
                shutil.copy2(md_file, backup_dir)
                print(f"✅ {md_file.name}")
                files_copied += 1
            except:
                print(f"❌ {md_file.name}")
        
        # Copy important config files
        important = ["requirements.txt", "azure.yaml", "Dockerfile", "pyproject.toml"]
        for filename in important:
            file_path = current_dir / filename
            if file_path.exists():
                try:
                    shutil.copy2(file_path, backup_dir)
                    print(f"✅ {filename}")
                    files_copied += 1
                except:
                    print(f"❌ {filename}")
        
        # Copy infra folder if exists
        infra_dir = current_dir / "infra"
        if infra_dir.exists():
            try:
                shutil.copytree(infra_dir, backup_dir / "infra")
                print("✅ infra/ directory")
                files_copied += 1
            except:
                print("❌ infra/ directory")
        
        # Create ZIP
        zip_path = desktop / f"LIFE_EMERGENCY_BACKUP_{timestamp}.zip"
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(backup_dir):
                    for file in files:
                        file_path = Path(root) / file
                        arc_name = file_path.relative_to(backup_dir)
                        zipf.write(file_path, arc_name)
            print(f"✅ ZIP: {zip_path.name}")
        except Exception as e:
            print(f"❌ ZIP failed: {e}")
        
        # Create info file
        info_file = backup_dir / "EMERGENCY_INFO.txt"
        with open(info_file, 'w') as f:
            f.write("🚨 L.I.F.E. PLATFORM EMERGENCY BACKUP 🚨\n")
            f.write("=" * 50 + "\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Files backed up: {files_copied}\n")
            f.write(f"Backup location: {backup_dir}\n")
            f.write(f"ZIP archive: {zip_path}\n\n")
            f.write("AZURE DETAILS:\n")
            f.write("Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca\n")
            f.write("Storage: stlifeplatformprod\n")
            f.write("Email: sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com\n")
            f.write("Launch: September 27, 2025 (TOMORROW!)\n\n")
            f.write("🛡️ Your work is SAFE! 🛡️\n")
        
        print()
        print("🎉 EMERGENCY BACKUP COMPLETE!")
        print("=" * 50)
        print(f"📁 Folder: {backup_dir}")
        print(f"📦 ZIP: {zip_path}")
        print(f"📊 Files: {files_copied}")
        print()
        print("🚀 READY FOR TOMORROW'S LAUNCH!")
        print("📧 Email the ZIP to yourself for safety!")
        print("☁️ Upload to OneDrive/Google Drive!")
        print()
        
        # Try to open the folder
        try:
            os.startfile(backup_dir)
        except:
            print(f"📂 Manually open: {backup_dir}")
            
        input("✅ Press Enter to exit...")
        return True
        
    except Exception as e:
        print(f"❌ Emergency backup failed: {e}")
        print()
        print("🆘 MANUAL BACKUP STEPS:")
        print("1. Copy all .py files to a safe location")
        print("2. Copy all .md files")  
        print("3. Copy requirements.txt, azure.yaml, Dockerfile")
        print("4. Email files to yourself")
        print("5. Upload to cloud storage")
        input("Press Enter to exit...")
        return False

if __name__ == "__main__":
    try:
        emergency_backup()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        input("Press Enter to exit...")        input("Press Enter to exit...")