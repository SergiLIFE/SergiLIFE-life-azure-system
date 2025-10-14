@echo off
cls
echo ================================================================
echo 🚀 L.I.F.E Platform - Interactive Launch Demo 
echo ================================================================
echo Learning Individually From Experience - October 15, 2025 Demo
echo Revolutionary Neuroplasticity & EEG Analysis Platform
echo Copyright 2025 - Sergio Paya Borrull
echo ================================================================
echo.

echo 🔍 Checking for Interactive Demo Platform...
if exist "LIFE_PLATFORM_INTERACTIVE_LAUNCH_DEMO.html" (
    echo ✅ Interactive Demo Platform found!
    echo.
    echo 🌟 Platform Features Available:
    echo    ✅ Interactive Launch Demo
    echo    ✅ Real-time Performance Metrics  
    echo    ✅ Admin Intelligence Panel
    echo    ✅ Personal Search Integration
    echo    ✅ Neuroplasticity Analysis
    echo    ✅ EEG Processing Visualization
    echo    ✅ Azure Marketplace Integration
    echo.
    echo 🚀 Launching Interactive Demo Platform...
    start "" "LIFE_PLATFORM_INTERACTIVE_LAUNCH_DEMO.html"
    echo.
    echo 🎉 Interactive Demo launched successfully!
    echo.
    echo 📊 Demo Capabilities:
    echo    • Interactive demos and tutorials
    echo    • Real-time system monitoring
    echo    • Performance analytics
    echo    • Azure cloud integration
    echo    • Educational scenarios
    echo.
    echo 💡 Tip: Use the admin panel for advanced features
    echo 🌐 Platform will open in your default browser
    echo.
) else (
    echo ❌ Interactive Demo Platform not found!
    echo Expected: LIFE_PLATFORM_INTERACTIVE_LAUNCH_DEMO.html
    echo.
    echo 💡 Available HTML files in current directory:
    dir *.html /b 2>nul
    echo.
)

echo ================================================================
echo 🎭 L.I.F.E Platform Interactive Demo Ready
echo ================================================================
echo.
echo Press any key to close this launcher...
pause >nul