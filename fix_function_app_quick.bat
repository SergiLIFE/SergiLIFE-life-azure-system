@echo off
REM Quick Fix for Azure Function App - Serve L.I.F.E Platform
REM October 18, 2025

echo 🔧 Quick Fix: Azure Function App Deployment
echo =============================================
echo.

REM Check if Azure CLI is available
az --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Azure CLI not found. Please install Azure CLI first.
    echo    Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
    pause
    exit /b 1
)

echo ✅ Azure CLI found

REM Check if logged in
az account show >nul 2>&1
if errorlevel 1 (
    echo ❌ Not logged in to Azure
    echo    Please run: az login
    pause
    exit /b 1
)

echo ✅ Azure authentication confirmed

REM Create basic function app structure
echo 📂 Creating Function App structure...
mkdir function_app 2>nul
mkdir function_app\wwwroot 2>nul
mkdir function_app\HttpTrigger 2>nul

REM Copy HTML file to wwwroot
if exist "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" (
    copy "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" "function_app\wwwroot\index.html" >nul
    echo ✅ Copied L.I.F.E Platform HTML to function app
) else (
    echo ❌ LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html not found
    pause
    exit /b 1
)

REM Create host.json
echo {"version": "2.0","extensionBundle": {"id": "Microsoft.Azure.Functions.ExtensionBundle","version": "[3.*, 4.0.0)"}} > function_app\host.json
echo ✅ Created host.json

REM Create requirements.txt
echo azure-functions>=1.11.0 > function_app\requirements.txt
echo ✅ Created requirements.txt

REM Create function.json for HTTP trigger
echo {"scriptFile": "__init__.py","bindings": [{"authLevel": "anonymous","type": "httpTrigger","direction": "in","name": "req","methods": ["get","post"],"route": "{*route:alpha?}"},{"type": "http","direction": "out","name": "$return"}]} > function_app\HttpTrigger\function.json
echo ✅ Created HTTP trigger function.json

REM Create Python function code
(
echo import azure.functions as func
echo import os
echo from pathlib import Path
echo.
echo def main^(req: func.HttpRequest^) -^> func.HttpResponse:
echo     try:
echo         html_path = Path^(__file__^).parent.parent / "wwwroot" / "index.html"
echo         if html_path.exists^(^):
echo             with open^(html_path, 'r', encoding='utf-8'^) as f:
echo                 html_content = f.read^(^)
echo             return func.HttpResponse^(html_content, status_code=200, mimetype="text/html"^)
echo         else:
echo             return func.HttpResponse^("L.I.F.E Platform Loading...", status_code=200, mimetype="text/html"^)
echo     except Exception as e:
echo         return func.HttpResponse^(f"Error: {str^(e^)}", status_code=500, mimetype="text/html"^)
) > function_app\HttpTrigger\__init__.py
echo ✅ Created Python function code

echo.
echo 🚀 DEPLOYMENT OPTIONS:
echo.
echo OPTION 1 - Auto Deploy (Recommended):
echo   1. cd function_app
echo   2. func azure functionapp publish lifeplatform1760781933 --python
echo.
echo OPTION 2 - Use your existing URLs:
echo   Function App: https://lifeplatform1760781933.azurewebsites.net
echo   Static Web App: https://green-ground-0c65efe0f.1.azurestaticapps.net
echo.
echo The Static Web App should already work correctly.
echo The Function App needs the deployment above to serve your L.I.F.E Platform.
echo.

set /p choice="Deploy now? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo 🚀 Deploying to Azure Function App...
    cd function_app
    func azure functionapp publish lifeplatform1760781933 --python
    
    if errorlevel 1 (
        echo ❌ Deployment failed. You may need to install Azure Functions Core Tools.
        echo    Download from: https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local
    ) else (
        echo.
        echo ✅ SUCCESS! L.I.F.E Platform deployed!
        echo 🌐 Function App: https://lifeplatform1760781933.azurewebsites.net
        echo 🌐 Static Web App: https://green-ground-0c65efe0f.1.azurestaticapps.net
        echo.
        echo Both URLs should now serve your complete L.I.F.E Platform with:
        echo   - October 18, 2025 updates
        echo   - Complete experimentP2L algorithm integration
        echo   - 100-cycle test functionality
        echo   - Fixed error handling
    )
    cd ..
) else (
    echo.
    echo Manual deployment instructions created.
    echo Run the commands above when ready.
)

echo.
pause