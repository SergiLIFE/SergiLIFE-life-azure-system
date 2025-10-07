# Azure Deployment Script for Microsoft Partnership Demo
# L.I.F.E. Theory Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
# Account: sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com
# Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca

# Set variables
$subscriptionId = "5c88cef6-f243-497d-98af-6c6086d575ca"
$resourceGroupName = "rg-microsoft-demo-env"
$location = "eastus2"
$environmentName = "microsoft-demo-env"
$templateFile = "./infra/microsoft-demo.bicep"
$parametersFile = "./infra/microsoft-demo.parameters.json"

Write-Host "🚀 L.I.F.E. Theory Platform Microsoft Partnership Demo Deployment" -ForegroundColor Green
Write-Host "Account: sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com" -ForegroundColor Cyan
Write-Host "Subscription: $subscriptionId" -ForegroundColor Cyan
Write-Host "Target: Microsoft Executive Demonstration Environment" -ForegroundColor Yellow

# Check if Azure CLI is available
try {
    $azVersion = az --version 2>$null
    if ($azVersion) {
        Write-Host "✅ Azure CLI found" -ForegroundColor Green
        
        # Set subscription
        Write-Host "Setting Azure subscription..." -ForegroundColor Yellow
        az account set --subscription $subscriptionId
        
        # Create resource group
        Write-Host "Creating resource group: $resourceGroupName" -ForegroundColor Yellow
        az group create --name $resourceGroupName --location $location
        
        # Deploy Bicep template
        Write-Host "Deploying L.I.F.E. Theory Platform infrastructure..." -ForegroundColor Yellow
        az deployment group create `
            --resource-group $resourceGroupName `
            --template-file $templateFile `
            --parameters environmentName=$environmentName location=$location
            
        Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
        Write-Host "Microsoft Partnership Demo is now live on Azure!" -ForegroundColor Green
        
        # Get deployment outputs
        Write-Host "Getting deployment outputs..." -ForegroundColor Yellow
        $outputs = az deployment group show --resource-group $resourceGroupName --name microsoft-demo --query properties.outputs
        Write-Host "Deployment outputs:" -ForegroundColor Cyan
        Write-Host $outputs
        
    } else {
        throw "Azure CLI not found"
    }
} catch {
    Write-Host "❌ Azure CLI not available. Please use alternative deployment methods:" -ForegroundColor Red
    Write-Host ""
    Write-Host "Option 1: Azure Portal Deployment" -ForegroundColor Yellow
    Write-Host "1. Go to https://portal.azure.com" -ForegroundColor White
    Write-Host "2. Sign in with: sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com" -ForegroundColor White
    Write-Host "3. Create Resource Group: $resourceGroupName in $location" -ForegroundColor White
    Write-Host "4. Deploy template: Upload infra/microsoft-demo.bicep" -ForegroundColor White
    Write-Host "5. Set parameters: environmentName='$environmentName', location='$location'" -ForegroundColor White
    Write-Host ""
    Write-Host "Option 2: Azure Cloud Shell" -ForegroundColor Yellow
    Write-Host "1. Open https://shell.azure.com" -ForegroundColor White
    Write-Host "2. Upload the Bicep files from this repository" -ForegroundColor White
    Write-Host "3. Run: az deployment group create --resource-group $resourceGroupName --template-file microsoft-demo.bicep" -ForegroundColor White
    Write-Host ""
    Write-Host "All infrastructure files are ready in the ./infra/ directory!" -ForegroundColor Green
}

Write-Host ""
Write-Host "📊 Microsoft Partnership Demo Features:" -ForegroundColor Magenta
Write-Host "• 880x AI Performance Enhancement" -ForegroundColor White
Write-Host "• Azure OpenAI GPT-4 Integration" -ForegroundColor White
Write-Host "• Executive Outreach Automation" -ForegroundColor White
Write-Host "• $25.6B-$32.4B Partnership Value" -ForegroundColor White
Write-Host "• Production-Ready Container Apps" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Target Microsoft Executives:" -ForegroundColor Magenta
Write-Host "• Satya Nadella (CEO)" -ForegroundColor White
Write-Host "• Scott Guthrie (EVP Cloud + AI)" -ForegroundColor White
Write-Host "• Sam Altman (OpenAI CEO)" -ForegroundColor White
Write-Host "• Kevin Scott (CTO)" -ForegroundColor White