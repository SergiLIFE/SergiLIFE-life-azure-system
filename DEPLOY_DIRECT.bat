@echo off
setlocal enabledelayedexpansion

echo.
echo ======================================================================
echo   L.I.F.E. PLATFORM - DIRECT AZURE DEPLOYMENT (No func CLI)
echo ======================================================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo [1/5] Verifying files...
if not exist "function_app.py" (
    echo   ERROR: function_app.py not found
    pause
    exit /b 1
)
if not exist "requirements.txt" (
    echo   ERROR: requirements.txt not found
    pause
    exit /b 1
)
if not exist "host.json" (
    echo   ERROR: host.json not found
    pause
    exit /b 1
)
echo   All files present
echo.

echo [2/5] Enabling run-from-package deployment...
az functionapp config appsettings set --name life-functions-app --resource-group life-platform-rg --settings WEBSITE_RUN_FROM_PACKAGE=1 >nul 2>&1
echo   Done
echo.

echo [3/5] Using Azure CLI to deploy (via zip)...
echo   Creating deployment package...

REM Use temp directory in user profile (no path issues)
set TEMP_DIR=%USERPROFILE%\life_deploy_temp
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

REM Copy files
copy function_app.py "%TEMP_DIR%\" >nul
copy requirements.txt "%TEMP_DIR%\" >nul
copy host.json "%TEMP_DIR%\" >nul

echo   Files copied to: %TEMP_DIR%
echo.

echo [4/5] Creating and deploying ZIP...
cd /d "%TEMP_DIR%"

REM Create zip using tar (built into Windows 10+)
tar -a -c -f deploy.zip function_app.py requirements.txt host.json

if exist deploy.zip (
    echo   ZIP created successfully
    echo   Uploading to Azure...
    echo.
    
    az functionapp deployment source config-zip --name life-functions-app --resource-group life-platform-rg --src deploy.zip
    
    echo.
    echo   Upload complete
) else (
    echo   ERROR: Failed to create ZIP
    cd /d "%~dp0"
    rmdir /s /q "%TEMP_DIR%"
    pause
    exit /b 1
)

cd /d "%~dp0"
rmdir /s /q "%TEMP_DIR%"
echo.

echo [5/5] Waiting for deployment to process (60 seconds)...
timeout /t 60 /nobreak >nul
echo   Done
echo.

echo Restarting Function App...
az functionapp restart --name life-functions-app --resource-group life-platform-rg
echo.

echo Waiting 30 more seconds for restart...
timeout /t 30 /nobreak >nul
echo.

echo ======================================================================
echo   TESTING DEPLOYMENT
echo ======================================================================
echo.

python test_deployment.py

echo.
echo ======================================================================
echo   DEPLOYMENT COMPLETE
echo ======================================================================
echo.
pause
