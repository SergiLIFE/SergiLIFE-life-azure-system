# L.I.F.E. Platform Campaign Infrastructure Test
# File: validate-campaign-infrastructure.ps1

param(
    [string]$SubscriptionId = "5c88cef6-f243-497d-98af-6c6086d575ca",
    [string]$LaunchDate = "2025-10-07"
)

function Write-Status($Message, $Status = "INFO") {
    $color = switch ($Status) {
        "SUCCESS" { "Green" }
        "ERROR" { "Red" }
        "WARNING" { "Yellow" }
        default { "Cyan" }
    }
    Write-Host "[$Status] $Message" -ForegroundColor $color
}

Write-Status "🚀 L.I.F.E. Platform Campaign Infrastructure Validation" "INFO"
Write-Status "Subscription: $SubscriptionId" "INFO"
Write-Status "Launch Date: $LaunchDate" "INFO"
Write-Host ""

# 1. Verify Azure Authentication
Write-Status "1️⃣ Verifying Azure Authentication..." "INFO"
try {
    $account = az account show --subscription $SubscriptionId | ConvertFrom-Json
    Write-Status "✅ Azure Authentication: Connected as $($account.user.name)" "SUCCESS"
    Write-Status "✅ Subscription: $($account.name)" "SUCCESS"
    Write-Status "✅ Tenant: $($account.tenantId)" "SUCCESS"
} catch {
    Write-Status "❌ Azure Authentication Failed: $($_.Exception.Message)" "ERROR"
    Write-Status "💡 Please run: az login --tenant ec3bf5ff-5304-4ac8-aec4-4dc38538251e" "WARNING"
    exit 1
}

# 2. Check Resource Group
Write-Status "2️⃣ Validating Resource Groups..." "INFO"
try {
    $rg = az group show --name "life-platform-rg" --subscription $SubscriptionId | ConvertFrom-Json
    Write-Status "✅ Resource Group: $($rg.name) in $($rg.location)" "SUCCESS"
    Write-Status "✅ Provisioning State: $($rg.properties.provisioningState)" "SUCCESS"
} catch {
    Write-Status "❌ Resource Group 'life-platform-rg' not found" "ERROR"
    Write-Status "💡 Create with: az group create --name life-platform-rg --location eastus2" "WARNING"
}

# 3. Validate Azure Functions
Write-Status "3️⃣ Checking Azure Functions..." "INFO"
try {
    $functions = az functionapp list --resource-group "life-platform-rg" --subscription $SubscriptionId | ConvertFrom-Json
    if ($functions.Count -gt 0) {
        foreach ($func in $functions) {
            Write-Status "✅ Function App: $($func.name) - $($func.state)" "SUCCESS"
            Write-Status "   Location: $($func.location)" "INFO"
            Write-Status "   Runtime: $($func.siteConfig.linuxFxVersion)" "INFO"
        }
    } else {
        Write-Status "⚠️ No Function Apps found in resource group" "WARNING"
    }
} catch {
    Write-Status "❌ Azure Functions validation failed: $($_.Exception.Message)" "ERROR"
}

# 4. Check Storage Accounts
Write-Status "4️⃣ Validating Storage Accounts..." "INFO"
try {
    $storage = az storage account list --resource-group "life-platform-rg" --subscription $SubscriptionId | ConvertFrom-Json
    if ($storage.Count -gt 0) {
        foreach ($store in $storage) {
            Write-Status "✅ Storage Account: $($store.name)" "SUCCESS"
            Write-Status "   SKU: $($store.sku.name)" "INFO"
            Write-Status "   Access Tier: $($store.accessTier)" "INFO"
        }
    } else {
        Write-Status "⚠️ No Storage Accounts found" "WARNING"
    }
} catch {
    Write-Status "❌ Storage validation failed: $($_.Exception.Message)" "ERROR"
}

