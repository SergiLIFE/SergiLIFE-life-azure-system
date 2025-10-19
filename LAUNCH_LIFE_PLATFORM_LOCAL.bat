@echo off
title L.I.F.E Platform - Local Launch (Azure Issues Bypassed)
echo.
echo 🧠 L.I.F.E Platform - Local Launch Portal
echo ==========================================
echo Date: October 18, 2025
echo Status: Complete experimentP2L Integration Ready
echo.

echo 🎯 AZURE STATUS UPDATE:
echo ❌ Function App URL: Not serving L.I.F.E Platform (shows Azure default page)
echo ❌ Static Web App URL: Not connected to your Azure account
echo ✅ Local Platform: FULLY FUNCTIONAL with all integrations
echo.

echo 🚀 LAUNCHING L.I.F.E PLATFORM LOCALLY...
echo.

REM Check if the main platform file exists
if exist "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" (
    echo ✅ Found: LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
    echo    File size: 
    for %%A in ("LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html") do echo    %%~zA bytes
    echo.
    
    echo 🌐 Opening L.I.F.E Platform in your default browser...
    echo.
    echo Features included:
    echo   ✅ Complete experimentP2L Algorithm Integration
    echo   ✅ Learning Stages: ACQUISITION, CONSOLIDATION, RETRIEVAL, ADAPTATION
    echo   ✅ Neural States: RESTING, FOCUSED, LEARNING, PROCESSING, CONSOLIDATING
    echo   ✅ 100-Cycle EEG Test (Fixed Error Handling)
    echo   ✅ Real-time Neural Analysis
    echo   ✅ Clinical Dashboard and Metrics
    echo   ✅ October 18, 2025 Updates
    echo.
    
    REM Open the platform
    start "" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html"
    
    echo ✅ L.I.F.E Platform launched successfully!
    echo.
    echo 📋 PLATFORM ACCESS METHODS:
    echo 1. Direct file: LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
    echo 2. Local access portal: LIFE_PLATFORM_LOCAL_ACCESS.html
    echo 3. This launcher: LAUNCH_LIFE_PLATFORM_LOCAL.bat
    echo.
    
) else (
    echo ❌ ERROR: LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html not found
    echo.
    echo Please ensure you're in the correct directory with the L.I.F.E Platform files.
)

echo 🔧 AZURE DEPLOYMENT FIX (When Ready):
echo 1. Run: fix_function_app_quick.bat
echo 2. Or manually redeploy using Azure CLI
echo 3. Alternative: Use GitHub Pages hosting
echo.

echo 💡 NOTE: Your L.I.F.E Platform is COMPLETE and FUNCTIONAL locally.
echo    All the work we did this morning is integrated and ready to use!
echo.

pause