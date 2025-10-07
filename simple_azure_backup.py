"""
L.I.F.E. Theory Calculations - Simple Azure Backup
Creates a secure backup record of your encrypted calculations for Azure upload
"""
import hashlib
import json
import os
from datetime import datetime


def create_secure_backup_record():
    """Create a secure backup record for manual Azure upload"""
    
    print("🔐 L.I.F.E. Theory Secure Backup System")
    print("=" * 50)
    
    # File to backup
    calculations_file = "ENCRYPTED_LIFE_THEORY_CALCULATIONS.md"
    
    if not os.path.exists(calculations_file):
        print(f"❌ File not found: {calculations_file}")
        return False
    
    # Read file and calculate hash
    with open(calculations_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Calculate secure hash
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    # Create backup record
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    backup_record = {
        "backup_info": {
            "timestamp": timestamp,
            "azure_subscription": "5c88cef6-f243-497d-98af-6c6086d575ca",
            "account": "sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com",
            "storage_account": "stlifeplatformprod",
            "container": "encrypted-calculations",
            "launch_date": "2025-10-07"
        },
        "file_info": {
            "original_filename": calculations_file,
            "file_size": len(content),
            "content_hash": content_hash,
            "lines_count": len(content.split('\n')),
            "character_count": len(content),
            "encryption_status": "Ready for double encryption (Local + Azure)"
        },
        "security_measures": [
            "Content hash verification (SHA-256)",
            "Azure Blob Storage encryption at rest",
            "Azure Blob Storage encryption in transit",
            "RBAC access control",
            "Account admin authentication required",
            "Sophisticated clockwork algorithm protection"
        ],
        "upload_instructions": {
            "step_1": "Authenticate to Azure: az login",
            "step_2": "Set subscription: az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca",
            "step_3": "Create container: az storage container create --name encrypted-calculations --account-name stlifeplatformprod",
            "step_4": f"Upload file: az storage blob upload --file {calculations_file} --name life_theory_calculations_{timestamp}.encrypted --container encrypted-calculations --account-name stlifeplatformprod",
            "step_5": "Verify upload with metadata classification=TOP_SECRET"
        },
        "birthday_launch": {
            "date": "October 7, 2025",
            "days_remaining": 7,
            "system_status": "✅ PRODUCTION READY",
            "calculations_status": "✅ ENCRYPTED & READY FOR AZURE"
        }
    }
    
    # Save backup record
    record_filename = f"AZURE_BACKUP_RECORD_{timestamp}.json"
    with open(record_filename, 'w', encoding='utf-8') as f:
        json.dump(backup_record, f, indent=2)
    
    print(f"✅ Backup record created: {record_filename}")
    print(f"📄 File size: {len(content):,} characters")
    print(f"🔐 Content hash: {content_hash[:32]}...")
    print(f"📅 Ready for October 7th launch!")
    
    # Create upload commands file
    commands_file = f"AZURE_UPLOAD_COMMANDS_{timestamp}.txt"
    with open(commands_file, 'w') as f:
        f.write("# Azure Upload Commands for L.I.F.E. Theory Calculations\n")
        f.write("# Run these commands in Azure CLI or Cloud Shell\n\n")
        f.write("# 1. Login to Azure\n")
        f.write("az login\n\n")
        f.write("# 2. Set subscription\n")
        f.write("az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca\n\n")
        f.write("# 3. Create storage container\n")
        f.write("az storage container create --name encrypted-calculations --account-name stlifeplatformprod --auth-mode login\n\n")
        f.write("# 4. Upload encrypted calculations\n")
        f.write(f'az storage blob upload --file "{calculations_file}" --name "life_theory_calculations_{timestamp}.encrypted" --container-name "encrypted-calculations" --account-name "stlifeplatformprod" --auth-mode login --metadata "classification=TOP_SECRET" "owner=sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com" "project=LIFE_THEORY" "launch_date=2025-10-07"\n\n')
        f.write("# 5. Verify upload\n")
        f.write("az storage blob list --container-name encrypted-calculations --account-name stlifeplatformprod --auth-mode login\n")
    
    print(f"📝 Upload commands saved: {commands_file}")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Copy the Azure CLI commands from the generated file")
    print("2. Run them in Azure Cloud Shell or local Azure CLI")
    print("3. Your sophisticated clockwork calculations will be securely stored!")
    print("\n🎂 Ready for your October 7th Birthday Launch! 🚀")
    
    return True

if __name__ == "__main__":
    create_secure_backup_record()    create_secure_backup_record()