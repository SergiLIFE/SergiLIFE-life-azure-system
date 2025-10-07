# Azure CLI Installation Guide - L.I.F.E. Platform

**Azure Marketplace Offer ID:** 9a600d96-fe1e-420b-902a-a0c42c561adb  
**Version:** 2025.1.0-PRODUCTION  
**Last Updated:** September 26, 2025  

## Overview

This guide provides comprehensive instructions for installing and configuring Azure CLI for the L.I.F.E. Platform. The Azure CLI is essential for managing Azure resources, deploying the platform, and accessing production services.

## 📋 Prerequisites

### System Requirements
- **Windows:** Windows 10/11 (x64) or Windows Server 2019/2022
- **macOS:** macOS 10.15+ (Catalina or later)
- **Linux:** Ubuntu 18.04+, RHEL 8+, or equivalent distributions
- **Memory:** Minimum 4GB RAM (8GB recommended)
- **Storage:** 1GB free disk space for Azure CLI and extensions

### Required Permissions
- Administrator/sudo access for system-wide installation
- Network access to download.microsoft.com
- Firewall exceptions for HTTPS (443) traffic

## 🚀 Quick Installation

### Option 1: Automated Installation (Recommended)

Run the L.I.F.E. Platform's automated installer:

```bash
# Clone and run automated installer
python azure_cli_installer.py --platform auto --verify
```

### Option 2: Manual Installation

Follow the platform-specific instructions below.

## 🖥️ Windows Installation

### Method 1: MSI Installer (Recommended)

1. **Download the Azure CLI installer:**
   ```powershell
   # Download using PowerShell
   Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
   
   # Install with administrative privileges
   Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'
   ```

2. **Verify installation:**
   ```powershell
   az --version
   az login --use-device-code
   ```

### Method 2: Package Manager (Chocolatey)

```powershell
# Install Chocolatey (if not already installed)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Azure CLI
choco install azure-cli -y
```

### Method 3: Winget (Windows Package Manager)

```powershell
winget install Microsoft.AzureCLI
```

## 🍎 macOS Installation

### Method 1: Homebrew (Recommended)

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Azure CLI
brew update && brew install azure-cli
```

### Method 2: Package Installer

```bash
# Download and install
curl -L https://aka.ms/InstallAzureCli | bash

# Reload shell
exec -l $SHELL
```

## 🐧 Linux Installation

### Ubuntu/Debian

```bash
# Update package index
sudo apt-get update

# Install required packages
sudo apt-get install ca-certificates curl apt-transport-https lsb-release gnupg

# Download and install Microsoft signing key
curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/microsoft.gpg > /dev/null

# Add Azure CLI repository
AZ_REPO=$(lsb_release -cs)
echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" | sudo tee /etc/apt/sources.list.d/azure-cli.list

# Install Azure CLI
sudo apt-get update
sudo apt-get install azure-cli
```

### Red Hat/CentOS/Fedora

```bash
# Import Microsoft repository key
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc

# Add Microsoft repository
echo -e "[azure-cli]
name=Azure CLI
baseurl=https://packages.microsoft.com/yumrepos/azure-cli
enabled=1
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/azure-cli.repo

# Install Azure CLI
sudo yum install azure-cli
```

### Using Snap (Universal Linux)

```bash
sudo snap install azure-cli --classic
```

## 🔧 L.I.F.E. Platform Configuration

### 1. Initial Authentication

```bash
# Login to Azure
az login

# Set subscription (use your L.I.F.E. Platform subscription)
az account set --subscription "5c88cef6-f243-497d-98af-6c6086d575ca"

# Verify current subscription
az account show
```

### 2. Install Required Extensions

```bash
# Function Apps extension
az extension add --name azure-functions-core-tools

# Storage extension
az extension add --name storage-preview

# Container extension
az extension add --name containerapp

# Monitor extension  
az extension add --name application-insights

