@echo off
REM Azure Credentials Quick Fix Script (Windows)
REM Generates properly formatted Azure service principal credentials for GitHub Actions
REM L.I.F.E Platform - November 2, 2025

setlocal enabledelayedexpansion

echo ==============================================================================
echo Azure Credentials Quick Fix - L.I.F.E Platform (Windows)
echo ==============================================================================
echo.

REM L.I.F.E Platform configuration
set SUBSCRIPTION_ID=5c88cef6-f243-497d-98af-6c6086d575ca
set TENANT_ID=e716161a-5e85-4d6d-82f9-96bcdd2e65ac
set RESOURCE_GROUP=life-platform-prod
set TIMESTAMP=%date:~-4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set SP_NAME=github-actions-life-platform-%TIMESTAMP%

echo Configuration:
echo   Subscription: %SUBSCRIPTION_ID%
echo   Tenant: %TENANT_ID%
echo   Resource Group: %RESOURCE_GROUP%
echo   Service Principal: %SP_NAME%
echo.

REM Check if Azure CLI is installed
where az >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Azure CLI not found!
    echo.
    echo Please install Azure CLI:
    echo   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows
    echo.
    echo Download the MSI installer and run it.
    echo After installation, restart this script.
    echo.
    pause
    exit /b 1
)

echo ✅ Azure CLI found
echo.

REM Check if logged in
echo Checking Azure login status...
az account show >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Not logged in to Azure
    echo.
    echo Launching Azure login...
    az login --tenant %TENANT_ID%
    if %errorlevel% neq 0 (
        echo ❌ Login failed
        pause
        exit /b 1
    )
)

echo ✅ Logged in to Azure
echo.

REM Set the correct subscription
echo Setting L.I.F.E Platform subscription...
az account set --subscription %SUBSCRIPTION_ID%
if %errorlevel% neq 0 (
    echo ❌ Failed to set subscription
    echo.
    echo Available subscriptions:
    az account list --output table
    echo.
    pause
    exit /b 1
)

echo ✅ Subscription set to %SUBSCRIPTION_ID%
echo.

REM Verify resource group exists
echo Verifying resource group exists...
az group show --name %RESOURCE_GROUP% >nul 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Resource group '%RESOURCE_GROUP%' not found
    echo.
    echo Available resource groups:
    az group list --query "[].name" -o table
    echo.
    set /p RESOURCE_GROUP="Enter the resource group name to use: "
)

echo ✅ Resource group '%RESOURCE_GROUP%' found
echo.

REM Generate credentials
echo ==============================================================================
echo Generating Azure Service Principal Credentials
echo ==============================================================================
echo.
echo Creating service principal: %SP_NAME%
echo.

set SCOPE=/subscriptions/%SUBSCRIPTION_ID%/resourceGroups/%RESOURCE_GROUP%

echo Running Azure CLI command...
echo az ad sp create-for-rbac --name "%SP_NAME%" --role contributor --scopes "%SCOPE%" --sdk-auth
echo.

REM Create temporary file for credentials
set CREDS_FILE=%TEMP%\azure_credentials_%TIMESTAMP%.json

REM Create service principal
az ad sp create-for-rbac --name "%SP_NAME%" --role contributor --scopes "%SCOPE%" --sdk-auth > "%CREDS_FILE%" 2>&1

if %errorlevel% neq 0 (
    echo ❌ Failed to create service principal
    echo.
    echo Error output:
    type "%CREDS_FILE%"
    echo.
    del "%CREDS_FILE%" 2>nul
    pause
    exit /b 1
)

echo ✅ Service principal created successfully!
echo.

REM Extract just the JSON from the file (remove deprecation warning lines)
set CLEAN_CREDS_FILE=%TEMP%\azure_credentials_clean_%TIMESTAMP%.json
findstr /V /C:"WARNING" /C:"Option '--sdk-auth'" /C:"deprecated" "%CREDS_FILE%" > "%CLEAN_CREDS_FILE%"

REM Validate JSON format
echo ==============================================================================
echo Validating Credentials Format
echo ==============================================================================
echo.

REM Try to validate with Python if available
where python >nul 2>nul
if %errorlevel% equ 0 (
    python -m json.tool "%CLEAN_CREDS_FILE%" >nul 2>nul
    if %errorlevel% equ 0 (
        echo ✅ JSON format is valid
    ) else (
        echo ⚠️  JSON validation warning - please verify manually
    )
) else (
    echo ℹ️  Python not found, skipping JSON validation
)

echo.

REM Display credentials
echo ==============================================================================
echo Azure Credentials (Copy the entire JSON below)
echo ==============================================================================
echo.
type "%CLEAN_CREDS_FILE%"
echo.

REM Save to permanent location in user's documents
set FINAL_CREDS_FILE=%USERPROFILE%\Documents\azure_credentials_%TIMESTAMP%.json
copy "%CLEAN_CREDS_FILE%" "%FINAL_CREDS_FILE%" >nul

echo ==============================================================================
echo Credentials saved to: %FINAL_CREDS_FILE%
echo ==============================================================================
echo.

REM Display next steps
echo ==============================================================================
echo Next Steps
echo ==============================================================================
echo.
echo 1. The credentials have been copied to your clipboard (if possible)
echo    Otherwise, select and copy the JSON from above
echo.
echo 2. Go to GitHub Secrets:
echo    https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/secrets/actions
echo.
echo 3. Create or update the 'AZURE_CREDENTIALS' secret:
echo    - Click 'New repository secret' or click existing 'AZURE_CREDENTIALS'
echo    - Paste the ENTIRE JSON (nothing before or after)
echo    - Click 'Add secret' or 'Update secret'
echo.
echo 4. Re-run your failed GitHub Actions workflow:
echo    https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions
echo.
echo 5. Monitor the Azure Login step - it should now succeed!
echo.

REM Try to copy to clipboard (requires clip command)
type "%CLEAN_CREDS_FILE%" | clip 2>nul
if %errorlevel% equ 0 (
    echo ✅ Credentials copied to clipboard!
    echo.
)

REM Open GitHub secrets page
echo.
set /p OPEN_GITHUB="Open GitHub Secrets page in browser? (Y/N): "
if /i "%OPEN_GITHUB%"=="Y" (
    start https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/secrets/actions
)

REM Open credentials file
echo.
set /p OPEN_FILE="Open credentials file in Notepad? (Y/N): "
if /i "%OPEN_FILE%"=="Y" (
    notepad "%FINAL_CREDS_FILE%"
)

REM Cleanup temporary files
del "%CREDS_FILE%" 2>nul
del "%CLEAN_CREDS_FILE%" 2>nul

echo.
echo ==============================================================================
echo ✅ Quick Fix Complete!
echo ==============================================================================
echo.
echo Credentials saved to: %FINAL_CREDS_FILE%
echo.
echo IMPORTANT: Delete this file after updating GitHub Secrets:
echo   del "%FINAL_CREDS_FILE%"
echo.
echo Or use File Explorer to delete it from your Documents folder.
echo.

pause
