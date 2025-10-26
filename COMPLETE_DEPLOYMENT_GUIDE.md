# 🚀 L.I.F.E Platform - Complete Deployment Guide

**Date:** October 19, 2025  
**Status:** Phase 1 Complete → Phase 2 Ready  
**Azure Subscription:** Microsoft Azure Sponsorship (5c88cef6-f243-497d-98af-6c6086d575ca)

---

## ✅ What's Already Deployed (Phase 1)

Your infrastructure is **100% deployed and operational**:

| Resource | Name | Status | Region |
|----------|------|--------|--------|
| Resource Group | `life-platform-rg` | ✅ Active | East US 2 |
| Storage Account | `stlifeplatformprod` | ✅ Active | East US 2 |
| Key Vault | `kv-life-platform-prod` | ✅ Active | East US 2 |
| Service Bus | `sb-life-platform-prod` | ✅ Active | East US 2 |
| App Service Plan | `life-app-service-plan` | ✅ Active | East US 2 |
| Function App | `life-functions-app` | ✅ Running | East US 2 |

**Plus 10+ supporting resources:** Application Insights, Container Instances, Log Analytics, DNS Zones, etc.

---

## 🎯 Complete Deployment Workflow (One-Click)

I've created an **all-in-one automated workflow** that combines all three steps you requested:

### Option 1: Run Everything at Once (Recommended)

```cmd
RUN_COMPLETE_DEPLOYMENT.bat
```

Or:

```cmd
python COMPLETE_DEPLOYMENT_WORKFLOW.py
```

This will automatically:
1. ⚙️ **Configure** Function App settings (Python extensions, runtime, storage)
2. ✅ **Validate** all 6 Azure resources (resource group, storage, key vault, service bus, function app, listing)
3. 📦 **Prepare** for code deployment (check tools, provide options)

**Output:**
- Live console output with progress indicators
- Log file: `logs/complete_deployment_YYYYMMDD_HHMMSS.log`
- JSON report: `results/complete_deployment_report_YYYYMMDD_HHMMSS.json`

---

## 📋 Step-by-Step Details

### Step 1: Configure Function App ⚙️

**What it does:**
- Enables Python worker extensions
- Configures Python runtime (version 3.x)
- Sets Function App extension version (~4)
- Retrieves and configures storage connection string
- Retrieves Service Bus connection string
- Sets AzureWebJobsStorage setting

**Manual commands (if needed):**
```cmd
az functionapp config appsettings set --name life-functions-app --resource-group life-platform-rg --settings PYTHON_ENABLE_WORKER_EXTENSIONS=1 FUNCTIONS_WORKER_RUNTIME=python FUNCTIONS_EXTENSION_VERSION=~4

az storage account show-connection-string --name stlifeplatformprod --resource-group life-platform-rg --query connectionString --output tsv

az servicebus namespace authorization-rule keys list --resource-group life-platform-rg --namespace-name sb-life-platform-prod --name RootManageSharedAccessKey --query primaryConnectionString --output tsv
```

**Expected Result:** ✅ All settings configured, connection strings retrieved

---

### Step 2: Validate Deployment ✅

**What it tests:**
1. Resource group exists and is `Succeeded`
2. Storage account is provisioned and `Succeeded`
3. Key Vault is accessible and provisioned
4. Service Bus namespace is `Succeeded`
5. Function App is `Running`
6. At least 5 resources are deployed in resource group

**Validation script:**
```cmd
python validate_deployment.py --environment staging
```

Or use the batch file:
```cmd
RUN_VALIDATION.bat
```

**Expected Result:** ✅ 6/6 tests PASSED (100% success rate)

**Output location:**
- `logs/deployment_validation_YYYYMMDD_HHMMSS.log`
- `results/deployment_validation_report_YYYYMMDD_HHMMSS.json`

---

### Step 3: Deploy Code 📦

**Option A: Azure Functions Core Tools** (Recommended if installed)

```cmd
func azure functionapp publish life-functions-app
```

**Check if installed:**
```cmd
func --version
```

If not installed, download from: https://learn.microsoft.com/azure/azure-functions/functions-run-local

---

**Option B: VS Code Extension** (Best for GUI experience)

1. Install extension: `Azure Functions` (ms-azuretools.vscode-azurefunctions)
2. Sign in to Azure: `Ctrl+Shift+P` → `Azure: Sign In`
3. View Azure panel (Azure icon in sidebar)
4. Expand your subscription → Function Apps
5. Right-click `life-functions-app` → `Deploy to Function App...`
6. Select workspace folder when prompted

---

**Option C: Azure CLI (ZIP Deploy)**

```cmd
# First, package your code
tar -czf deployment.zip function_app.py host.json requirements.txt

# Then deploy
az functionapp deployment source config-zip --resource-group life-platform-rg --name life-functions-app --src deployment.zip
```

---

**Option D: GitHub Actions** (For continuous deployment)

Create `.github/workflows/deploy-function-app.yml`:

```yaml
name: Deploy to Azure Functions

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Deploy to Azure Functions
      uses: Azure/functions-action@v1
      with:
        app-name: life-functions-app
        package: .
        publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}
```

---

