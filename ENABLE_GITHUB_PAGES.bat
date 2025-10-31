@echo off
REM ========================================
REM Enable GitHub Pages for Repository
REM ========================================

echo ===== ENABLE GITHUB PAGES =====
echo.

echo This script will guide you through enabling GitHub Pages.
echo.
echo OPTION 1 (Recommended - Web Interface):
echo ----------------------------------------
echo 1. Open this URL in your browser:
echo    https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/pages
echo.
echo 2. Under "Build and deployment":
echo    - Source: Deploy from a branch
echo    - Branch: main
echo    - Folder: /docs
echo    - Click SAVE
echo.
echo 3. Wait 30-60 seconds
echo.
echo 4. Your site will be live at:
echo    https://sergilife.github.io/SergiLIFE-life-azure-system/
echo.
echo.

echo OPTION 2 (GitHub CLI):
echo ----------------------------------------
echo.
set /p use_cli="Do you have GitHub CLI installed? (y/n): "

if /i "%use_cli%"=="y" (
    echo.
    echo Enabling GitHub Pages via CLI...
    gh api repos/SergiLIFE/SergiLIFE-life-azure-system/pages -X POST -f source[branch]=main -f source[path]=/docs
    
    if %ERRORLEVEL% EQU 0 (
        echo ✓ GitHub Pages enabled successfully!
        echo.
        echo Your site will be live in 30-60 seconds at:
        echo https://sergilife.github.io/SergiLIFE-life-azure-system/
    ) else (
        echo ✗ Error: GitHub CLI command failed
        echo Please use Option 1 (web interface) instead
    )
) else (
    echo.
    echo Please use Option 1 (web interface) to enable GitHub Pages.
    echo Opening browser now...
    start https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/pages
)

echo.
echo.
echo ===== NEXT STEPS AFTER ENABLING =====
echo.
echo 1. Verify GitHub Pages is enabled:
echo    https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/pages
echo.
echo 2. Wait for deployment (check Actions tab):
echo    https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions
echo.
echo 3. Access your platform at:
echo    https://sergilife.github.io/SergiLIFE-life-azure-system/life-theory-platform.html
echo.
echo 4. (Optional) Configure custom domain:
echo    - Add DNS CNAME: lifecoach-121.com → sergilife.github.io
echo    - Enter custom domain in GitHub Pages settings
echo.

pause
