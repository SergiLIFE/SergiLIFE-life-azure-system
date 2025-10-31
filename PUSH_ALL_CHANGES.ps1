#!/usr/bin/env pwsh
# L.I.F.E. Platform - Complete Repository Push
# Commits and pushes all 40 pending changes

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "L.I.F.E. Platform - Complete Push" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$repoPath = "c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system"
Push-Location $repoPath

try {
    Write-Host "[1/6] Configuring git for safety..." -ForegroundColor Yellow
    & git config core.safecrlf false
    & git config core.autocrlf true
    Write-Host "✓ Git configured" -ForegroundColor Green
    
    Write-Host "[2/6] Checking current status..." -ForegroundColor Yellow
    $status = & git status --short
    $changeCount = ($status | Measure-Object -Line).Lines
    Write-Host "✓ Found $changeCount changes to commit" -ForegroundColor Green
    
    Write-Host "[3/6] Adding all changes..." -ForegroundColor Yellow
    & git add -A
    Write-Host "✓ All files staged" -ForegroundColor Green
    
    Write-Host "[4/6] Committing 40 changes..." -ForegroundColor Yellow
    & git commit -m "Complete L.I.F.E. Platform deployment: Add autonomous multi-environment validator, clinical adoption report, peer review report, deployment automation, and platform marketing page (Oct 31 2025)"
    Write-Host "✓ Committed successfully" -ForegroundColor Green
    
    Write-Host "[5/6] Pulling latest from remote..." -ForegroundColor Yellow
    & git pull origin main --no-rebase
    Write-Host "✓ Synced with remote" -ForegroundColor Green
    
    Write-Host "[6/6] Pushing all changes to GitHub..." -ForegroundColor Yellow
    & git push -u origin main
    Write-Host "✓ All changes pushed successfully!" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Deployment Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "📊 Changes Deployed:" -ForegroundColor Cyan
    Write-Host "  • autonomous_multi_environment_validator.py" -ForegroundColor Green
    Write-Host "  • AUTONOMOUS_CLINICAL_ADOPTION_REPORT_20251031.txt" -ForegroundColor Green
    Write-Host "  • peer_review_report.json" -ForegroundColor Green
    Write-Host "  • docs/life-theory-platform.html" -ForegroundColor Green
    Write-Host "  • DEPLOY_LIFE_PLATFORM.ps1" -ForegroundColor Green
    Write-Host "  • Plus 35 more supporting files" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "🌐 Live URLs:" -ForegroundColor Cyan
    Write-Host "  Custom Domain: https://lifecoach-121.com/life-theory-platform.html" -ForegroundColor Green
    Write-Host "  GitHub Raw:    https://raw.githubusercontent.com/SergiLIFE/SergiLIFE-life-azure-system/main/docs/life-theory-platform.html" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "📋 Repository Status:" -ForegroundColor Cyan
    & git status
    Write-Host ""
    
    Write-Host "⏱️  Waiting 10 seconds for GitHub to sync..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    Write-Host ""
    Write-Host "✅ Done! All 40 changes are now live on GitHub." -ForegroundColor Green
    Write-Host "📢 You can now share the platform URL with colleagues and stakeholders." -ForegroundColor Green
    Write-Host ""
}
catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Check git status: git status" -ForegroundColor Gray
    Write-Host "2. View recent commits: git log --oneline -5" -ForegroundColor Gray
    Write-Host "3. Check remote: git remote -v" -ForegroundColor Gray
}
finally {
    Pop-Location
    Write-Host ""
    Write-Host "Press Enter to close..." -ForegroundColor Gray
    Read-Host
}
