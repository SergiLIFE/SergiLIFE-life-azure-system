@echo off
echo ======================================================================
echo  LAUNCHER - Handle Paths with Spaces Properly
echo ======================================================================
echo.

REM Navigate to the workspace using proper quoted paths
cd /d "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"

echo Current directory: %CD%
echo.

echo Available deployment options:
echo [1] QUICK_FULL_DEPLOY.bat     - Updated with verification
echo [2] VERIFIED_DEPLOY.bat       - New robust script  
echo [3] MANUAL_DEPLOY.bat         - Simple manual process
echo.

set /p choice="Select option (1-3): "

if "%choice%"=="1" (
    echo Running QUICK_FULL_DEPLOY.bat...
    call "QUICK_FULL_DEPLOY.bat"
) else if "%choice%"=="2" (
    echo Running VERIFIED_DEPLOY.bat...
    call "VERIFIED_DEPLOY.bat"  
) else if "%choice%"=="3" (
    echo Running MANUAL_DEPLOY.bat...
    call "MANUAL_DEPLOY.bat"
) else (
    echo Invalid choice. Exiting.
    pause
    exit /b 1
)

echo.
echo Deployment launcher completed.
pause