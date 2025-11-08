# L.I.F.E. Platform Azure Deployment - Ready for Tomorrow

## Current Situation

- ✅ Simplified Bicep template created (`infra/microsoft-partnership-simple.bicep`) - 357 lines, 9 resources
- ✅ All validation errors fixed (reserved words, storage naming, zone redundancy, Functions removed)
- ❌ Azure CLI has persistent "content consumed" bug blocking deployment
- ❌ Local Azure CLI not installed on Windows machine

## Deployment Method for Tomorrow: GitHub Actions (RECOMMENDED)

This completely **bypasses the Azure CLI bug** by using GitHub's infrastructure to deploy.

### Step 1: Create Azure Service Principal (5 minutes)

**In Azure Cloud Shell (PowerShell or Bash):**

```bash
az ad sp create-for-rbac \
  --name "life-github-deploy" \
  --role contributor \
  --scopes /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/rg-life-microsoft-demo \
  --sdk-auth
```

**Copy the entire JSON output** (looks like this):

```json
{
  "clientId": "...",
  "clientSecret": "...",
  "subscriptionId": "5c88cef6-f243-497d-98af-6c6086d575ca",
  "tenantId": "e716161a-5e85-4d6d-82f9-96bcdd2e65ac",
  ...
}
```

### Step 2: Add GitHub Secret (2 minutes)

1. Go to: <https://github.com/SergiPaya/SergiLIFE-life-azure-system/settings/secrets/actions>
2. Click **"New repository secret"**
3. Name: `AZURE_CREDENTIALS`
4. Value: **Paste the entire JSON** from Step 1
5. Click **"Add secret"**

### Step 3: Create GitHub Actions Workflow (Already Done ✅)

File already exists: `.github/workflows/deploy-infrastructure.yml`

### Step 4: Trigger Deployment from GitHub (30 seconds)

**Option A: Via GitHub Web UI (Easiest)**

1. Go to: <https://github.com/SergiPaya/SergiLIFE-life-azure-system/actions>
2. Click **"Deploy L.I.F.E. Infrastructure"** workflow
3. Click **"Run workflow"** dropdown
4. Click **"Run workflow"** button
5. Wait 10-15 minutes for deployment

**Option B: Git Push (Automatic)**

```cmd
git add .
git commit -m "Deploy infrastructure via GitHub Actions"
git push origin main
```

---

## Alternative Method 2: Azure Portal ARM Template (If GitHub Fails)

### Step 1: Convert Bicep to ARM JSON Locally

Since Azure CLI isn't installed, use the **online Bicep Playground**:

1. Go to: <https://aka.ms/bicepdemo>
2. Open `infra/microsoft-partnership-simple.bicep` in VSCode
3. Copy **entire Bicep template** (Ctrl+A, Ctrl+C)
4. Paste into Bicep Playground left panel
5. Copy the **JSON output** from right panel
6. Save to `infra/simple-deploy.json`

### Step 2: Deploy via Azure Portal

1. Go to: <https://portal.azure.com/#create/Microsoft.Template>
2. Click **"Build your own template in the editor"**
3. Delete existing content
4. Paste the **JSON from Step 1**
5. Click **"Save"**
6. Fill parameters:
   - Subscription: `Microsoft Azure Sponsorship`
   - Resource Group: `rg-life-microsoft-demo`
   - Region: `East US 2`
   - Environment Name: `msftpartnership`
   - Life Container Image: `nginx:latest`
7. Click **"Review + create"**
8. Click **"Create"**
9. Wait 8-12 minutes

---

## Alternative Method 3: Install Azure CLI Locally (Long-term Fix)

### Windows Installation (5 minutes)

**Option A: Windows Package Manager (Recommended)**

```cmd
winget install -e --id Microsoft.AzureCLI
```

**Option B: MSI Installer**
Download: <https://aka.ms/installazurecliwindows>

### After Installation

```cmd
az login --tenant e716161a-5e85-4d6d-82f9-96bcdd2e65ac
az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca
az deployment group create --resource-group rg-life-microsoft-demo --template-file infra\microsoft-partnership-simple.bicep --parameters environmentName=msftpartnership location=eastus2 lifeContainerImage=nginx:latest
```

---

## Expected Deployment Results

After successful deployment, you will have **9 Azure resources**:

1. **Managed Identity**: `lifemsftpartnership-identity`
2. **Key Vault**: `lifemsftpartnership-kv-{uniqueId}`
3. **Log Analytics**: `lifemsftpartnership-logs-{uniqueId}`
4. **Application Insights**: `lifemsftpartnership-ai-{uniqueId}`
5. **Container Registry**: `lifemsftpartnershipacr{uniqueId}`
6. **Storage Account**: `lifemsftpartnershipst{uniqueId}`
7. **Container Apps Environment**: `lifemsftpartnership-env-{uniqueId}`
8. **Container App**: `lifemsftpartnership-app`
9. **Cosmos DB**: `lifemsftpartnership-cosmos-{uniqueId}`
10. **Event Hub Namespace**: `lifemsftpartnership-events-{uniqueId}`
11. **Event Hub**: `eeg-data`

### Deployment Outputs

- `containerAppUrl`: `https://{generated-fqdn}` (L.I.F.E. Platform URL)
- `containerRegistryName`: For pushing Docker images
- `cosmosDbEndpoint`: Database connection endpoint
- `storageAccountName`: Blob storage for data

---

## Next Steps After Deployment

### 1. Verify Resources (5 minutes)

```bash
az resource list --resource-group rg-life-microsoft-demo --output table
```

### 2. Deploy L.I.F.E. Platform Code (15 minutes)

**Via Cloud Shell:**

```bash
# Upload repository files to Cloud Shell first
cd ~
# Then run:
ACR_NAME=$(az acr list --resource-group rg-life-microsoft-demo --query "[0].name" -o tsv)
az acr build --registry $ACR_NAME --image life-platform:v1 --file Dockerfile .
az containerapp update --name lifemsftpartnership-app --resource-group rg-life-microsoft-demo --image $ACR_NAME.azurecr.io/life-platform:v1
```

### 3. Test Endpoints (2 minutes)

```bash
APP_URL=$(az containerapp show --name lifemsftpartnership-app --resource-group rg-life-microsoft-demo --query properties.configuration.ingress.fqdn -o tsv)
curl https://$APP_URL/health
```

---

## Files Ready for Tomorrow

✅ `infra/microsoft-partnership-simple.bicep` - Deployment template (357 lines)
✅ `.github/workflows/deploy-infrastructure.yml` - GitHub Actions workflow
✅ `Dockerfile` - Container image definition
✅ `CODE_DEPLOYMENT_GUIDE.md` - Code deployment instructions

---

## Recommendation

**Use GitHub Actions (Method 1)** - It's the most reliable method that completely avoids the Azure CLI bug and provides full deployment logs.

Total time: ~15-20 minutes from start to deployed infrastructure.
