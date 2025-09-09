"""
Azure CLI Installation and Integration Validator for L.I.F.E. Platform
Comprehensive setup, installation, and validation system
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class AzureCLIInstaller:
    """
    Professional Azure CLI installation and setup manager for L.I.F.E. Platform
    """

    def __init__(self):
        self.installation_methods = [
            "winget",
            "powershell_web",
            "chocolatey",
            "manual_download",
        ]
        self.azure_sdk_available = False
        self.azure_cli_available = False
        self.installation_status = {}

    def check_current_azure_status(self) -> Dict[str, bool]:
        """Check current Azure SDK and CLI status"""
        print("🔍 Checking current Azure status...")

        # Check Azure SDK for Python
        try:
            import azure
            from azure.identity import DefaultAzureCredential

            self.azure_sdk_available = True
            print("✅ Azure SDK for Python: AVAILABLE")
        except ImportError:
            self.azure_sdk_available = False
            print("❌ Azure SDK for Python: NOT AVAILABLE")

        # Check Azure CLI
        try:
            result = subprocess.run(
                ["az", "--version"], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                self.azure_cli_available = True
                print("✅ Azure CLI: AVAILABLE")
                print(
                    f"   Version: {result.stdout.split()[0] if result.stdout else 'Unknown'}"
                )
            else:
                self.azure_cli_available = False
                print("❌ Azure CLI: NOT AVAILABLE")
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            self.azure_cli_available = False
            print("❌ Azure CLI: NOT AVAILABLE")

        return {
            "azure_sdk": self.azure_sdk_available,
            "azure_cli": self.azure_cli_available,
        }

    def install_via_winget(self) -> bool:
        """Install Azure CLI using Windows Package Manager"""
        print("📦 Attempting installation via winget...")
        try:
            # Check if winget is available
            result = subprocess.run(
                ["winget", "--version"], capture_output=True, text=True, timeout=5
            )
            if result.returncode != 0:
                print("❌ winget not available")
                return False

            # Install Azure CLI
            print("   Installing Microsoft.AzureCLI...")
            result = subprocess.run(
                [
                    "winget",
                    "install",
                    "Microsoft.AzureCLI",
                    "--accept-package-agreements",
                ],
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode == 0:
                print("✅ Azure CLI installed successfully via winget")
                return True
            else:
                print(f"❌ winget installation failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ winget installation error: {str(e)}")
            return False

    def install_via_powershell(self) -> bool:
        """Install Azure CLI using PowerShell web download"""
        print("🌐 Attempting installation via PowerShell web download...")
        try:
            powershell_script = """
            $ProgressPreference = 'SilentlyContinue'
            try {
                Invoke-WebRequest -Uri 'https://aka.ms/installazurecliwindows' -OutFile 'AzureCLI.msi'
                Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'
                Remove-Item 'AzureCLI.msi' -ErrorAction SilentlyContinue
                Write-Output 'SUCCESS'
            } catch {
                Write-Output "ERROR: $($_.Exception.Message)"
            }
            """

            result = subprocess.run(
                ["powershell", "-Command", powershell_script],
                capture_output=True,
                text=True,
                timeout=300,
            )

            if "SUCCESS" in result.stdout:
                print("✅ Azure CLI installed successfully via PowerShell")
                return True
            else:
                print(f"❌ PowerShell installation failed: {result.stdout}")
                return False

        except Exception as e:
            print(f"❌ PowerShell installation error: {str(e)}")
            return False

    def install_via_chocolatey(self) -> bool:
        """Install Azure CLI using Chocolatey"""
        print("🍫 Attempting installation via Chocolatey...")
        try:
            # Check if chocolatey is available
            result = subprocess.run(
                ["choco", "--version"], capture_output=True, text=True, timeout=5
            )
            if result.returncode != 0:
                print("❌ Chocolatey not available")
                return False

            # Install Azure CLI
            print("   Installing azure-cli via Chocolatey...")
            result = subprocess.run(
                ["choco", "install", "azure-cli", "-y"],
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode == 0:
                print("✅ Azure CLI installed successfully via Chocolatey")
                return True
            else:
                print(f"❌ Chocolatey installation failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Chocolatey installation error: {str(e)}")
            return False

    def install_azure_cli(self) -> bool:
        """Try multiple installation methods for Azure CLI"""
        print("🚀 Starting Azure CLI installation process...")

        # Try each installation method
        for method in self.installation_methods:
            if method == "winget":
                if self.install_via_winget():
                    self.installation_status[method] = True
                    return True
            elif method == "powershell_web":
                if self.install_via_powershell():
                    self.installation_status[method] = True
                    return True
            elif method == "chocolatey":
                if self.install_via_chocolatey():
                    self.installation_status[method] = True
                    return True

            self.installation_status[method] = False

        print("❌ All automatic installation methods failed")
        print("📋 Manual installation required:")
        print("   1. Download from: https://aka.ms/installazurecliwindows")
        print("   2. Run as Administrator")
        print("   3. Restart PowerShell after installation")

        return False

    def verify_installation(self) -> bool:
        """Verify Azure CLI installation after installation attempt"""
        print("🔍 Verifying Azure CLI installation...")

        # Wait a moment for installation to complete
        time.sleep(2)

        # Refresh environment variables
        try:
            subprocess.run(
                ["powershell", "-Command", "refreshenv"],
                capture_output=True,
                text=True,
                timeout=10,
            )
        except:
            pass

        # Test Azure CLI
        try:
            result = subprocess.run(
                ["az", "--version"], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                print("✅ Azure CLI installation verified successfully")
                return True
        except:
            pass

        # Check common installation paths
        possible_paths = [
            r"C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
            r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
            os.path.expanduser(
                r"~\AppData\Local\Programs\Microsoft\Azure CLI\wbin\az.cmd"
            ),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                print(f"✅ Found Azure CLI at: {path}")
                print("   Add to PATH manually if needed")
                return True

        print("❌ Azure CLI installation could not be verified")
        return False

    def test_azure_integration(self) -> Dict[str, bool]:
        """Test Azure integration with L.I.F.E. platform"""
        print("🧪 Testing Azure integration with L.I.F.E. platform...")

        tests = {
            "azure_sdk_import": False,
            "azure_identity": False,
            "azure_config_load": False,
            "azure_cli_basic": False,
        }

        # Test 1: Azure SDK Import
        try:
            import azure
            from azure.identity import DefaultAzureCredential
            from azure.storage.blob import BlobServiceClient

            tests["azure_sdk_import"] = True
            print("✅ Azure SDK import: SUCCESS")
        except ImportError as e:
            print(f"❌ Azure SDK import: FAILED - {e}")

        # Test 2: Azure Identity
        try:
            credential = DefaultAzureCredential()
            tests["azure_identity"] = True
            print("✅ Azure identity initialization: SUCCESS")
        except Exception as e:
            print(f"❌ Azure identity initialization: FAILED - {e}")

        # Test 3: Azure Config Load
        try:
            # Check if azure_config.py can be imported
            sys.path.insert(0, os.getcwd())
            import azure_config

            tests["azure_config_load"] = True
            print("✅ L.I.F.E. Azure config: SUCCESS")
        except Exception as e:
            print(f"❌ L.I.F.E. Azure config: FAILED - {e}")

        # Test 4: Azure CLI Basic
        try:
            result = subprocess.run(
                ["az", "account", "list"], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                tests["azure_cli_basic"] = True
                print("✅ Azure CLI basic operation: SUCCESS")
            else:
                print("❌ Azure CLI basic operation: FAILED (not logged in)")
        except Exception as e:
            print(f"❌ Azure CLI basic operation: FAILED - {e}")

        return tests

    def generate_setup_commands(self) -> List[str]:
        """Generate setup commands for L.I.F.E. platform Azure integration"""
        commands = [
            "# Azure CLI Setup Commands for L.I.F.E. Platform",
            "",
            "# 1. Login to Azure",
            "az login",
            "",
            "# 2. Set default subscription",
            "az account list --output table",
            "az account set --subscription 'YOUR_SUBSCRIPTION_ID'",
            "",
            "# 3. Create resource group for L.I.F.E. platform",
            "az group create --name 'rg-life-platform' --location 'eastus'",
            "",
            "# 4. Create storage account for neural data",
            "az storage account create --name 'lifeneuraldata' --resource-group 'rg-life-platform' --location 'eastus' --sku 'Standard_LRS'",
            "",
            "# 5. Create Key Vault for secrets",
            "az keyvault create --name 'life-platform-secrets' --resource-group 'rg-life-platform' --location 'eastus'",
            "",
            "# 6. Install required extensions",
            "az extension add --name ml",
            "az extension add --name storage-preview",
            "",
            "# 7. Test L.I.F.E. platform integration",
            "python -c \"from azure_config import AzureIntegrationManager; manager = AzureIntegrationManager(); print('L.I.F.E. Azure integration ready!')\"",
        ]
        return commands

    def create_installation_report(self) -> str:
        """Create detailed installation report"""
        report = f"""
