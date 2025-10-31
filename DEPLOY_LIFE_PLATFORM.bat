@echo off
setlocal enabledelayedexpansion

REM L.I.F.E. Theory Platform - GitHub Deployment with Sync
REM Handles pulling latest, staging, committing, and pushing

echo ========================================
echo L.I.F.E. Platform GitHub Deployment
echo ========================================
echo.

REM Use pushd to navigate with spaces in path
pushd "c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system"

echo [1/6] Stashing any uncommitted changes...
git stash

echo.
echo [2/6] Fetching latest from remote...
git fetch origin

echo.
echo [3/6] Pulling latest changes (rebase)...
git pull origin main --rebase

echo.
echo [4/6] Staging life-theory-platform.html...
git add docs/life-theory-platform.html
echo File staged.

echo.
echo [5/6] Committing...
git commit -m "Add L.I.F.E. Theory Platform marketing page with clinical validation metrics (Oct 31 2025)"

echo.
echo [6/6] Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Your page is now live at:
echo https://lifecoach-121.com/life-theory-platform.html
echo.
echo Raw GitHub URL:
echo https://raw.githubusercontent.com/SergiLIFE/SergiLIFE-life-azure-system/main/docs/life-theory-platform.html
echo.
echo Verification - waiting 10 seconds for GitHub to sync...
timeout /t 10 /nobreak

popd
echo.
echo Done! You can now share the URL with colleagues.
pause
