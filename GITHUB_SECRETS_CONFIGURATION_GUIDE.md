# 🔐 GitHub Repository Secrets Configuration Guide
**L.I.F.E Platform - Azure Staging Deployment**

---

## 📋 OVERVIEW

This guide provides step-by-step instructions to configure GitHub repository secrets for automated Azure deployment of the L.I.F.E Platform staging environment.

**Repository:** `SergiLIFE/SergiLIFE-life-azure-system`  
**Target:** Azure staging deployment automation  
**Revenue Impact:** $345K Q4 2025 → $50.7M by 2029  

---

## 🎯 REQUIRED SECRETS

You need to configure these 5 secrets in your GitHub repository:

| Secret Name | Purpose | Example Value |
|-------------|---------|---------------|
| `AZURE_CREDENTIALS` | Azure service principal authentication | `{"clientId": "...", "clientSecret": "...", ...}` |
| `AZURE_SUBSCRIPTION_ID` | Your Azure subscription ID | `5c88cef6-f243-497d-98af-6c6086d575ca` |
| `AZURE_RG_STAGING` | Resource group for staging | `life-platform-staging-rg` |
| `AZURE_WEBAPP_NAME_STAGING` | Staging web app name | `life-platform-staging` |
| `AZURE_LOCATION` | Azure region | `eastus2` |

---

## 🚀 STEP 1: Access GitHub Repository Settings

### 1.1 Navigate to Your Repository
```
https://github.com/SergiLIFE/SergiLIFE-life-azure-system
```

### 1.2 Click on "Settings" Tab
- Located in the top navigation bar of your repository
- Must be logged in as repository owner or have admin permissions

### 1.3 Navigate to Secrets and Variables
- In the left sidebar, click **"Secrets and variables"**
- Select **"Actions"** from the dropdown

**Direct URL:**
```
https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/secrets/actions
```

---

## 🔧 STEP 2: Create Azure Service Principal

### 2.1 Open Azure Cloud Shell or Local Terminal
**Option A: Azure Cloud Shell (Recommended)**
```
https://shell.azure.com
```

**Option B: Local Azure CLI**
```cmd
# Install Azure CLI if not already installed
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login to Azure
az login
```

### 2.2 Set Your Subscription
```bash
# List available subscriptions
az account list --output table

# Set your subscription (replace with your subscription ID)
az account set --subscription "5c88cef6-f243-497d-98af-6c6086d575ca"

# Verify current subscription
az account show --output table
```

### 2.3 Create Service Principal

**🚨 DEPRECATION NOTE:** The `--sdk-auth` flag is deprecated but still works. Use it for GitHub Actions compatibility.

**For Bash/Linux/Mac (Azure Cloud Shell):**
```bash
# Create service principal for L.I.F.E Platform staging
az ad sp create-for-rbac \
  --name "sp-life-platform-staging" \
  --role "Contributor" \
  --scopes "/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca" \
  --sdk-auth
```

**For PowerShell (Windows):**
```powershell
# Create service principal for L.I.F.E Platform staging (PowerShell syntax)
az ad sp create-for-rbac `
  --name "sp-life-platform-staging" `
  --role "Contributor" `
  --scopes "/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca" `
  --sdk-auth
```

**Single Line (works in any shell):**
```bash
az ad sp create-for-rbac --name "sp-life-platform-staging" --role "Contributor" --scopes "/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca" --sdk-auth
```

**⚠️ Expected Output:** You'll see a deprecation warning, but the command will work and output the required JSON.

