// get_urls.js

/**
 * Copilot: Please output a JSON array of all current LIFE Platform URLs.
 * Include:
 *  - Azure Function App endpoints (production and staging)
 *  - Web App / Dashboard URLs
 *  - Base API endpoints
 * Use the actual names from the `life-platform-prod` resource group.
 */

const CURRENT_LIFE_PLATFORM_URLS = [
    // 🚀 Azure Function Apps (Production - October 18, 2025 Deployments)
    "https://lifeplatform1760781933.azurewebsites.net",                    // Main Function App (Recently deployed, needs Python 3.13)
    "https://life-theory-functions-1756511146.azurewebsites.net",          // Legacy Function App (OPERATIONAL)
    "https://life-functions-app.azurewebsites.net",                        // Enhanced Dashboard Function App

    // 🌐 Web Apps & Static Deployments
    "https://green-ground-0c65efe0f.1.azurestaticapps.net",               // Current Azure Static Web App (LIVE)
    "https://life-platform-webapp.azurewebsites.net",                      // Main Web App Platform
    "https://life-platform-webapp.azurestaticapps.net",                    // Alternative Static Web App

    // 🎯 API Endpoints - Main Function App (lifeplatform1760781933)
    "https://lifeplatform1760781933.azurewebsites.net/api/validate-ingestion",
    "https://lifeplatform1760781933.azurewebsites.net/api/ingestion-stats",
    "https://lifeplatform1760781933.azurewebsites.net/api/ingest-external-eeg",

    // 🎯 API Endpoints - Dashboard Function App (life-functions-app)
    "https://life-functions-app.azurewebsites.net/api/dashboard/metrics",
    "https://life-functions-app.azurewebsites.net/api/dashboard/neural",
    "https://life-functions-app.azurewebsites.net/api/dashboard/health",
    "https://life-functions-app.azurewebsites.net/api/dashboard/eeg",
    "https://life-functions-app.azurewebsites.net/api/dashboard/venturi",
    "https://life-functions-app.azurewebsites.net/api/eeg_processor",
    "https://life-functions-app.azurewebsites.net/api/learning_api",
    "https://life-functions-app.azurewebsites.net/api/analytics_monitor",
    "https://life-functions-app.azurewebsites.net/api/campaign_automation",

    // 🔧 Development & Testing URLs
    "http://localhost:7071",                                               // Azure Functions Core Tools
    "http://localhost:8080",                                               // L.I.F.E Platform Server
    "http://localhost:8081",                                               // Enhanced Dashboard Server
    "http://localhost:8082",                                               // EEG Processing Server
    "http://localhost:5000",                                               // Flask Development Server

    // 🏢 Demo & Microsoft Partnership URLs
    "https://life-microsoft-demo-app.azurewebsites.net",                   // Microsoft Partnership Demo
    "https://life-clinical-demo.azurewebsites.net",                        // Clinical Scenario Demo
    "https://life-education-demo.azurewebsites.net"                        // Educational Demo
];

// 🏗️ Infrastructure Endpoints (from resource group: life-platform-prod)
const INFRASTRUCTURE_URLS = [
    "https://stlifeplatform1760781772.blob.core.windows.net",             // Storage Account (Timestamped)
    "https://kvlifeplatform17607819.vault.azure.net",                     // Key Vault (From deployment logs)
    "https://sb-life-platform-1760781772.servicebus.windows.net"          // Service Bus (From deployment logs)
];

// 📊 Current Deployment Status (October 18, 2025)
const DEPLOYMENT_STATUS = {
    timestamp: "October 18, 2025 10:08:43 UTC",
    primaryFunctionApp: {
        name: "lifeplatform1760781933",
        status: "Running",
        deployed: true,
        pythonVersion: "Needs 3.13 upgrade",
        deploymentId: "d6b3b6cf-504e-41c1-877b-5feb36fc2f2f"
    },
    keyVault: {
        name: "kvlifeplatform17607819",
        vaultUri: "https://kvlifeplatform17607819.vault.azure.net/"
    },
    resourceGroup: "life-platform-prod",
    subscription: "5c88cef6-f243-497d-98af-6c6086d575ca"
};

// Combine all URLs for complete output
const ALL_CURRENT_URLS = [
    ...CURRENT_LIFE_PLATFORM_URLS,
    ...INFRASTRUCTURE_URLS
];

console.log("🧠 L.I.F.E Platform - All Current URLs (October 18, 2025)");
console.log("=" * 60);
console.log(JSON.stringify(ALL_CURRENT_URLS, null, 2));

console.log("\n📊 Deployment Status:");
console.log(JSON.stringify(DEPLOYMENT_STATUS, null, 2));

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        CURRENT_LIFE_PLATFORM_URLS,
        INFRASTRUCTURE_URLS,
        DEPLOYMENT_STATUS,
        ALL_CURRENT_URLS
    };
}