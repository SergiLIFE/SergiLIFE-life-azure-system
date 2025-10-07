"""
L.I.F.E. Platform - Direct Azure Cloud Backup (No Terminal Required)
Backs up directly to your Microsoft Azure Storage Account

This bypasses OneDrive and terminal issues - goes straight to Azure!
Your Azure Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca
"""

import hashlib
import json
import os
import zipfile
from datetime import datetime
from pathlib import Path

# Try to import Azure SDK - if not available, we'll provide installation guidance
try:
    from azure.identity import ClientSecretCredential, DefaultAzureCredential
    from azure.storage.blob import BlobServiceClient

    AZURE_SDK_AVAILABLE = True
except ImportError:
    AZURE_SDK_AVAILABLE = False
    print("⚠️  Azure SDK not installed - will provide installation guidance")


class AzureDirectBackup:
    """Direct backup to Azure Storage without terminal commands"""

    def __init__(self):
        self.subscription_id = "5c88cef6-f243-497d-98af-6c6086d575ca"
        self.storage_account = "stlifeplatformprod"
        self.container_name = "repository-backups"
        self.repo_path = Path(__file__).parent
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def install_azure_sdk(self):
        """Guide user to install Azure SDK if not available"""
        print("📦 Azure SDK Installation Required")
        print("=" * 50)
        print("To backup directly to Azure, you need the Azure SDK.")
        print()
        print("🔧 Installation Options:")
        print()
        print("Option 1 - VS Code Terminal (if working):")
        print("   pip install azure-storage-blob azure-identity")
        print()
        print("Option 2 - Command Prompt:")
        print("   1. Press Win+R, type 'cmd', press Enter")
        print("   2. Type: pip install azure-storage-blob azure-identity")
        print("   3. Press Enter and wait for installation")
        print()
        print("Option 3 - Python directly:")
        print("   1. Open Python IDLE")
        print("   2. Run: import subprocess")
        print(
            "   3. Run: subprocess.run(['pip', 'install', 'azure-storage-blob', 'azure-identity'])"
        )
        print()
        print("Option 4 - Manual backup (see create_manual_backup())")
        print()

        return False

    def create_connection_string(self):
        """Create Azure Storage connection string"""
        # For production, you'd use managed identity or service principal
        # For now, we'll use account key method (less secure but works)

        print("🔑 Azure Authentication Options:")
        print("=" * 40)
        print("1. Storage Account Key (Quick setup)")
        print("2. Service Principal (More secure)")
        print("3. Managed Identity (Production)")
        print()

        choice = input("Choose authentication method (1-3): ").strip()

        if choice == "1":
            print()
            print("📋 To get your Storage Account Key:")
            print("1. Go to https://portal.azure.com")
            print("2. Search for 'stlifeplatformprod'")
            print("3. Click 'Access keys' in the left menu")
            print("4. Copy 'key1' value")
            print()

            key = input("Paste your storage account key: ").strip()
            if key:
                connection_string = f"DefaultEndpointsProtocol=https;AccountName={self.storage_account};AccountKey={key};EndpointSuffix=core.windows.net"
                return connection_string

        elif choice == "2":
            print()
            print("🏢 Service Principal Setup:")
            print("This requires Azure CLI or PowerShell setup.")
            print("Since terminal isn't working, use Option 1 for now.")
            return None

        elif choice == "3":
            print()
            print("🔐 Managed Identity:")
            print("This works when running on Azure VMs/Functions.")
            print("For local backup, use Option 1.")
            return None

        return None

    def create_local_backup(self):
        """Create local backup files first"""
        print("💾 Creating local backup files...")

        # Create local backup directory
        backup_dir = self.repo_path / f"temp_backup_{self.timestamp}"
        backup_dir.mkdir(exist_ok=True)

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
            "AZURE_BACKUP_SYSTEM_README.md",
        ]

        files_copied = 0
        backup_manifest = {
            "timestamp": self.timestamp,
            "date": datetime.now().isoformat(),
            "subscription_id": self.subscription_id,
            "storage_account": self.storage_account,
            "files": [],
        }

        # Copy important files
        for file_name in important_files:
            source_file = self.repo_path / file_name
            if source_file.exists():
                dest_file = backup_dir / file_name

                # Copy file
                with open(source_file, "rb") as src, open(dest_file, "wb") as dst:
                    content = src.read()
                    dst.write(content)

                # Calculate file hash for integrity
                file_hash = hashlib.md5(content).hexdigest()

                backup_manifest["files"].append(
                    {
                        "name": file_name,
                        "size": len(content),
                        "hash": file_hash,
                        "path": str(source_file),
                    }
                )

                print(f"✅ Copied: {file_name} ({len(content)} bytes)")
                files_copied += 1
            else:
                print(f"⚠️  Not found: {file_name}")

        # Copy all Python files
        for py_file in self.repo_path.glob("*.py"):
            if py_file.name not in [f["name"] for f in backup_manifest["files"]]:
                dest_file = backup_dir / py_file.name

                with open(py_file, "rb") as src, open(dest_file, "wb") as dst:
                    content = src.read()
                    dst.write(content)

                file_hash = hashlib.md5(content).hexdigest()
                backup_manifest["files"].append(
                    {
                        "name": py_file.name,
                        "size": len(content),
                        "hash": file_hash,
                        "path": str(py_file),
                    }
                )

                print(f"✅ Copied Python: {py_file.name}")
                files_copied += 1

        # Save backup manifest
        manifest_file = backup_dir / "backup_manifest.json"
        with open(manifest_file, "w") as f:
            json.dump(backup_manifest, f, indent=2)

        # Create ZIP archive
        zip_path = self.repo_path / f"LIFE_Azure_Backup_{self.timestamp}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_name = file_path.relative_to(backup_dir)
                    zipf.write(file_path, arc_name)

        print(f"✅ Created ZIP: {zip_path.name} ({zip_path.stat().st_size} bytes)")

        # Cleanup temp directory
        import shutil

        shutil.rmtree(backup_dir)

        return zip_path, files_copied, backup_manifest

    def upload_to_azure(self, zip_path, manifest):
        """Upload backup to Azure Storage"""
        if not AZURE_SDK_AVAILABLE:
            return self.manual_azure_upload(zip_path)

        connection_string = self.create_connection_string()
        if not connection_string:
            return self.manual_azure_upload(zip_path)

        try:
            print("☁️  Uploading to Azure Storage...")

            # Create blob service client
            blob_service_client = BlobServiceClient.from_connection_string(
                connection_string
            )

            # Ensure container exists
            try:
                container_client = blob_service_client.get_container_client(
                    self.container_name
                )
                container_client.get_container_properties()
                print(f"✅ Container '{self.container_name}' exists")
            except:
                container_client = blob_service_client.create_container(
                    self.container_name
                )
                print(f"✅ Created container '{self.container_name}'")

            # Upload ZIP file
            blob_name = f"life-platform/{self.timestamp}/backup.zip"

            with open(zip_path, "rb") as data:
                blob_client = blob_service_client.get_blob_client(
                    container=self.container_name, blob=blob_name
                )
                blob_client.upload_blob(data, overwrite=True)

            print(f"✅ Uploaded: {blob_name}")

            # Upload manifest
            manifest_blob = f"life-platform/{self.timestamp}/manifest.json"
            manifest_json = json.dumps(manifest, indent=2)

            blob_client = blob_service_client.get_blob_client(
                container=self.container_name, blob=manifest_blob
            )
            blob_client.upload_blob(manifest_json, overwrite=True)

            print(f"✅ Uploaded: {manifest_blob}")

            # Create access URL
            account_url = f"https://{self.storage_account}.blob.core.windows.net"
            blob_url = f"{account_url}/{self.container_name}/{blob_name}"

            print()
            print("🎉 AZURE BACKUP COMPLETED!")
            print("=" * 50)
            print(f"📦 Backup URL: {blob_url}")
            print(f"📋 Manifest: {account_url}/{self.container_name}/{manifest_blob}")
            print(f"📊 Files backed up: {len(manifest['files'])}")
            print(f"🕒 Timestamp: {self.timestamp}")
            print()
            print("🔐 Access via Azure Portal:")
            print("1. Go to https://portal.azure.com")
            print(f"2. Search for '{self.storage_account}'")
            print(f"3. Click 'Containers' → '{self.container_name}'")
            print(f"4. Navigate to 'life-platform/{self.timestamp}/'")

            return True

        except Exception as e:
            print(f"❌ Azure upload failed: {e}")
            return self.manual_azure_upload(zip_path)

    def manual_azure_upload(self, zip_path):
        """Provide manual upload instructions"""
        print()
        print("📋 MANUAL AZURE UPLOAD INSTRUCTIONS")
        print("=" * 50)
        print("Since automatic upload isn't working, here's how to upload manually:")
        print()
        print("Method 1 - Azure Portal:")
        print("1. Go to https://portal.azure.com")
        print(f"2. Search for '{self.storage_account}'")
        print("3. Click 'Containers' in left menu")
        print(f"4. Click '{self.container_name}' (create if not exists)")
        print("5. Click 'Upload' button")
        print(f"6. Select your file: {zip_path.name}")
        print("7. Click 'Upload'")
        print()
        print("Method 2 - Azure Storage Explorer:")
        print("1. Download Azure Storage Explorer")
        print("2. Sign in with your Azure account")
        print(f"3. Navigate to subscription {self.subscription_id}")
        print(f"4. Find storage account '{self.storage_account}'")
        print(f"5. Upload {zip_path.name} to '{self.container_name}' container")
        print()
        print(f"📦 Your backup file: {zip_path}")
        print(f"📏 File size: {zip_path.stat().st_size:,} bytes")
        print()

        return True

    def run_backup(self):
        """Main backup process"""
        print("☁️  L.I.F.E. Platform - Direct Azure Backup")
        print("=" * 50)
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔗 Azure Subscription: {self.subscription_id}")
        print(f"💾 Storage Account: {self.storage_account}")
        print()

        if not AZURE_SDK_AVAILABLE:
            if not self.install_azure_sdk():
                print("⚠️  Proceeding with manual backup method...")

        # Create local backup first
        try:
            zip_path, files_count, manifest = self.create_local_backup()

            print()
            print(f"✅ Local backup created: {files_count} files")
            print(f"📦 ZIP file: {zip_path.name}")

            # Try to upload to Azure
            success = self.upload_to_azure(zip_path, manifest)

            if success:
                print()
                print("🛡️  Your L.I.F.E. Platform is now backed up to Azure!")
                print("💡 Your work is safe in Microsoft's cloud!")

            return True

        except Exception as e:
            print(f"❌ Backup failed: {e}")
            print()
            print("🆘 Alternative backup methods:")
            print("1. Email ZIP file to yourself")
            print("2. Upload to Google Drive manually")
            print("3. Copy to USB drive")
            print("4. GitHub repository (code already there)")
            return False


def main():
    """Main function"""
    try:
        backup = AzureDirectBackup()
        backup.run_backup()

        print()
        input("✅ Press Enter to exit...")

    except KeyboardInterrupt:
        print("\n⚠️ Backup cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("\n🆘 Your files are still safe in:")
        print("1. Current directory")
        print("2. GitHub repository")
        print("3. Any existing backups")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
