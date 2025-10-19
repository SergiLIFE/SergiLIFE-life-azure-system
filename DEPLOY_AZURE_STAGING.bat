@echo off
REM L.I.F.E Platform Azure Staging Deployment
REM Copyright 2025 - Sergio Paya Borrull

echo.
echo ================================================================================
echo      L.I.F.E PLATFORM - AZURE STAGING DEPLOYMENT
echo ================================================================================
echo Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
echo Production-Ready: September 27, 2025
echo Target Revenue: $345K Q4 2025 to $50.7M by 2029
echo ================================================================================
echo.

echo Step 1: Verifying Azure CLI authentication...
az account show >nul 2>&1
if errorlevel 1 (
    echo ERROR: Azure CLI not authenticated
    echo Please run: az login
    pause
    exit /b 1
)

echo Step 2: Setting subscription...
az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca
if errorlevel 1 (
    echo ERROR: Failed to set subscription
    pause
    exit /b 1
)

echo Step 3: Running deployment script...
echo.
python DEPLOY_LIFE_AZURE_STAGING.py

if errorlevel 1 (
    echo.
    echo ERROR: Deployment failed
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo    DEPLOYMENT COMPLETED SUCCESSFULLY!
echo ================================================================================
echo.
echo Check AZURE_DEPLOYMENT_SUMMARY.json for details
echo.
pause
