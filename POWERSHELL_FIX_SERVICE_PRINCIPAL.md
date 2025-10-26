# 🔐 POWERSHELL FIX - Azure Service Principal for L.I.F.E Platform

## ⚡ IMMEDIATE SOLUTION

You're in PowerShell, so use this exact command (copy and paste as ONE line):

```powershell
az ad sp create-for-rbac --name "sp-life-platform-staging" --role "Contributor" --scopes "/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca" --sdk-auth
```

## 🚨 WHAT WENT WRONG

- **Problem:** PowerShell doesn't recognize `\` for line continuation (that's bash syntax)  
- **Solution:** Use backtick `` ` `` for PowerShell line continuation, OR use single line

## ✅ POWERSHELL OPTIONS

### Option 1: Single Line (Recommended)
```powershell
az ad sp create-for-rbac --name "sp-life-platform-staging" --role "Contributor" --scopes "/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca" --sdk-auth
```

### Option 2: Multi-line with PowerShell continuation
```powershell
az ad sp create-for-rbac `
  --name "sp-life-platform-staging" `
  --role "Contributor" `
  --scopes "/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca" `
  --sdk-auth
```

### Option 3: Switch to Azure Cloud Shell (Bash)
```
https://shell.azure.com
```
Then use the original bash command with `\` continuation.

## 🎯 NEXT STEPS AFTER RUNNING COMMAND

1. **Copy the entire JSON output**
2. **Go to GitHub:** https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/secrets/actions
3. **Add secret:** AZURE_CREDENTIALS with the JSON value
4. **Add 4 more secrets:**
   - AZURE_SUBSCRIPTION_ID: `5c88cef6-f243-497d-98af-6c6086d575ca`
   - AZURE_RG_STAGING: `life-platform-staging-rg`
   - AZURE_WEBAPP_NAME_STAGING: `life-platform-staging`
   - AZURE_LOCATION: `eastus2`

## 💰 L.I.F.E Platform Ready!
Revenue Target: $345K Q4 2025 → $50.7M by 2029