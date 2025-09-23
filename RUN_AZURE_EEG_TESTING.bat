@echo off
REM L.I.F.E. Azure EEG Testing Execution Script
REM Sergio Paya Borrull - Azure Marketplace Offer: 9a600d96-fe1e-420b-902a-a0c42c561adb

echo.
echo ==================================================================================
echo 🧠 L.I.F.E. AZURE EEG TESTING - EXECUTING WITH YOUR AZURE ACCOUNT 🧠
echo ==================================================================================
echo ⚡ Tenant: lifecoach121.com
echo ⚡ Azure Account: Sergio Paya Borrull
echo ⚡ Marketplace Offer: 9a600d96-fe1e-420b-902a-a0c42c561adb
echo ==================================================================================
echo.

REM Try different Python paths
echo 🔍 Searching for Python installation...

REM Try Python 3.13 (Microsoft Store)
if exist "C:\Users\Sergio Paya Borrull\AppData\Local\Microsoft\WindowsApps\python3.13.exe" (
    echo ✅ Found Python 3.13 - Executing Azure EEG Testing...
    "C:\Users\Sergio Paya Borrull\AppData\Local\Microsoft\WindowsApps\python3.13.exe" EXECUTE_AZURE_EEG_TESTING.py
    goto :success
)

REM Try standard Python
if exist "C:\Users\Sergio Paya Borrull\AppData\Local\Microsoft\WindowsApps\python.exe" (
    echo ✅ Found Python - Executing Azure EEG Testing...
    "C:\Users\Sergio Paya Borrull\AppData\Local\Microsoft\WindowsApps\python.exe" EXECUTE_AZURE_EEG_TESTING.py
    goto :success
)

REM Try Python in Programs
for /d %%i in ("C:\Users\Sergio Paya Borrull\AppData\Local\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        echo ✅ Found Python in Programs - Executing Azure EEG Testing...
        "%%i\python.exe" EXECUTE_AZURE_EEG_TESTING.py
        goto :success
    )
)

REM Try system Python
if exist "C:\Python*\python.exe" (
    echo ✅ Found System Python - Executing Azure EEG Testing...
    for /d %%i in ("C:\Python*") do (
        if exist "%%i\python.exe" (
            "%%i\python.exe" EXECUTE_AZURE_EEG_TESTING.py
            goto :success
        )
    )
)

echo ❌ Python not found in expected locations.
echo 💡 Please install Python from: https://www.python.org/downloads/
echo    Or enable Python in Microsoft Store
goto :end

:success
echo.
echo ==================================================================================
echo ✅ AZURE EEG TESTING COMPLETED SUCCESSFULLY!
echo 📊 Check azure_eeg_test_outputs/ directory for results
echo ☁️ Azure integration ready for your lifecoach121.com tenant
echo 🐙 GitHub integration prepared for SergiLIFE/SergiLIFE-life-azure-system
echo ==================================================================================

:end
pause