# 🚀 L.I.F.E. Platform Code Deployment Guide

## ✅ Infrastructure Status

Your Azure infrastructure is deploying now via `cloudshell-deploy.sh`

## 📦 What's Ready for Code Deployment

### Files Created

1. ✅ **Dockerfile** (already exists) - Builds your L.I.F.E. Platform container
2. ✅ **`.github/workflows/deploy-life-to-azure.yml`** - Automatic GitHub deployment
3. ✅ **`infra/deploy-code.sh`** - Manual deployment script

---

## 🎯 Option 1: Automatic GitHub Actions Deployment (RECOMMENDED)

### Step 1: Get Azure Credentials

Run this in Azure Cloud Shell (after infrastructure completes):

```bash
az ad sp create-for-rbac \
  --name "life-github-deploy" \
  --role contributor \
  --scopes /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/rg-life-microsoft-demo \
  --sdk-auth
```

**Copy the entire JSON output!**

### Step 2: Add to GitHub Secrets

1. Go to your GitHub repo: `https://github.com/SergiLIFE/life-azure-system`
2. Settings → Secrets and variables → Actions
3. Click **"New repository secret"**
4. Name: `AZURE_CREDENTIALS`
5. Paste the JSON from Step 1
6. Click **"Add secret"**

### Step 3: Deploy

```bash
# Commit and push the new workflow
git add .github/workflows/deploy-life-to-azure.yml
git add Dockerfile
git commit -m "Add Azure deployment automation"
git push origin main
```

**That's it!** GitHub Actions will automatically:

- ✅ Build your Docker image with all 686+ Python files
- ✅ Push to Azure Container Registry
- ✅ Deploy to Container Apps
- ✅ Update Azure Functions

---

## 🎯 Option 2: Manual Cloud Shell Deployment

### After infrastructure completes, upload and run

```bash
# Upload your entire repository to Cloud Shell
# Then run:

chmod +x infra/deploy-code.sh
./infra/deploy-code.sh
```

This will guide you through manual deployment steps.

---

## 🎯 Option 3: Quick Manual Build

### In Cloud Shell (requires uploading your repo)

```bash
# Get ACR name
ACR_NAME=$(az acr list --resource-group rg-life-microsoft-demo --query "[0].name" -o tsv)

# Build and push
az acr build \
  --registry $ACR_NAME \
  --image life-platform:latest \
  --file Dockerfile \
  .

# Update Container App
CONTAINER_APP=$(az containerapp list --resource-group rg-life-microsoft-demo --query "[0].name" -o tsv)

az containerapp update \
  --name $CONTAINER_APP \
  --resource-group rg-life-microsoft-demo \
  --image $ACR_NAME.azurecr.io/life-platform:latest
```

---

## 📋 What Gets Deployed

### Your L.I.F.E. Platform Code

- ✅ **686+ Python files** from `algorithms/python-core/`
- ✅ **Venturi adaptive system** (`venturi_adaptive_system.py`)
- ✅ **Section 3 multi-domain platform** (`life_algorithm_ultimate_section3.py`)
- ✅ **Section 12 orchestrator** (`life_algorithm_section12_integration.py`)
- ✅ **Advanced quantum integration** (`advanced_life_quantum_integration.py`)
- ✅ **EEG processing algorithms**
- ✅ **Neural processing core**
- ✅ **Azure Functions** (marketplace webhooks, APIs)
- ✅ **All dependencies** from `requirements.txt`

### Docker Image Contents

```
/app/
├── algorithms/python-core/     # All 686+ algorithm files
├── life_algorithm_*.py         # Core platform files
├── azure_functions/            # Function apps
├── requirements.txt            # Python dependencies
├── logs/                       # Application logs
└── data/                       # Runtime data
```

---

## 🔗 After Deployment URLs

Once deployed, your L.I.F.E. Platform will be accessible at:

```
Container App (Main Platform):
https://life-microsoft-demo-app.eastus2.azurecontainerapps.io

Azure Functions (APIs):
https://life-microsoft-demo-func.azurewebsites.net/api/

Monitoring Dashboard:
https://portal.azure.com/#@e716161a-5e85-4d6d-82f9-96bcdd2e65ac/resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/rg-life-microsoft-demo
```

---

## 🧪 Testing Deployment

### Health Check

```bash
curl https://life-microsoft-demo-app.eastus2.azurecontainerapps.io/health
```

### View Logs

```bash
az containerapp logs show \
  --name life-microsoft-demo-app \
  --resource-group rg-life-microsoft-demo \
  --follow
```

---

## 🎉 Deployment Timeline

1. **NOW:** Infrastructure deploying (10-15 minutes) ⏱️
2. **NEXT:** Set up GitHub secrets (2 minutes)
3. **THEN:** Push code → automatic deployment (5-10 minutes)
4. **RESULT:** Fully operational L.I.F.E. Platform in Azure! 🚀

---

## 💰 What This Costs

**Monthly estimate:**

- Infrastructure: ~$25/month (from your previous estimate)
- Container storage: ~$2/month
- Data transfer: ~$1/month
- **Total: ~$28/month** from Azure Sponsorship

---

## 📞 Next Steps

### Immediate (Now)

1. ✅ Wait for infrastructure deployment to complete
2. ⏳ Prepare GitHub credentials

### After Infrastructure Completes

1. Run command to get Azure credentials
2. Add credentials to GitHub secrets
3. Push deployment workflow
4. Watch automatic deployment! 🎉

### Within 30 Minutes

- ✅ Fully deployed L.I.F.E. Platform
- ✅ Live Azure URLs
- ✅ Automated CI/CD pipeline
- ✅ Ready for demos and production use!

---

**Status:** Ready to deploy code as soon as infrastructure finishes! 🚀