### 2.4 Copy Service Principal Output
The command will return JSON like this:
```json
{
  "clientId": "12345678-1234-1234-1234-123456789012",
  "clientSecret": "abcdefghijklmnopqrstuvwxyz123456789",
  "subscriptionId": "5c88cef6-f243-497d-98af-6c6086d575ca",
  "tenantId": "87654321-4321-4321-4321-210987654321",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

**⚠️ IMPORTANT: Copy this entire JSON output - you'll need it for the AZURE_CREDENTIALS secret**

---

## 🔐 STEP 3: Configure GitHub Secrets

### 3.1 Add AZURE_CREDENTIALS Secret

1. **Click "New repository secret"**
2. **Name:** `AZURE_CREDENTIALS`
3. **Value:** Paste the entire JSON output from Step 2.4
4. **Click "Add secret"**

### 3.2 Add AZURE_SUBSCRIPTION_ID Secret

1. **Click "New repository secret"**
2. **Name:** `AZURE_SUBSCRIPTION_ID`
3. **Value:** `5c88cef6-f243-497d-98af-6c6086d575ca`
4. **Click "Add secret"**

### 3.3 Add AZURE_RG_STAGING Secret

1. **Click "New repository secret"**
2. **Name:** `AZURE_RG_STAGING`
3. **Value:** `life-platform-staging-rg`
4. **Click "Add secret"**

### 3.4 Add AZURE_WEBAPP_NAME_STAGING Secret

1. **Click "New repository secret"**
2. **Name:** `AZURE_WEBAPP_NAME_STAGING`
3. **Value:** `life-platform-staging`
4. **Click "Add secret"**

### 3.5 Add AZURE_LOCATION Secret

1. **Click "New repository secret"**
2. **Name:** `AZURE_LOCATION`
3. **Value:** `eastus2`
4. **Click "Add secret"**

---

## ✅ STEP 4: Verify Secrets Configuration

After adding all secrets, you should see 5 secrets in your repository:

```
Repository secrets (5)
├── AZURE_CREDENTIALS          ••••••••
├── AZURE_SUBSCRIPTION_ID      ••••••••
├── AZURE_RG_STAGING          ••••••••
├── AZURE_WEBAPP_NAME_STAGING ••••••••
└── AZURE_LOCATION            ••••••••
```

---

## 🚀 STEP 5: Trigger Staging Deployment

### 5.1 Push Changes to GitHub
```cmd
# Navigate to your local repository
cd "c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"

# Add all changes
git add .

# Commit with deployment message
git commit -m "L.I.F.E Platform staging deployment ready - GitHub secrets configured"

# Push to trigger GitHub Actions
git push origin main
```

### 5.2 Monitor Deployment
1. **Navigate to GitHub Actions:**
   ```
   https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions
   ```

2. **Watch the deployment workflow:**
   - Workflow name: "Azure Deployment Pipeline"
   - Look for the staging deployment job
   - Monitor each step for success/failure

### 5.3 Expected Deployment Steps
The GitHub Actions workflow will:
1. ✅ **Checkout code**
2. ✅ **Setup Python 3.11**
3. ✅ **Install dependencies**
4. ✅ **Run tests**
5. ✅ **Build application**
6. ✅ **Deploy to Azure staging**
7. ✅ **Test health endpoints**

---

## 🔍 STEP 6: Validate Staging Deployment

### 6.1 Check Azure Resources
```bash
# Verify resource group created
az group show --name life-platform-staging-rg --output table

# Verify web app created
az webapp show --name life-platform-staging --resource-group life-platform-staging-rg --output table
```

### 6.2 Test Staging Endpoints
```bash
# Test health endpoint
curl https://life-platform-staging.azurewebsites.net/health

# Test status endpoint
curl https://life-platform-staging.azurewebsites.net/api/status

# Test metrics endpoint
curl https://life-platform-staging.azurewebsites.net/api/metrics
```

### 6.3 Expected Health Response
```json
{
  "status": "healthy",
  "platform": "L.I.F.E Platform",
  "environment": "staging",
  "marketplace_id": "9a600d96-fe1e-420b-902a-a0c42c561adb",
  "revenue_target": "$345K Q4 2025",
  "services": {
    "neural_processing": "operational",
    "eeg_analysis": "ready",
    "learning_adaptation": "active",
    "azure_integration": "connected"
  }
}
```

---

## 🚨 TROUBLESHOOTING

### Common Issues and Solutions

#### Issue 1: Service Principal Permissions
**Error:** `Insufficient privileges to complete the operation`
**Solution:**
```bash
# Add additional roles if needed
az role assignment create \
  --assignee "12345678-1234-1234-1234-123456789012" \
  --role "Web Plan Contributor" \
  --scope "/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca"
