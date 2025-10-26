# Azure Functions Core Tools - Installation Guide

## ❌ Current Status
**Azure Functions Core Tools:** Not Installed
**Error:** `'func' is not recognized as an internal or external command`

---

## ✅ Solution: Install Azure Functions Core Tools

### Option 1: Install via npm (Recommended - Fastest)

**Prerequisites:** Node.js must be installed

```cmd
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

**Check if Node.js is installed:**
```cmd
node --version
npm --version
```

If Node.js is not installed, download from: https://nodejs.org/

---

### Option 2: Install via MSI Installer (Easiest)

**Download and run the installer:**

1. Visit: https://github.com/Azure/azure-functions-core-tools/releases
2. Download: `Azure.Functions.Cli.win-x64.4.x.xxxx.msi`
3. Run the installer
4. Restart your terminal after installation

**Direct link to latest stable:**
https://go.microsoft.com/fwlink/?linkid=2174087

---

### Option 3: Install via Chocolatey

If you have Chocolatey package manager:

```cmd
choco install azure-functions-core-tools-4
```

---

### Option 4: Install via winget

If you have winget (Windows Package Manager):

```cmd
winget install Microsoft.Azure.FunctionsCoreTools
```

---

## ✅ Verify Installation

After installing, **restart your terminal** and run:

```cmd
func --version
```

Expected output: `4.x.xxxx`

---

## 🚀 Alternative Deployment Methods (No func CLI needed)

Since you don't have `func` installed, you can still deploy using these methods:

### Method 1: VS Code Extension (RECOMMENDED)

**This is the easiest way to deploy without func CLI!**

1. **Install VS Code Extension:**
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Azure Functions"
   - Install: `Azure Functions` (by Microsoft)

2. **Sign in to Azure:**
   - Press `Ctrl+Shift+P`
   - Type: `Azure: Sign In`
   - Follow the browser authentication

3. **Deploy:**
   - Click Azure icon in left sidebar
   - Expand your subscription
   - Find `life-functions-app`
   - Right-click → `Deploy to Function App...`
   - Select your workspace folder

**No func CLI required!** ✅

---

### Method 2: Azure CLI ZIP Deploy

```cmd
REM First, create a ZIP of your function app
powershell Compress-Archive -Path function_app.py,host.json,requirements.txt -DestinationPath deployment.zip -Force

REM Then deploy the ZIP
az functionapp deployment source config-zip --resource-group life-platform-rg --name life-functions-app --src deployment.zip
```

---

### Method 3: GitHub Actions (Continuous Deployment)

Create `.github/workflows/deploy-function.yml`:

```yaml
name: Deploy Function App

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: windows-latest
    
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

To get publish profile:
```cmd
az functionapp deployment list-publishing-profiles --name life-functions-app --resource-group life-platform-rg --xml
```

---

## 🎯 Recommended Next Steps

### For Immediate Deployment (Today):

**Use VS Code Extension** - No installation needed, just the extension!

1. Install Azure Functions extension in VS Code
2. Sign in to Azure
3. Right-click and deploy

**Estimated time:** 5 minutes

---

### For Future Automation:

**Install Azure Functions Core Tools** - Enables CLI deployments

1. Download MSI installer (Option 2 above)
2. Install (takes 2 minutes)
3. Restart terminal
4. Verify with `func --version`

**Estimated time:** 5 minutes + restart

---

## 📋 Quick Decision Matrix

| Method | Requires | Time | Complexity | Recommended For |
|--------|----------|------|------------|-----------------|
| **VS Code Extension** | VS Code + Extension | 5 min | ⭐ Easy | **First deployment** |
| **func CLI** | Node.js or MSI | 5 min | ⭐⭐ Medium | Automation |
| **Azure CLI ZIP** | Azure CLI only | 2 min | ⭐⭐⭐ Hard | Quick updates |
| **GitHub Actions** | GitHub setup | 15 min | ⭐⭐⭐ Hard | CI/CD |

---

## ✅ What Should You Do RIGHT NOW?

### Option A: Deploy Today (VS Code Extension)
```
1. Open VS Code
2. Install "Azure Functions" extension
3. Sign in to Azure (Ctrl+Shift+P → Azure: Sign In)
4. Deploy (Right-click life-functions-app → Deploy)
```

### Option B: Install func CLI for Future
```
1. Download: https://go.microsoft.com/fwlink/?linkid=2174087
2. Run the MSI installer
3. Restart terminal
4. Verify: func --version
5. Then deploy: func azure functionapp publish life-functions-app
```

---

## 🔧 Troubleshooting

**Issue:** Node.js not found
```cmd
REM Download Node.js from: https://nodejs.org/
REM Or use MSI installer instead (Option 2)
```

**Issue:** Permission denied during npm install
```cmd
REM Run as Administrator or use MSI installer
```

**Issue:** func installed but not recognized
```cmd
REM Restart your terminal completely (close and reopen)
REM Or restart VS Code
```

---

## 📞 Quick Links

- Azure Functions Core Tools Releases: https://github.com/Azure/azure-functions-core-tools/releases
- VS Code Azure Functions Extension: https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions
- Node.js Download: https://nodejs.org/
- Azure Functions Documentation: https://learn.microsoft.com/azure/azure-functions/

---

**Generated:** October 19, 2025  
**Status:** func CLI not installed - VS Code extension recommended for immediate deployment

🎯 **Recommendation: Use VS Code Extension for your first deployment today!**
