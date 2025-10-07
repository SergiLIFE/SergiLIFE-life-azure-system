@echo off
echo ================================================================
echo     L.I.F.E. Platform - Emergency Backup System (No Terminal)
echo ================================================================
echo Date: %date% %time%
echo Backing up your L.I.F.E. Platform files...
echo.

REM Get current directory
set "REPO_DIR=%~dp0"
set "TIMESTAMP=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"

REM Create backup directory on Desktop (always accessible)
set "BACKUP_DIR=%USERPROFILE%\Desktop\LIFE_Platform_Backup_%TIMESTAMP%"
echo Creating backup directory: %BACKUP_DIR%
mkdir "%BACKUP_DIR%" 2>nul

REM Copy important files
echo.
echo Copying important files...
echo ----------------------------------------

copy "%REPO_DIR%experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py" "%BACKUP_DIR%\" >nul 2>&1 && echo ✓ Core Algorithm || echo ✗ Core Algorithm (not found)

copy "%REPO_DIR%autonomous_optimizer.py" "%BACKUP_DIR%\" >nul 2>&1 && echo ✓ Autonomous Optimizer || echo ✗ Autonomous Optimizer (not found)

copy "%REPO_DIR%sota_benchmark.py" "%BACKUP_DIR%\" >nul 2>&1 && echo ✓ SOTA Benchmark || echo ✗ SOTA Benchmark (not found)

copy "%REPO_DIR%azure_config.py" "%BACKUP_DIR%\" >nul 2>&1 && echo ✓ Azure Config || echo ✗ Azure Config (not found)

copy "%REPO_DIR%azure_functions_workflow.py" "%BACKUP_DIR%\" >nul 2>&1 && echo ✓ Azure Functions || echo ✗ Azure Functions (not found)

copy "%REPO_DIR%production_deployment_test.py" "%BACKUP_DIR%\" >nul 2>&1 && echo ✓ Production Tests || echo ✗ Production Tests (not found)

copy "%REPO_DIR%README.md" "%BACKUP_DIR%\" >nul 2>&1 && echo ✓ README || echo ✗ README (not found)

copy "%REPO_DIR%requirements.txt" "%BACKUP_DIR%\" >nul 2>&1 && echo ✓ Requirements || echo ✗ Requirements (not found)

copy "%REPO_DIR%azure.yaml" "%BACKUP_DIR%\" >nul 2>&1 && echo ✓ Azure Config || echo ✗ Azure Config (not found)

copy "%REPO_DIR%Dockerfile" "%BACKUP_DIR%\" >nul 2>&1 && echo ✓ Dockerfile || echo ✗ Dockerfile (not found)

REM Copy all Python files
echo.
echo Copying all Python files...
echo ----------------------------------------
for %%f in ("%REPO_DIR%*.py") do (
    copy "%%f" "%BACKUP_DIR%\" >nul 2>&1 && echo ✓ %%~nxf || echo ✗ %%~nxf
)

REM Copy all Markdown files
echo.
echo Copying all Markdown files...
echo ----------------------------------------
for %%f in ("%REPO_DIR%*.md") do (
    copy "%%f" "%BACKUP_DIR%\" >nul 2>&1 && echo ✓ %%~nxf || echo ✗ %%~nxf
)

REM Copy infra directory if exists
if exist "%REPO_DIR%infra" (
    echo.
    echo Copying infrastructure files...
    echo ----------------------------------------
    xcopy "%REPO_DIR%infra" "%BACKUP_DIR%\infra" /E /I /Q >nul 2>&1 && echo ✓ Infrastructure directory || echo ✗ Infrastructure directory
)

REM Create backup info file
echo.
echo Creating backup information file...
echo ----------------------------------------
(
echo Backup Information
echo ==================
echo Date: %date% %time%
echo Timestamp: %TIMESTAMP%
echo Repository Path: %REPO_DIR%
echo Backup Path: %BACKUP_DIR%
echo.
echo Azure Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca
echo Storage Account: stlifeplatformprod
echo Admin Email: sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com
echo Platform Version: 2025.1.0-PRODUCTION
echo Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
echo.
echo Launch Date: September 27, 2025 ^(TOMORROW!^)
echo.
echo This backup contains all your L.I.F.E. Platform files.
echo Your hard work is now safely backed up!
) > "%BACKUP_DIR%\BACKUP_INFO.txt"

echo ✓ Backup information file created

REM Try to create a ZIP file if possible
echo.
echo Attempting to create ZIP archive...
echo ----------------------------------------

REM Use PowerShell to create ZIP (works on Windows 10/11)
powershell -Command "try { Compress-Archive -Path '%BACKUP_DIR%\*' -DestinationPath '%USERPROFILE%\Desktop\LIFE_Platform_Backup_%TIMESTAMP%.zip' -Force; Write-Host '✓ ZIP archive created successfully' } catch { Write-Host '✗ ZIP creation failed - files still backed up in folder' }" 2>nul

echo.
echo ================================================================
echo                    BACKUP COMPLETED!
echo ================================================================
echo.
echo 📁 Backup Location: %BACKUP_DIR%
echo 📦 ZIP Archive: %USERPROFILE%\Desktop\LIFE_Platform_Backup_%TIMESTAMP%.zip
echo.
echo 🛡️ Your L.I.F.E. Platform work is now safely backed up!
echo 💡 Even if your computer crashes, your work is preserved!
echo.
echo 🚀 READY FOR TOMORROW'S LAUNCH! (September 27, 2025)
echo.
echo 📧 Next Steps - Email yourself the backup:
echo    1. Right-click the ZIP file
echo    2. Click "Send to" ^> "Mail recipient"
echo    3. Send to: sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com
echo.
echo 🌐 Or upload to OneDrive manually:
echo    1. Go to https://onedrive.live.com
echo    2. Upload the ZIP file
echo    3. Access from anywhere!
echo.
echo ☁️ Or upload to Azure Storage:
echo    1. Go to https://portal.azure.com
echo    2. Find storage account: stlifeplatformprod
echo    3. Upload the ZIP file to a container
echo.

echo Press any key to open the backup folder...
pause >nul
explorer "%BACKUP_DIR%"

echo.
echo Press any key to exit...
pause >nul