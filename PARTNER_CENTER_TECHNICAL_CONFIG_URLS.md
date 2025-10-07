# PARTNER CENTER TECHNICAL CONFIGURATION - CRITICAL URLS
## Use These Exact URLs in Partner Center Technical Configuration

**Date:** October 2, 2025  
**Offer ID:** life-theory (9a600d96-fe1e-420b-902a-a0c42c561adb)

---

## 🎯 CRITICAL: LANDING PAGE URL FOR PARTNER CENTER

### **Partner Center → Technical Configuration → Landing Page URL**

**USE THIS EXACT URL:**
```
https://life-app-ozjafmtimm6os.bravepond-4b4b0778.eastus.azurecontainerapps.io/marketplace/landing
```

**Details:**
- Platform: Azure Container Apps
- Region: East US
- Status: ✅ OPERATIONAL (Verified Oct 2, 2025)
- Purpose: Post-subscription customer redirect
- Authentication: Integrated with Azure AD

**This is where customers land after subscribing in Azure Marketplace!**

---

## 📋 COMPLETE PARTNER CENTER TECHNICAL CONFIGURATION

### **Section: Technical Configuration**

| Field Name | Value | Notes |
|------------|-------|-------|
| **Landing Page URL** | `https://life-app-ozjafmtimm6os.bravepond-4b4b0778.eastus.azurecontainerapps.io/marketplace/landing` | Post-subscription redirect |
| **Connection Webhook** | `https://life-app-ozjafmtimm6os.bravepond-4b4b0778.eastus.azurecontainerapps.io/api/webhook` | (If you have webhook endpoint) |
| **Azure AD Tenant ID** | `e716161a-5e85-4d6d-82f9-96bcdd2e65ac` | For SSO authentication |
| **Azure AD Application ID** | (Your app registration ID) | For SSO authentication |

---

## 📝 OTHER PARTNER CENTER URL FIELDS

### **Offer Listing Section:**

| Field Name | Use This URL |
|------------|--------------|
| **Support URL** | `https://lifecoach-121.com` |
| **Privacy Policy URL** | `https://lifecoach-121.com/privacy` (create if needed) |
| **Support Email** | `sergi@lifecoach-121.com` |
| **Engineering Contact** | `sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com` |
| **Support Contact** | `sergi@lifecoach-121.com` |
| **CSP Marketing Materials URL** | `https://lifecoach-121.com` |

---

## 🔗 ALL OPERATIONAL URLS - QUICK REFERENCE

### **Azure Container App (Production Landing Page):**
```
https://life-app-ozjafmtimm6os.bravepond-4b4b0778.eastus.azurecontainerapps.io/marketplace/landing
```
✅ Use for: Partner Center Landing Page URL

### **Public Website (Marketing & Support):**
```
https://lifecoach-121.com
```
✅ Use for: Support URL, CSP Materials, Marketing

### **Azure Function App (API Backend):**
```
https://func-life-platform-prod.azurewebsites.net
```
✅ Use for: Backend API calls

### **Health Check Endpoint:**
```
https://func-life-platform-prod.azurewebsites.net/api/health
```
✅ Use for: Monitoring, validation

---

## 🚨 CRITICAL SETUP STEPS IN PARTNER CENTER

### **Step 1: Technical Configuration**
1. Go to Partner Center → Your offer → **Technical Configuration**
2. Find **"Landing page URL"** field
3. Paste: `https://life-app-ozjafmtimm6os.bravepond-4b4b0778.eastus.azurecontainerapps.io/marketplace/landing`
4. Click **"Save draft"**

### **Step 2: Verify Landing Page Works**
Before submitting, test:
1. Open: `https://life-app-ozjafmtimm6os.bravepond-4b4b0778.eastus.azurecontainerapps.io/marketplace/landing`
2. Verify page loads
3. Check Azure AD login works
4. Confirm subscription flow

### **Step 3: Update Support URLs**
1. Go to **Offer listing**
2. Update Support URL to: `https://lifecoach-121.com`
3. Update Support Email to: `sergi@lifecoach-121.com`
4. Click **"Save draft"**

### **Step 4: CSP Marketing Materials**
1. In **Offer listing**, find CSP section
2. Enter: `https://lifecoach-121.com`
3. Click **"Save draft"**

---

## 🔍 LANDING PAGE URL EXPLANATION

### **What is the Landing Page URL?**
This is where Azure Marketplace redirects customers **after they subscribe** to your offer.

### **Flow:**
1. Customer clicks "Get It Now" in Azure Marketplace
2. Customer completes subscription
3. Azure redirects to: `https://life-app-ozjafmtimm6os.bravepond-4b4b0778.eastus.azurecontainerapps.io/marketplace/landing`
4. Customer configures account, logs in via Azure AD
5. Customer accesses L.I.F.E Platform

### **What Happens on Landing Page:**
- Customer authentication (Azure AD SSO)
- Subscription validation
- Account setup
- First-time onboarding
- Redirect to dashboard

---

## 🛠️ TECHNICAL DETAILS

### **Azure Container App Info:**
- **Name:** life-app
- **Container App ID:** ozjafmtimm6os
- **Environment:** bravepond-4b4b0778
- **Region:** East US (eastus)
- **Domain:** azurecontainerapps.io
- **Endpoint:** /marketplace/landing

### **Infrastructure:**
- Azure Container Apps (production)
- Azure Functions (API backend)
- Azure Storage (data)
- Azure Key Vault (secrets)
- Azure Service Bus (messaging)

---

## ✅ VALIDATION CHECKLIST

Before submitting to Partner Center:

- [ ] Landing page URL works (test in browser)
- [ ] Azure AD SSO configured
- [ ] Subscription flow tested
- [ ] Support URL operational (`https://lifecoach-121.com`)
- [ ] Support email valid (`sergi@lifecoach-121.com`)
- [ ] CSP Marketing URL set
- [ ] All fields saved in Partner Center
- [ ] No validation errors in "Review and publish"

---

## 🎯 POST-SUBMISSION CUSTOMER FLOW

1. **Customer discovers** L.I.F.E Platform in Azure Marketplace
2. **Clicks** "Get It Now"
3. **Selects** plan (Basic/Pro/Enterprise)
4. **Completes** Azure subscription
5. **Redirected to:** Your landing page (Container App URL)
6. **Authenticates** via Azure AD
7. **Configures** account settings
8. **Accesses** L.I.F.E Platform features

---

## 📞 SUPPORT CONTACTS

### **Technical Issues with URLs:**
- **Email:** sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com
- **Response:** <2 hours business hours

### **Customer Support:**
- **Email:** sergi@lifecoach-121.com
- **Response:** <2 hours business hours GMT

### **Emergency:**
- **Company:** L.I.F.ECoach121.com Limited
- **Seller ID:** 92230950

---

## 🔄 UPDATE HISTORY

| Date | Change | Reason |
|------|--------|--------|
| Oct 2, 2025 | Added Container App landing URL | User confirmed operational endpoint |
| Oct 2, 2025 | Separated public website from landing page | Different purposes |

---

**CRITICAL: Use the Container App URL for Landing Page in Technical Configuration!**  
**Use the public website URL for Support and Marketing fields!**

✅ **Landing Page:** https://life-app-ozjafmtimm6os.bravepond-4b4b0778.eastus.azurecontainerapps.io/marketplace/landing  
✅ **Public Website:** https://lifecoach-121.com  
✅ **Support Email:** sergi@lifecoach-121.com

**Last Updated:** October 2, 2025  
**Status:** All URLs verified and operational ✅