```

#### Issue 2: GitHub Actions Failure
**Error:** `The subscription is not registered to use namespace 'Microsoft.Web'`
**Solution:**
```bash
# Register required resource providers
az provider register --namespace Microsoft.Web
az provider register --namespace Microsoft.Storage
az provider register --namespace Microsoft.KeyVault
```

#### Issue 3: Secret Format Issues
**Error:** `Invalid JSON format in AZURE_CREDENTIALS`
**Solution:**
- Ensure the JSON is valid (use JSONLint.com to validate)
- Copy the exact output from `az ad sp create-for-rbac --sdk-auth`
- No extra spaces or characters

#### Issue 4: Resource Naming Conflicts
**Error:** `The name 'life-platform-staging' is already taken`
**Solution:**
```bash
# Use unique naming with suffix
AZURE_WEBAPP_NAME_STAGING: life-platform-staging-$(date +%Y%m%d)
```

---

## 📞 SUPPORT COMMANDS

### Quick Status Check
```cmd
# Run validation script
VALIDATE_STAGING_DEPLOYMENT.bat

# Check current Azure login
az account show

# List GitHub repository secrets (requires GitHub CLI)
gh secret list
```

### Azure CLI Setup Verification
```bash
# Check Azure CLI version
az --version

# Check current subscription
az account show --output table

# List available locations
az account list-locations --output table
```

---

## 🎯 SUCCESS CRITERIA

### ✅ Configuration Complete When:
1. **All 5 GitHub secrets are configured**
2. **Service principal has Contributor role**
3. **GitHub Actions workflow runs without errors**
4. **Azure resources are created in staging**
5. **Health endpoints return successful responses**

### 💰 Business Impact Achieved:
- ✅ **L.I.F.E Platform staging environment operational**
- ✅ **Production deployment pathway validated** 
- ✅ **$345K Q4 2025 revenue target enabled**
- ✅ **$50.7M by 2029 scaling pathway confirmed**

---

## 🎉 NEXT STEPS

After successful staging deployment:

1. **Production Deployment:** Configure production secrets and deploy
2. **Azure Marketplace:** Submit to Azure Marketplace with ID `9a600d96-fe1e-420b-902a-a0c42c561adb`
3. **Revenue Validation:** Begin customer acquisition for $345K Q4 2025 target
4. **Scaling Preparation:** Prepare infrastructure for $50.7M by 2029 growth

---

## 📋 QUICK REFERENCE

### GitHub Repository Secrets URL:
```
https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/secrets/actions
```

### Azure Service Principal Creation:
**Single line (recommended):**
```bash
az ad sp create-for-rbac --name "sp-life-platform-staging" --role "Contributor" --scopes "/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca" --sdk-auth
```

**PowerShell multi-line:**
```powershell
az ad sp create-for-rbac `
  --name "sp-life-platform-staging" `
  --role "Contributor" `
  --scopes "/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca" `
  --sdk-auth
```

### Deployment Trigger:
```bash
git add . && git commit -m "L.I.F.E Platform staging ready" && git push
```

### Staging Health Check:
```
https://life-platform-staging.azurewebsites.net/health
```

---

*L.I.F.E Platform - Learning Individually from Experience*  
*Azure Marketplace ID: 9a600d96-fe1e-420b-902a-a0c42c561adb*  
*Revenue Target: $345K Q4 2025 → $50.7M by 2029*  
*Copyright 2025 - Sergio Paya Borrull*