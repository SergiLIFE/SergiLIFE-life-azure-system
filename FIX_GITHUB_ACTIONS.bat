@echo off
REM ========================================
REM Fix GitHub Actions Submodule Failure
REM Removes broken LIFE-RECOVERY submodule
REM ========================================

cd /d "c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system"

echo Fixing broken submodule configuration...

REM Remove submodule from git index
git rm --cached LIFE-RECOVERY 2>nul

REM Remove submodule configuration
git config --remove-section submodule.LIFE-RECOVERY 2>nul

REM Remove submodule directories
if exist LIFE-RECOVERY rmdir /s /q LIFE-RECOVERY
if exist .git\modules\LIFE-RECOVERY rmdir /s /q .git\modules\LIFE-RECOVERY

REM Ensure .gitmodules is clean
echo # Git submodules configuration > .gitmodules
echo # This file intentionally left empty - no submodules are used in this repository >> .gitmodules
echo. >> .gitmodules

REM Stage all changes
git add -A

REM Show status
echo.
echo Current repository status:
git status --short

echo.
echo Committing fix...
git commit -m "Fix: Remove broken LIFE-RECOVERY submodule causing GitHub Actions CI/CD failure (Exit code 128)"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ===== FIX COMPLETE =====
echo GitHub Actions should now pass on next workflow run
echo Check: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions

pause
