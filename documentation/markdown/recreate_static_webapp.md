# Recreate Azure Static Web App - Free Alternative to Support Ticket

## Why This Might Work
- Sometimes Azure Static Web Apps get stuck in an inconsistent state
- Recreation often resolves backend deployment issues
- Free alternative to $29/month support plan

## Steps to Recreate Static Web App

### 1. Document Current Configuration
- **Resource Name**: icy-tree-0c638f80f
- **Resource Group**: rg-life-platform-static  
- **Subscription**: 5c88cef6-f243-497d-98af-6c6086d575ca
- **GitHub Repository**: SergiLIFE/SergiLIFE-life-azure-system
- **Branch**: main
- **App Location**: docs
- **Deployment Token**: AZURE_STATIC_WEB_APPS_API_TOKEN_ICY_TREE_0C638F80F

### 2. Delete Current Resource
```bash
az staticwebapp delete \
  --name icy-tree-0c638f80f \
  --resource-group rg-life-platform-static \
  --subscription 5c88cef6-f243-497d-98af-6c6086d575ca
```

### 3. Create New Static Web App
```bash
az staticwebapp create \
  --name life-platform-static \
  --resource-group rg-life-platform-static \
  --source https://github.com/SergiLIFE/SergiLIFE-life-azure-system \
  --location "East US 2" \
  --branch main \
  --app-location "docs" \
  --login-with-github
```

### 4. Update GitHub Secret
- Go to GitHub Repository Settings → Secrets and Variables → Actions
- Update AZURE_STATIC_WEB_APPS_API_TOKEN_ICY_TREE_0C638F80F with new deployment token

## Alternative: Create with Different Name
If deletion fails, create with new name:
- **New Name**: life-platform-v2
- **New URL**: life-platform-v2.azurestaticapps.net

## Backup Plan: Alternative Hosting
If Static Web Apps continues having issues:

1. **Azure App Service** (already working at lifecoach-121.com)
2. **GitHub Pages** (free for public repos)
3. **Netlify** (free tier available)
4. **Vercel** (free tier available)

## Expected Outcome
- Fresh Static Web App resource should properly serve docs folder content
- New deployment token will trigger clean GitHub Actions workflow
- Custom domain can be configured on working resource