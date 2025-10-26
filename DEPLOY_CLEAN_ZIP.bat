@echo off
echo.
echo ========================================
echo   CLEAN DEPLOYMENT - ZIP METHOD
echo ========================================
echo.

echo [1/3] Creating clean deployment package...
echo.

REM Create temporary deployment directory
if exist "deploy_temp" rmdir /s /q deploy_temp
mkdir deploy_temp

REM Copy only essential files
echo Copying function_app.py...
copy function_app.py deploy_temp\ >nul
copy requirements.txt deploy_temp\ >nul
copy host.json deploy_temp\ >nul

echo Files copied successfully!
echo.

echo [2/3] Creating ZIP package...
cd deploy_temp
powershell -Command "Compress-Archive -Path * -DestinationPath ..\deployment.zip -Force"
cd ..

if exist deployment.zip (
    echo ✅ ZIP created successfully
) else (
    echo ❌ Failed to create ZIP
    pause
    exit /b 1
)
echo.

echo [3/3] Deploying to Azure...
az functionapp deployment source config-zip --name life-functions-app --resource-group life-platform-rg --src deployment.zip
echo.

echo [Cleanup] Removing temporary files...
rmdir /s /q deploy_temp
del deployment.zip
echo.

echo ========================================
echo   DEPLOYMENT COMPLETE
echo ========================================
echo.
echo Waiting 30 seconds for Azure to process...
timeout /t 30 /nobreak >nul
echo.
echo Testing health endpoint...
python test_deployment.py
echo.
pause
