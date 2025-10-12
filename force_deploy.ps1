# L.I.F.E. Platform Force Deployment Script
# January 10, 2025 - Critical October 15 Demo Preparation

Write-Host "🚀 L.I.F.E. Platform Force Deployment - January 10, 2025 16:45 UTC" -ForegroundColor Green
Write-Host "📅 Target Demo: October 15, 2025 | 23 Participants | $771K+ Pipeline" -ForegroundColor Yellow

# Set working directory
Set-Location -Path $PSScriptRoot
Write-Host "📍 Working Directory: $PWD" -ForegroundColor Cyan

# Check git status
Write-Host "`n🔍 Git Status Check:" -ForegroundColor Blue
try {
    git status
    Write-Host "✅ Git status checked successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Git status error: $($_.Exception.Message)" -ForegroundColor Red
}

# Add changes
Write-Host "`n📝 Adding changes:" -ForegroundColor Blue
try {
    git add index.html
    Write-Host "✅ Index.html added to staging" -ForegroundColor Green
} catch {
    Write-Host "❌ Git add error: $($_.Exception.Message)" -ForegroundColor Red
}

# Commit changes
Write-Host "`n💾 Committing changes:" -ForegroundColor Blue
try {
    git commit -m "🚀 FORCE DEPLOY: L.I.F.E. Platform January 10, 2025 16:45 UTC - October 15 Demo Ready"
    Write-Host "✅ Changes committed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Git commit error: $($_.Exception.Message)" -ForegroundColor Red
}

# Push to GitHub
Write-Host "`n🌐 Pushing to GitHub:" -ForegroundColor Blue
try {
    git push origin main
    Write-Host "✅ Push to GitHub successful" -ForegroundColor Green
} catch {
    Write-Host "❌ Git push error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎯 Deployment Actions:" -ForegroundColor Magenta
Write-Host "1. GitHub Actions should trigger automatically"
Write-Host "2. Azure Static Web App will rebuild"
Write-Host "3. Platform URL: https://green-ground-0c65efe0f.1.azurestaticapps.net"
Write-Host "4. Demo countdown ready for October 15, 2025"

Write-Host "`n⏱️  Expected Processing Time: 2-5 minutes" -ForegroundColor Yellow
Write-Host "🔄 Monitor deployment at: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions" -ForegroundColor Cyan

Read-Host "`nPress Enter to continue..."