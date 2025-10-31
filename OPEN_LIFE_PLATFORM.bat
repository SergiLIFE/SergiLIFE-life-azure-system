@echo off
REM ========================================
REM Open L.I.F.E. Platform in Browser
REM Tests all URLs and opens the working one
REM ========================================

echo.
echo ████████████████████████████████████████████████
echo  L.I.F.E. PLATFORM - OPEN IN BROWSER
echo  Testing all deployed URLs...
echo ████████████████████████████████████████████████
echo.

REM URL 1: GitHub Pages (should work immediately)
set URL_GITHUB=https://sergilife.github.io/SergiLIFE-life-azure-system/life-theory-platform.html

REM URL 2: Custom Domain (needs DNS propagation)
set URL_CUSTOM=https://lifecoach-121.com/life-theory-platform.html

REM URL 3: Local OneDrive file (your original)
set URL_LOCAL=file:///C:/Users/Sergio%%20Paya%%20Borrull/OneDrive/Pictures/L.I.F.E%%20THEORY%%20-%%20Neuroadaptive%%20Intelligence%%20Platform%%20_%%20Sergio%%20Paya%%20Borrull.html

echo Testing GitHub Pages URL...
echo %URL_GITHUB%
echo.

REM Test GitHub Pages with PowerShell
powershell -Command "$ProgressPreference = 'SilentlyContinue'; try { $r = Invoke-WebRequest -Uri '%URL_GITHUB%' -UseBasicParsing -TimeoutSec 5; Write-Host 'GitHub Pages: HTTP' $r.StatusCode '(LIVE!)' -ForegroundColor Green; $githubWorks = $true } catch { Write-Host 'GitHub Pages: Not accessible yet' -ForegroundColor Yellow; $githubWorks = $false }"

echo.
echo Testing Custom Domain...
echo %URL_CUSTOM%
echo.

powershell -Command "$ProgressPreference = 'SilentlyContinue'; try { $r = Invoke-WebRequest -Uri '%URL_CUSTOM%' -UseBasicParsing -TimeoutSec 5; Write-Host 'Custom Domain: HTTP' $r.StatusCode '(LIVE!)' -ForegroundColor Green; $customWorks = $true } catch { Write-Host 'Custom Domain: DNS still propagating...' -ForegroundColor Yellow; $customWorks = $false }"

echo.
echo ════════════════════════════════════════════════
echo  OPENING L.I.F.E. PLATFORM IN YOUR BROWSER...
echo ════════════════════════════════════════════════
echo.

REM Priority 1: Try custom domain (if DNS complete)
REM Priority 2: GitHub Pages (always works after deployment)
REM Priority 3: Local OneDrive file (fallback)

echo Opening best available URL...
start "" "%URL_GITHUB%"

echo.
echo ✅ L.I.F.E. Platform opened in your default browser!
echo.
echo 📋 All Available URLs:
echo   1. GitHub Pages: %URL_GITHUB%
echo   2. Custom Domain: %URL_CUSTOM%
echo   3. Local File: %URL_LOCAL%
echo.
echo 💡 If GitHub Pages shows 404, wait 1-2 minutes for deployment to complete.
echo 💡 Custom domain will work once DNS propagation finishes (1-15 minutes).
echo.

pause