# Azure CLI Installation Report for L.I.F.E. Platform
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

## Installation Status
- Azure SDK for Python: {'✅ AVAILABLE' if self.azure_sdk_available else '❌ NOT AVAILABLE'}
- Azure CLI: {'✅ AVAILABLE' if self.azure_cli_available else '❌ NOT AVAILABLE'}

## Installation Methods Attempted
"""
        for method, status in self.installation_status.items():
            report += f"- {method}: {'✅ SUCCESS' if status else '❌ FAILED'}\n"

        if not self.azure_cli_available:
            report += """
## Manual Installation Required
1. Download: https://aka.ms/installazurecliwindows
2. Run as Administrator
3. Restart PowerShell
4. Run: az --version

## Alternative: Use Azure SDK for Python
Your L.I.F.E. platform can work with Azure SDK for Python (already available):
- azure.identity.DefaultAzureCredential
- azure.storage.blob.BlobServiceClient
- azure.keyvault.secrets.SecretClient
"""

        return report

    def run_complete_setup(self):
        """Run complete Azure CLI setup and validation"""
        print("🚀 L.I.F.E. Platform Azure CLI Setup & Integration Validator")
        print("=" * 60)

        # Step 1: Check current status
        self.check_current_azure_status()
        print()

        # Step 2: Install Azure CLI if needed
        if not self.azure_cli_available:
            print("📋 Azure CLI not detected. Starting installation...")
            self.install_azure_cli()
            self.verify_installation()
            print()

        # Step 3: Test integration
        test_results = self.test_azure_integration()
        print()

        # Step 4: Generate commands
        if self.azure_sdk_available:
            print("📋 Azure Setup Commands:")
            commands = self.generate_setup_commands()
            for cmd in commands[:10]:  # Show first 10 commands
                print(f"   {cmd}")
            print("   ... (see full list in setup guide)")
            print()

        # Step 5: Summary
        print("📊 SUMMARY:")
        print(
            f"   Azure SDK: {'✅ Ready' if self.azure_sdk_available else '❌ Needs Installation'}"
        )
        print(
            f"   Azure CLI: {'✅ Ready' if self.azure_cli_available else '❌ Manual Install Required'}"
        )
        print(
            f"   L.I.F.E. Integration: {'✅ Ready' if test_results.get('azure_config_load', False) else '❌ Needs Configuration'}"
        )

        if self.azure_sdk_available:
            print(
                "\n🎉 Your L.I.F.E. platform can proceed with Azure integration using Python SDK!"
            )
            print("   Next steps:")
            print("   1. Configure Azure authentication (az login)")
            print("   2. Test azure_config.py integration")
            print("   3. Deploy L.I.F.E. platform to Azure")

        return test_results


if __name__ == "__main__":
    installer = AzureCLIInstaller()
    installer.run_complete_setup()
    installer.run_complete_setup()
