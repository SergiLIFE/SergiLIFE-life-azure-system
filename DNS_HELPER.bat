@echo off
REM ========================================
REM DNS Configuration Helper for lifecoach-121.com
REM Quick DNS verification and troubleshooting
REM ========================================

echo.
echo ████████████████████████████████████████████████
echo  DNS CONFIGURATION HELPER
echo  lifecoach-121.com → L.I.F.E. Platform
echo ████████████████████████████████████████████████
echo.

:MENU
echo.
echo ═══ MENU ═══
echo 1. Check current DNS status
echo 2. Flush DNS cache (fix stale records)
echo 3. Open GitHub Pages settings
echo 4. Open online DNS checker
echo 5. Test GitHub Pages URL (works now)
echo 6. Test custom domain URL (after DNS)
echo 7. View DNS configuration guide
echo 8. Show DNS records you need to add
echo 0. Exit
echo.

set /p choice="Select option (0-8): "

if "%choice%"=="1" goto CHECK_DNS
if "%choice%"=="2" goto FLUSH_DNS
if "%choice%"=="3" goto OPEN_GITHUB
if "%choice%"=="4" goto OPEN_CHECKER
if "%choice%"=="5" goto TEST_GITHUB
if "%choice%"=="6" goto TEST_CUSTOM
if "%choice%"=="7" goto VIEW_GUIDE
if "%choice%"=="8" goto SHOW_RECORDS
if "%choice%"=="0" goto END
echo Invalid choice!
goto MENU

:CHECK_DNS
echo.
echo ═══════════════════════════════════════
echo  Checking DNS Status for lifecoach-121.com
echo ═══════════════════════════════════════
echo.

echo [1/3] Checking A records...
nslookup lifecoach-121.com

echo.
echo [2/3] Checking www CNAME...
nslookup www.lifecoach-121.com

echo.
echo [3/3] Expected GitHub Pages IPs:
echo   185.199.108.153
echo   185.199.109.153
echo   185.199.110.153
echo   185.199.111.153
echo.

echo ═══════════════════════════════════════
echo  DNS Check Complete!
echo ═══════════════════════════════════════
echo.
echo ✅ If you see the GitHub IPs above, DNS is configured correctly
echo ⏳ If you see different IPs or errors, DNS needs configuration or more time
echo.

pause
goto MENU

:FLUSH_DNS
echo.
echo ═══════════════════════════════════════
echo  Flushing DNS Cache...
echo ═══════════════════════════════════════
echo.

ipconfig /flushdns

echo.
echo ✅ DNS cache cleared!
echo 💡 Now your computer will fetch fresh DNS records
echo.

pause
goto MENU

:OPEN_GITHUB
echo.
echo Opening GitHub Pages settings in browser...
start https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/pages
echo.
echo 💡 Look for "DNS check is in progress" message
echo 💡 When it shows green checkmark, DNS is validated!
echo.

pause
goto MENU

:OPEN_CHECKER
echo.
echo Opening online DNS checker...
start https://dnschecker.org
echo.
echo 📋 Instructions:
echo   1. Enter: lifecoach-121.com
echo   2. Select: A record
echo   3. Click Search
echo   4. Wait for green checkmarks worldwide
echo.

pause
goto MENU

:TEST_GITHUB
echo.
echo ═══════════════════════════════════════
echo  Testing GitHub Pages URL (This should work NOW!)
echo ═══════════════════════════════════════
echo.

set URL_GITHUB=https://sergilife.github.io/SergiLIFE-life-azure-system/life-theory-platform.html

echo Testing: %URL_GITHUB%
echo.

powershell -Command "$ProgressPreference = 'SilentlyContinue'; try { $r = Invoke-WebRequest -Uri '%URL_GITHUB%' -UseBasicParsing -TimeoutSec 10; Write-Host 'SUCCESS! HTTP Status:' $r.StatusCode -ForegroundColor Green; Write-Host 'Page Size:' $r.Content.Length 'bytes' -ForegroundColor Green; Write-Host '' ; Write-Host 'Opening in browser...' -ForegroundColor Cyan } catch { Write-Host 'ERROR:' $_.Exception.Message -ForegroundColor Red }"

