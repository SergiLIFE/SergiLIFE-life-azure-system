# PowerShell Deployment Script with Invoke-WebRequest Testing
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " POWERSHELL DEPLOYMENT - Best Practices" -ForegroundColor Cyan  
Write-Host "======================================================================" -ForegroundColor Cyan

# Step 1: Verify Function App exists
Write-Host "[VERIFY] Checking Function App existence..." -ForegroundColor Yellow
try {
    $functionApp = az functionapp show --name life-func-12525 --resource-group life-platform-prod --query "name" --output tsv 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Function App 'life-func-12525' verified exists" -ForegroundColor Green
    } else {
        Write-Host "❌ ERROR: Function App 'life-func-12525' not found in 'life-platform-prod'" -ForegroundColor Red
        Write-Host "Available Function Apps:" -ForegroundColor Yellow
        az functionapp list --resource-group life-platform-prod --query "[].name" --output table
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "❌ Error checking Function App: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Step 2: Check symlink (optional - avoid if not needed)
if (Test-Path "C:\LIFE-Platform") {
    Write-Host "ℹ️  Symlink C:\LIFE-Platform already exists, skipping creation" -ForegroundColor Cyan
}

# Step 3: Create deployment directory
$DEPLOY_DIR = "$env:USERPROFILE\ps_deploy_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "Creating deployment directory: $DEPLOY_DIR" -ForegroundColor Yellow

if (Test-Path $DEPLOY_DIR) { Remove-Item $DEPLOY_DIR -Recurse -Force }
New-Item -ItemType Directory -Path $DEPLOY_DIR | Out-Null
Set-Location $DEPLOY_DIR

# Step 4: Create Function App files
Write-Host "[1/3] Creating function_app.py with Python v2 model..." -ForegroundColor Yellow

@"
import azure.functions as func
import json

app = func.FunctionApp()

@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"])
async def health_check(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"status": "healthy", "platform": "L.I.F.E Platform", "version": "2.0.0"}),
        mimetype="application/json"
    )

@app.route(route="eeg/process", auth_level=func.AuthLevel.FUNCTION, methods=["POST"])
async def eeg_processor(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"status": "success", "message": "EEG processor ready"}),
        mimetype="application/json"
    )
"@ | Out-File -FilePath "function_app.py" -Encoding UTF8

@"
{
  "version": "2.0",
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[4.*, 5.0.0)"
  }
}
"@ | Out-File -FilePath "host.json" -Encoding UTF8

"azure-functions" | Out-File -FilePath "requirements.txt" -Encoding UTF8

# Step 5: Deploy
Write-Host "[2/3] Creating ZIP and deploying..." -ForegroundColor Yellow
Compress-Archive -Path "function_app.py", "host.json", "requirements.txt" -DestinationPath "deployment.zip" -Force

Write-Host "Deploying to: life-func-12525 (verified exists)" -ForegroundColor Green
$deployResult = az functionapp deployment source config-zip --resource-group life-platform-prod --name life-func-12525 --src deployment.zip 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Deployment command completed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Deployment failed! Output:" -ForegroundColor Red
    Write-Host $deployResult -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 6: Test with Invoke-WebRequest (BEST PRACTICE)
Write-Host "[3/3] Testing after 60 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 60

Write-Host "Testing health endpoint with Invoke-WebRequest..." -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "https://life-func-12525.azurewebsites.net/api/health" -TimeoutSec 15
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ HEALTH SUCCESS: $($data | ConvertTo-Json -Compress)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health endpoint test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " DEPLOYMENT COMPLETE - L.I.F.E Platform v2.0" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Health (anonymous): https://life-func-12525.azurewebsites.net/api/health" -ForegroundColor White
Write-Host "🔒 EEG (auth required): https://life-func-12525.azurewebsites.net/api/eeg/process" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Open health URL in browser: https://life-func-12525.azurewebsites.net/api/health" -ForegroundColor Cyan
Write-Host "2. Get function keys: az functionapp keys list --name life-func-12525 --resource-group life-platform-prod" -ForegroundColor Cyan

# Cleanup
Set-Location "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
Remove-Item $DEPLOY_DIR -Recurse -Force
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")