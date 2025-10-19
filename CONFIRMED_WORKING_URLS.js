/**
 * 🎉 CONFIRMED L.I.F.E Platform URLs - October 18, 2025
 * Based on ACTUAL Azure Cloud Shell output - these URLs are verified!
 */

// ✅ CONFIRMED from Azure CLI commands:
// az functionapp list --resource-group life-platform-prod --output table
// az staticwebapp list --output table

const CONFIRMED_WORKING_LIFE_PLATFORM_URLS = [
    // 🚀 Function App (CONFIRMED Running)
    "https://lifeplatform1760781933.azurewebsites.net",                    // Status: Running, ResourceGroup: life-platform-prod

    // 🌐 Static Web App (CONFIRMED Active)  
    "https://green-ground-0c65efe0f.1.azurestaticapps.net"                // DefaultHostname from Azure CLI, State: Active
];

// 📊 CONFIRMED Azure Resources (from your Cloud Shell output)
const AZURE_RESOURCES = {
    functionApp: {
        name: "lifeplatform1760781933",
        location: "East US",
        state: "Running",
        resourceGroup: "life-platform-prod",
        defaultHostName: "lifeplatform1760781933.azurewebsites.net",
        appServicePlan: "EastUSLinuxDynamicPlan"
    },
    staticWebApp: {
        name: "life-platform-webapp",
        location: "East US 2",
        branch: "main",
        defaultHostname: "green-ground-0c65efe0f.1.azurestaticapps.net",
        resourceGroup: "life-platform-rg",
        repositoryUrl: "https://github.com/SergiLIFE/SergiLIFE-life-azure-system",
        provider: "GitHub"
    }
};

// 🎯 Function URLs to test (Function App is running but may not have endpoints configured yet)
const FUNCTION_ENDPOINTS_TO_TEST = [
    "https://lifeplatform1760781933.azurewebsites.net/api/validate-ingestion",
    "https://lifeplatform1760781933.azurewebsites.net/api/ingestion-stats",
    "https://lifeplatform1760781933.azurewebsites.net/api/ingest-external-eeg",
    "https://lifeplatform1760781933.azurewebsites.net/api/health"
];

console.log("🎉 CONFIRMED L.I.F.E Platform URLs (October 18, 2025):");
console.log("=" * 60);
console.log("✅ Function App:", AZURE_RESOURCES.functionApp.defaultHostName);
console.log("✅ Static Web App:", AZURE_RESOURCES.staticWebApp.defaultHostname);
console.log("\n📋 Complete JSON Array:");
console.log(JSON.stringify(CONFIRMED_WORKING_LIFE_PLATFORM_URLS, null, 2));

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        CONFIRMED_WORKING_LIFE_PLATFORM_URLS,
        AZURE_RESOURCES,
        FUNCTION_ENDPOINTS_TO_TEST
    };
}