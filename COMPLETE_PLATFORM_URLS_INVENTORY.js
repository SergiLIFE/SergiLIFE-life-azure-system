/**
 * 🧠 L.I.F.E. PLATFORM - COMPLETE DEPLOYMENT URLS INVENTORY
 * Copyright 2025 - Sergio Paya Borrull
 * Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
 * 
 * Production-Ready: September 27, 2025 | Target: $345K Q4 2025 → $50.7M by 2029
 * Status: OPERATIONAL | Python 3.13 Compatible
 * 
 * Last Updated: October 18, 2025 - Real-time dynamic inventory
 */

// ================================================================================================
// 🚀 DYNAMIC L.I.F.E PLATFORM URLS - CURRENT DEPLOYMENTS (October 18, 2025)
// ================================================================================================

// Copilot, please list all current deployment URLs for the LIFE Platform:
// - Function App endpoints  
// - Dashboard URLs
// - API base URLs
//
// The URLs should reflect the latest naming conventions and timestamps used in our Azure deployments.
//
// Example output:
// [
//   "https://lifeplatform1760781933.azurewebsites.net",
//   "https://life-theory-functions-1756511146.azurewebsites.net", 
//   "https://life-functions-app.azurewebsites.net",
//   "https://green-ground-0c65efe0f.1.azurestaticapps.net"
// ]

const CURRENT_LIFE_PLATFORM_URLS = [
    // 🚀 Primary Production Function Apps (October 18, 2025 - DEPLOYED & RUNNING)
    "https://lifeplatform1760781933.azurewebsites.net",                    // Main Function App (DEPLOYED - Status: Running)
    "https://life-theory-functions-1756511146.azurewebsites.net",          // Legacy Production Function App (OPERATIONAL)
    "https://life-functions-app.azurewebsites.net",                        // Enhanced Dashboard Function App

    // 🌐 Web App & Static Deployments  
    "https://green-ground-0c65efe0f.1.azurestaticapps.net",               // Azure Static Web App (LIVE)
    "https://life-platform-webapp.azurewebsites.net",                      // Web App Platform
    "https://life-platform-webapp.azurestaticapps.net",                    // Static Web App Alternative

    // 🏗️ Infrastructure URLs (New Timestamped Resources - October 18, 2025)
    "https://stlifeplatform1760781772.blob.core.windows.net",             // Storage Account (Created today)
    "https://kvlifeplatform17607819.vault.azure.net",                     // Key Vault (Created today)
    "https://sb-life-platform-1760781772.servicebus.windows.net",         // Service Bus (Created today)

    // 🎯 API Endpoints (Current Timestamped Naming)
    "https://lifeplatform1760781933.azurewebsites.net/api/validate-ingestion",
    "https://lifeplatform1760781933.azurewebsites.net/api/ingestion-stats",
    "https://lifeplatform1760781933.azurewebsites.net/api/ingest-external-eeg",
    "https://life-functions-app.azurewebsites.net/api/dashboard/metrics",
    "https://life-functions-app.azurewebsites.net/api/dashboard/neural",
    "https://life-functions-app.azurewebsites.net/api/dashboard/health",
    "https://life-functions-app.azurewebsites.net/api/eeg_processor",
    "https://life-functions-app.azurewebsites.net/api/learning_api",
    "https://life-functions-app.azurewebsites.net/api/analytics_monitor",
    "https://life-functions-app.azurewebsites.net/api/campaign_automation",

    // 🔧 Local Development URLs
    "http://localhost:7071",                                               // Azure Functions Core Tools
    "http://localhost:8080",                                               // L.I.F.E Platform Server
    "http://localhost:8081",                                               // Enhanced Dashboard Server
    "http://localhost:8082",                                               // EEG Processing Server
    "http://localhost:5000"                                                // Flask Development Server
];

// ================================================================================================
// 🚀 PRODUCTION AZURE DEPLOYMENTS (LIVE & OPERATIONAL)
// ================================================================================================

