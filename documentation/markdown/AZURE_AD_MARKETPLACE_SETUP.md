# L.I.F.E Platform - Azure AD Marketplace Setup Guide

**Azure Marketplace Offer ID:** `9a600d96-fe1e-420b-902a-a0c42c561adb`  
**Production Launch:** September 27, 2025  
**System Status:** Operational and Enterprise-Ready

## Azure AD Configuration

### Directory Information
- **Directory Name:** Sergio Paya Borrull (lifecoach-121.com)
- **Tenant Domain:** `sergiomiguelpayaborrullmsn.onmicrosoft.com`
- **Subscription ID:** `5c88cef6-f243-497d-98af-6c6086d575ca`
- **Role:** Account Admin

## App Registration Setup

### Step 1: Access Azure Active Directory
1. **Login to Azure Portal:** https://portal.azure.com
   - Username: `sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com`
2. **Navigate:** Azure Active Directory → App registrations
3. **Search for existing apps:** L.I.F.E Platform, LIFE Coach 121, lifecoach-121

### Step 2: Create App Registration (if needed)
```
Application Name: L.I.F.E Platform - Neuroadaptive Learning System
Account Types: Multitenant + Personal Microsoft accounts
Redirect URI: https://lifecoach-121.com/auth/callback
```

### Step 3: Obtain Application ID
- **Location:** Azure Portal → Azure AD → App registrations → [Your App] → Overview
- **Format:** `12345678-1234-1234-1234-123456789012` (GUID)

## Azure CLI Quick Setup

### Check Current Configuration
```powershell
az account show --query "{subscriptionId:id, tenantId:tenantId, user:user.name}"
```

### List Existing App Registrations
```powershell
az ad app list --display-name "L.I.F.E" --query "[].{displayName:displayName, appId:appId}"
```

### Create New App Registration
```powershell
az ad app create --display-name "L.I.F.E Platform - Neuroadaptive Learning System" \
  --sign-in-audience "AzureADandPersonalMicrosoftAccount" \
  --web-redirect-uris "https://lifecoach-121.com/auth/callback"
```

## Marketplace Integration

### Microsoft Graph Integration
- **Question:** Does your SaaS offer integrate with Microsoft Graph?
- **Answer:** Yes, my SaaS offer integrates with Microsoft Graph
- **App ID:** [Your Application (client) ID from Azure AD]

### Benefits of Graph Integration
1. **Enterprise Credibility:** Professional platform validation
2. **Better Discovery:** Microsoft 365 marketplace visibility
3. **Simplified Deployment:** IT admin deployment through M365 admin center
4. **Premium Pricing Justification:** Enterprise-grade integration validates $50/user pricing

## Action Plan

### Immediate Steps (15 minutes)
1. Open Azure Portal: portal.azure.com
2. Login with Azure credentials
3. Navigate to Azure AD → App registrations
4. Check for existing L.I.F.E Platform app or create new one
5. Copy Application (client) ID
6. Complete marketplace form with Graph integration

### Marketplace Submission
1. Select "Yes" for Microsoft Graph integration
2. Enter Application (client) ID
3. Submit for certification
4. Target: Live on marketplace by Monday

## Enterprise Enhancement Options

### Current Integration
- Microsoft Graph API connectivity
- Enterprise authentication support
- Professional platform certification

### Future Enhancements
- **Teams Integration:** Collaborative learning features
- **Office Add-ins:** Learning analytics integration
- **Directory Sync:** Enterprise user management
- **SSO Integration:** Seamless Microsoft 365 login

## Security & Compliance

### Microsoft Ecosystem Alignment
- **JIT Security:** Just-in-time access implementation
- **Enterprise Authentication:** Microsoft account integration
- **Professional Validation:** Graph integration demonstrates platform maturity
- **Customer Confidence:** Microsoft compatibility assurance

## Support & Resources

### Troubleshooting
- **Portal Access:** portal.azure.com
- **Search:** "App registrations" in Azure Portal
- **Create:** "New registration" if no existing app found
- **Copy ID:** Application (client) ID from app overview

### Timeline
- **Today:** Complete marketplace offer setup
- **Certification:** Microsoft review process
- **Target Launch:** Monday following submission

---

**Next Steps:** Access your Azure AD App registrations now to obtain the Application ID required for marketplace submission.