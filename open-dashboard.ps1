# L.I.F.E. Platform Dashboard Test Script
# Opens the field-specific dashboard in the default browser

Write-Host "🧠 L.I.F.E. Platform - Field-Specific Dashboard Test" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Blue

$dashboardPath = Join-Path $PSScriptRoot "field-specific-dashboard.html"

if (Test-Path $dashboardPath) {
    Write-Host "✅ Dashboard file found: $dashboardPath" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Opening dashboard in default browser..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📚 EDUCATION FIELD FEATURES:" -ForegroundColor Cyan
    Write-Host "   • Field-specific subscription plans" -ForegroundColor White
    Write-Host "   • Real-time education metrics" -ForegroundColor White
    Write-Host "   • Azure Marketplace integration" -ForegroundColor White
    Write-Host "   • Role-based interface design" -ForegroundColor White
    Write-Host "   • Responsive mobile layout" -ForegroundColor White
    Write-Host ""
    Write-Host "🔍 TEST INSTRUCTIONS:" -ForegroundColor Cyan
    Write-Host "   1. Overview tab shows all available fields" -ForegroundColor White
    Write-Host "   2. Education tab displays active metrics" -ForegroundColor White
    Write-Host "   3. Other tabs show 'Coming Soon' alerts" -ForegroundColor White
    Write-Host "   4. Check subscription pricing plans" -ForegroundColor White
    Write-Host "   5. Observe real-time metric updates" -ForegroundColor White
    Write-Host ""
    
    # Open the dashboard
    Start-Process $dashboardPath
    
    Write-Host "🌐 Dashboard opened successfully!" -ForegroundColor Green
    Write-Host "📍 File location: $dashboardPath" -ForegroundColor Gray
} else {
    Write-Host "❌ Dashboard file not found: $dashboardPath" -ForegroundColor Red
    Write-Host "💡 Make sure you're running this script from the correct directory" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Blue
Write-Host "✨ L.I.F.E. Platform Ready for Testing!" -ForegroundColor Cyan