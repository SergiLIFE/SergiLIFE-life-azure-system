@echo off
REM ========================================
REM L.I.F.E. Repository Recovery Tool
REM Lists and restores from available backups
REM ========================================

set BACKUP_LOCATION=C:\Users\%USERNAME%\Desktop\LIFE_Repository_Backups

echo ===== L.I.F.E. Repository Recovery Tool =====
echo.

REM Check if backup location exists
if not exist "%BACKUP_LOCATION%" (
    echo ❌ Backup location not found: %BACKUP_LOCATION%
    echo Run working_backup.bat first to create backups
    pause
    exit /b 1
)

echo 📍 Backup location: %BACKUP_LOCATION%
echo.

REM Show available file backups
echo 📁 Available file backups:
if exist "%BACKUP_LOCATION%\daily" (
    dir "%BACKUP_LOCATION%\daily\life_repo_*" /ad /b 2>nul | sort /r
    if %ERRORLEVEL% neq 0 echo   No file backups found
) else (
    echo   Daily backup folder not found
)

echo.

REM Show available git bundles
echo 📦 Available git bundles:
if exist "%BACKUP_LOCATION%\git_bundles" (
    dir "%BACKUP_LOCATION%\git_bundles\*.bundle" /b 2>nul | sort /r
    if %ERRORLEVEL% neq 0 echo   No git bundles found
) else (
    echo   Bundle folder not found
)

echo.
echo ===== Recovery Options =====
echo 1. List backup contents
echo 2. Recover specific files from latest backup
echo 3. Full repository recovery from bundle
echo 4. Show backup details
echo 5. Create new backup
echo 0. Exit
echo.

set /p choice="Select option (0-5): "

if "%choice%"=="1" goto list_contents
if "%choice%"=="2" goto recover_files
if "%choice%"=="3" goto recover_full
if "%choice%"=="4" goto show_details
if "%choice%"=="5" goto create_backup
if "%choice%"=="0" goto end
goto invalid_choice

:list_contents
echo.
echo 📋 Listing backup contents...
for /f %%f in ('dir "%BACKUP_LOCATION%\daily\life_repo_*" /ad /b 2^>nul ^| sort /r') do (
    echo.
    echo Contents of %%f:
    dir "%BACKUP_LOCATION%\daily\%%f" /b | more
    goto :show_one
)
:show_one
pause
goto menu

:recover_files
echo.
echo 📁 File recovery from latest backup...
for /f %%f in ('dir "%BACKUP_LOCATION%\daily\life_repo_*" /ad /b 2^>nul ^| sort /r') do (
    set LATEST_BACKUP=%%f
    goto :found_latest
)
:found_latest
echo Latest backup: %LATEST_BACKUP%
echo.
set /p target="Enter target directory (or press Enter for current): "
if "%target%"=="" set target=%CD%

echo Recovering files from %LATEST_BACKUP% to %target%
robocopy "%BACKUP_LOCATION%\daily\%LATEST_BACKUP%" "%target%" /E /R:1 /W:1
echo.
echo Recovery completed!
pause
goto menu

:recover_full
echo.
echo 📦 Full repository recovery from bundle...
for /f %%f in ('dir "%BACKUP_LOCATION%\git_bundles\*.bundle" /b 2^>nul ^| sort /r') do (
    set LATEST_BUNDLE=%%f
    goto :found_bundle
)
:found_bundle
echo Latest bundle: %LATEST_BUNDLE%
echo.
set /p target="Enter directory name for recovered repository: "
if "%target%"=="" set target=recovered_repository

cd /d "%BACKUP_LOCATION%\git_bundles"
git clone "%LATEST_BUNDLE%" "%target%"
if %ERRORLEVEL% eq 0 (
    echo ✅ Repository recovered to: %BACKUP_LOCATION%\git_bundles\%target%
    echo.
    echo Verifying recovery...
    cd "%target%"
    git fsck --full
    git log --oneline -3
) else (
    echo ❌ Recovery failed
)
pause
goto menu

:show_details
echo.
echo 📊 Backup details...
if exist "%BACKUP_LOCATION%\last_backup.txt" (
    type "%BACKUP_LOCATION%\last_backup.txt"
) else (
    echo No backup summary found
)
echo.
echo Disk usage:
for /d %%d in ("%BACKUP_LOCATION%\daily\*") do echo   %%~nd: %%~zd bytes
pause
goto menu

:create_backup
echo.
echo 🔄 Creating new backup...
cd /d "c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system"
call working_backup.bat
goto menu

:invalid_choice
echo Invalid choice. Please select 0-5.
goto menu

:menu
echo.
goto main

:end
echo.
echo Repository recovery tool closed.
pause