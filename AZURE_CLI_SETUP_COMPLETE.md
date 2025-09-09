# Azure CLI Installation and Setup Guide for L.I.F.E. Platform
*Production-Ready Azure Integration for Autonomous Optimization Systems*

## Overview
This guide provides comprehensive Azure CLI installation and configuration for the L.I.F.E. (Learning Individually from Experience) platform, ensuring seamless Azure integration for your autonomous optimization systems.

## 1. Azure CLI Installation Methods

### Method 1: Windows Package Manager (Recommended)
```powershell
# Install using winget (requires Windows 10 1709 or later)
winget install Microsoft.AzureCLI

# Verify installation
az --version
```

### Method 2: PowerShell Automated Installation
```powershell
# Run as Administrator
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'
Remove-Item .\AzureCLI.msi

# Restart PowerShell and verify
az --version
```

### Method 3: Manual MSI Installation
1. Download from: https://aka.ms/installazurecliwindows
2. Run the MSI installer as Administrator
3. Follow installation wizard
4. Restart PowerShell/Command Prompt

### Method 4: Chocolatey Installation
```powershell
# If you have Chocolatey installed
choco install azure-cli

# Verify installation
az --version
```

## 2. Post-Installation Configuration

### Verify Installation
```powershell
# Check Azure CLI version and components
az --version

# Check available extensions
az extension list-available --output table
```

### Environment Path Configuration
If Azure CLI is not recognized, add to PATH:

1. **Check Installation Path:**
   ```powershell
   Get-ChildItem "C:\Program Files*" -Recurse -Name "*azure*" -ErrorAction SilentlyContinue
   ```

2. **Common Installation Paths:**
   - `C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin`
   - `C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin`
   - `C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft\Azure CLI\wbin`

3. **Add to PATH:**
   ```powershell
   # Temporary (current session)
   $env:PATH += ";C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin"
   
   # Permanent (requires restart)
   [Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin", "Machine")
   ```

## 3. Azure Authentication Setup

### Login to Azure
```powershell
# Interactive login
az login

# Login with specific tenant
az login --tenant YOUR_TENANT_ID

# Login with service principal
az login --service-principal -u APP_ID -p PASSWORD --tenant TENANT_ID
```

### Set Default Subscription
```powershell
# List available subscriptions
az account list --output table

# Set default subscription
az account set --subscription "YOUR_SUBSCRIPTION_NAME_OR_ID"

# Verify current account
az account show
```

## 4. L.I.F.E. Platform Azure Integration

### Configure Azure Services for L.I.F.E.
```powershell
# Create resource group for L.I.F.E. platform
az group create --name "rg-life-platform" --location "eastus"

# Create storage account for neural data
az storage account create \
  --name "lifeplatformstorage" \
  --resource-group "rg-life-platform" \
  --location "eastus" \
  --sku "Standard_LRS"

# Create Key Vault for secrets
az keyvault create \
  --name "life-platform-kv" \
  --resource-group "rg-life-platform" \
  --location "eastus"

# Create Service Bus for real-time processing
az servicebus namespace create \
  --name "life-platform-bus" \
  --resource-group "rg-life-platform" \
  --location "eastus"
```

### Install Required Azure CLI Extensions
```powershell
# Extensions for L.I.F.E. platform components
az extension add --name azure-devops
az extension add --name ml
az extension add --name containerapp
az extension add --name storage-preview
az extension add --name keyvault
```

## 5. Integration with L.I.F.E. Azure Configuration

### Update azure_config.py Integration
Your existing `azure_config.py` will work with Azure CLI authentication:

```python
# In azure_config.py, the DefaultAzureCredential will automatically 
# use Azure CLI credentials when available
from azure.identity import DefaultAzureCredential

# This will use az login credentials
credential = DefaultAzureCredential()
```

### Test Azure Integration
```powershell
# Test connection to your L.I.F.E. platform resources
python -c "
import sys
sys.path.append('.')
from azure_config import AzureIntegrationManager
manager = AzureIntegrationManager()
print('Azure integration test successful!')
"
```

