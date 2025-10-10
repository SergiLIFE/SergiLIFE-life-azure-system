# 🚀 L.I.F.E. Platform Campaign Trigger - Quick Command Reference

## ❌ **The Problem You Encountered:**
You were trying to run PowerShell commands from Command Prompt (CMD) without being in the correct directory.

## ✅ **The Solutions:**

### **EASIEST METHOD: Use the Quick Launch**
```cmd
# From anywhere, run this:
c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system\QUICK_LAUNCH.bat
```

### **METHOD 1: Command Prompt (CMD) - What You Were Using**

**Step 1: Navigate to project directory**
```cmd
cd "c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
```

**Step 2a: Use Batch Script (Simplest)**
```cmd
TRIGGER_CAMPAIGN.bat
```

**Step 2b: Run PowerShell from CMD**
```cmd
powershell -ExecutionPolicy Bypass -File "TRIGGER_CAMPAIGN.ps1" -Action normal
powershell -ExecutionPolicy Bypass -File "TRIGGER_CAMPAIGN.ps1" -Action emergency  
powershell -ExecutionPolicy Bypass -File "TRIGGER_CAMPAIGN.ps1" -Action validate
```

**Step 2c: Use Python Directly**
```cmd
python simple_ui_test.py
python campaign_automatic_trigger.py
```

### **METHOD 2: PowerShell Terminal**

**Step 1: Open PowerShell and navigate**
```powershell
cd "c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
```

**Step 2: Run PowerShell script**
```powershell
.\TRIGGER_CAMPAIGN.ps1 -Action normal
.\TRIGGER_CAMPAIGN.ps1 -Action emergency
.\TRIGGER_CAMPAIGN.ps1 -Action validate
```

### **METHOD 3: VS Code Terminal**

**From VS Code terminal (already in correct directory):**
```cmd
# Batch script
TRIGGER_CAMPAIGN.bat

# Or PowerShell
powershell .\TRIGGER_CAMPAIGN.ps1 -Action normal

# Or Python
python simple_ui_test.py
```

## 🎯 **Recommended Action Right Now:**

1. **Copy this command and paste it in your CMD:**
   ```cmd
   cd "c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system" && TRIGGER_CAMPAIGN.bat
   ```

2. **Or use the quick launcher:**
   ```cmd
   "c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system\QUICK_LAUNCH.bat"
   ```

## 💡 **Why Your Commands Didn't Work:**

❌ **Wrong:** `.\TRIGGER_CAMPAIGN.ps1 -Action normal` from CMD in wrong directory  
✅ **Right:** Navigate to project directory first, then use proper syntax

❌ **Wrong:** PowerShell syntax in Command Prompt  
✅ **Right:** Use `powershell -File` or open PowerShell terminal

❌ **Wrong:** Wrong working directory  
✅ **Right:** Must be in the project directory where scripts exist

## 🔥 **Emergency Quick Fix:**

**Just copy and paste this ONE LINE in your CMD:**
```cmd
cd "c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system" && TRIGGER_CAMPAIGN.bat
```

This will navigate to the correct directory and run the batch script immediately!