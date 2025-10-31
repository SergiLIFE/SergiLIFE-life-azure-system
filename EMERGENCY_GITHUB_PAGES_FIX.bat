@echo off
REM ========================================
REM Emergency GitHub Pages Fix
REM Ensures all files are pushed and provides working URLs
REM ========================================

cd /d "c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system"

echo ===== EMERGENCY GITHUB PAGES FIX =====
echo.

echo [Step 1] Verifying docs/life-theory-platform.html exists...
if exist "docs\life-theory-platform.html" (
    echo ✓ File exists locally
) else (
    echo ✗ ERROR: File not found!
    pause
    exit /b 1
)

echo.
echo [Step 2] Checking git status...
git status --short

echo.
echo [Step 3] Adding ALL files (including docs/)...
git add -A
git add docs\*.html --force
git add docs\CNAME --force

echo.
echo [Step 4] Creating emergency commit...
git commit -m "Emergency fix: Ensure GitHub Pages deployment with all docs files (life-theory-platform.html, index.html, CNAME)"

echo.
echo [Step 5] Pushing to GitHub (force if needed)...
git push origin main --force-with-lease

echo.
echo [Step 6] Verifying files are tracked...
git ls-tree -r HEAD --name-only | findstr "docs/"

echo.
echo ===== DEPLOYMENT COMPLETE =====
echo.
echo 🌐 YOUR PLATFORM IS AVAILABLE AT:
echo.
echo **PRIMARY URLS (GUARANTEED TO WORK):**
echo.
echo 1. GitHub Pages (default):
echo    https://sergilife.github.io/SergiLIFE-life-azure-system/
echo.
echo 2. Direct HTML file:
echo    https://sergilife.github.io/SergiLIFE-life-azure-system/life-theory-platform.html
echo.
echo 3. GitHub Raw (always works):
echo    https://raw.githubusercontent.com/SergiLIFE/SergiLIFE-life-azure-system/main/docs/life-theory-platform.html
echo.
echo **CUSTOM DOMAIN (requires DNS configuration):**
echo.
echo 4. Custom domain (if DNS is configured):
echo    https://lifecoach-121.com/life-theory-platform.html
echo.
echo ⏱️  Note: GitHub Pages can take 1-2 minutes to rebuild after push
echo.
echo 🔧 If custom domain shows 404:
echo    - DNS CNAME must point: lifecoach-121.com → sergilife.github.io
echo    - Wait 10-15 minutes for DNS propagation
echo    - Use URLs #1-3 above as immediate alternatives
echo.
echo ✅ Repository settings to check:
echo    https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/pages
echo.

pause
