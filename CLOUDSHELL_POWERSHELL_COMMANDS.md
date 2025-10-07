# 🚨 L.I.F.E Platform - Azure Cloud Shell PowerShell Commands

## 📋 **COPY & PASTE THESE COMMANDS (PowerShell Mode)**

### **Step 1: Set Subscription**
```powershell
az account set --subscription "5c88cef6-f243-497d-98af-6c6086d575ca"
az account show --query "{name:name, id:id}" --output table
```

### **Step 2: Check Function App Status**
```powershell
az functionapp show --name "life-functions-app" --resource-group "life-platform-rg" --query "{name:name,state:state}" --output table
```

### **Step 3: Fix Runtime Version**
```powershell
az functionapp config set --name "life-functions-app" --resource-group "life-platform-rg" --linux-fx-version "Python|3.11"
```

### **Step 4: Configure App Settings**
```powershell
az functionapp config appsettings set --name "life-functions-app" --resource-group "life-platform-rg" --settings "FUNCTIONS_WORKER_RUNTIME=python" "FUNCTIONS_EXTENSION_VERSION=~4" "PYTHON_VERSION=3.11" "LIFE_PLATFORM_VERSION=2025.1.0-PRODUCTION"
```

### **Step 5: Restart Function App**
```powershell
az functionapp restart --name "life-functions-app" --resource-group "life-platform-rg"
```

### **Step 6: Wait and Verify**
```powershell
Start-Sleep -Seconds 30
az functionapp show --name "life-functions-app" --resource-group "life-platform-rg" --query "{name:name,state:state}" --output table
```

### **Step 7: Test Functions**
```powershell
az functionapp function list --name "life-functions-app" --resource-group "life-platform-rg" --output table
```

## 🎯 **COPY EACH COMMAND ONE BY ONE INTO CLOUD SHELL**