# Key Vault extension
az extension add --name keyvault-preview
```

### 3. Configure Default Resource Group

```bash
# Set default resource group for L.I.F.E. Platform
az configure --defaults group=life-platform-rg location=eastus2
```

### 4. Enable Features

```bash
# Enable required Azure features
az feature register --name Microsoft.Web/AppServiceEnvironmentV3 --namespace Microsoft.Web
az feature register --name Microsoft.Storage/AllowBlobPublicAccess --namespace Microsoft.Storage
az feature register --name Microsoft.KeyVault/VaultTransferUnits --namespace Microsoft.KeyVault
```

## 🏗️ L.I.F.E. Platform Deployment Commands

### Resource Group Setup

```bash
# Create L.I.F.E. Platform resource group
az group create --name life-platform-rg --location eastus2 --tags "project=life-platform" "environment=production" "owner=sergio-paya-borrull"
```

### Storage Account Configuration

```bash
# Create storage account for L.I.F.E. Platform
az storage account create \
  --name stlifeplatformprod \
  --resource-group life-platform-rg \
  --location eastus2 \
  --sku Standard_LRS \
  --kind StorageV2 \
  --access-tier Hot \
  --https-only true
```

### Key Vault Setup

```bash
# Create Key Vault for secrets management
az keyvault create \
  --name kv-life-platform-prod \
  --resource-group life-platform-rg \
  --location eastus2 \
  --sku standard \
  --enabled-for-deployment true \
  --enabled-for-template-deployment true
```

### Function App Deployment

```bash
# Create Function App for L.I.F.E. Platform
az functionapp create \
  --name life-platform-functions \
  --resource-group life-platform-rg \
  --storage-account stlifeplatformprod \
  --consumption-plan-location eastus2 \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4
```

## 🔍 Verification & Testing

### 1. Installation Verification

```bash
# Check Azure CLI version
az --version

# Verify authentication
az account show

# List available subscriptions
az account list --output table

# Test resource access
az resource list --resource-group life-platform-rg --output table
```

### 2. L.I.F.E. Platform Health Check

```bash
# Run platform-specific health checks
python azure_cli_installer.py --verify --health-check

# Check Function App status
az functionapp show --name life-platform-functions --resource-group life-platform-rg --query "state"

# Verify storage account
az storage account show --name stlifeplatformprod --resource-group life-platform-rg --query "primaryEndpoints"

# Test Key Vault access
az keyvault secret list --vault-name kv-life-platform-prod
```

## 🚨 Troubleshooting

### Common Installation Issues

#### Issue 1: Permission Denied
```bash
# Solution: Run with appropriate permissions
# Windows: Run PowerShell as Administrator
# macOS/Linux: Use sudo for system-wide installation
sudo azure-cli-installer.py --install --system-wide
```

#### Issue 2: Network Connectivity
```bash
# Test connectivity
curl -I https://packages.microsoft.com/

# Configure proxy (if needed)
az configure --set core.proxy_url=http://proxy.company.com:8080
```

#### Issue 3: Version Conflicts
```bash
# Clean installation
az extension remove --name azure-cli-iot-ext
az upgrade
az extension add --name azure-iot
```

### L.I.F.E. Platform Specific Issues

#### Authentication Problems
```bash
# Clear cached credentials
az account clear
az login --use-device-code

# Reset configuration
az configure --defaults group= location=
```

#### Resource Access Issues
```bash
# Check RBAC permissions
az role assignment list --assignee $(az account show --query user.name -o tsv)

# Verify subscription access
az account list-locations --query "[?name=='eastus2']"
```

## 📊 Advanced Configuration

### Environment Variables

```bash
# Set L.I.F.E. Platform environment variables
export AZURE_SUBSCRIPTION_ID="5c88cef6-f243-497d-98af-6c6086d575ca"
export AZURE_RESOURCE_GROUP="life-platform-rg"
export AZURE_LOCATION="eastus2"
export LIFE_PLATFORM_VERSION="2025.1.0-PRODUCTION"
export AZURE_MARKETPLACE_OFFER_ID="9a600d96-fe1e-420b-902a-a0c42c561adb"
```

### Configuration Files

Create `~/.azure/config`:
```ini
[core]
output = table
collect_telemetry = no

[cloud "AzureCloud"]
subscription = 5c88cef6-f243-497d-98af-6c6086d575ca

[defaults]
group = life-platform-rg
location = eastus2
```

### Automated Scripts

```bash
# Create deployment script
cat > deploy-life-platform.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 Deploying L.I.F.E. Platform to Azure..."

