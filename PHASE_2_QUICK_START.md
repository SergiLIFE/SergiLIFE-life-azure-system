# L.I.F.E Platform - Phase 2 Quick Start Guide
**Deployment Phase 1**: ✅ COMPLETE  
**Current Phase**: Phase 2 - Configuration & Code Deployment

---

## 🎯 Quick Commands Reference

### View Your Deployed Resources
```cmd
az resource list --resource-group life-platform-rg --output table
```

### Check Function App Status
```cmd
az functionapp show --name life-functions-app --resource-group life-platform-rg --query "{Name:name, State:state, URL:defaultHostName}" --output table
```

### Access Azure Portal
```cmd
start https://portal.azure.com/#resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-rg/overview
```

---

## 📦 Phase 2 Tasks (Priority Order)

### 1. Configure Function App Application Settings

```cmd
az functionapp config appsettings set --name life-functions-app --resource-group life-platform-rg --settings ^
  PYTHON_ENABLE_WORKER_EXTENSIONS=1 ^
  EEG_SAMPLE_RATE=256 ^
  EEG_CHANNELS=64 ^
  VENTURI_INPUT_GATE_TIMEOUT=0.38 ^
  VENTURI_PROCESSING_GATE_TIMEOUT=0.42 ^
  VENTURI_OUTPUT_GATE_TIMEOUT=0.45 ^
  AZURE_STORAGE_ACCOUNT=stlifeplatformprod ^
  AZURE_KEY_VAULT=kv-life-platform-prod ^
  AZURE_SERVICE_BUS=sb-life-platform-prod
```

### 2. Get Storage Account Connection String

```cmd
az storage account show-connection-string --name stlifeplatformprod --resource-group life-platform-rg --query connectionString --output tsv
```

### 3. Get Service Bus Connection String

```cmd
az servicebus namespace authorization-rule keys list --namespace-name sb-life-platform-prod --resource-group life-platform-rg --name RootManageSharedAccessKey --query primaryConnectionString --output tsv
```

### 4. Store Secrets in Key Vault

```cmd
REM Get storage connection string first
az storage account show-connection-string --name stlifeplatformprod --resource-group life-platform-rg --query connectionString --output tsv > temp_storage.txt

REM Store in Key Vault (replace <connection-string> with actual value from temp_storage.txt)
az keyvault secret set --vault-name kv-life-platform-prod --name STORAGE-CONNECTION-STRING --value "<paste-connection-string-here>"

REM Clean up temp file
del temp_storage.txt
```

### 5. Enable Managed Identity for Function App

```cmd
az functionapp identity assign --name life-functions-app --resource-group life-platform-rg
```

### 6. Grant Function App Access to Key Vault

```cmd
REM Get Function App principal ID
az functionapp identity show --name life-functions-app --resource-group life-platform-rg --query principalId --output tsv > temp_principal.txt
set /p PRINCIPAL_ID=<temp_principal.txt

REM Grant Key Vault Secrets User role
az role assignment create --assignee %PRINCIPAL_ID% --role "Key Vault Secrets User" --scope /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-rg/providers/Microsoft.KeyVault/vaults/kv-life-platform-prod

del temp_principal.txt
```

---

## 🚀 Deploy Code to Function App

### Option 1: Using VS Code

1. Install Azure Functions extension
2. Right-click on `azure_functions` folder
3. Select "Deploy to Function App..."
4. Choose `life-functions-app`

### Option 2: Using Azure Functions Core Tools

```cmd
cd azure_functions
func azure functionapp publish life-functions-app --python
```

### Option 3: Using ZIP Deploy

```cmd
REM Create deployment package
powershell Compress-Archive -Path azure_functions\* -DestinationPath azure_functions.zip -Force

REM Deploy ZIP
az functionapp deployment source config-zip --resource-group life-platform-rg --name life-functions-app --src azure_functions.zip
```

---

## 🧪 Test Your Deployment

### 1. Health Check
```cmd
curl https://life-functions-app.azurewebsites.net/api/health
```

### 2. Test EEG Processing (if endpoint exists)
```cmd
curl -X POST https://life-functions-app.azurewebsites.net/api/process-eeg ^
  -H "Content-Type: application/json" ^
  -d "{\"user_id\":\"test-001\",\"eeg_data\":[0.1,0.2,0.3,0.4,0.5]}"
```

### 3. View Function App Logs
```cmd
az functionapp log tail --name life-functions-app --resource-group life-platform-rg
```

---

## 📊 Monitor Your Platform

### Application Insights Query
```cmd
az monitor app-insights query --app life-functions-app --resource-group life-platform-rg --analytics-query "requests | where timestamp > ago(1h) | summarize count() by resultCode" --output table
```

### View Metrics
```cmd
az monitor metrics list --resource /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-rg/providers/Microsoft.Web/sites/life-functions-app --metric "Requests" --output table
```

---

## 🔧 Troubleshooting Commands

### Restart Function App
```cmd
az functionapp restart --name life-functions-app --resource-group life-platform-rg
```

### View Configuration
```cmd
az functionapp config appsettings list --name life-functions-app --resource-group life-platform-rg --output table
```

### Check Deployment History
```cmd
az deployment group list --resource-group life-platform-rg --output table
```

### View Storage Containers
```cmd
az storage container list --account-name stlifeplatformprod --output table
```

---

## 📋 Checklist for Phase 2

- [ ] Configure Function App application settings
- [ ] Store connection strings in Key Vault
- [ ] Enable managed identity
- [ ] Grant Key Vault access to Function App
- [ ] Deploy application code
- [ ] Test health endpoints
- [ ] Verify EEG processing
- [ ] Set up monitoring alerts
- [ ] Configure custom domain (optional)
- [ ] Run full integration tests

---

## 🆘 Need Help?

### View All Function App Details
```cmd
az functionapp show --name life-functions-app --resource-group life-platform-rg --output json
```

### Get Deployment Credentials
```cmd
az functionapp deployment list-publishing-credentials --name life-functions-app --resource-group life-platform-rg
```

### View Azure Portal
```cmd
start https://portal.azure.com/#resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-rg/providers/Microsoft.Web/sites/life-functions-app/appServices
```

---

**Created**: October 19, 2025  
**Status**: Ready for Phase 2  
**Next Update**: After code deployment complete
