@echo off
REM ================================================================
REM AZURE STORAGE RECOVERY SCRIPT
REM Check Azure Storage for original uncorrupted algorithm files
REM ================================================================

echo.
echo ========================================================
echo   CHECKING AZURE STORAGE FOR ORIGINAL FILES
echo ========================================================
echo.

REM Step 1: Login to Azure (interactive)
echo [1/5] Logging into Azure...
echo Please complete the login in your browser...
az login --tenant e716161a-5e85-4d6d-82f9-96bcdd2e65ac
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Azure login failed
    pause
    exit /b 1
)

REM Step 2: Set subscription
echo.
echo [2/5] Setting subscription...
az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca

REM Step 3: List storage accounts
echo.
echo [3/5] Finding your storage accounts...
az storage account list --output table

REM Step 4: List containers in stlifeplatformprod
echo.
echo [4/5] Checking containers in stlifeplatformprod...
az storage container list --account-name stlifeplatformprod --output table --auth-mode login

REM Step 5: List blobs in each container
echo.
echo [5/5] Searching for algorithm files...
echo.
echo === Checking for experimentP2L files ===
az storage blob list --account-name stlifeplatformprod --container-name algorithms --output table --auth-mode login 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Container 'algorithms' not found, trying other names...
)

az storage blob list --account-name stlifeplatformprod --container-name python-core --output table --auth-mode login 2>nul
az storage blob list --account-name stlifeplatformprod --container-name backups --output table --auth-mode login 2>nul
az storage blob list --account-name stlifeplatformprod --container-name life-platform --output table --auth-mode login 2>nul

echo.
echo ========================================================
echo   RECOVERY INSTRUCTIONS
echo ========================================================
echo.
echo If you found the file in Azure Storage, download it with:
echo.
echo   az storage blob download --account-name stlifeplatformprod ^
echo      --container-name [CONTAINER_NAME] ^
echo      --name [FILE_NAME] ^
echo      --file recovered_from_azure.py ^
echo      --auth-mode login
echo.
echo Then check the file size to confirm it's the larger version!
echo.
pause
