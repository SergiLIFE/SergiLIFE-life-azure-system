# Azure Resource Inventory Script for Azure Sponsorship Subscription
# Subscription ID: 5c88cef6-f243-497d-98af-6c6086d575ca
# This script uses PowerShell to interact with Azure REST APIs directly

param(
    [string]$SubscriptionId = "5c88cef6-f243-497d-98af-6c6086d575ca",
    [string]$OutputPath = ".\azure_inventory.json"
)

Write-Host "=== Azure Resource Inventory for L.I.F.E. Platform ===" -ForegroundColor Cyan
Write-Host "Subscription ID: $SubscriptionId" -ForegroundColor Yellow
Write-Host "Date: $(Get-Date)" -ForegroundColor Yellow
Write-Host ""

# Function to get Azure access token
function Get-AzureAccessToken {
    Write-Host "Step 1: Getting Azure Access Token..." -ForegroundColor Green
    
    # This will open browser for interactive login
    $context = [Microsoft.Azure.Commands.Common.Authentication.Abstractions.AzureRmProfileProvider]::Instance.Profile.DefaultContext
    
    if (-not $context -or -not $context.Account) {
        Write-Host "Please login to Azure first. Opening browser..." -ForegroundColor Yellow
        
        # Alternative approach using Azure CLI if available
        try {
            $result = az login --output json 2>$null | ConvertFrom-Json
            if ($result) {
                Write-Host "✓ Successfully logged in to Azure" -ForegroundColor Green
                return (az account get-access-token --query accessToken -o tsv)
            }
        }
        catch {
            Write-Warning "Azure CLI not available. Please install Azure CLI or Azure PowerShell module."
            Write-Host "Installation options:" -ForegroundColor Yellow
            Write-Host "1. Azure CLI: https://aka.ms/installazurecliwindows" -ForegroundColor White
            Write-Host "2. Azure PowerShell: Install-Module -Name Az -Force -AllowClobber" -ForegroundColor White
            exit 1
        }
    }
}

# Function to make Azure REST API calls
function Invoke-AzureRestApi {
    param(
        [string]$Uri,
        [string]$AccessToken,
        [string]$Method = "GET"
    )
    
    $headers = @{
        'Authorization' = "Bearer $AccessToken"
        'Content-Type'  = 'application/json'
    }
    
    try {
        $response = Invoke-RestMethod -Uri $Uri -Headers $headers -Method $Method
        return $response
    }
    catch {
        Write-Warning "Failed to call API: $Uri"
        Write-Warning "Error: $($_.Exception.Message)"
        return $null
    }
}

# Alternative approach using Azure PowerShell cmdlets if available
function Get-AzureResourcesWithPowerShell {
    Write-Host "Attempting to use Azure PowerShell module..." -ForegroundColor Green
    
    try {
        # Check if Az module is available
        Import-Module Az.Accounts -ErrorAction Stop
        Import-Module Az.Resources -ErrorAction Stop
        
        # Connect to Azure
        $context = Get-AzContext
        if (-not $context) {
            Write-Host "Please login to Azure..." -ForegroundColor Yellow
            Connect-AzAccount
        }
        
        # Set subscription context
        Set-AzContext -SubscriptionId $SubscriptionId
        
        Write-Host "✓ Connected to Azure PowerShell" -ForegroundColor Green
        
        # Get resources
        $inventory = @{}
        
        Write-Host "Getting subscription information..." -ForegroundColor Blue
        $subscription = Get-AzSubscription -SubscriptionId $SubscriptionId
        $inventory.Subscription = $subscription
        
        Write-Host "Getting resource groups..." -ForegroundColor Blue
        $resourceGroups = Get-AzResourceGroup
        $inventory.ResourceGroups = $resourceGroups
        
        Write-Host "Getting all resources..." -ForegroundColor Blue
        $resources = Get-AzResource
        $inventory.Resources = $resources
        
        Write-Host "Getting storage accounts..." -ForegroundColor Blue
        $storageAccounts = Get-AzStorageAccount
        $inventory.StorageAccounts = $storageAccounts
        
        Write-Host "Getting function apps..." -ForegroundColor Blue
        $functionApps = Get-AzFunctionApp
        $inventory.FunctionApps = $functionApps
        
        Write-Host "Getting web apps..." -ForegroundColor Blue
        $webApps = Get-AzWebApp
        $inventory.WebApps = $webApps
        
        Write-Host "Getting Key Vaults..." -ForegroundColor Blue
        $keyVaults = Get-AzKeyVault
        $inventory.KeyVaults = $keyVaults
        
        # Save to file
        $inventory | ConvertTo-Json -Depth 10 | Out-File -FilePath $OutputPath -Encoding UTF8
        
        Write-Host "✓ Inventory saved to: $OutputPath" -ForegroundColor Green
        
        # Display summary
        Write-Host "`n=== AZURE RESOURCE SUMMARY ===" -ForegroundColor Cyan
        Write-Host "Subscription: $($subscription.Name)" -ForegroundColor White
        Write-Host "Resource Groups: $($resourceGroups.Count)" -ForegroundColor White
        Write-Host "Total Resources: $($resources.Count)" -ForegroundColor White
        Write-Host "Storage Accounts: $($storageAccounts.Count)" -ForegroundColor White
        Write-Host "Function Apps: $($functionApps.Count)" -ForegroundColor White
        Write-Host "Web Apps: $($webApps.Count)" -ForegroundColor White
        Write-Host "Key Vaults: $($keyVaults.Count)" -ForegroundColor White
        
        # Show resource breakdown by type
        if ($resources.Count -gt 0) {
            Write-Host "`n=== RESOURCE BREAKDOWN BY TYPE ===" -ForegroundColor Cyan
            $resourcesByType = $resources | Group-Object ResourceType | Sort-Object Count -Descending
            foreach ($group in $resourcesByType) {
                Write-Host "$($group.Name): $($group.Count)" -ForegroundColor White
            }
        }
        
        # Show resource breakdown by location
        if ($resources.Count -gt 0) {
            Write-Host "`n=== RESOURCE BREAKDOWN BY LOCATION ===" -ForegroundColor Cyan
            $resourcesByLocation = $resources | Group-Object Location | Sort-Object Count -Descending
            foreach ($group in $resourcesByLocation) {
                Write-Host "$($group.Name): $($group.Count)" -ForegroundColor White
            }
        }
        
        return $inventory
    }
    catch {
        Write-Warning "Azure PowerShell module not available or not configured."
        Write-Warning "Error: $($_.Exception.Message)"
        return $null
    }
}

