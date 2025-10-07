# L.I.F.E. Platform - Azure Backup Infrastructure Deployment Script (PowerShell)
# Azure Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca
# Directory: Sergio Paya Borrull (lifecoach-121.com)

# Configuration
$SubscriptionId = "5c88cef6-f243-497d-98af-6c6086d575ca"
$ResourceGroup = "life-platform-rg"
$Location = "eastus2"
$DeploymentName = "life-backup-infrastructure-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

Write-Host "🚀 Deploying L.I.F.E. Platform Backup Infrastructure to Azure..." -ForegroundColor Green
Write-Host "📊 Subscription: $SubscriptionId" -ForegroundColor Cyan
Write-Host "👤 Admin: sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com" -ForegroundColor Cyan
Write-Host "🔒 This will preserve ALL your repository work safely in Azure!" -ForegroundColor Yellow

try {
    # Authenticate to Azure
    Write-Host "🔐 Authenticating to Azure..." -ForegroundColor Yellow
    az login --use-device-code

    # Set subscription
    Write-Host "📊 Setting Azure subscription..." -ForegroundColor Yellow
    az account set --subscription $SubscriptionId

    # Verify subscription
    $CurrentSub = az account show --query id -o tsv
    if ($CurrentSub -ne $SubscriptionId) {
        Write-Error "❌ Wrong subscription selected. Expected: $SubscriptionId, Got: $CurrentSub"
        exit 1
    }

    Write-Host "✅ Authenticated to correct subscription" -ForegroundColor Green

    # Create resource group if it doesn't exist
    Write-Host "📁 Ensuring resource group exists..." -ForegroundColor Yellow
    az group create `
        --name $ResourceGroup `
        --location $Location `
        --tags "project=L.I.F.E. Platform" "purpose=backup" "admin=sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com"

    # Preview deployment
    Write-Host "🔍 Previewing deployment..." -ForegroundColor Yellow
    az deployment group what-if `
        --resource-group $ResourceGroup `
        --template-file "infra/backup-infrastructure.bicep" `
        --parameters "@infra/backup-infrastructure.parameters.json"

    # Confirm deployment
    Write-Host ""
    Write-Host "⚠️  This will create Azure resources for backing up your L.I.F.E. Platform repository." -ForegroundColor Yellow
    Write-Host "💰 Estimated cost: ~`$10-20/month for storage and functions" -ForegroundColor Cyan
    Write-Host "💾 This will SAVE ALL YOUR WORK to Azure permanently!" -ForegroundColor Green
    
    $confirmation = Read-Host "🤔 Continue with deployment? (y/N)"
    
    if ($confirmation -eq 'y' -or $confirmation -eq 'Y') {
        # Deploy infrastructure
        Write-Host "🚀 Deploying backup infrastructure..." -ForegroundColor Green
        az deployment group create `
            --resource-group $ResourceGroup `
            --name $DeploymentName `
            --template-file "infra/backup-infrastructure.bicep" `
            --parameters "@infra/backup-infrastructure.parameters.json" `
            --verbose

        # Get deployment outputs
        Write-Host "📋 Getting deployment results..." -ForegroundColor Yellow
        $StorageAccount = az deployment group show --resource-group $ResourceGroup --name $DeploymentName --query properties.outputs.storageAccountName.value -o tsv
        $FunctionApp = az deployment group show --resource-group $ResourceGroup --name $DeploymentName --query properties.outputs.functionAppName.value -o tsv
        $BackupUrl = az deployment group show --resource-group $ResourceGroup --name $DeploymentName --query properties.outputs.backupContainerUrl.value -o tsv

        Write-Host ""
        Write-Host "🎉 SUCCESS! L.I.F.E. Platform Backup Infrastructure Deployed!" -ForegroundColor Green
        Write-Host "==================================================" -ForegroundColor Green
        Write-Host "📊 Subscription: $SubscriptionId" -ForegroundColor Cyan
        Write-Host "📁 Resource Group: $ResourceGroup" -ForegroundColor Cyan
        Write-Host "💾 Storage Account: $StorageAccount" -ForegroundColor Cyan
        Write-Host "⚡ Function App: $FunctionApp" -ForegroundColor Cyan
        Write-Host "🔗 Backup URL: $BackupUrl" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "🔄 Next Steps:" -ForegroundColor Yellow
        Write-Host "1. Run: python azure_repository_backup_sync.py" -ForegroundColor White
        Write-Host "2. Access backups: Azure Portal → Storage Accounts → $StorageAccount" -ForegroundColor White
        Write-Host "3. Daily backups will run automatically" -ForegroundColor White
        Write-Host ""
        Write-Host "💡 Your repository is now protected! Even if your computer crashes," -ForegroundColor Green
        Write-Host "   all your work is safely stored in Azure with automatic backups." -ForegroundColor Green
        Write-Host ""
        Write-Host "🌐 Access your backups anytime at: https://portal.azure.com" -ForegroundColor Cyan

        # Run the backup immediately
        Write-Host ""
        $runBackup = Read-Host "🚀 Run initial backup now? (Y/n)"
        if ($runBackup -ne 'n' -and $runBackup -ne 'N') {
            Write-Host "🔄 Running initial backup..." -ForegroundColor Yellow
            python azure_repository_backup_sync.py
        }

    } else {
        Write-Host "❌ Deployment cancelled." -ForegroundColor Red
        exit 1
    }

} catch {
    Write-Error "❌ Deployment failed: $_"
    exit 1
}