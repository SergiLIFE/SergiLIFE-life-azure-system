# 🚀 ONE-CLICK DEPLOYMENT - Microsoft Partnership Infrastructure

## Instant Deployment to Your Azure Subscription

**Subscription:** Microsoft Azure Sponsorship (5c88cef6-f243-497d-98af-6c6086d575ca)  
**Existing Resource Group:** rg-life-platform-static  
**Location:** East US 2

---

## 🎯 FASTEST METHOD: Azure Portal Upload

### Step 1: Open Azure Portal

Click here: [Azure Portal - Custom Deployment](https://portal.azure.com/#create/Microsoft.Template)

### Step 2: Build Custom Template

1. Click **"Build your own template in the editor"**
2. Click **"Load file"** button
3. Navigate to: `C:\Users\SergiPaya\Documents\GitHub\SergiLIFE-life-azure-system\infra\microsoft-partnership-clean.bicep`
4. Click **"Save"**

### Step 3: Configure Deployment

**Basics:**

- **Subscription:** Microsoft Azure Sponsorship
- **Resource Group:**
  - ✅ Use existing: `rg-life-platform-static` (RECOMMENDED - saves costs)
  - OR create new: `rg-life-microsoft-demo`
- **Region:** East US 2

**Parameters:**

- **Environment Name:** `microsoft-demo`
- **Location:** `eastus2`
- **Life Container Image:** `nginx:latest` (will update later with real L.I.F.E. image)
- **Enable High Availability:** `true`

### Step 4: Deploy

1. Click **"Review + create"**
2. Verify configuration
3. Click **"Create"**
4. ⏱️ Wait 10-15 minutes for deployment completion

---

## 📦 What Gets Deployed

### Core Infrastructure (11 Resources)

```
✅ Managed Identity       → Secure credential-free access
✅ Key Vault             → Secrets: EEG-API-KEY, OPENAI-API-KEY
✅ Log Analytics         → Centralized monitoring
✅ Application Insights  → Performance tracking
✅ Container Registry    → Docker image hosting
✅ Storage Account       → Demo data + backups
✅ Container Apps Env    → Serverless hosting environment
✅ Container App         → L.I.F.E. Platform (auto-scaling 1-10)
✅ Function App          → Executive outreach API
✅ Cosmos DB             → Serverless NoSQL (partitioned by userId)
✅ Event Hub Namespace   → Real-time EEG streaming
```

### Resource Naming Convention

All resources use pattern: `life-microsoft-demo-{type}-{unique}`

Example:

- Key Vault: `life-microsoft-demo-kv-abc123`
- Storage: `stmicrosoftdemoabc123`
- Container App: `life-microsoft-demo-app`

---

## 💰 Cost Estimate (Azure Sponsorship Credits)

**Monthly estimate with light usage:**

- Container Apps (idle): ~$5/month
- Functions (consumption): ~$1/month
- Cosmos DB (serverless): ~$3/month
- Storage (50GB): ~$1/month
- Event Hub (basic): ~$10/month
- Other services: ~$5/month

**Total: ~$25/month** (well within sponsorship limits)

---

## ✅ Post-Deployment Checklist

### Immediate (Within 5 Minutes)

- [ ] Navigate to Resource Group in Azure Portal
- [ ] Verify all 11 resources show "Succeeded" status
- [ ] Click on Key Vault → Access Policies → Verify managed identity has access

### Configuration (15-30 Minutes)

- [ ] Add secrets to Key Vault:
  - `EEG-API-KEY`: Your EEG device API key
  - `OPENAI-API-KEY`: Azure OpenAI key
  - `IOT-HUB-CONNECTION-STRING`: From existing IoT Hub
- [ ] Container App → Configuration → Add environment variables
- [ ] Container Registry → Upload L.I.F.E. Platform Docker image
- [ ] Function App → Deployment Center → Connect to GitHub

### Integration (1-2 Hours)

- [ ] Link `lifecoach-121.com` to Container App endpoint
- [ ] Configure GitHub Actions for CI/CD
- [ ] Seed Cosmos DB with demo EEG datasets
- [ ] Test all API endpoints
- [ ] Configure Application Insights alerts

---

## 🔗 Quick Links After Deployment

### Azure Portal Dashboards

```
Resource Group:
https://portal.azure.com/#@e716161a-5e85-4d6d-82f9-96bcdd2e65ac/resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/rg-life-platform-static

Container Apps:
https://portal.azure.com/#view/HubsExtension/BrowseResource/resourceType/Microsoft.App%2FcontainerApps

Application Insights:
https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.Insights%2Fcomponents
```

---

## 🧪 Test Deployment

### Health Check (Container App)

Once deployed, your Container App will be accessible at:

```
https://life-microsoft-demo-app.eastus2.azurecontainerapps.io/api/health
```

### Function App Endpoint

```
https://life-microsoft-demo-func.azurewebsites.net/api/HttpTrigger1
```

### Cosmos DB Query

Use Azure Portal → Cosmos DB → Data Explorer:

```sql
SELECT * FROM c WHERE c.type = 'demo'
```

---

## 🚨 Troubleshooting

### Deployment Fails

**Error:** "Resource quota exceeded"

- **Solution:** Use existing resource group `rg-life-platform-static` to share quotas

**Error:** "Name already exists"

- **Solution:** Change `environmentName` parameter to `microsoft-demo-v2`

**Error:** "Insufficient permissions"

- **Solution:** Verify you're Owner/Contributor on subscription 5c88cef6-f243-497d-98af-6c6086d575ca

### Post-Deployment Issues

**Container App not starting:**

1. Check logs: Container App → Log stream
2. Verify image exists in Container Registry
3. Check environment variables are set

**Key Vault access denied:**

1. Navigate to Key Vault → Access policies
2. Add policy for managed identity
3. Grant permissions: Get secrets, List secrets

---

## 🔄 Update Deployment

If you need to modify infrastructure:

1. Edit `infra/microsoft-partnership-clean.bicep`
2. Re-upload via Azure Portal Custom Deployment
3. Select **existing resource group**
4. Azure will update only changed resources (incremental deployment)

---

## 🗑️ Cleanup (If Needed)

**Remove all resources:**

```
Azure Portal → Resource Groups → rg-life-platform-static → Delete resource group
```

⚠️ **Warning:** This will delete ALL resources including your existing Static Web App!

**Remove only Microsoft demo resources:**
Use Azure Portal to selectively delete resources with `microsoft-demo` in the name.

---

## 📊 Monitoring Dashboard

After deployment, create a custom dashboard:

1. Azure Portal → Dashboard → New dashboard
2. Add tiles:
   - Container App requests/sec
   - Function App invocations
   - Cosmos DB request units
   - Event Hub throughput
   - Application Insights response times

Save as: **"L.I.F.E. Microsoft Partnership Dashboard"**

---

## 🎉 Success Indicators

Your deployment is successful when:

✅ All 11 resources show green "Running" status  
✅ Container App responds to health check  
✅ Function App shows in Functions list  
✅ Cosmos DB data explorer accessible  
✅ Event Hub shows "Active" status  
✅ Application Insights receiving telemetry  
✅ Key Vault contains required secrets  

---

## 📞 Next Actions

**Immediate:**

1. Deploy infrastructure (10-15 minutes)
2. Verify resource creation
3. Add secrets to Key Vault

**Today:**
4. Upload L.I.F.E. Platform container image
5. Configure environment variables
6. Test API endpoints

**This Week:**
7. Connect to `lifecoach-121.com`
8. Setup CI/CD with GitHub Actions
9. Load demo datasets
10. Configure monitoring alerts

---

**Deployment Ready:** All files validated and ready  
**Template:** `infra/microsoft-partnership-clean.bicep` (616 lines)  
**Parameters:** `infra/microsoft-partnership-clean.parameters.json`  
**Status:** ✅ GO FOR LAUNCH