# Manual inventory collection if Azure tools are not available
function Get-ManualInventoryInstructions {
    Write-Host "`n=== MANUAL INVENTORY INSTRUCTIONS ===" -ForegroundColor Yellow
    Write-Host "Since Azure CLI and PowerShell modules are not available, please follow these manual steps:" -ForegroundColor White
    Write-Host ""
    
    Write-Host "1. Open Azure Portal (portal.azure.com)" -ForegroundColor Cyan
    Write-Host "2. Navigate to your subscription: $SubscriptionId" -ForegroundColor White
    Write-Host "3. Go to 'All resources' to see complete inventory" -ForegroundColor White
    Write-Host ""
    
    Write-Host "Key areas to review:" -ForegroundColor Cyan
    Write-Host "• Resource Groups" -ForegroundColor White
    Write-Host "• Function Apps" -ForegroundColor White
    Write-Host "• Logic Apps" -ForegroundColor White
    Write-Host "• Storage Accounts" -ForegroundColor White
    Write-Host "• Key Vaults" -ForegroundColor White
    Write-Host "• Application Insights" -ForegroundColor White
    Write-Host "• Cosmos DB" -ForegroundColor White
    Write-Host ""
    
    Write-Host "Cost Management:" -ForegroundColor Cyan
    Write-Host "• Go to 'Cost Management + Billing'" -ForegroundColor White
    Write-Host "• Check 'Cost analysis' for current spending" -ForegroundColor White
    Write-Host "• Set up 'Budgets' with alerts at 50% and 80%" -ForegroundColor White
    Write-Host ""
    
    Write-Host "Security Review:" -ForegroundColor Cyan
    Write-Host "• Check 'Security Center' for recommendations" -ForegroundColor White
    Write-Host "• Review 'Identity and Access Management (IAM)'" -ForegroundColor White
    Write-Host "• Verify 'Key Vault' access policies" -ForegroundColor White
}

# Main execution
Write-Host "Attempting Azure resource inventory..." -ForegroundColor Green

# Try Azure PowerShell first
$inventory = Get-AzureResourcesWithPowerShell

if (-not $inventory) {
    Write-Host "Azure PowerShell not available. Providing manual instructions..." -ForegroundColor Yellow
    Get-ManualInventoryInstructions
}

Write-Host "`n=== NEXT STEPS FOR L.I.F.E. PLATFORM DEPLOYMENT ===" -ForegroundColor Cyan
Write-Host "1. Review the generated inventory" -ForegroundColor White
Write-Host "2. Identify existing resources that can be reused" -ForegroundColor White
Write-Host "3. Plan new resource deployment strategy" -ForegroundColor White
Write-Host "4. Set up cost monitoring and budgets" -ForegroundColor White
Write-Host "5. Implement security best practices" -ForegroundColor White
Write-Host ""
Write-Host "Recommended Azure CLI installation: https://aka.ms/installazurecliwindows" -ForegroundColor Yellow
Write-Host "Script completed: $(Get-Date)" -ForegroundColor Green