## 6. Troubleshooting Common Issues

### Issue: 'az' is not recognized
**Solution:**
1. Verify installation path exists
2. Add to PATH environment variable
3. Restart PowerShell/Command Prompt
4. Try running from installation directory directly

### Issue: Authentication failures
**Solution:**
1. Clear cached credentials: `az account clear`
2. Re-login: `az login`
3. Verify subscription: `az account show`
4. Check permissions in Azure portal

### Issue: Extension conflicts
**Solution:**
```powershell
# Remove problematic extensions
az extension remove --name EXTENSION_NAME

# Clear extension cache
az cache purge

# Reinstall extensions
az extension add --name EXTENSION_NAME
```

## 7. L.I.F.E. Platform Deployment Commands

### Deploy Core Infrastructure
```powershell
# Navigate to your L.I.F.E. platform directory
cd "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system"

# Deploy using Azure CLI
az deployment group create \
  --resource-group "rg-life-platform" \
  --template-file "azure-infrastructure.json" \
  --parameters "parameters.json"
```

### Monitor Deployment
```powershell
# Check deployment status
az deployment group list --resource-group "rg-life-platform" --output table

# View deployment logs
az deployment group show \
  --resource-group "rg-life-platform" \
  --name "DEPLOYMENT_NAME"
```

## 8. Integration with Your Repository

### Git and Azure DevOps Integration
```powershell
# Your git remote is already configured correctly:
# origin  https://github.com/SergiLIFE/SergiLIFE-life-azure-system.git (fetch)
# origin  https://github.com/SergiLIFE/SergiLIFE-life-azure-system.git (push)

# Azure DevOps integration (if needed)
az devops configure --defaults organization=YOUR_ORG project=YOUR_PROJECT
```

### CI/CD Pipeline Integration
```powershell
# Create Azure DevOps pipeline for L.I.F.E. platform
az pipelines create \
  --name "life-platform-ci-cd" \
  --repository "SergiLIFE-life-azure-system" \
  --branch "main"
```

## 9. Performance Optimization Commands

### Monitor L.I.F.E. Platform Performance
```powershell
# Check resource utilization
az monitor metrics list \
  --resource "RESOURCE_ID" \
  --metric "Percentage CPU" \
  --start-time "2025-09-09T00:00:00Z"

# Query application logs
az monitor log-analytics query \
  --workspace "WORKSPACE_ID" \
  --analytics-query "ApplicationInsights | where TimeGenerated > ago(1h)"
```

## 10. Security Best Practices

### Secure Configuration
```powershell
# Use managed identity when possible
az vm identity assign --name "life-platform-vm" --resource-group "rg-life-platform"

# Store secrets in Key Vault
az keyvault secret set \
  --vault-name "life-platform-kv" \
  --name "neural-processing-key" \
  --value "YOUR_SECRET_VALUE"

# Configure network security
az network nsg rule create \
  --resource-group "rg-life-platform" \
  --nsg-name "life-platform-nsg" \
  --name "AllowHTTPS" \
  --protocol "TCP" \
  --priority 100 \
  --destination-port-range 443
```

## 11. Next Steps for L.I.F.E. Platform

1. **Complete Azure CLI Installation** using one of the methods above
2. **Authenticate with Azure** using `az login`
3. **Test Integration** with your existing `azure_config.py`
4. **Deploy Infrastructure** for your autonomous optimization systems
5. **Configure Monitoring** for your 22.66x SOTA performance metrics
6. **Set up CI/CD** for continuous deployment of improvements

## Support Resources

- **Azure CLI Documentation:** https://docs.microsoft.com/en-us/cli/azure/
- **Azure Identity Documentation:** https://docs.microsoft.com/en-us/python/api/azure-identity/
- **L.I.F.E. Platform Issues:** Contact your development team

---

**Note:** This guide is specifically tailored for the L.I.F.E. platform's autonomous optimization requirements and champion-level performance targets. Ensure all configurations align with your September 27th launch timeline.