start "" "%URL_GITHUB%"

echo.
echo ✅ GitHub Pages URL opened in browser!
echo.

pause
goto MENU

:TEST_CUSTOM
echo.
echo ═══════════════════════════════════════
echo  Testing Custom Domain URL
echo ═══════════════════════════════════════
echo.

set URL_CUSTOM=https://lifecoach-121.com/life-theory-platform.html

echo Testing: %URL_CUSTOM%
echo.

powershell -Command "$ProgressPreference = 'SilentlyContinue'; try { $r = Invoke-WebRequest -Uri '%URL_CUSTOM%' -UseBasicParsing -TimeoutSec 10; Write-Host 'SUCCESS! HTTP Status:' $r.StatusCode -ForegroundColor Green; Write-Host 'Page Size:' $r.Content.Length 'bytes' -ForegroundColor Green; Write-Host 'DNS is working!' -ForegroundColor Green; Write-Host '' ; Write-Host 'Opening in browser...' -ForegroundColor Cyan; $success = $true } catch { Write-Host 'Not accessible yet - DNS still propagating' -ForegroundColor Yellow; Write-Host 'Error:' $_.Exception.Message -ForegroundColor Red; $success = $false }"

echo.
echo 💡 If this fails, DNS needs more time to propagate (5-60 minutes typical)
echo.

pause
goto MENU

:VIEW_GUIDE
echo.
echo Opening DNS Configuration Guide...
start DNS_CONFIGURATION_GUIDE.md
echo.
echo ✅ Guide opened in your default markdown viewer
echo.

pause
goto MENU

:SHOW_RECORDS
echo.
echo ████████████████████████████████████████████████
echo  DNS RECORDS TO ADD AT YOUR DOMAIN REGISTRAR
echo ████████████████████████████████████████████████
echo.
echo OPTION A: Add these 4 A records (Recommended)
echo ───────────────────────────────────────────────
echo Type: A     │ Name: @   │ Value: 185.199.108.153 │ TTL: 3600
echo Type: A     │ Name: @   │ Value: 185.199.109.153 │ TTL: 3600
echo Type: A     │ Name: @   │ Value: 185.199.110.153 │ TTL: 3600
echo Type: A     │ Name: @   │ Value: 185.199.111.153 │ TTL: 3600
echo.
echo OPTION B: Add this CNAME (if registrar allows)
echo ───────────────────────────────────────────────
echo Type: CNAME │ Name: @   │ Value: sergilife.github.io │ TTL: 3600
echo.
echo OPTIONAL: Add www subdomain
echo ───────────────────────────────────────────────
echo Type: CNAME │ Name: www │ Value: sergilife.github.io │ TTL: 3600
echo.
echo ════════════════════════════════════════════════
echo.
echo 📋 Steps to add these records:
echo   1. Log into your domain registrar (where you bought lifecoach-121.com)
echo   2. Find "DNS Management" or "DNS Settings"
echo   3. Click "Add Record" or "Add DNS Record"
echo   4. Copy the values above exactly
echo   5. Save changes
echo   6. Wait 5-60 minutes for propagation
echo.
echo 💡 Don't know your registrar? Check https://who.is/whois/lifecoach-121.com
echo.

pause
goto MENU

:END
echo.
echo DNS Configuration Helper closed.
echo.
echo 📋 Quick Reference:
echo   GitHub Pages URL: https://sergilife.github.io/SergiLIFE-life-azure-system/life-theory-platform.html
echo   Custom Domain:    https://lifecoach-121.com/life-theory-platform.html
echo   DNS Guide:        DNS_CONFIGURATION_GUIDE.md
echo.
pause
exit
