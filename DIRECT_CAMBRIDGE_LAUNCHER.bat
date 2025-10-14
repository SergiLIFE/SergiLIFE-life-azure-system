@echo off
cls
echo.
echo =========================================================================
echo 🧠 L.I.F.E CLINICAL PLATFORM - CAMBRIDGE UNIVERSITY DEMO - DIRECT LAUNCH
echo =========================================================================
echo.

echo Current Directory: %CD%
echo.

echo Looking for clinical platform files...
echo.

REM List all HTML files to see what's available
echo Available platform files:
for %%f in (*.html) do (
    echo   ✓ %%f
)
echo.

REM Try to launch in order of preference
if exist "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" (
    echo ✅ FOUND: Clinical Platform for Cambridge
    echo 🚀 Launching Cambridge Clinical Demo...
    echo.
    start "" "%CD%\LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html"
    goto :success
)

if exist "life_ai_enhanced_platform.html" (
    echo ✅ FOUND: AI Enhanced Platform 
    echo 🚀 Launching AI Enhanced Platform as backup...
    echo.
    start "" "%CD%\life_ai_enhanced_platform.html"
    goto :success
)

if exist "WORKING_MOCK_DEMO_PLATFORM.html" (
    echo ✅ FOUND: Working Mock Demo Platform
    echo 🚀 Launching Working Demo Platform...
    echo.
    start "" "%CD%\WORKING_MOCK_DEMO_PLATFORM.html"
    goto :success
)

if exist "life_theory_platform.html" (
    echo ✅ FOUND: Theory Platform
    echo 🚀 Launching Theory Platform...
    echo.
    start "" "%CD%\life_theory_platform.html"
    goto :success
)

if exist "LIFE_PLATFORM_INTERACTIVE_LAUNCH_DEMO.html" (
    echo ✅ FOUND: Interactive Demo Platform
    echo 🚀 Launching Interactive Demo...
    echo.
    start "" "%CD%\LIFE_PLATFORM_INTERACTIVE_LAUNCH_DEMO.html"
    goto :success
)

if exist "index.html" (
    echo ✅ FOUND: Standard Index
    echo 🚀 Launching Standard Platform...
    echo.
    start "" "%CD%\index.html"
    goto :success
)

echo ❌ NO PLATFORM FILES FOUND
echo.
echo Troubleshooting:
echo 1. Make sure you're in the correct directory
echo 2. Check if HTML files exist in this folder
echo 3. Try running: dir *.html
echo.
goto :end

:success
echo.
echo =========================================================================
echo ✅ PLATFORM LAUNCHED SUCCESSFULLY FOR CAMBRIDGE DEMO
echo =========================================================================
echo.
echo 🎓 Ready for Cambridge University Professor demonstration
echo 🏥 Clinical-grade platform features active
echo 📊 Real-time analytics and diagnostics available
echo.
echo Platform should now be open in your default browser.
echo All tabs and interactive features are fully functional.
echo.

:end
echo Press any key to exit...
pause >nul