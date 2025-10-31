#!/usr/bin/env pwsh
# L.I.F.E. Theory Platform GitHub Deployment - PowerShell Version

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "L.I.F.E. Platform GitHub Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$repoPath = "c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system"
Push-Location $repoPath

try {
    Write-Host "[1/5] Disabling CRLF safety checks..." -ForegroundColor Yellow
    & git config core.safecrlf false
    
    Write-Host "[2/5] Adding all files..." -ForegroundColor Yellow
    & git add .
    
    Write-Host "[3/5] Committing changes..." -ForegroundColor Yellow
    & git commit -m "Add L.I.F.E. Theory Platform marketing page with clinical validation metrics (Oct 31 2025)" --allow-empty
    
    Write-Host "[4/5] Pulling latest from remote..." -ForegroundColor Yellow
    & git pull origin main --no-rebase
    
    Write-Host "[5/5] Pushing to GitHub..." -ForegroundColor Yellow
    & git push origin main
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Deployment Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your page is now live at:" -ForegroundColor Cyan
    Write-Host "https://lifecoach-121.com/life-theory-platform.html" -ForegroundColor Green
    Write-Host ""
    Write-Host "Raw GitHub URL:" -ForegroundColor Cyan
    Write-Host "https://raw.githubusercontent.com/SergiLIFE/SergiLIFE-life-azure-system/main/docs/life-theory-platform.html" -ForegroundColor Green
    Write-Host ""
    Write-Host "Waiting 10 seconds for GitHub to sync..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    Write-Host "Done! You can now share the URL with colleagues." -ForegroundColor Green
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
finally {
    Pop-Location
}
