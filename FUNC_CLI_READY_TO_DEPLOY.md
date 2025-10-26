# 🎉 FUNC CLI INSTALLED SUCCESSFULLY!

**Status:** ✅ Azure Functions Core Tools 4.3.0 installed  
**Date:** October 19, 2025  
**Next Step:** Deploy your L.I.F.E Platform code

---

## ✅ What's Working Now:

1. ✅ **Azure CLI** - Authenticated to Microsoft Azure Sponsorship
2. ✅ **Infrastructure** - 15+ resources deployed and running
3. ✅ **func CLI** - Version 4.3.0 installed via npm
4. ✅ **Configuration** - Function App settings applied

**Validation Results:**
- Resource Group: `"Succeeded"`
- Storage Account: `"Succeeded"`
- Function App: `"Running"`

---

## 🚀 DEPLOY NOW (Simple Command)

```cmd
func azure functionapp publish life-functions-app --python
```

**What this does:**
1. Detects Python runtime
2. Installs dependencies from requirements.txt
3. Packages your code
4. Deploys to life-functions-app
5. Shows deployment URL

**Expected runtime:** 2-4 minutes

---

## 📋 If Deployment Asks Questions:

**Q: "Would you like to overwrite?"**  
A: Type `y` and press Enter

**Q: "Install dependencies remotely?"**  
A: Type `y` and press Enter

**Q: "Select Python version"**  
A: Select `3.11` or `3.10`

---

## 🔧 Alternative: Deploy from Specific Folder

If func can't find your files, specify the folder:

```cmd
cd "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
func azure functionapp publish life-functions-app --python
```

---

## ✅ After Deployment - Verify It Works

### Test 1: Health Check
```cmd
curl https://life-functions-app.azurewebsites.net/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "L.I.F.E Platform",
  "version": "1.0.0",
  "life_core_available": true
}
```

### Test 2: View Functions in Portal
```cmd
start https://portal.azure.com/#resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-rg/providers/Microsoft.Web/sites/life-functions-app/functions
```

### Test 3: Stream Logs
```cmd
az webapp log tail --name life-functions-app --resource-group life-platform-rg
```

---

## 🚨 Troubleshooting

### Issue: "No such file or directory: function_app.py"

**Solution:** Make sure you're in the correct directory
```cmd
cd "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
dir function_app.py
```

---

### Issue: "Could not find requirements.txt"

**Solution:** Verify requirements.txt exists
```cmd
dir requirements.txt
```

If missing, create it:
```cmd
echo azure-functions > requirements.txt
echo azure-storage-blob >> requirements.txt
echo azure-servicebus >> requirements.txt
echo azure-identity >> requirements.txt
```

---

### Issue: "Deployment failed: Unauthorized"

**Solution:** Re-authenticate
```cmd
az login
az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca
func azure functionapp publish life-functions-app --python
```

---

### Issue: "Python version not found"

**Solution:** Specify Python version in deployment
```cmd
func azure functionapp publish life-functions-app --build remote
```

---

## 📊 Deployment Progress

When you run the deploy command, you'll see:

```
Getting site publishing info...
Creating archive for current directory...
Uploading 2.5 MB
Upload completed successfully.
Deployment in progress...
Deployment successful.
Functions in life-functions-app:
    health_check - [httpTrigger]
        Invoke url: https://life-functions-app.azurewebsites.net/api/health
    process_eeg - [httpTrigger]
        Invoke url: https://life-functions-app.azurewebsites.net/api/process_eeg
```

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| **Deploy** | `func azure functionapp publish life-functions-app --python` |
| **Test health** | `curl https://life-functions-app.azurewebsites.net/api/health` |
| **View logs** | `az webapp log tail --name life-functions-app --resource-group life-platform-rg` |
| **List functions** | `func azure functionapp list-functions life-functions-app` |
| **Check status** | `az functionapp show --name life-functions-app --resource-group life-platform-rg --query state` |

---

## 🎉 YOU'RE READY!

**One command away from production:**

```cmd
func azure functionapp publish life-functions-app --python
```

**Then test:**

```cmd
curl https://life-functions-app.azurewebsites.net/api/health
```

---

**Let's deploy! 🚀**
