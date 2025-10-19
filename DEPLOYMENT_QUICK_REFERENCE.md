# L.I.F.E Platform - Deployment Quick Reference
**One-Page Cheat Sheet**

---

## 🚀 Three-Phase Deployment (Fully Automated)

```
Phase 1: Infrastructure ✅ DONE
Phase 2: Validation     → Run now
Phase 3: Production     → After 24h monitoring
```

---

## ⚡ Quick Commands

### Phase 2: Validate Deployment
```cmd
python validate_deployment.py --environment staging
```
**or**
```cmd
VALIDATE_DEPLOYMENT.bat
```

### Phase 3: Deploy to Production
```cmd
python deploy_to_production.py
```
**or**
```cmd
DEPLOY_TO_PRODUCTION.bat
```

---

## 📋 Validation Checklist

Before running validation:
- [x] Infrastructure deployed (Phase 1 complete)
- [ ] Azure CLI authenticated (`az account show`)
- [ ] Resources initialized (wait 3-5 minutes after deployment)

---

## 🎯 Production Checklist

Before deploying to production:
- [ ] Validation passed (100% success rate)
- [ ] 24 hours of monitoring completed
- [ ] No critical errors found
- [ ] Performance metrics acceptable
- [ ] Backup plan ready

---

## 📊 Quick Status Checks

### Check all resources
```cmd
az resource list --resource-group life-platform-rg --output table
```

### Check Function App
```cmd
az functionapp show --name life-functions-app --resource-group life-platform-rg --query "{state:state}" --output table
```

### View logs
```cmd
az functionapp log tail --name life-functions-app --resource-group life-platform-rg
```

---

## 🔧 Troubleshooting

### Validation fails?
1. Check log file: `deployment_validation_*.log`
2. Verify authentication: `az account show`
3. Re-deploy if needed: `SIMPLE_DEPLOY.bat`

### Production deployment fails?
1. Check log file: `production_deployment_*.log`
2. Verify staging health
3. Manual rollback if needed

### Rollback command
```cmd
az functionapp restart --name life-functions-app --resource-group life-platform-rg
```

---

## 📞 Quick Links

**Azure Portal**: https://portal.azure.com/#resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-rg/overview

**Function App**: https://life-functions-app.azurewebsites.net

**Application Insights**: Check Azure Portal → life-functions-app → Application Insights

---

## 🎉 Success Indicators

**Validation Pass**:
- ✅ 6/6 tests passed
- ✅ All resources healthy
- ✅ Function App running

**Production Success**:
- ✅ Slot swap complete
- ✅ Health checks passing
- ✅ Monitoring active

---

**Status**: Phase 1 ✅ Complete | Phase 2 Ready | Phase 3 Pending
