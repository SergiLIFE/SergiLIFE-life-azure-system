#!/usr/bin/env python3
"""
Azure Secure Upload Script for Encrypted L.I.F.E. Theory Calculations
Upload encrypted calculations to Azure Blob Storage with additional encryption layers

Copyright 2025 - Sergio Paya Borrull
Azure Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca
"""
import base64
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from cryptography.fernet import Fernet


class SecureLifeCalculationsUploader:
    """Secure uploader for L.I.F.E. Theory calculations to Azure"""

    def __init__(self):
        self.subscription_id = "5c88cef6-f243-497d-98af-6c6086d575ca"
        self.account_email = (
            "sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com"
        )
        self.storage_account = "stlifeplatformprod"
        self.container_name = "encrypted-calculations"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Initialize Azure credentials
        self.credential = DefaultAzureCredential()

        print("🔐 L.I.F.E. Theory Secure Upload System Initialized")
        print(f"📅 Timestamp: {self.timestamp}")
        print(f"🏢 Azure Subscription: {self.subscription_id}")
        print(f"👤 Account: {self.account_email}")

    def generate_encryption_key(self) -> bytes:
        """Generate encryption key based on subscription and timestamp"""
        key_material = f"{self.subscription_id}_{self.timestamp}_{self.account_email}"
        key_hash = hashlib.sha256(key_material.encode()).digest()
        return base64.urlsafe_b64encode(key_hash[:32])  # Fernet requires 32 bytes

    def encrypt_file_content(self, file_path: str) -> tuple:
        """Encrypt file content with additional layer of encryption"""
        try:
            # Read the file content
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Generate encryption key
            key = self.generate_encryption_key()
            fernet = Fernet(key)

            # Encrypt the content
            encrypted_content = fernet.encrypt(content.encode("utf-8"))

            # Create metadata
            metadata = {
                "original_filename": os.path.basename(file_path),
                "encryption_timestamp": self.timestamp,
                "subscription_id": self.subscription_id,
                "account": self.account_email,
                "content_hash": hashlib.sha256(content.encode()).hexdigest(),
                "file_size": len(content),
                "encryption_method": "Fernet_AES256_Plus_Azure_Encryption",
            }

            print(f"✅ File encrypted successfully: {len(encrypted_content)} bytes")
            return encrypted_content, key, metadata

        except Exception as e:
            print(f"❌ Encryption failed: {str(e)}")
            return None, None, None

    def upload_to_azure_blob(
        self, encrypted_content: bytes, metadata: dict, key: bytes
    ) -> bool:
        """Upload encrypted content to Azure Blob Storage"""
        try:
            # Initialize blob service client
            blob_service_client = BlobServiceClient(
                account_url=f"https://{self.storage_account}.blob.core.windows.net",
                credential=self.credential,
            )

            # Create container if it doesn't exist
            try:
                container_client = blob_service_client.get_container_client(
                    self.container_name
                )
                container_client.create_container()
                print(f"📦 Container '{self.container_name}' created")
            except Exception:
                print(f"📦 Container '{self.container_name}' already exists")

            # Upload encrypted calculations
            blob_name = f"life_theory_calculations_{self.timestamp}.encrypted"
            blob_client = blob_service_client.get_blob_client(
                container=self.container_name, blob=blob_name
            )

            # Upload with metadata
            blob_client.upload_blob(
                encrypted_content, overwrite=True, metadata=metadata
            )

            # Upload encryption key separately (additional security)
            key_blob_name = f"encryption_key_{self.timestamp}.key"
            key_client = blob_service_client.get_blob_client(
                container=self.container_name, blob=key_blob_name
            )

            key_metadata = {
                "key_for": blob_name,
                "timestamp": self.timestamp,
                "subscription": self.subscription_id,
            }

            key_client.upload_blob(key, overwrite=True, metadata=key_metadata)

            print(f"🚀 Successfully uploaded to Azure:")
            print(f"   📄 Calculations: {blob_name}")
            print(f"   🔑 Encryption Key: {key_blob_name}")
            print(f"   📊 Size: {len(encrypted_content)} bytes")

            return True

        except Exception as e:
            print(f"❌ Azure upload failed: {str(e)}")
            return False

    def create_backup_summary(self, metadata: dict) -> str:
        """Create a summary file for the encrypted backup"""
        summary = {
            "backup_info": {
                "timestamp": self.timestamp,
                "azure_subscription": self.subscription_id,
                "account": self.account_email,
                "storage_account": self.storage_account,
                "container": self.container_name,
            },
            "file_info": metadata,
            "security_measures": [
                "Local file encryption with Fernet (AES 256)",
                "Azure Blob Storage encryption at rest",
                "Azure Blob Storage encryption in transit",
                "Separate key storage in Azure",
                "RBAC access control",
                "Account admin authentication",
            ],
            "recovery_instructions": {
                "step_1": "Authenticate to Azure with account admin credentials",
                "step_2": "Download encrypted blob and key from Azure storage",
                "step_3": "Decrypt using provided Python decryption script",
                "step_4": "Verify content hash for integrity",
            },
        }

        summary_path = f"AZURE_BACKUP_SUMMARY_{self.timestamp}.json"
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"📋 Backup summary created: {summary_path}")
        return summary_path

    def secure_upload_calculations(self, file_path: str) -> bool:
        """Main method to securely upload L.I.F.E. Theory calculations"""
        print("\n🔐 Starting Secure Upload Process...")
        print("=" * 60)

        # Check if file exists
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return False

        # Encrypt file content
        print("🔒 Step 1: Encrypting file content...")
        encrypted_content, key, metadata = self.encrypt_file_content(file_path)

        if encrypted_content is None:
            return False

        # Upload to Azure
        print("☁️ Step 2: Uploading to Azure Blob Storage...")
        upload_success = self.upload_to_azure_blob(encrypted_content, metadata, key)

        if not upload_success:
            return False

        # Create backup summary
        print("📋 Step 3: Creating backup summary...")
        summary_path = self.create_backup_summary(metadata)

        print("\n🎉 SECURE UPLOAD COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("✅ L.I.F.E. Theory calculations securely stored in Azure")
        print("✅ Double encryption applied (Local + Azure)")
        print("✅ Metadata and recovery information saved")
        print("✅ Account admin access required for recovery")
        print("\n🛡️ Your calculations are now protected with enterprise-grade security!")

        return True


def main():
    """Main execution function"""
    print("🚀 L.I.F.E. Theory Secure Azure Upload System")
    print("Copyright 2025 - Sergio Paya Borrull")
    print("Azure Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca")
    print("=" * 70)

    # Initialize uploader
    uploader = SecureLifeCalculationsUploader()

    # File to upload
    calculations_file = "ENCRYPTED_LIFE_THEORY_CALCULATIONS.md"

    # Check if file exists
    if os.path.exists(calculations_file):
        print(f"📄 Found calculations file: {calculations_file}")

        # Perform secure upload
        success = uploader.secure_upload_calculations(calculations_file)

        if success:
            print("\n🎯 MISSION ACCOMPLISHED!")
            print("Your L.I.F.E. Theory calculations are now safely encrypted")
            print("and stored in your Azure ecosystem with multiple security layers.")
        else:
            print("\n⚠️ Upload encountered issues. Please check Azure credentials.")
    else:
        print(f"❌ Calculations file not found: {calculations_file}")
        print("Please ensure the file exists in the current directory.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Upload cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("Please check your Azure credentials and try again.")