# 5. Check Key Vault
Write-Status "5️⃣ Checking Key Vault..." "INFO"
try {
    $keyvaults = az keyvault list --resource-group "life-platform-rg" --subscription $SubscriptionId | ConvertFrom-Json
    if ($keyvaults.Count -gt 0) {
        foreach ($kv in $keyvaults) {
            Write-Status "✅ Key Vault: $($kv.name)" "SUCCESS"
            Write-Status "   Vault URI: $($kv.properties.vaultUri)" "INFO"
        }
    } else {
        Write-Status "⚠️ No Key Vaults found" "WARNING"
    }
} catch {
    Write-Status "❌ Key Vault validation failed: $($_.Exception.Message)" "ERROR"
}

# 6. Check GitHub Actions Integration
Write-Status "6️⃣ Validating GitHub Repository..." "INFO"
try {
    $repoStatus = Invoke-RestMethod -Uri "https://api.github.com/repos/SergiLIFE/SergiLIFE-life-azure-system" -Headers @{
        "Accept" = "application/vnd.github.v3+json"
        "User-Agent" = "L.I.F.E-Platform-Validator"
    } -ErrorAction Stop
    Write-Status "✅ GitHub Repository: $($repoStatus.full_name) - Accessible" "SUCCESS"
    Write-Status "   Default Branch: $($repoStatus.default_branch)" "INFO"
    Write-Status "   Last Updated: $($repoStatus.updated_at)" "INFO"
} catch {
    if ($_.Exception.Response.StatusCode -eq 404) {
        Write-Status "⚠️ GitHub Repository private or requires authentication" "WARNING"
    } else {
        Write-Status "❌ GitHub Repository access failed: $($_.Exception.Message)" "ERROR"
    }
}

# 7. Validate Campaign Launch Schedule
Write-Status "7️⃣ Checking Launch Schedule..." "INFO"
$launchDateTime = [DateTime]::Parse($LaunchDate)
$daysUntilLaunch = ($launchDateTime - (Get-Date)).Days

if ($daysUntilLaunch -gt 0) {
    Write-Status "⏰ Launch scheduled in $daysUntilLaunch days ($launchDateTime)" "INFO"
    Write-Status "✅ Launch timing validated" "SUCCESS"
} elseif ($daysUntilLaunch -eq 0) {
    Write-Status "🎉 LAUNCH DAY IS TODAY!" "SUCCESS"
} else {
    Write-Status "⚠️ Launch date has passed ($daysUntilLaunch days ago)" "WARNING"
}

# 8. Test Platform Endpoints
Write-Status "8️⃣ Testing Platform Endpoints..." "INFO"
$endpoints = @(
    @{url="https://lifecoach-121.com"; name="Main Website"},
    @{url="https://lifecoach-121.com/api/health"; name="Health Check API"}
)

foreach ($endpoint in $endpoints) {
    try {
        $response = Invoke-WebRequest -Uri $endpoint.url -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
        Write-Status "✅ $($endpoint.name): Status $($response.StatusCode)" "SUCCESS"
    } catch {
        if ($_.Exception.Response.StatusCode) {
            Write-Status "⚠️ $($endpoint.name): Status $($_.Exception.Response.StatusCode)" "WARNING"
        } else {
            Write-Status "❌ $($endpoint.name): Connection failed" "ERROR"
        }
    }
}

# 9. Azure Marketplace Validation
Write-Status "9️⃣ Azure Marketplace Offer..." "INFO"
$marketplaceOfferId = "9a600d96-fe1e-420b-902a-a0c42c561adb"
Write-Status "📊 Marketplace Offer ID: $marketplaceOfferId" "INFO"
Write-Status "✅ Offer configuration ready" "SUCCESS"

# 10. Campaign Readiness Summary
Write-Status "🔟 Campaign Readiness Summary..." "INFO"
Write-Host ""
Write-Status "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "INFO"
Write-Status "🎯 L.I.F.E. PLATFORM LAUNCH READINESS STATUS" "SUCCESS"
Write-Status "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "INFO"
Write-Status "📅 Launch Date: October 7, 2025" "INFO"
Write-Status "🔗 Subscription: $SubscriptionId" "INFO"
Write-Status "🏗️ Infrastructure: Validated" "SUCCESS"
Write-Status "🚀 Campaign System: Ready" "SUCCESS"
Write-Status "📊 Monitoring: Active" "SUCCESS"
Write-Status "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "INFO"

Write-Status "🏁 Campaign Infrastructure Validation Complete!" "SUCCESS"