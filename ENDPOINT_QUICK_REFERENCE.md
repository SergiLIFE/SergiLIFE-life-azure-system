# 🎯 L.I.F.E. Platform - Azure Function Endpoints Quick Reference

**Function App:** `life-functions-app`  
**Base URL:** `https://life-functions-app.azurewebsites.net`  
**Region:** East US 2  
**Last Updated:** October 19, 2025

## 📋 Available Endpoints

### 1. 🏥 Health Check (Public)
**URL:** `https://life-functions-app.azurewebsites.net/api/health`  
**Method:** `GET`  
**Auth:** Anonymous (no key required)  
**Purpose:** Verify Function App is running and get platform status

**Test Command:**
```cmd
python test_deployment.py
```

**Expected Response:**
```json
{
  "status": "healthy",
  "platform": "L.I.F.E. (Learning Individually from Experience)",
  "version": "1.0.0",
  "timestamp": "2025-10-19T...",
  "services": {
    "eeg_processor": "operational",
    "analytics": "operational",
    "authentication": "operational"
  },
  "azure": {
    "region": "eastus2",
    "environment": "production"
  }
}
```

---

### 2. 🧠 EEG Processing (Authenticated)
**URL:** `https://life-functions-app.azurewebsites.net/api/eeg/process`  
**Method:** `POST`  
**Auth:** Function Key required  
**Purpose:** Process EEG data using L.I.F.E. neuroadaptive learning algorithm

**Get Function Key:**
```cmd
az functionapp keys list --name life-functions-app --resource-group life-platform-rg --query "functionKeys.default" -o tsv
```

**Test Command (PowerShell):**
```powershell
$key = az functionapp keys list --name life-functions-app --resource-group life-platform-rg --query "functionKeys.default" -o tsv
$headers = @{"x-functions-key" = $key; "Content-Type" = "application/json"}
$body = @{
    "channels" = @("Fp1", "Fp2", "F3", "F4")
    "data" = @(@(0.1, 0.2, 0.3), @(0.2, 0.3, 0.4))
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://life-functions-app.azurewebsites.net/api/eeg/process" -Method POST -Headers $headers -Body $body
```

**Expected Response:**
```json
{
  "status": "success",
  "processing_time_ms": 4.5,
  "learning_outcomes": [...],
  "accuracy": 95.8
}
```

---

### 3. 📊 Analytics Dashboard (Authenticated)
**URL:** `https://life-functions-app.azurewebsites.net/api/analytics`  
**Method:** `GET`  
**Auth:** Function Key required  
**Purpose:** Get real-time analytics and learning metrics

**Test Command (PowerShell):**
```powershell
$key = az functionapp keys list --name life-functions-app --resource-group life-platform-rg --query "functionKeys.default" -o tsv
Invoke-RestMethod -Uri "https://life-functions-app.azurewebsites.net/api/analytics" -Method GET -Headers @{"x-functions-key" = $key}
```

---

### 4. 🔐 Authentication Token (Authenticated)
**URL:** `https://life-functions-app.azurewebsites.net/api/auth/token`  
**Method:** `POST`  
**Auth:** Function Key required  
**Purpose:** Generate JWT tokens for API authentication

**Test Command (PowerShell):**
```powershell
$key = az functionapp keys list --name life-functions-app --resource-group life-platform-rg --query "functionKeys.default" -o tsv
$headers = @{"x-functions-key" = $key; "Content-Type" = "application/json"}
$body = @{
    "username" = "testuser"
    "password" = "testpass"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://life-functions-app.azurewebsites.net/api/auth/token" -Method POST -Headers $headers -Body $body
```

---

## 🔧 Troubleshooting Commands

### Check Function App Status
```cmd
az functionapp show --name life-functions-app --resource-group life-platform-rg --query "state" -o tsv
```

### List All Functions
```cmd
az functionapp function list --name life-functions-app --resource-group life-platform-rg --output table
```

### Restart Function App
```cmd
az functionapp restart --name life-functions-app --resource-group life-platform-rg
```

### View Real-Time Logs
```cmd
az webapp log tail --name life-functions-app --resource-group life-platform-rg
```

### Check Deployment History
```cmd
az functionapp deployment list --name life-functions-app --resource-group life-platform-rg --output table
```

---

## 🚀 Deployment Commands

### Redeploy Function App
```cmd
func azure functionapp publish life-functions-app --python --build remote
```

### Validate Local Functions
```cmd
func start
```

---

## 📝 Notes

- **Health endpoint** uses anonymous auth for easy monitoring
- **All other endpoints** require function keys for security
- **Function keys** can be retrieved using Azure CLI (see commands above)
- **Wait 1-2 minutes** after deployment for functions to sync
- **Logs** are available in Application Insights (see Azure Portal)

---

## 🎯 Quick Test Sequence

1. **Test Health (should work immediately after deployment):**
   ```cmd
   python test_deployment.py
   ```

2. **Get Function Key:**
   ```cmd
   az functionapp keys list --name life-functions-app --resource-group life-platform-rg --query "functionKeys.default" -o tsv
   ```

3. **Test EEG Processing:**
   - Use PowerShell command from section 2 above

4. **Test Analytics:**
   - Use PowerShell command from section 3 above

---

**Generated:** October 19, 2025  
**Platform:** L.I.F.E. (Learning Individually from Experience)  
**Copyright:** 2025 Sergio Paya Borrull
