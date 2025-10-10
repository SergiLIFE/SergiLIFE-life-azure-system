@echo off
REM Quick Launch Script for L.I.F.E. Platform Campaign Trigger
REM This script helps you run the campaign triggers from any directory

echo ========================================
echo L.I.F.E. Platform - Quick Launch
echo ========================================
echo.

REM Change to project directory
set PROJECT_DIR=c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system

echo Changing to project directory...
cd /d "%PROJECT_DIR%"

echo Current directory: %CD%
echo.

REM Check if files exist
if exist "TRIGGER_CAMPAIGN.ps1" (
    echo ✅ PowerShell script found
) else (
    echo ❌ PowerShell script missing
    goto end
)

if exist "TRIGGER_CAMPAIGN.bat" (
    echo ✅ Batch script found
) else (
    echo ❌ Batch script missing
    goto end
)

echo.
echo ========================================
echo Choose your method:
echo ========================================
echo.
echo 1. Use Batch Script (Easiest - works in CMD)
echo 2. Use PowerShell Script (Advanced)
echo 3. Use Python Directly
echo 4. Show Correct Commands Only
echo.

set /p method="Enter your choice (1-4): "

if "%method%"=="1" (
    echo.
    echo 🚀 Launching batch script...
    call TRIGGER_CAMPAIGN.bat
    goto end
)

if "%method%"=="2" (
    echo.
    echo 🚀 Instructions for PowerShell:
    echo.
    echo From CMD, run:
    echo   powershell -ExecutionPolicy Bypass -File "TRIGGER_CAMPAIGN.ps1" -Action normal
    echo.
    echo Or open PowerShell and run:
    echo   .\TRIGGER_CAMPAIGN.ps1 -Action normal
    echo.
    set /p runps="Run PowerShell command now? (y/n): "
    if /i "%runps%"=="y" (
        powershell -ExecutionPolicy Bypass -File "TRIGGER_CAMPAIGN.ps1" -Action normal
    )
    goto end
)

if "%method%"=="3" (
    echo.
    echo 🚀 Running Python directly...
    echo Step 1: UI Validation
    python simple_ui_test.py
    if %errorlevel% equ 0 (
        echo.
        echo Step 2: Campaign Trigger
        python campaign_automatic_trigger.py
    ) else (
        echo.
        echo ❌ UI validation failed - not proceeding with trigger
    )
    goto end
)

if "%method%"=="4" (
    echo.
    echo 📋 CORRECT COMMANDS TO USE:
    echo.
    echo === From Command Prompt (CMD) ===
    echo 1. Navigate to project directory:
    echo    cd "c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
    echo.
    echo 2a. Use batch script (easiest):
    echo    TRIGGER_CAMPAIGN.bat
    echo.
    echo 2b. Use PowerShell from CMD:
    echo    powershell -ExecutionPolicy Bypass -File "TRIGGER_CAMPAIGN.ps1" -Action normal
    echo    powershell -ExecutionPolicy Bypass -File "TRIGGER_CAMPAIGN.ps1" -Action emergency
    echo    powershell -ExecutionPolicy Bypass -File "TRIGGER_CAMPAIGN.ps1" -Action validate
    echo.
    echo 2c. Use Python directly:
    echo    python simple_ui_test.py
    echo    python campaign_automatic_trigger.py
    echo.
    echo === From PowerShell ===
    echo 1. Navigate to project directory:
    echo    cd "c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
    echo.
    echo 2. Run PowerShell script:
    echo    .\TRIGGER_CAMPAIGN.ps1 -Action normal
    echo    .\TRIGGER_CAMPAIGN.ps1 -Action emergency
    echo    .\TRIGGER_CAMPAIGN.ps1 -Action validate
    echo.
    goto end
)

echo Invalid choice.

:end
echo.
echo ========================================
echo Press any key to exit...
pause >nul