# Authenticate
az login --use-device-code

# Set subscription
az account set --subscription "5c88cef6-f243-497d-98af-6c6086d575ca"

# Deploy resources
az deployment group create \
  --resource-group life-platform-rg \
  --template-file azure-deploy.json \
  --parameters @azure-deploy.parameters.json

echo "✅ L.I.F.E. Platform deployment complete!"
EOF

chmod +x deploy-life-platform.sh
```

## 🔐 Security Best Practices

### 1. Service Principal Setup
```bash
# Create service principal for automation
az ad sp create-for-rbac --name "life-platform-sp" \
  --role contributor \
  --scopes /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca

# Store credentials in Key Vault
az keyvault secret set --vault-name kv-life-platform-prod \
  --name "sp-client-id" --value "<client-id>"
```

### 2. Access Control
```bash
# Assign minimal required permissions
az role assignment create \
  --assignee "<user-or-sp>" \
  --role "Reader" \
  --scope "/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-rg"
```

### 3. Network Security
```bash
# Configure storage account network rules
az storage account network-rule add \
  --account-name stlifeplatformprod \
  --ip-address "YOUR_IP_ADDRESS"
```

## 📚 Useful Commands Reference

### Resource Management
```bash
# List all resources
az resource list --output table

# Get resource details
az resource show --ids <resource-id>

# Delete resource group (CAUTION!)
az group delete --name life-platform-rg --yes --no-wait
```

### Monitoring & Logs
```bash
# Get Function App logs
az functionapp log tail --name life-platform-functions --resource-group life-platform-rg

# Monitor deployment
az deployment group show --resource-group life-platform-rg --name <deployment-name>
```

### Cost Management
```bash
# Check costs
az consumption usage list --top 10

# Set budget alerts
az consumption budget create --amount 1000 --budget-name life-platform-budget
```

## ✅ Installation Checklist

### Pre-Installation
- [ ] Verify system requirements
- [ ] Ensure administrator/sudo access
- [ ] Check network connectivity
- [ ] Review firewall settings

### Installation
- [ ] Download and install Azure CLI
- [ ] Verify installation with `az --version`
- [ ] Complete authentication with `az login`
- [ ] Set correct subscription
- [ ] Install required extensions

### L.I.F.E. Platform Setup
- [ ] Configure default resource group
- [ ] Set environment variables
- [ ] Create configuration files
- [ ] Test resource access
- [ ] Verify deployment capabilities

### Post-Installation
- [ ] Run health checks
- [ ] Test deployment scripts
- [ ] Configure monitoring
- [ ] Document credentials securely
- [ ] Train team members

## 🆘 Support & Resources

### Official Documentation
- [Azure CLI Documentation](https://docs.microsoft.com/cli/azure/)
- [Azure CLI Release Notes](https://docs.microsoft.com/cli/azure/release-notes-azure-cli)
- [Azure CLI Extensions](https://docs.microsoft.com/cli/azure/azure-cli-extensions-overview)

### L.I.F.E. Platform Resources
- [Azure Integration Guide](AZURE_INTEGRATION_SUCCESS_REPORT.md)
- [Azure OIDC Setup](AZURE_OIDC_SETUP.md)
- [Production Deployment Guide](AZURE_PRODUCTION_VALIDATION_REPORT_SEPTEMBER_2025.md)

### Community Support
- [Azure CLI GitHub Repository](https://github.com/Azure/azure-cli)
- [Stack Overflow - Azure CLI](https://stackoverflow.com/questions/tagged/azure-cli)
- [Microsoft Q&A](https://docs.microsoft.com/answers/topics/azure-cli.html)

---

## 🎯 Next Steps

After completing the Azure CLI installation:

1. **Run the automated installer:** `python azure_cli_installer.py --verify`
2. **Deploy L.I.F.E. Platform:** `azd up`
3. **Verify deployment:** `python production_deployment_test.py`
4. **Monitor status:** Check Azure Portal for resource health

---

**Installation Status:** Ready for September 27, 2025 Azure Marketplace Launch! 🚀

---
*Copyright 2025 - Sergio Paya Borrull*  
*L.I.F.E. Platform - Leading Innovation in Neural Processing*
