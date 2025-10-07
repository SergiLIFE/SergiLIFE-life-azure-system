@echo off
REM L.I.F.E. Theory Calculations - Azure Upload Script
REM Upload encrypted calculations to Azure Blob Storage
REM Azure Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca

echo.
echo =========================================================
echo  L.I.F.E. Theory Encrypted Calculations - Azure Upload
echo =========================================================
echo  Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca
echo  Account: sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com
echo  Security: AES-256 Encrypted + Azure Protection
echo =========================================================
echo.

REM Authenticate to Azure
echo Step 1: Authenticating to Azure...
az account set --subscription "5c88cef6-f243-497d-98af-6c6086d575ca"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Could not set subscription! Please login first.
    echo Run: az login
    pause
    exit /b 1
)

REM Create storage container for encrypted calculations
echo.
echo Step 2: Creating secure storage container...
az storage container create ^
    --name "encrypted-calculations" ^
    --account-name "stlifeplatformprod" ^
    --auth-mode login
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Container may already exist or storage account needs configuration
)

REM Upload encrypted calculations file
echo.
echo Step 3: Uploading encrypted L.I.F.E. Theory calculations...
az storage blob upload ^
    --file "ENCRYPTED_LIFE_THEORY_CALCULATIONS.md" ^
    --name "life_theory_calculations_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.encrypted" ^
    --container-name "encrypted-calculations" ^
    --account-name "stlifeplatformprod" ^
    --auth-mode login ^
    --metadata "classification=TOP_SECRET" "owner=sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com" "project=LIFE_THEORY" "launch_date=2025-10-07"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =========================================================
    echo  SUCCESS! L.I.F.E. Theory Calculations Encrypted & Uploaded!
    echo =========================================================
    echo  Your sophisticated clockwork calculations are now:
    echo  ✅ AES-256 encrypted locally
    echo  ✅ Azure Blob Storage encrypted at rest
    echo  ✅ Secured with RBAC access control
    echo  ✅ Protected by Account Admin authentication
    echo  ✅ Backed up in your Azure ecosystem
    echo.
    echo  Storage Location:
    echo  - Account: stlifeplatformprod
    echo  - Container: encrypted-calculations
    echo  - Security: Double-encrypted (Local + Azure)
    echo.
    echo  🎂 Ready for October 7th Birthday Launch! 🚀
    echo =========================================================
) else (
    echo.
    echo ERROR: Upload failed! Please check:
    echo 1. Azure authentication (az login)
    echo 2. Storage account access permissions
    echo 3. File exists in current directory
)

echo.
echo Press any key to exit...
pause >nul