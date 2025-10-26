# 🔐 QUICK CHECKLIST: GitHub Secrets Configuration

## ✅ PREPARATION (5 minutes)
- [ ] Open GitHub repository: https://github.com/SergiLIFE/SergiLIFE-life-azure-system
- [ ] Navigate to: Settings → Secrets and variables → Actions
- [ ] Open Azure Cloud Shell: https://shell.azure.com
- [ ] Verify Azure subscription: `az account show`

## 🚀 CREATE SERVICE PRINCIPAL (2 minutes)
```bash
az ad sp create-for-rbac \
  --name "sp-life-platform-staging" \
  --role "Contributor" \
  --scopes "/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca" \
  --sdk-auth
```
- [ ] Copy the entire JSON output

## 🔑 ADD 5 GITHUB SECRETS (3 minutes)

### Secret 1: AZURE_CREDENTIALS
- [ ] Name: `AZURE_CREDENTIALS`
- [ ] Value: [Paste entire JSON from service principal creation]

### Secret 2: AZURE_SUBSCRIPTION_ID  
- [ ] Name: `AZURE_SUBSCRIPTION_ID`
- [ ] Value: `5c88cef6-f243-497d-98af-6c6086d575ca`

### Secret 3: AZURE_RG_STAGING
- [ ] Name: `AZURE_RG_STAGING` 
- [ ] Value: `life-platform-staging-rg`

### Secret 4: AZURE_WEBAPP_NAME_STAGING
- [ ] Name: `AZURE_WEBAPP_NAME_STAGING`
- [ ] Value: `life-platform-staging`

### Secret 5: AZURE_LOCATION
- [ ] Name: `AZURE_LOCATION`
- [ ] Value: `eastus2`

## 🎯 TRIGGER DEPLOYMENT (1 minute)
```cmd
git add .
git commit -m "L.I.F.E Platform staging deployment ready"
git push origin main
```
- [ ] Push changes to GitHub
- [ ] Monitor at: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions

## 🏥 VALIDATE DEPLOYMENT (2 minutes)
- [ ] Check Azure resources created
- [ ] Test: https://life-platform-staging.azurewebsites.net/health
- [ ] Verify JSON response with "status": "healthy"

## 🎉 SUCCESS CRITERIA
- [ ] All 5 secrets configured in GitHub
- [ ] GitHub Actions workflow completes successfully
- [ ] Azure staging resources created
- [ ] Health endpoint returns 200 OK
- [ ] L.I.F.E Platform staging operational

**Total Time: ~15 minutes**
**Revenue Impact: Enables $345K Q4 2025 → $50.7M by 2029**