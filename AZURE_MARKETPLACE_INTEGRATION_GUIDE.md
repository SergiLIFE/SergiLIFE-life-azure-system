# 🔗 Azure Marketplace Integration Guide
## Complete Setup for L.I.F.E. Platform Connection

**Date:** November 5, 2025  
**Status:** Ready for Implementation  
**Marketplace Offer:** lifecoach121comlimited1759055603743.life-theory

---

## 🎯 Quick Overview

Your Azure Marketplace offer is currently **disconnected** from your L.I.F.E. Platform. This guide provides everything needed to establish the connection and enable customers to purchase and immediately access your neuroadaptive learning platform.

## 📋 Phase 1: Partner Center Configuration

### Step 1: Access Partner Center
1. Go to **[Partner Center](https://partner.microsoft.com)**
2. Sign in with your publisher account
3. Navigate to **Commercial Marketplace > Overview**
4. Find your offer: `lifecoach121comlimited1759055603743.life-theory`

### Step 2: Update Offer Setup
```
Offer Setup Tab:
✅ Offer type: SaaS
✅ Landing page URL: https://lifecoach-121.com/marketplace/landing
✅ Connection webhook: https://life-functions-app.azurewebsites.net/api/connection-webhook
✅ Enable metered billing: Yes
✅ Enable per-seat pricing: Yes
```

### Step 3: Technical Configuration
```
Technical Configuration Tab:
✅ SaaS fulfillment APIs: v2
✅ Webhook endpoint: https://life-functions-app.azurewebsites.net/api/marketplace-webhook
✅ Azure AD tenant ID: e716161a-5e85-4d6d-82f9-96bcdd2e65ac
✅ Connection webhook: https://life-functions-app.azurewebsites.net/api/connection-webhook
✅ Enable single sign-on: Yes
```

### Step 4: Pricing and Availability
Copy these exact pricing plans:

**Plan 1: L.I.F.E. Individual**
- Plan ID: `life-individual`
- Price: $99.00 USD/month
- Description: "Personal neuroadaptive learning with EEG integration"

**Plan 2: L.I.F.E. Professional** 
- Plan ID: `life-professional`
- Price: $299.00 USD/month
- Description: "Advanced neural processing for healthcare professionals"

**Plan 3: L.I.F.E. Enterprise**
- Plan ID: `life-enterprise`
- Price: $2,999.00 USD/month
- Description: "Full neuroadaptive platform for institutions"

### Step 5: Offer Listing Update
```
Title: L.I.F.E. Platform - Neuroadaptive Learning Technology
Subtitle: Advanced EEG-based personalized learning with AI-driven neural adaptation
Short Description: Transform learning with neuroadaptive technology that adapts to individual brain patterns in real-time

Keywords: EEG, neuroadaptive, personalized learning, AI, neuroscience, brain-computer interface, educational technology, healthcare

Categories: 
- AI + Machine Learning
- Analytics  
- Developer Tools
- Education

Industries:
- Education
- Healthcare
- Professional Services
- Government
```

---

## 🚀 Phase 2: Azure Infrastructure Deployment

### Deploy Azure Function App
Run these Azure CLI commands:

```bash
# Create resource group (if not exists)
az group create --name rg-life-marketplace --location "East US 2"

# Create Function App
az functionapp create \
  --resource-group rg-life-marketplace \
  --consumption-plan-location "East US 2" \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --name life-marketplace-functions \
  --storage-account stlifeplatformprod

# Configure app settings
az functionapp config appsettings set \
  --name life-marketplace-functions \
  --resource-group rg-life-marketplace \
  --settings \
    "AZURE_TENANT_ID=e716161a-5e85-4d6d-82f9-96bcdd2e65ac" \
    "AZURE_SUBSCRIPTION_ID=5c88cef6-f243-497d-98af-6c6086d575ca" \
    "LIFE_PLATFORM_URL=https://lifecoach-121.com"

# Deploy function code
func azure functionapp publish life-marketplace-functions --python
```

### Test Webhook Endpoints
```bash
# Test marketplace webhook
curl -X POST https://life-marketplace-functions.azurewebsites.net/api/marketplace-webhook \
  -H "Content-Type: application/json" \
  -d '{"subscriptionId":"test123","action":"Subscribe","planId":"life-individual"}'

# Test connection webhook  
curl -X POST https://life-marketplace-functions.azurewebsites.net/api/connection-webhook \
  -H "Content-Type: application/json" \
  -d '{"test":true}'
```

---

## 🌐 Phase 3: Static Web App Update

### Add Marketplace Landing Page Route
Update your Static Web App configuration to include the marketplace landing page:

```json
{
  "routes": [
    {
      "route": "/marketplace/landing",
      "serve": "/marketplace/landing.html"
    },
    {
      "route": "/api/*",
      "allowedRoles": ["authenticated"]
    }
  ]
}
```

### Deploy Updated Content
The marketplace landing page is already created at:
- `docs/marketplace/landing.html` ✅

---

## 🧪 Phase 4: Testing & Validation

### Partner Center Testing Tools
1. In Partner Center, go to **Technical Configuration**
2. Use **Test connection** button to verify webhook
3. Test the **Landing page URL** 
4. Validate **Connection webhook** response

### End-to-End Test Scenario
1. **Simulate Purchase:** Use Partner Center sandbox
2. **Webhook Processing:** Monitor Function App logs
3. **Landing Page:** Verify customer experience
4. **Platform Access:** Test L.I.F.E. dashboard integration

### Monitoring Setup
```bash
# View Function App logs
az functionapp log tail --name life-marketplace-functions --resource-group rg-life-marketplace

# Check webhook health
curl https://life-marketplace-functions.azurewebsites.net/api/health
```

---

## 📊 Phase 5: Go-Live Checklist

### Pre-Launch Validation
- [ ] Partner Center configuration complete
- [ ] Azure Function App deployed and tested
- [ ] Webhook endpoints responding correctly
- [ ] Landing page functional with subscription handling
- [ ] Test purchase flow working end-to-end
- [ ] Monitoring and alerting configured

### Launch Day Tasks
1. **Publish Offer:** Click "Publish" in Partner Center
2. **Monitor Initial Sales:** Watch for first customer activations
3. **Customer Support:** Monitor info@lifecoach121.com for issues
4. **Performance Metrics:** Track webhook success rates

### Post-Launch Optimization
- Monitor customer onboarding metrics
- Optimize landing page conversion rates
- Gather customer feedback for improvements
- Scale Azure resources based on demand

---

## 🆘 Emergency Contacts & Resources

### Support Channels
- **Azure Marketplace Support:** [Partner Center Support](https://partner.microsoft.com/support)
- **Technical Issues:** info@lifecoach121.com
- **Platform Status:** https://lifecoach-121.com/status

### Key URLs for Reference
- **Current Marketplace Offer:** https://marketplace.microsoft.com/en-us/product/SaaS/lifecoach121comlimited1759055603743.life-theory
- **New Landing Page:** https://lifecoach-121.com/marketplace/landing
- **Webhook Endpoint:** https://life-marketplace-functions.azurewebsites.net/api/marketplace-webhook
- **L.I.F.E. Dashboard:** https://lifecoach-121.com/dashboard

### File Locations
- **Partner Center Config:** `.azure/partner_center_config.json`
- **Azure Function Code:** `azure_functions/function_app.py`
- **Landing Page:** `docs/marketplace/landing.html`
- **Integration Plan:** `.azure/marketplace-integration-plan.md`

---

## ✅ Success Criteria

**Integration is successful when:**
1. ✅ Customers can purchase from Azure Marketplace
2. ✅ Purchase immediately triggers webhook to your Function App
3. ✅ Customer is redirected to functional landing page
4. ✅ Customer gets instant access to L.I.F.E. Platform dashboard
5. ✅ Subscription lifecycle (upgrade/downgrade/cancel) works automatically
6. ✅ All webhook events are logged and monitored

**🎯 Target Outcome:** Seamless customer journey from Azure Marketplace purchase to active L.I.F.E. Platform usage within 2 minutes.

---

*This integration connects your $345K Q4 2025 target marketplace offer to your production-ready L.I.F.E. Platform, enabling immediate customer access to neuroadaptive learning technology.*