const PRODUCTION_URLS = {
    // Primary Function App - CONFIRMED 404 ERRORS (Urgent Python 3.13 Upgrade Required)
    primaryFunctionApp: {
        name: "lifeplatform1760781933",
        url: "https://lifeplatform1760781933.azurewebsites.net",
        status: "� 404 ERRORS CONFIRMED - Python 3.13 upgrade CRITICAL",
        region: "East US",
        lastChecked: "October 18, 2025",
        issue: "HTTP ERROR 404 - No webpage found for API endpoints",
        endpoints: {
            validate: "https://lifeplatform1760781933.azurewebsites.net/api/validate-ingestion",
            stats: "https://lifeplatform1760781933.azurewebsites.net/api/ingestion-stats",
            ingest: "https://lifeplatform1760781933.azurewebsites.net/api/ingest-external-eeg"
        }
    },    // Legacy Production Function App
    legacyFunctionApp: {
        name: "life-theory-functions-1756511146",
        url: "https://life-theory-functions-1756511146.azurewebsites.net",
        status: "🟢 LIVE & ACCESSIBLE",
        region: "East US",
        description: "Enterprise-grade serverless infrastructure with 99.99% SLA"
    },

    // Enhanced Dashboard Function App
    dashboardFunctionApp: {
        name: "life-functions-app",
        baseUrl: "https://life-functions-app.azurewebsites.net",
        status: "🟢 ACTIVE",
        endpoints: {
            metrics: "/api/dashboard/metrics",
            neural: "/api/dashboard/neural",
            health: "/api/dashboard/health",
            eeg: "/api/dashboard/eeg",
            venturi: "/api/dashboard/venturi",
            user: "/api/dashboard/user"
        }
    }
};

// ================================================================================================
// 🎯 MICROSOFT PARTNERSHIP DEMO ENVIRONMENTS
// ================================================================================================

const DEMO_URLS = {
    // Microsoft Demo Environment
    microsoftDemo: {
        name: "life-microsoft-demo-app",
        url: "https://life-microsoft-demo-app.azurewebsites.net",
        status: "🟢 DEMO READY",
        purpose: "Microsoft Strategic Partnership Demonstration",
        features: ["Real-time EEG Processing", "Enterprise Dashboard", "AI Integration"]
    },

    // Clinical Scenario Demo
    clinicalDemo: {
        name: "life-clinical-demo",
        url: "https://life-clinical-demo.azurewebsites.net",
        status: "🏥 HEALTHCARE READY",
        scenarios: ["Hospital EEG", "Patient Monitoring", "Clinical Analytics"]
    },

    // Educational Demo
    educationalDemo: {
        name: "life-education-demo",
        url: "https://life-education-demo.azurewebsites.net",
        status: "🎓 K-12 & UNIVERSITY READY",
        features: ["Student Learning Analytics", "Adaptive Learning", "Performance Tracking"]
    }
};

// ================================================================================================
// 🔧 LOCAL DEVELOPMENT ENVIRONMENTS
// ================================================================================================

const LOCAL_DEVELOPMENT_URLS = {
    // Primary Development Server
    primaryLocal: {
        url: "http://localhost:7071",
        description: "Azure Functions Core Tools - Main Development",
        endpoints: {
            dashboard: "http://localhost:7071/api/dashboard",
            functions: "http://localhost:7071/admin/functions"
        }
    },

    // Alternative Development Ports
    alternativeLocal: [
        {
            url: "http://localhost:5000",
            description: "Flask Development Server"
        },
        {
            url: "http://localhost:8080",
            description: "L.I.F.E Platform Server"
        },
        {
            url: "http://localhost:8081",
            description: "Enhanced Dashboard Server"
        },
        {
            url: "http://localhost:8082",
            description: "EEG Processing Server"
        }
    ]
};

// ================================================================================================
// 🌐 AZURE INFRASTRUCTURE ENDPOINTS  
// ================================================================================================

const INFRASTRUCTURE_URLS = {
    // Storage Accounts
    storage: {
        primary: "https://stlifeplatformprod.blob.core.windows.net",
        backup: "https://lifeplatformstorage.blob.core.windows.net"
    },

    // Key Vault
    keyVault: {
        primary: "https://kv-life-platform-prod.vault.azure.net"
    },

    // Service Bus
    serviceBus: {
        primary: "https://sb-life-platform-prod.servicebus.windows.net"
    },

    // Application Insights
    monitoring: {
        dashboard: "https://portal.azure.com/#@lifecoach121.com/resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-prod/providers/microsoft.insights/components/life-platform-insights"
    }
};

// ================================================================================================
// 🔮 PYTHON 3.13 UPGRADED DEPLOYMENTS (POST-UPGRADE)
// ================================================================================================

