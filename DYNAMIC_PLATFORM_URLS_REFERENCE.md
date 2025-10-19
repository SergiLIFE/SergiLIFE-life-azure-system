# 🧠 L.I.F.E Platform Dynamic URL Reference - October 18, 2025

<!-- Copilot: Generate a JSON array of all current LIFE Platform URLs:
  - Azure Function App URLs
  - Web App/Dashboard URLs
  - Base API endpoints
Use the naming patterns from our resource group `life-platform-prod`. -->

## 🚀 Current Production URLs (Live)

```javascript
// Copilot, please list all current deployment URLs for the LIFE Platform:
// - Function App endpoints
// - Dashboard URLs  
// - API base URLs
//
// The URLs should reflect the latest naming conventions and timestamps used in our Azure deployments.
//
// Example output:
const LIFE_PLATFORM_URLS = [
  "https://lifeplatform1760781933.azurewebsites.net",                    // Main Function App (needs Python 3.13)
  "https://life-theory-functions-1756511146.azurewebsites.net",          // Legacy Function App (OPERATIONAL)
  "https://life-functions-app.azurewebsites.net",                        // Enhanced Dashboard Function App
  "https://green-ground-0c65efe0f.1.azurestaticapps.net",               // Azure Static Web App (LIVE)
  "https://life-platform-webapp.azurewebsites.net"                       // Web App Platform
];
```

## 📊 URLs by Category (Current Naming Conventions)

### **Function Apps with Timestamps**
- `lifeplatform1760781933` ← **Primary** (needs Python 3.13 upgrade)
- `life-theory-functions-1756511146` ← **Legacy** (OPERATIONAL)
- `life-functions-app` ← **Dashboard** (ACTIVE)

### **Static Web Apps**  
- `green-ground-0c65efe0f.1.azurestaticapps.net` ← **Current Live Deployment**
- `life-platform-webapp.azurestaticapps.net` ← **Alternative Static App**

### **API Endpoints (Latest)**
```
✅ https://life-theory-functions-1756511146.azurewebsites.net (Working)
✅ https://life-functions-app.azurewebsites.net/api/dashboard (Working)
✅ https://green-ground-0c65efe0f.1.azurestaticapps.net (Working)
❌ https://lifeplatform1760781933.azurewebsites.net/api/* (404 - Python 3.13 needed)
```

## 🔧 Dynamic Access Methods

### **JavaScript/Node.js:**
```javascript
const { getAllCurrentLIFEPlatformURLs } = require('./COMPLETE_PLATFORM_URLS_INVENTORY.js');
const urls = getAllCurrentLIFEPlatformURLs();
console.log('All URLs:', urls);
```

### **Browser Console:**
```javascript
// Load the inventory file then:
const productionUrls = getProductionURLsOnly();
const categories = getURLsByCategory();
const status = getCurrentPlatformStatus();
```

## 📈 Current Status (October 18, 2025)

```json
{
  "totalDeployments": 21,
  "productionUrls": 16,
  "workingUrls": 15,
  "criticalIssue": "lifeplatform1760781933 needs Python 3.13 upgrade",
  "nextAction": "Deploy Python 3.13 fix to restore API endpoints"
}
```

---

**File:** `COMPLETE_PLATFORM_URLS_INVENTORY.js`  
**Dynamic Functions:** `getAllCurrentLIFEPlatformURLs()`, `getProductionURLsOnly()`, `getURLsByCategory()`  
**Last Updated:** October 18, 2025 - Real-time dynamic inventory