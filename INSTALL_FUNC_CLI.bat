@echo off
echo ============================================================
echo  AZURE FUNCTIONS CORE TOOLS - QUICK INSTALLER
echo ============================================================
echo.
echo This will help you install Azure Functions Core Tools
echo.

REM Check if Node.js is installed
echo [1/3] Checking for Node.js...
node --version >nul 2>&1
if %errorlevel% == 0 (
    echo   ✅ Node.js is installed
    node --version
    echo.
    echo [2/3] Installing Azure Functions Core Tools via npm...
    echo   This may take 2-3 minutes...
    echo.
    npm install -g azure-functions-core-tools@4 --unsafe-perm true
    echo.
    echo [3/3] Verifying installation...
    func --version
    if %errorlevel% == 0 (
        echo.
        echo ============================================================
        echo  ✅ SUCCESS! Azure Functions Core Tools installed
        echo ============================================================
        echo.
        echo You can now deploy with:
        echo   func azure functionapp publish life-functions-app
        echo.
    ) else (
        echo.
        echo ⚠️  Installation completed but func command not found
        echo Please restart your terminal and try: func --version
        echo.
    )
) else (
    echo   ❌ Node.js not found
    echo.
    echo ============================================================
    echo  OPTION 1: Install Node.js first (then re-run this script)
    echo ============================================================
    echo   Download from: https://nodejs.org/
    echo   Then run this script again
    echo.
    echo ============================================================
    echo  OPTION 2: Install via MSI (No Node.js required)
    echo ============================================================
    echo   Opening download page in browser...
    echo   Download: Azure.Functions.Cli.win-x64.4.x.xxxx.msi
    echo   Run the installer and restart your terminal
    echo.
    start https://github.com/Azure/azure-functions-core-tools/releases
    echo.
    echo ============================================================
    echo  OPTION 3: Use VS Code Extension (No CLI needed!)
    echo ============================================================
    echo   1. Open VS Code
    echo   2. Install "Azure Functions" extension
    echo   3. Sign in to Azure (Ctrl+Shift+P → Azure: Sign In)
    echo   4. Right-click life-functions-app → Deploy
    echo.
    echo   This is the EASIEST method for first deployment!
    echo.
)

echo.
echo For detailed instructions, see: INSTALL_FUNC_CLI_GUIDE.md
echo.
pause
