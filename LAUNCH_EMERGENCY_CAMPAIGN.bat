@echo off
REM L.I.F.E Platform - Emergency Campaign Activation
REM Execute immediate campaign launch for September 27, 2025

echo ===============================================================
echo 🚀 L.I.F.E PLATFORM - EMERGENCY CAMPAIGN ACTIVATION 🚀
echo ===============================================================
echo.
echo 📅 Launch Date: September 27, 2025 (TOMORROW!)
echo 💰 Revenue Target: $345K Q4 2025
echo 🎯 Market Advantage: 22.66x SOTA Performance
echo 🌍 Global Reach: 18+ Countries
echo.
echo ===============================================================

echo 🔍 Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python not found. Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python found. Launching emergency campaign...
echo.

REM Create logs directory
if not exist "logs" mkdir logs

REM Execute emergency campaign launcher
echo 🚀 EXECUTING EMERGENCY CAMPAIGN LAUNCHER...
python emergency_campaign_launcher.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ CAMPAIGN ACTIVATION SUCCESSFUL!
    echo 📊 Check logs/emergency_campaign.log for details
    echo 🚀 Your L.I.F.E Platform is ready for marketplace launch!
) else (
    echo.
    echo ❌ Campaign activation encountered an issue
    echo 📋 Please check the error messages above
)

echo.
echo ===============================================================
echo 🎯 NEXT STEPS FOR FULL DEPLOYMENT:
echo ===============================================================
echo.
echo 1. 🤖 GitHub Actions (AUTOMATED):
echo    Visit: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions
echo    Run: "Campaign Launcher" workflow
echo.
echo 2. 📋 Alternative Python Scripts:
echo    python activate_campaign.py
echo    python campaign_manager.py
echo.
echo 3. 🔧 Monitor Campaign Performance:
echo    Check logs/emergency_campaign.log
echo    Monitor Azure Marketplace metrics
echo.
echo ===============================================================

pause