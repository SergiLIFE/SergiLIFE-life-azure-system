@echo off
REM 🚀 Quick VS Code Repository Sync
REM ================================
REM 
REM Quickly sync VS Code configurations from the .vscode repository
REM and other common sources to set up your development environment.

echo.
echo 🚀 VS Code Repository Sync
echo ================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)

REM Check if Git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git not found. Please install Git first.
    pause
    exit /b 1
)

echo ✅ Python and Git are available
echo.

REM Show menu
echo 📋 Quick Setup Options:
echo.
echo 1. Sync from SergiLIFE/.vscode repository (Recommended)
echo 2. Sync from custom GitHub repository
echo 3. Create minimal VS Code configuration
echo 4. Install VS Code extensions only
echo 5. Run full interactive setup
echo.

set /p choice="Select option (1-5): "

if "%choice%"=="1" (
    echo.
    echo 🔄 Syncing from SergiLIFE/.vscode repository...
    python setup_vscode_repo.py --quick-setup
) else if "%choice%"=="2" (
    echo.
    set /p repo="Enter GitHub repository (owner/repo): "
    echo 🔄 Syncing from %repo%...
    python setup_vscode_repo.py --repo %repo%
) else if "%choice%"=="3" (
    echo.
    echo 🔧 Creating minimal VS Code configuration...
    python -c "from setup_vscode_repo import QuickVSCodeSetup; s=QuickVSCodeSetup(); s.create_backup(); s.create_essential_configs(); s.validate_setup()"
) else if "%choice%"=="4" (
    echo.
    echo 🔌 Installing VS Code extensions...
    python setup_vscode_repo.py --extensions-only
) else if "%choice%"=="5" (
    echo.
    echo 🚀 Running interactive setup...
    python setup_vscode_repo.py
) else (
    echo ❌ Invalid choice
    pause
    exit /b 1
)

echo.
echo ✅ Setup completed!
echo.
echo 💡 Next steps:
echo    1. Restart VS Code to apply changes
echo    2. Open your workspace file: life-autonomous-optimizer.code-workspace
echo    3. Press F5 to start debugging your autonomous optimizer
echo.

pause