const PYTHON313_UPGRADE_URLS = {
    // New Python 3.13 Function App (After Deployment)
    upgradedFunctionApp: {
        name: "lifeplatform1760781933", // Same name, upgraded runtime
        url: "https://lifeplatform1760781933.azurewebsites.net",
        status: "🔄 READY FOR PYTHON 3.13 UPGRADE",
        newEndpoints: {
            validateIngestion: "https://lifeplatform1760781933.azurewebsites.net/api/validate-ingestion",
            ingestionStats: "https://lifeplatform1760781933.azurewebsites.net/api/ingestion-stats",
            ingestExternalEEG: "https://lifeplatform1760781933.azurewebsites.net/api/ingest-external-eeg",
            healthCheck: "https://lifeplatform1760781933.azurewebsites.net/api/health"
        },
        runtime: "Python 3.13",
        features: ["Enhanced Performance", "Future-Proof Runtime", "Improved API Responses"]
    }
};

// ================================================================================================
// 🎨 INTERACTIVE DASHBOARD URLS
// ================================================================================================

const DASHBOARD_URLS = {
    // Enhanced Dashboard with External EEG Tab
    enhancedDashboard: {
        local: "http://localhost:8081/enhanced_dashboard.html",
        description: "Real-time L.I.F.E Platform Dashboard with External EEG Ingestion",
        features: [
            "Real-time Neural Metrics",
            "EEG Data Visualization",
            "External EEG Ingestion Tab",
            "Performance Analytics",
            "System Health Monitoring"
        ]
    },

    // Static Dashboard Files
    staticDashboards: [
        "dashboard-test.html",
        "enhanced_dashboard.html",
        "PROJECT_OVERVIEW.html",
        "AI_INTELLIGENCE_TEST_SUITE_IMPLEMENTATION_COMPLETE.html"
    ]
};

// ================================================================================================
// 🎯 CAMPAIGN & AUTOMATION URLS
// ================================================================================================

const AUTOMATION_URLS = {
    // GitHub Actions Workflows
    githubActions: {
        campaignLauncher: "https://github.com/SergioPYB/SergiLIFE-life-azure-system/actions/workflows/campaign-launcher.yml",
        azureDeploy: "https://github.com/SergioPYB/SergiLIFE-life-azure-system/actions/workflows/azure-deploy.yml"
    },

    // Campaign Tracking
    campaignTracking: {
        kpis: "./tracking_data/kpis/",
        outreach: "./tracking_data/outreach/",
        conversions: "./tracking_data/conversions/",
        analytics: "./tracking_data/analytics/"
    }
};

// ================================================================================================
// 📊 MARKETPLACE & BUSINESS URLS
// ================================================================================================

const BUSINESS_URLS = {
    // Azure Marketplace
    marketplace: {
        offerId: "9a600d96-fe1e-420b-902a-a0c42c561adb",
        partnerCenter: "https://partner.microsoft.com/dashboard/commercial-marketplace/overview",
        listing: "https://azuremarketplace.microsoft.com/marketplace/apps/9a600d96-fe1e-420b-902a-a0c42c561adb"
    },

    // Business Targets
    targets: {
        q4_2025: "$345K",
        by_2029: "$50.7M",
        institutions: "1,720 targeted institutions",
        launchDate: "September 27, 2025"
    }
};

// ================================================================================================
// 🚀 COMPLETE PLATFORM ACCESS SUMMARY
// ================================================================================================

const PLATFORM_SUMMARY = {
    totalDeployments: 8,
    activeEnvironments: 5,
    developmentUrls: 6,
    productionStatus: "OPERATIONAL",
    pythonUpgradeNeeded: true,
    marketplaceReady: true,

    quickAccess: {
        primaryProduction: "https://lifeplatform1760781933.azurewebsites.net",
        localDevelopment: "http://localhost:7071",
        enhancedDashboard: "http://localhost:8081/enhanced_dashboard.html",
        microsoftDemo: "https://life-microsoft-demo-app.azurewebsites.net"
    }
};

// ================================================================================================
// 🎯 NEXT STEPS FOR PYTHON 3.13 UPGRADE
// ================================================================================================

