# Quick Start: Azure OIDC for GitHub Actions

## 🚀 Run the Setup Script

```powershell
# In PowerShell, run the automated setup script
.\setup-azure-oidc.ps1
```

## 📋 Manual Setup (Alternative)

If you prefer manual setup, follow these commands:

```powershell
# 1. Login to Azure
az login

# 2. Create Azure AD App
az ad app create --display-name "GitHub-SergiLIFE-life-azure-system"

# 3. Note the appId from output, then create service principal
az ad sp create --id <YOUR_APP_ID>

# 4. Assign role (replace with your subscription ID and app ID)
az role assignment create --assignee <YOUR_APP_ID> --role "Contributor" --scope "/subscriptions/<YOUR_SUBSCRIPTION_ID>"

# 5. Create federated credential for main branch
az ad app federated-credential create --id <YOUR_APP_ID> --parameters '{
    "name": "github-main",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:SergiLIFE/SergiLIFE-life-azure-system:ref:refs/heads/main",
    "description": "GitHub Actions for main branch",
    "audiences": ["api://AzureADTokenExchange"]
}'
```

## 🔧 GitHub Repository Setup

1. Go to your repository: https://github.com/SergiLIFE/SergiLIFE-life-azure-system
2. Navigate to: Settings → Secrets and variables → Actions → Variables tab
3. Add these variables:
   - `AZURE_CLIENT_ID`: Your application (client) ID
   - `AZURE_TENANT_ID`: Your Azure AD tenant ID  
   - `AZURE_SUBSCRIPTION_ID`: Your Azure subscription ID

## ✅ Test Your Setup

1. Push changes to trigger the workflow
2. Check GitHub Actions tab: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions
3. Verify Azure login step succeeds

## 🛠️ Troubleshooting

- **Variables not found**: Ensure you added them as repository variables (not secrets)
- **Permission denied**: Check service principal has Contributor role
- **OIDC token exchange failed**: Verify federated credential subject matches exactly

## 📚 What Changed

- ❌ **Before**: Used `creds` with JSON secret (insecure)
- ✅ **After**: Uses OIDC with federated credentials (secure, no secrets!)

Your workflow now uses:
```yaml
- name: Azure Login
  uses: azure/login@v2
  with:
    client-id: ${{ vars.AZURE_CLIENT_ID }}
    tenant-id: ${{ vars.AZURE_TENANT_ID }}
    subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
```
