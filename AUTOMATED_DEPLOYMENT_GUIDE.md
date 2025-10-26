# L.I.F.E Platform - Automated Deployment Guide
**Complete Automation for Phase 2 & 3**

---

## 📋 Overview

This guide covers the automated deployment validation and production launch process for the L.I.F.E Platform.

---

## ✅ Phase 2: Deployment Validation (Automated)

### Quick Start

**Option 1: Using Batch File (Recommended)**
```cmd
VALIDATE_DEPLOYMENT.bat
```

**Option 2: Using Python Script Directly**
```cmd
python validate_deployment.py --environment staging
```

### What It Does

The validation script automatically:

1. ✅ **Resource Group Check** - Verifies `life-platform-rg` exists
2. ✅ **Storage Account** - Validates `stlifeplatformprod` is active
3. ✅ **Key Vault** - Confirms `kv-life-platform-prod` is accessible
4. ✅ **Service Bus** - Checks `sb-life-platform-prod` status
5. ✅ **Function App** - Verifies `life-functions-app` is running
6. ✅ **Resource Listing** - Lists all deployed resources

### Output Files

- **Log File**: `deployment_validation_YYYYMMDD_HHMMSS.log`
- **JSON Report**: `deployment_validation_report_YYYYMMDD_HHMMSS.json`

### Validation Report Format

```json
{
  "timestamp": "2025-10-19T14:30:00",
  "environment": "staging",
  "tests": [
    {
      "name": "Resource Group Validation",
      "status": "PASS",
      "details": {...}
    },
    ...
  ]
}
```

### Success Criteria

All tests must pass (100% success rate) before proceeding to production.

---

## 🚀 Phase 3: Production Launch (Automated)

### Prerequisites

Before running production deployment:

- [ ] Phase 1 infrastructure deployed (✅ Already done!)
- [ ] Phase 2 validation passed
- [ ] 24 hours of monitoring completed
- [ ] No critical issues identified
- [ ] Backup plan ready

### Quick Start

**Option 1: Using Batch File (Recommended)**
```cmd
DEPLOY_TO_PRODUCTION.bat
```

**Option 2: Using Python Script with Confirmation**
```cmd
python deploy_to_production.py
```

**Option 3: Skip Confirmation (Advanced)**
```cmd
python deploy_to_production.py --skip-confirmation
```

### What It Does

The production deployment script automatically:

1. ✅ **Health Check** - Verifies staging environment is healthy
2. ✅ **Backup** - Creates production backup tag
3. ✅ **Slot Swap** - Swaps staging to production (if slots configured)
4. ✅ **Verification** - Validates production deployment
5. ✅ **Monitoring** - Sets up 24h post-deployment monitoring

### Safety Features

- **10-Second Confirmation**: Gives you time to cancel
- **Health Checks**: Won't deploy if staging is unhealthy
- **Backup Tags**: Creates recovery point
- **Rollback Ready**: Easy to revert if issues occur

### Output Files

- **Log File**: `production_deployment_YYYYMMDD_HHMMSS.log`
- **JSON Report**: `production_deployment_report_YYYYMMDD_HHMMSS.json`

---

## 🔄 Complete Automation Workflow

### End-to-End Automated Process

```cmd
REM Step 1: Deploy infrastructure (already done!)
SIMPLE_DEPLOY.bat

REM Step 2: Wait a few minutes for resources to initialize
timeout /t 180

REM Step 3: Validate deployment
python validate_deployment.py --environment staging

REM Step 4: Monitor for 24 hours (manual)
REM - Check Application Insights
REM - Review error rates
REM - Validate EEG processing

REM Step 5: Deploy to production
python deploy_to_production.py
```

### One-Command Validation + Production (Advanced)

```cmd
python validate_deployment.py --environment staging && python deploy_to_production.py --skip-confirmation
```

⚠️ **Warning**: This skips safety checks. Only use if you're 100% confident!

---

## 📊 Monitoring During 24h Period

### Automated Monitoring Checks

The scripts set up automated monitoring for:

- **Function App Failures** > 5%
- **Response Time** > 5000ms
- **Availability** < 99%

### Manual Monitoring Commands

```cmd
REM View Function App status
az functionapp show --name life-functions-app --resource-group life-platform-rg --query "{state:state,health:healthCheckPath}" --output table

REM Check Application Insights metrics
az monitor app-insights metrics show --app life-functions-app --resource-group life-platform-rg --metric "requests/count" --aggregation count --interval PT1H

REM View recent logs
az functionapp log tail --name life-functions-app --resource-group life-platform-rg

REM Get error rate
az monitor metrics list --resource /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-rg/providers/Microsoft.Web/sites/life-functions-app --metric "Http5xx" --aggregation count
```

---

## 🔧 Advanced Options

### Custom Validation

```python
# Run validation programmatically
from validate_deployment import DeploymentValidator
import asyncio

async def custom_validation():
    validator = DeploymentValidator(environment="staging")
    success = await validator.run_validation()
    return success

# Run it
success = asyncio.run(custom_validation())
```

### Custom Production Deployment

```python
# Run production deployment programmatically
from deploy_to_production import ProductionDeployer
import asyncio

async def custom_deployment():
    deployer = ProductionDeployer()
    success = await deployer.run_deployment()
    return success

# Run it
success = asyncio.run(custom_deployment())
```

---

## 🆘 Troubleshooting

### Validation Fails

If validation fails:

1. Check the log file for detailed errors
2. Review the JSON report
3. Verify Azure CLI is authenticated: `az account show`
4. Check resource status in Azure Portal
5. Re-run SIMPLE_DEPLOY.bat if resources are missing

### Production Deployment Fails

If production deployment fails:

1. Check the deployment log file
2. Verify staging environment is healthy
3. Check for permission issues
4. Review Application Insights for errors
5. Consider manual rollback if needed

### Rollback Procedure

```cmd
REM If you need to rollback production
az webapp deployment slot swap --resource-group life-platform-rg --name life-platform-webapp --slot production --target-slot staging

REM Or restart Function App
az functionapp restart --name life-functions-app --resource-group life-platform-rg
```

---

## 📈 Success Metrics

### Phase 2 Validation

- ✅ 100% test pass rate
- ✅ All resources in "Succeeded" state
- ✅ Function App responding
- ✅ No critical errors in logs

### Phase 3 Production

- ✅ Slot swap successful
- ✅ All resources healthy
- ✅ < 5% error rate
- ✅ < 5000ms response time
- ✅ > 99% availability

---

## 🎯 Next Steps After Production

1. **Monitor for 24 hours**
   - Application Insights
   - Error rates
   - Performance metrics

2. **Verify functionality**
   - EEG processing
   - Venturi gates latency
   - User authentication

3. **Optimize if needed**
   - Scale resources
   - Adjust configurations
   - Fine-tune monitoring

4. **Document lessons learned**
   - Update runbooks
   - Improve automation
   - Share with team

---

## 📞 Support

**Azure Subscription**: 5c88cef6-f243-497d-98af-6c6086d575ca  
**Resource Group**: life-platform-rg  
**Region**: East US 2

**Azure Portal**:
https://portal.azure.com/#resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-rg/overview

**GitHub**: https://github.com/SergiLIFE/SergiLIFE-life-azure-system

---

**Created**: October 19, 2025  
**Status**: Ready for automated deployment  
**Target**: Production-ready by September 27, 2025
