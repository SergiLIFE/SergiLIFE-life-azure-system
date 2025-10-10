@echo off
REM Campaign Trigger Batch Script for L.I.F.E. Platform
REM Copyright 2025 - Sergio Paya Borrull

echo ========================================
echo L.I.F.E. Platform Campaign Trigger
echo ========================================
echo.

echo 1. Normal Campaign Check (with UI validation)
echo 2. Emergency Campaign Launch (with safety checks)
echo 3. GitHub Actions Manual Trigger
echo 4. System Status Check
echo 5. UI Operational Validation Only
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Step 1: Validating UI operational status...
    python ui_operational_validator.py
    if %errorlevel% equ 0 (
        echo UI validation passed - system operational
        echo.
        echo Step 2: Running campaign trigger...
        python campaign_automatic_trigger.py
    ) else (
        echo UI validation failed - system not ready for triggering
        echo Please check the validation report in logs/ui_validation_report.md
    )
    goto end
)

if "%choice%"=="2" (
    echo.
    echo EMERGENCY CAMPAIGN TRIGGER INITIATED
    echo Step 1: Quick UI validation...
    python ui_operational_validator.py
    if %errorlevel% equ 0 (
        echo UI validation passed
        echo.
        echo Step 2: Creating emergency trigger...
        python campaign_automatic_trigger.py emergency
        echo.
        echo Step 3: Executing emergency campaign...
        python campaign_automatic_trigger.py
    ) else (
        echo UI validation failed - emergency trigger aborted for safety
        echo Manual intervention may be required
    )
    goto end
)

if "%choice%"=="3" (
    echo.
    echo Triggering GitHub Actions workflow manually...
    echo This requires GitHub CLI (gh) to be installed and authenticated.
    echo.
    gh workflow run campaign-launcher.yml --repo SergiLIFE/SergiLIFE-life-azure-system -f campaign_type=marketplace_promotion -f target_audience=all_segments
    echo.
    echo GitHub Actions workflow triggered!
    goto end
)

if "%choice%"=="4" (
    echo.
    echo Checking system status...
    python -c "import campaign_automatic_trigger; import asyncio; asyncio.run(campaign_automatic_trigger.CampaignAutomaticTrigger().get_campaign_status())"
    goto end
)

if "%choice%"=="5" (
    echo.
    echo Running UI Operational Validation...
    python ui_operational_validator.py
    echo.
    echo Check logs/ui_validation_report.md for detailed results.
    goto end
)

echo Invalid choice. Please run the script again.

:end
echo.
echo Press any key to exit...
pause >nul