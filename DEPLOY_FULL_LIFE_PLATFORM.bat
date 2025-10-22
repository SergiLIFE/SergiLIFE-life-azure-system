@echo off
REM DEPLOY_FULL_LIFE_PLATFORM.bat - Deploys complete L.I.F.E Platform

echo ======================================================================
echo  DEPLOY FULL L.I.F.E PLATFORM - Complete System
echo ======================================================================
echo.

REM Use the working temp directory approach
set TEMP_DEPLOY=%USERPROFILE%\life_full_deploy
if exist "%TEMP_DEPLOY%" rmdir /s /q "%TEMP_DEPLOY%"
mkdir "%TEMP_DEPLOY%"
cd /d "%TEMP_DEPLOY%"

echo [1/4] Creating full L.I.F.E Platform package...

REM Copy the working function_app.py from the original location
copy "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system\function_app.py" . >nul
copy "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system\requirements.txt" . >nul
copy "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system\host.json" . >nul

echo [2/4] Creating deployment ZIP...
tar -a -c -f full_deployment.zip function_app.py requirements.txt host.json

echo [3/4] Deploying full L.I.F.E Platform to Azure...
REM Try both resource groups to find the correct one
az functionapp deployment source config-zip --resource-group life-platform-prod --name life-functions-app --src full_deployment.zip 2>nul
if errorlevel 1 (
    echo Trying alternative resource group...
    az functionapp deployment source config-zip --resource-group life-platform-rg --name life-functions-app --src full_deployment.zip
)

echo [4/4] Waiting for deployment and testing...
echo Waiting 90 seconds for Azure to process the full platform...
timeout /t 90 /nobreak >nul

echo.
echo Testing endpoints:
echo.

echo 1. Health Check:
python -c "import urllib.request; import json; response = urllib.request.urlopen('https://life-functions-app.azurewebsites.net/api/health_check', timeout=10); data = json.loads(response.read()); print('✅ HEALTH:', data.get('status'))" 2>nul || echo "❌ Health endpoint failed"

echo.
echo 2. EEG Processor (needs auth):
python -c "import urllib.request; response = urllib.request.urlopen('https://life-functions-app.azurewebsites.net/api/eeg_processor', timeout=10); print('✅ EEG endpoint accessible')" 2>nul || echo "❌ EEG endpoint (expected - needs auth)"

echo.
echo ======================================================================
echo  FULL L.I.F.E PLATFORM DEPLOYMENT COMPLETE
echo ======================================================================
echo.
echo Available endpoints:
echo   Health: https://life-functions-app.azurewebsites.net/api/health_check
echo   EEG:    https://life-functions-app.azurewebsites.net/api/eeg_processor  
echo   Analytics: https://life-functions-app.azurewebsites.net/api/analytics_monitor
echo   Learning:  https://life-functions-app.azurewebsites.net/api/learning_api
echo   Campaign:  https://life-functions-app.azurewebsites.net/api/campaign_automation
echo.

REM Cleanup
cd /d "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
rmdir /s /q "%TEMP_DEPLOY%"
pause