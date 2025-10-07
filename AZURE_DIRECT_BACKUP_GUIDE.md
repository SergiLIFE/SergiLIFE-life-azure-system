# Azure Direct Backup - Quick Setup Guide

## 🚀 **Quick Start - Backup to Your Azure Account**

Since your terminal and OneDrive aren't working, this creates a direct backup to your **Microsoft Azure cloud account**.

### **Your Azure Details:**
- **Subscription ID:** `5c88cef6-f243-497d-98af-6c6086d575ca`
- **Storage Account:** `stlifeplatformprod`
- **Admin Email:** `sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com`

## 📦 **Step 1: Install Azure SDK (One Time Only)**

### **Option A - Simple Command (if any terminal works):**
```bash
pip install azure-storage-blob azure-identity
```

### **Option B - Python IDLE Method:**
1. Press **Win+R**, type `idle`, press Enter
2. In Python IDLE, run these commands:
```python
import subprocess
subprocess.run(['pip', 'install', 'azure-storage-blob', 'azure-identity'])
```

### **Option C - Manual Download:**
1. Go to [https://pypi.org/project/azure-storage-blob/](https://pypi.org/project/azure-storage-blob/)
2. Download the `.whl` file
3. Run: `pip install downloaded-file.whl`

## ☁️ **Step 2: Run the Backup**

### **Easy Method:**
1. **Double-click** `azure_direct_backup.py` in Windows Explorer
2. **Or** open in VS Code and press **F5**
3. Follow the prompts to authenticate with Azure

### **What it does:**
- ✅ Creates a ZIP of all your L.I.F.E. Platform files
- ✅ Uploads directly to your Azure Storage Account
- ✅ Creates backup manifest with file integrity checks
- ✅ Provides download URLs for recovery

## 🔑 **Step 3: Get Your Storage Key**

The script will ask for your Azure Storage Account Key:

1. Go to [https://portal.azure.com](https://portal.azure.com)
2. Search for `stlifeplatformprod`
3. Click **"Access keys"** in left menu
4. Copy the **"key1"** value
5. Paste it when prompted

## 📱 **Alternative - Manual Upload Method**

If the automated script doesn't work:

### **Azure Portal Upload:**
1. Run `azure_direct_backup.py` - it creates a ZIP file
2. Go to [https://portal.azure.com](https://portal.azure.com)
3. Search for `stlifeplatformprod`
4. Click **"Containers"** → **"repository-backups"**
5. Click **"Upload"** and select your ZIP file

### **Azure Storage Explorer:**
1. Download [Azure Storage Explorer](https://azure.microsoft.com/features/storage-explorer/)
2. Sign in with your Azure account
3. Navigate to your storage account
4. Upload the ZIP file

## 🛡️ **Your Files Will Be Safe At:**

```
Azure Storage Account: stlifeplatformprod
Container: repository-backups
Path: life-platform/[timestamp]/backup.zip
```

## 🎯 **Benefits:**

- ✅ **Direct Microsoft Cloud Storage** - bypasses OneDrive issues
- ✅ **No terminal required** - works entirely through Python
- ✅ **Automatic integrity checks** - ensures files aren't corrupted
- ✅ **Version control** - timestamped backups
- ✅ **Enterprise-grade security** - Azure encryption at rest
- ✅ **Global accessibility** - access from anywhere
- ✅ **Cost-effective** - uses your existing Azure subscription

## 🚨 **Tomorrow is Launch Day!**

**September 27, 2025** - Your L.I.F.E. Platform launches on Azure Marketplace!

This backup ensures your hard work is protected before the big day. Even if your computer crashes, everything will be safely stored in Microsoft's cloud.

---

**Just run `azure_direct_backup.py` and your work will be safely backed up to Microsoft Azure! 🚀**