# 🚀 Deploy Microsoft Partnership Infrastructure - Azure Portal Method

## Quick Deployment Links

### Option 1: Azure Portal Custom Deployment (RECOMMENDED)

1. **Open Azure Portal Custom Deployment:**

   ```
   https://portal.azure.com/#create/Microsoft.Template
   ```

2. **Select "Build your own template in the editor"**

3. **Load the Bicep template:**
   - Click "Load file"
   - Select: `infra/microsoft-partnership-clean.bicep`
   - OR copy/paste the entire contents

4. **Configure Parameters:**
   - **Subscription:** `Microsoft Azure Sponsorship` (5c88cef6-f243-497d-98af-6c6086d575ca)
   - **Resource Group:** Create new `rg-life-microsoft-demo` OR use existing `rg-life-platform-static`
   - **Region:** `East US 2`
   - **Environment Name:** `microsoft-demo`
   - **Enable High Availability:** `true`

5. **Review + Create** → **Create**

---

## Option 2: Azure Cloud Shell Deployment

1. **Open Azure Cloud Shell:**

   ```
   https://shell.azure.com
   ```

2. **Upload files:**
   - Upload `infra/microsoft-partnership-clean.bicep`
   - Upload `infra/microsoft-partnership-clean.parameters.json`

3. **Run deployment:**

   ```bash
   # Set subscription
   az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca
   
   # Create resource group (if needed)
   az group create --name rg-life-microsoft-demo --location eastus2
   
   # Deploy infrastructure
   az deployment group create \
       --resource-group rg-life-microsoft-demo \
       --template-file microsoft-partnership-clean.bicep \
       --parameters @microsoft-partnership-clean.parameters.json
   ```

---

## Option 3: GitHub Actions Deployment (Automated)

Create `.github/workflows/deploy-microsoft-partnership.yml`:

```yaml
name: Deploy Microsoft Partnership Infrastructure

on:
  workflow_dispatch:
  push:
    paths:
      - 'infra/microsoft-partnership-clean.bicep'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Deploy Bicep
        uses: azure/arm-deploy@v1
        with:
          subscriptionId: 5c88cef6-f243-497d-98af-6c6086d575ca
          resourceGroupName: rg-life-microsoft-demo
          template: ./infra/microsoft-partnership-clean.bicep
          parameters: ./infra/microsoft-partnership-clean.parameters.json
```

---

## Resources That Will Be Created

| Resource Type | Name Pattern | Purpose |
|---------------|--------------|---------|
| **Managed Identity** | life-microsoft-demo-identity | Secure credential-free access |
| **Key Vault** | life-microsoft-demo-kv-{unique} | Secrets management |
| **Log Analytics** | life-microsoft-demo-logs | Monitoring workspace |
| **App Insights** | life-microsoft-demo-ai | Performance monitoring |
| **Container Registry** | acrmicrosoftdemo{unique} | Docker images |
| **Storage Account** | stmicrosoftdemo{unique} | Demo data storage |
| **Container Apps Env** | life-microsoft-demo-env | Hosting environment |
| **Container App** | life-microsoft-demo-app | L.I.F.E. Platform |
| **Function App** | life-microsoft-demo-func | Executive API |
| **Cosmos DB** | cosmos-microsoft-demo | NoSQL database |
| **Event Hub** | eh-microsoft-demo | EEG streaming |

---

## Estimated Costs (Azure Sponsorship)

- **Container Apps (Consumption):** ~$0.02/hour when idle
- **Functions (Consumption):** Pay-per-execution, minimal when inactive
- **Cosmos DB (Serverless):** Pay-per-request, ~$0.25/million requests
- **Storage:** ~$0.02/GB/month
- **Key Vault:** ~$0.03/10K operations

**Total Estimated Monthly Cost (Light Usage):** $15-30/month from sponsorship credits

---

## Post-Deployment Configuration

### 1. Configure Managed Identity Permissions

```bash
# Grant identity access to resources
az role assignment create \
    --assignee $(az identity show --resource-group rg-life-microsoft-demo --name life-microsoft-demo-identity --query principalId -o tsv) \
    --role "Contributor" \
    --scope /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/rg-life-microsoft-demo
```

### 2. Add Secrets to Key Vault

- Navigate to Key Vault in Azure Portal
- Add secrets:
  - `EEG-API-KEY`
  - `OPENAI-API-KEY`
  - `IOT-HUB-CONNECTION-STRING`

### 3. Configure Container App

- Update environment variables
- Deploy L.I.F.E. Platform container image
- Configure ingress for external access

### 4. Test Endpoints

```bash
# Health check
curl https://life-microsoft-demo-app.{region}.azurecontainerapps.io/api/health

# Demo endpoint
curl https://life-microsoft-demo-app.{region}.azurecontainerapps.io/api/demo
```

---

## Validation Checklist

- [ ] All resources deployed successfully
- [ ] Managed identity has required permissions
- [ ] Key Vault secrets configured
- [ ] Container App is running
- [ ] Function App endpoints responding
- [ ] Cosmos DB accessible
- [ ] Event Hub receiving test data
- [ ] Monitoring dashboards active

---

## Rollback Plan

If deployment fails or issues occur:

```bash
# Delete entire resource group (clean slate)
az group delete --name rg-life-microsoft-demo --yes --no-wait

# Or delete specific deployment
az deployment group delete \
    --resource-group rg-life-microsoft-demo \
    --name microsoft-partnership-clean
```

---

## Next Steps After Deployment

1. **Connect Static Web App:** Link `lifecoach-121.com` to Container Apps backend
2. **Configure GitHub Actions:** Automate container deployments
3. **Setup Monitoring Alerts:** Configure Application Insights alerts
4. **Demo Data Seeding:** Load sample EEG datasets into Cosmos DB
5. **Executive Dashboard:** Deploy Power BI dashboard for real-time metrics

---

## Support & Troubleshooting

**Deployment Issues:**

- Check Activity Log in Azure Portal
- Review deployment operations for errors
- Verify subscription limits haven't been reached

**Access Issues:**

- Confirm managed identity role assignments
- Check Key Vault access policies
- Verify network security rules

**Performance Issues:**

- Check Application Insights for bottlenecks
- Review Container Apps scaling configuration
- Monitor Cosmos DB request units (RU/s)

---

## 📞 Contact

**Deployment Status:** Ready for immediate deployment  
**Documentation:** `.azure/microsoft-demo-deployment-status.md`  
**Infrastructure Code:** `infra/microsoft-partnership-clean.bicep`  
**Parameters:** `infra/microsoft-partnership-clean.parameters.json`
