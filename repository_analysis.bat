@echo off
REM Repository Analysis Script (GitHub Codespace)
REM Check workspace size, file counts, and largest files

echo ==================================================
echo REPOSITORY ANALYSIS - GITHUB CODESPACE
echo ==================================================
echo.

echo 1. CHECKING WORKSPACE FILE COUNTS...
echo --------------------------------------------------
REM Count total files and directories
for /f %%i in ('dir /s /b /a-d ^| find /c /v ""') do set filecount=%%i
for /f %%i in ('dir /s /b /ad ^| find /c /v ""') do set dircount=%%i
echo Total files: %filecount%
echo Total directories: %dircount%
echo.

echo 2. CHECKING LARGEST FILES IN WORKSPACE...
echo --------------------------------------------------
REM Find largest files (Windows equivalent)
echo Scanning for large files...
dir /s /-c /o-s | findstr /v "Directory" | head -15
echo.

echo 3. CHECKING CLEANUP STATUS...
echo --------------------------------------------------
if exist ".cleanup" (
    echo Cleanup directory found
    if exist ".cleanup\logs" (
        echo Cleanup logs available:
        dir /b ".cleanup\logs"
    )
    if exist ".cleanup\quarantine" (
        echo Quarantine directories:
        dir /b ".cleanup\quarantine"
    )
) else (
    echo No cleanup directory found
)
echo.

echo 4. CHECKING FILE PATTERNS...
echo --------------------------------------------------
echo Auto-generated file counts:
echo COMPREHENSIVE files:
for /f %%i in ('dir /s /b *COMPREHENSIVE* 2^>nul ^| find /c /v ""') do echo   COMPREHENSIVE: %%i files
echo EMERGENCY files:
for /f %%i in ('dir /s /b *EMERGENCY* 2^>nul ^| find /c /v ""') do echo   EMERGENCY: %%i files
echo DEPLOY files:
for /f %%i in ('dir /s /b *DEPLOY* 2^>nul ^| find /c /v ""') do echo   DEPLOY: %%i files
echo CORRECTED files:
for /f %%i in ('dir /s /b *CORRECTED* 2^>nul ^| find /c /v ""') do echo   CORRECTED: %%i files
echo.

echo 5. WORKSPACE HEALTH CHECK...
echo --------------------------------------------------
if exist "requirements.txt" (echo ✅ Requirements.txt found) else (echo ❌ Requirements.txt missing)
if exist "azure_config.py" (echo ✅ Azure config found) else (echo ❌ Azure config missing)
if exist ".gitignore" (echo ✅ .gitignore found) else (echo ❌ .gitignore missing)
if exist "README.md" (echo ✅ README.md found) else (echo ❌ README.md missing)
echo.

echo ==================================================
echo REPOSITORY ANALYSIS COMPLETE
echo ==================================================
pause