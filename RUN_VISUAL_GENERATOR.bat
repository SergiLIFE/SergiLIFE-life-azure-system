@echo off
REM Simple Visual Generator - Just Run This!
REM Copyright 2025 - Sergio Paya Borrull

echo.
echo ============================================================
echo L.I.F.E PLATFORM - VISUAL GENERATOR
echo ============================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python or activate your virtual environment
    pause
    exit /b 1
)

echo [1/2] Generating Logo...
python create_logo.py
echo.

echo [2/2] Generating Screenshot...
python create_screenshot_simple.py
echo.

echo ============================================================
echo CHECKING GENERATED FILES...
echo ============================================================
if exist marketplace_assets (
    echo.
    echo ✅ marketplace_assets folder created!
    echo.
    dir /B marketplace_assets
    echo.
) else (
    echo ❌ marketplace_assets folder not found
    echo Check for errors above
)

echo.
echo ============================================================
echo NEXT STEPS:
echo ============================================================
echo.
echo 1. Open 'marketplace_assets' folder
echo 2. Upload files to Azure Marketplace Partner Center:
echo    - Logo: LIFE_Platform_Logo_280x280.png
echo    - Screenshot: LIFE_Platform_Screenshot_1280x720.png
echo.
echo 3. Run interactive demo: python interactive_demo.py
echo.
echo ============================================================
pause
