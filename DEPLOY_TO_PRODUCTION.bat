@echo off
REM L.I.F.E Platform - Phase 3: Production Deployment
REM Run this AFTER validation and 24h monitoring

cls
echo.
echo ================================================================================
echo      L.I.F.E PLATFORM - PRODUCTION DEPLOYMENT
echo ================================================================================
echo Phase 3: Deploy to Production
echo ================================================================================
echo.
echo WARNING: This will deploy your application to PRODUCTION!
echo.
echo Prerequisites:
echo   [x] Phase 1: Infrastructure deployed
echo   [x] Phase 2: Validation passed
echo   [ ] 24 hours of monitoring completed
echo   [ ] No critical issues found
echo.

set /p CONFIRM="Have you completed 24h monitoring? (yes/no): "

if /i not "%CONFIRM%"=="yes" (
    echo.
    echo Deployment cancelled. Please complete monitoring first.
    pause
    exit /b 0
)

echo.
echo ================================================================================
echo                       STARTING PRODUCTION DEPLOYMENT
echo ================================================================================
echo.

python deploy_to_production.py

if errorlevel 1 (
    echo.
    echo ================================================================================
    echo                         DEPLOYMENT FAILED
    echo ================================================================================
    echo.
    echo Please review the errors above and check the log file.
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo                     PRODUCTION DEPLOYMENT COMPLETE!
echo ================================================================================
echo.
echo L.I.F.E Platform is now LIVE in production!
echo.
echo Monitor for the next 24 hours:
echo   - Application Insights
echo   - Error rates
echo   - Performance metrics
echo   - User traffic
echo.

REM Open Azure Portal
set /p OPEN_PORTAL="Open Azure Portal? (yes/no): "
if /i "%OPEN_PORTAL%"=="yes" (
    start https://portal.azure.com/#resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-rg/overview
)

echo.
pause
