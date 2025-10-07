@echo off
REM Generate all L.I.F.E Platform visuals and run interactive demo
REM Copyright 2025 - Sergio Paya Borrull

echo ============================================================
echo L.I.F.E PLATFORM - COMPLETE VISUAL GENERATION
echo ============================================================
echo.
echo This will generate:
echo   1. Logo (280x280 and 216x216 PNG)
echo   2. Screenshots (1280x720 PNG)
echo   3. Interactive demo walkthrough
echo.
echo Estimated time: 2-5 minutes
echo ============================================================
echo.

pause

REM Step 1: Generate logo
echo.
echo [STEP 1/3] Generating Logo...
echo ----------------------------------------
python create_logo.py
if errorlevel 1 (
    echo ERROR: Logo generation failed!
    pause
    exit /b 1
)
echo ✅ Logo generated successfully!
echo.

REM Step 2: Generate screenshot
echo [STEP 2/3] Generating Screenshot...
echo ----------------------------------------
python create_screenshot_simple.py
if errorlevel 1 (
    echo ERROR: Screenshot generation failed!
    pause
    exit /b 1
)
echo ✅ Screenshot generated successfully!
echo.

REM Step 3: Show what was created
echo [STEP 3/3] Checking Generated Files...
echo ----------------------------------------
echo.
echo Generated files:
echo.
dir /B marketplace_assets 2>nul
echo.

REM Optional: Run interactive demo
echo ============================================================
echo.
choice /C YN /M "Do you want to run the interactive demo walkthrough"

if errorlevel 2 goto skip_demo
if errorlevel 1 goto run_demo

:run_demo
echo.
echo Starting interactive demo...
python interactive_demo.py
goto end

:skip_demo
echo.
echo Skipping interactive demo.
goto end

:end
echo.
echo ============================================================
echo ✅ ALL VISUALS GENERATED!
echo ============================================================
echo.
echo Next steps:
echo   1. Open 'marketplace_assets' folder to see your files
echo   2. Upload to Azure Marketplace Partner Center:
echo      - Logo: LIFE_Platform_Logo_280x280.png
echo      - Screenshot: LIFE_Platform_Screenshot_1280x720.png
echo.
echo   3. Run 'interactive_demo.py' anytime to see user walkthrough
echo.
echo ============================================================
pause