## 🔧 Required Files for Deployment

Your Function App needs these files:

### 1. `host.json` (Function App configuration)

```json
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "maxTelemetryItemsPerSecond": 20
      }
    }
  },
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[4.*, 5.0.0)"
  }
}
```

### 2. `requirements.txt` (Python dependencies)

```txt
azure-functions
azure-storage-blob
azure-servicebus
azure-identity
azure-keyvault-secrets
numpy
scipy
mne
asyncio
```

### 3. `function_app.py` (Your L.I.F.E Platform code)

```python
import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="process_eeg")
async def process_eeg(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('L.I.F.E Platform: Processing EEG data')
    
    # Your L.I.F.E algorithm code here
    # Import from experimentP2L...py
    
    return func.HttpResponse(
        "EEG processing complete",
        status_code=200
    )
```

---

## 📊 Monitoring Your Deployment

### Application Insights

**Access:**
https://portal.azure.com/#resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-rg/providers/microsoft.insights/components/life-functions-app

**Key Metrics to Monitor:**
- Request rate (requests/second)
- Response time (milliseconds)
- Failed requests (count)
- Exceptions (count)
- Availability (%)

### Function App Logs

**Real-time streaming:**
```cmd
az webapp log tail --name life-functions-app --resource-group life-platform-rg
```

**Or in Azure Portal:**
1. Go to Function App → `life-functions-app`
2. Click "Log stream" in left menu
3. Watch real-time logs

---

## 🎯 Success Criteria

Your deployment is successful when:

✅ **Configuration:**
- [ ] Function App has Python runtime configured
- [ ] Storage connection string is set
- [ ] Service Bus connection string is retrieved
- [ ] All app settings are configured

✅ **Validation:**
- [ ] All 6 validation tests pass (100%)
- [ ] Function App shows "Running" status
- [ ] Can access Function App URL: https://life-functions-app.azurewebsites.net

✅ **Code Deployment:**
- [ ] Code deployed to Function App
- [ ] Functions are visible in Azure Portal
- [ ] Can trigger functions via HTTP
- [ ] Logs show successful execution

---

## 🚨 Troubleshooting

### Issue: "func: command not found"

**Solution:** Install Azure Functions Core Tools
```cmd
# Windows (using npm)
npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Or download installer:
# https://learn.microsoft.com/azure/azure-functions/functions-run-local
```

---

### Issue: "Deployment failed: Unauthorized"

**Solution:** Re-authenticate with Azure
```cmd
az login
az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca
```

---

### Issue: "Function App not responding"

**Solution:** Check Function App status
```cmd
az functionapp show --name life-functions-app --resource-group life-platform-rg --query state --output tsv
```

If stopped, restart:
```cmd
az functionapp start --name life-functions-app --resource-group life-platform-rg
```

---

### Issue: "Module import errors in Function App"

**Solution:** Ensure `requirements.txt` is complete and deployed
```cmd
# Check if requirements.txt exists
dir requirements.txt

# Redeploy with dependencies
func azure functionapp publish life-functions-app --build remote
```

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Run complete workflow | `RUN_COMPLETE_DEPLOYMENT.bat` |
| Configure only | Azure CLI commands (see Step 1) |
| Validate only | `RUN_VALIDATION.bat` |
| Deploy code (CLI) | `func azure functionapp publish life-functions-app` |
| Deploy code (VS Code) | Right-click Function App → Deploy |
| View logs | `az webapp log tail --name life-functions-app --resource-group life-platform-rg` |
| Restart Function App | `az functionapp restart --name life-functions-app --resource-group life-platform-rg` |
| Check status | `az functionapp show --name life-functions-app --resource-group life-platform-rg` |

---

## 🎉 Next Steps After Deployment

1. **Test Your Functions**
   - Use Postman or curl to send HTTP requests
   - Check Application Insights for telemetry
   - Monitor logs for errors

2. **Set Up Continuous Deployment**
   - Configure GitHub Actions (see Option D above)
   - Set up deployment slots for staging/production
   - Enable auto-swap for zero-downtime deployments

3. **Configure Custom Domain** (Optional)
   - You have `coach121life.com` and `lifementor121.com` DNS zones
   - Add custom domain to Function App
   - Configure SSL certificate

4. **Scale Your Function App**
   - Review consumption plan vs. premium plan
   - Configure auto-scaling rules
   - Set up geo-replication if needed

5. **Security Hardening**
   - Store all secrets in Key Vault
   - Enable managed identity for Function App
   - Configure network restrictions (firewall rules)
   - Set up Azure AD authentication

---

## 📚 Documentation & Resources

- **Azure Functions Python:** https://learn.microsoft.com/azure/azure-functions/functions-reference-python
- **Azure CLI Reference:** https://learn.microsoft.com/cli/azure/
- **Application Insights:** https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview
- **L.I.F.E Platform Architecture:** See `copilot-instructions.md`

---

**Generated:** October 19, 2025  
**Author:** Sergio Paya Borrull  
**L.I.F.E Platform Offer ID:** 9a600d96-fe1e-420b-902a-a0c42c561adb

🧠 **Your L.I.F.E Platform is ready to transform neuroadaptive learning!**
