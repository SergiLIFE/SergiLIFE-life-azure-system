@echo off
echo.
echo ======================================================================
echo   SIMPLE HEALTH FUNCTION DEPLOYMENT
echo ======================================================================
echo.

REM Change to user temp to avoid path issues
set TEMP_DIR=%USERPROFILE%\simple_deploy
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

echo [1/4] Copying simple function files...
xcopy health_simple "%TEMP_DIR%\health_simple\" /E /I /Q
copy requirements_minimal.txt "%TEMP_DIR%\requirements.txt" >nul
copy host.json "%TEMP_DIR%\" >nul

echo [2/4] Creating ZIP...
cd /d "%TEMP_DIR%"
tar -a -c -f simple.zip health_simple requirements.txt host.json

echo [3/4] Deploying to Azure...
az functionapp deployment source config-zip --name life-functions-app --resource-group life-platform-rg --src simple.zip

echo [4/4] Waiting and testing...
timeout /t 60 /nobreak >nul

echo Testing: https://life-functions-app.azurewebsites.net/api/health_simple
echo.

REM Cleanup
cd /d "%~dp0"
rmdir /s /q "%TEMP_DIR%"

echo ======================================================================
echo   SIMPLE DEPLOYMENT COMPLETE
echo ======================================================================
echo.
echo Test URL: https://life-functions-app.azurewebsites.net/api/health_simple
echo.
pause