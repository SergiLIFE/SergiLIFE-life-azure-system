# 🔧 Azure Credentials Configuration Guide
## GitHub Repository Setup for L.I.F.E. Platform

### ⚠️ **ISSUE IDENTIFIED**
```
Azure Deployment Status
⚠️ Azure credentials not configured
ℹ️ Configure repository variables: AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_SUBSCRIPTION_ID
```

---

## 🔑 **REQUIRED AZURE CREDENTIALS**

Based on your L.I.F.E. Platform configuration, you need these GitHub repository variables:

### Required Variables:
1. **AZURE_CLIENT_ID** - Service Principal Client ID
2. **AZURE_TENANT_ID** - Azure AD Tenant ID  
3. **AZURE_SUBSCRIPTION_ID** - Azure Subscription ID
4. **AZURE_STATIC_WEB_APPS_API_TOKEN** - Static Web App deployment token

### Your Known Values:
- **Subscription ID**: `5c88cef6-f243-497d-98af-6c6086d575ca`
- **Tenant ID**: Available from Azure Portal → Azure Active Directory
- **Region**: East US 2
- **Static Web App**: `life-platform-webapp`

---

## 🚀 **QUICK FIX METHODS**

### Method 1: GitHub Web Interface (Recommended)
1. Go to: https://github.com/SergiLIFE/SergiLIFE-life-azure-system
2. Click **Settings** tab
3. Go to **Secrets and variables** → **Actions**
4. Click **Variables** tab
5. Add each variable:

```
AZURE_CLIENT_ID = [Your Service Principal Client ID]
AZURE_TENANT_ID = [Your Azure AD Tenant ID]  
AZURE_SUBSCRIPTION_ID = 5c88cef6-f243-497d-98af-6c6086d575ca
```

### Method 2: GitHub CLI (If available)
```bash
gh variable set AZURE_SUBSCRIPTION_ID --body "5c88cef6-f243-497d-98af-6c6086d575ca"
gh variable set AZURE_TENANT_ID --body "[YOUR_TENANT_ID]"
gh variable set AZURE_CLIENT_ID --body "[YOUR_CLIENT_ID]"
```

### Method 3: Azure CLI Setup
```bash
# Get your tenant ID
az account show --query tenantId -o tsv

# Create service principal for GitHub Actions
az ad sp create-for-rbac --name "github-actions-life-platform" --role contributor --scopes /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca --sdk-auth
```

---

## 🔍 **HOW TO FIND YOUR AZURE VALUES**

### Tenant ID:
1. Azure Portal → **Azure Active Directory**
2. **Overview** → Copy **Tenant ID**

### Client ID (Service Principal):
1. Azure Portal → **Azure Active Directory** 
2. **App registrations** → Find your app
3. Copy **Application (client) ID**

### Static Web App Token:
1. Azure Portal → **Static Web Apps**
2. Select **life-platform-webapp**
3. **Overview** → **Manage deployment token**
4. Copy the token

---

## 🎯 **IMMEDIATE ACTION PLAN**

### Step 1: Get Azure Information
```bash
# If you have Azure CLI installed:
az account show --output table
az account list --output table
```

### Step 2: Configure GitHub Variables
Go to your repository settings and add the missing variables.

### Step 3: Re-run Deployment
Once variables are set, GitHub Actions will automatically use them for Azure deployment.

---

## 🚨 **TEMPORARY WORKAROUND**

Since your platform is already live at https://green-ground-0c65efe0f.1.azurestaticapps.net, the missing credentials won't affect your October 15 demo. However, future deployments will need these credentials.

### For October 15 Demo:
- ✅ Platform is already deployed and working
- ✅ Demo shortcuts are ready  
- ✅ 23 participants can access the platform
- ⚠️ Future updates will need proper Azure credentials

---

## 📞 **SUPPORT RESOURCES**

### Azure Documentation:
- [GitHub Actions with Azure](https://docs.microsoft.com/en-us/azure/developer/github/)
- [Service Principal Setup](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals)

### Quick Links:
- **Azure Portal**: https://portal.azure.com
- **GitHub Repository**: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/variables/actions

---

## 🎉 **CONCLUSION**

Your L.I.F.E. Platform is working perfectly for the October 15 demo! The missing Azure credentials are only needed for future automated deployments. You can configure them after your successful demo presentation.

**Priority**: Demo first, credentials setup second! 🚀

---

*L.I.F.E. Platform - Learning Individually from Experience*  
*Copyright 2025 - Sergio Paya Borrull*