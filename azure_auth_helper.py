"""
L.I.F.E Platform - Azure Authentication Helper
Simple Azure CLI installation and authentication assistant

This module helps users connect to Azure services for the L.I.F.E Platform
without requiring administrative privileges.

Copyright 2025 - Sergio Paya Benaully
Azure Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca
"""

import json
import os
import subprocess
import sys
from typing import Dict, Optional, Tuple


def check_azure_cli_installed() -> bool:
    """Check if Azure CLI is installed and accessible"""
    try:
        result = subprocess.run(['az', '--version'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def install_azure_cli_instructions() -> str:
    """Return Azure CLI installation instructions"""
    return """
🔧 Azure CLI Installation Required

The L.I.F.E Platform requires Azure CLI for cloud integration.

INSTALLATION OPTIONS:

1. Windows Package Manager (Recommended):
   winget install -e --id Microsoft.AzureCLI

2. PowerShell (Run as Administrator):
   $ProgressPreference = 'SilentlyContinue'
   Invoke-WebRequest -Uri https://aka.ms/installazurecliwindowsx64 -OutFile .\\AzureCLI.msi
   Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'
   Remove-Item .\\AzureCLI.msi

3. Direct Download:
   Visit: https://aka.ms/installazurecliwindowsx64

After installation:
1. Restart your terminal
2. Run: az --version (to verify installation)
3. Run: az login (to authenticate)

Your Azure Subscription Details:
- Subscription ID: 5c88cef6-f243-497d-98af-6c6086d575ca
- Tenant ID: e716161a-5e85-4d6d-82f9-96bcdd2e65ac
- Subscription Name: Microsoft Azure Sponsorship
- Directory: Sergio Paya Borrull (lifecoach-121.com)
"""

def azure_login_helper() -> Tuple[bool, str]:
    """Help user login to Azure"""
    if not check_azure_cli_installed():
        return False, install_azure_cli_instructions()
    
    try:
        # Check if already logged in
        result = subprocess.run(['az', 'account', 'show'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            account_info = json.loads(result.stdout)
            return True, f"""
✅ Already logged into Azure!

Current Account:
- Subscription: {account_info.get('name', 'Unknown')}
- ID: {account_info.get('id', 'Unknown')}
- User: {account_info.get('user', {}).get('name', 'Unknown')}
- State: {account_info.get('state', 'Unknown')}
"""
        
        # Not logged in, provide login instructions
        return False, """
🔐 Azure Login Required

Please run one of these commands to login:

1. Standard login:
   az login

2. Login with specific tenant:
   az login --tenant e716161a-5e85-4d6d-82f9-96bcdd2e65ac

3. Device code login (for restricted environments):
   az login --use-device-code

4. Set your subscription after login:
   az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca

After successful login, your L.I.F.E Platform Azure integration will be fully functional!
"""
        
    except Exception as e:
        return False, f"Error checking Azure login status: {str(e)}"

def get_azure_subscription_info() -> Optional[Dict]:
    """Get Azure subscription information"""
    if not check_azure_cli_installed():
        return None
    
    try:
        result = subprocess.run(['az', 'account', 'show', '--output', 'json'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return None
            
    except Exception:
        return None

def validate_life_azure_resources() -> Dict[str, bool]:
    """Validate L.I.F.E Platform Azure resources"""
    if not check_azure_cli_installed():
        return {"azure_cli": False}
    
    resources_status = {
        "azure_cli": True,
        "resource_group": False,
        "function_app": False,
        "storage_account": False,
        "key_vault": False,
        "iot_hub": False
    }
    
    # Check resource group
    try:
        result = subprocess.run([
            'az', 'group', 'show', 
            '--name', 'life-platform-prod',
            '--output', 'json'
        ], capture_output=True, text=True, timeout=10)
        resources_status["resource_group"] = (result.returncode == 0)
    except Exception:
        pass
    
    # Check function app
    try:
        result = subprocess.run([
            'az', 'functionapp', 'show',
            '--name', 'life-functions-app',
            '--resource-group', 'life-platform-prod',
            '--output', 'json'
        ], capture_output=True, text=True, timeout=10)
        resources_status["function_app"] = (result.returncode == 0)
    except Exception:
        pass
    
    # Check storage account
    try:
        result = subprocess.run([
            'az', 'storage', 'account', 'show',
            '--name', 'stlifeplatformprod',
            '--resource-group', 'life-platform-prod',
            '--output', 'json'
        ], capture_output=True, text=True, timeout=10)
        resources_status["storage_account"] = (result.returncode == 0)
    except Exception:
        pass
    
    # Check key vault
    try:
        result = subprocess.run([
            'az', 'keyvault', 'show',
            '--name', 'kv-life-platform-prod',
            '--output', 'json'
        ], capture_output=True, text=True, timeout=10)
        resources_status["key_vault"] = (result.returncode == 0)
    except Exception:
        pass
    
    return resources_status

def main():
    """Main function to help with Azure authentication"""
    print("🧠 L.I.F.E Platform - Azure Authentication Helper")
    print("=" * 55)
    
    # Check Azure CLI
    print("🔍 Checking Azure CLI installation...")
    if check_azure_cli_installed():
        print("   ✅ Azure CLI is installed")
        
        # Check login status
        print("🔐 Checking Azure login status...")
        logged_in, message = azure_login_helper()
        print(message)
        
        if logged_in:
            # Validate L.I.F.E resources
            print("🏗️ Validating L.I.F.E Platform Azure resources...")
            resources = validate_life_azure_resources()
            
            for resource_name, status in resources.items():
                status_icon = "✅" if status else "❌"
                resource_display = resource_name.replace("_", " ").title()
                print(f"   {status_icon} {resource_display}")
            
            # Get subscription info
            sub_info = get_azure_subscription_info()
            if sub_info:
                print("\n📋 Current Azure Subscription:")
                print(f"   Name: {sub_info.get('name', 'Unknown')}")
                print(f"   ID: {sub_info.get('id', 'Unknown')}")
                print(f"   State: {sub_info.get('state', 'Unknown')}")
                print(f"   Tenant: {sub_info.get('tenantId', 'Unknown')}")
        
    else:
        print("   ❌ Azure CLI not found")
        print(install_azure_cli_instructions())
    
    print("\n🚀 L.I.F.E Platform Azure integration ready!")
    print("💡 Run 'python azure_auth_helper.py' anytime to check status")

if __name__ == "__main__":
    main()