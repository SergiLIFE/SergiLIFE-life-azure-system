# PowerShell version of QUICK_FULL_DEPLOY
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " QUICK FULL DEPLOYMENT - Use Working Method" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# Set up temp directory
$TEMP_DEPLOY = "$env:USERPROFILE\life_quick_deploy"
if (Test-Path $TEMP_DEPLOY) {
    Remove-Item $TEMP_DEPLOY -Recurse -Force
}
New-Item -ItemType Directory -Path $TEMP_DEPLOY | Out-Null
Set-Location $TEMP_DEPLOY

Write-Host "[1/3] Creating function_app.py with Python v2 model..." -ForegroundColor Yellow

# Create function_app.py
@"
import azure.functions as func
import json
import logging
from datetime import datetime, timezone

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

# Create host.json
@"
{
  "version": "2.0",
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[4.*, 5.0.0)"
  }
}
"@ | Out-File -FilePath "host.json" -Encoding UTF8

# Create requirements.txt
"azure-functions" | Out-File -FilePath "requirements.txt" -Encoding UTF8

Write-Host "[2/3] Creating ZIP and deploying..." -ForegroundColor Yellow

# Create ZIP file
Compress-Archive -Path "function_app.py", "requirements.txt", "host.json" -DestinationPath "deployment.zip" -Force

# Deploy to Azure
Write-Host "Deploying to Azure Functions..." -ForegroundColor Green
az functionapp deployment source config-zip --resource-group life-platform-rg --name life-functions-app --src deployment.zip

Write-Host "[3/3] Testing after 60 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 60

Write-Host "Testing health endpoint..." -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "https://life-functions-app.azurewebsites.net/api/health" -TimeoutSec 10
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ SUCCESS: $($data | ConvertTo-Json -Compress)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " DEPLOYMENT COMPLETE - L.I.F.E Platform v2.0" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Health: https://life-functions-app.azurewebsites.net/api/health" -ForegroundColor White
Write-Host "EEG:    https://life-functions-app.azurewebsites.net/api/eeg/process" -ForegroundColor White
Write-Host ""

# Cleanup
Set-Location "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
Remove-Item $TEMP_DEPLOY -Recurse -Force
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")