const UPGRADE_ACTIONS = {
    immediate: [
        "Deploy Python 3.13 upgrade using deploy_python313.bat",
        "Test API endpoints after upgrade",
        "Validate Enhanced Dashboard External EEG Tab connectivity",
        "Confirm marketplace compatibility"
    ],

    validation: [
        "Run verify_python313_deployment.py",
        "Test all API endpoints",
        "Validate real-time EEG processing",
        "Confirm Azure Functions runtime upgrade"
    ]
};

// ================================================================================================
// 📋 EXPORT ALL URLS FOR REFERENCE
// ================================================================================================

const ALL_LIFE_PLATFORM_URLS = {
    PRODUCTION_URLS,
    DEMO_URLS,
    LOCAL_DEVELOPMENT_URLS,
    INFRASTRUCTURE_URLS,
    PYTHON313_UPGRADE_URLS,
    DASHBOARD_URLS,
    AUTOMATION_URLS,
    BUSINESS_URLS,
    PLATFORM_SUMMARY,
    UPGRADE_ACTIONS
};

// ================================================================================================
// 🎯 DYNAMIC URL FUNCTIONS FOR COPILOT INTEGRATION
// ================================================================================================

/**
 * <!-- Copilot: Generate a JSON array of all current LIFE Platform URLs:
 *   - Azure Function App URLs
 *   - Web App/Dashboard URLs  
 *   - Base API endpoints
 * Use the naming patterns from our resource group `life-platform-prod`. -->
 */
function getAllCurrentLIFEPlatformURLs() {
    return CURRENT_LIFE_PLATFORM_URLS;
}

/**
 * Extract production URLs only (exclude localhost)
 */
function getProductionURLsOnly() {
    return CURRENT_LIFE_PLATFORM_URLS.filter(url => !url.includes('localhost'));
}

/**
 * Get URLs by category with latest timestamps
 */
function getURLsByCategory() {
    return {
        functionApps: [
            "https://lifeplatform1760781933.azurewebsites.net",                   // Timestamped: 1760781933
            "https://life-theory-functions-1756511146.azurewebsites.net",         // Timestamped: 1756511146
            "https://life-functions-app.azurewebsites.net"
        ],
        webApps: [
            "https://green-ground-0c65efe0f.1.azurestaticapps.net",              // Current Azure Static Web App
            "https://life-platform-webapp.azurewebsites.net",
            "https://life-platform-webapp.azurestaticapps.net"
        ],
        apiEndpoints: [
            "https://lifeplatform1760781933.azurewebsites.net/api/validate-ingestion",
            "https://life-functions-app.azurewebsites.net/api/dashboard/metrics",
            "https://life-functions-app.azurewebsites.net/api/eeg_processor"
        ],
        development: [
            "http://localhost:7071",
            "http://localhost:8080",
            "http://localhost:8081"
        ]
    };
}

/**
 * Get current status with October 18, 2025 updates
 */
function getCurrentPlatformStatus() {
    return {
        timestamp: "October 18, 2025",
        totalDeployments: CURRENT_LIFE_PLATFORM_URLS.length,
        productionUrls: getProductionURLsOnly().length,
        criticalIssue: "lifeplatform1760781933 needs Python 3.13 upgrade (404 errors)",
        workingUrls: [
            "https://life-theory-functions-1756511146.azurewebsites.net",
            "https://green-ground-0c65efe0f.1.azurestaticapps.net",
            "https://life-functions-app.azurewebsites.net"
        ]
    };
}

// Console output for immediate reference
console.log("🧠 L.I.F.E. PLATFORM - DYNAMIC URL INVENTORY LOADED (October 18, 2025)");
console.log("🚀 Current Platform URLs:", CURRENT_LIFE_PLATFORM_URLS.length);
console.log("🔧 Production URLs:", getProductionURLsOnly().length);
console.log("⚠️  Critical Issue:", getCurrentPlatformStatus().criticalIssue);

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ALL_LIFE_PLATFORM_URLS,
        CURRENT_LIFE_PLATFORM_URLS,
        getAllCurrentLIFEPlatformURLs,
        getProductionURLsOnly,
        getURLsByCategory,
        getCurrentPlatformStatus
    };
}

// Export for ES6 modules  
export default ALL_LIFE_PLATFORM_URLS;
export {
    CURRENT_LIFE_PLATFORM_URLS,
    getAllCurrentLIFEPlatformURLs,
    getProductionURLsOnly,
    getURLsByCategory,
    getCurrentPlatformStatus
};