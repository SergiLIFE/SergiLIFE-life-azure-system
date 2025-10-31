@echo off
REM ========================================
REM Fix GitHub Actions Submodule Error
REM Remove all traces of LIFE-RECOVERY submodule
REM ========================================

echo.
echo ████████████████████████████████████████████████
echo  FIXING GITHUB ACTIONS BUILD FAILURE
echo  Removing broken LIFE-RECOVERY submodule
echo ████████████████████████████████████████████████
echo.

cd /d "c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system"

echo [1/8] Removing submodule from git index...
git rm --cached LIFE-RECOVERY 2>nul
if %ERRORLEVEL% equ 0 (
    echo ✅ Removed from index
) else (
    echo ℹ️  Not in index ^(already removed^)
)

echo.
echo [2/8] Removing .gitmodules file...
if exist .gitmodules (
    del /f .gitmodules
    echo ✅ .gitmodules deleted
) else (
    echo ℹ️  .gitmodules not found
)

echo.
echo [3/8] Cleaning git config...
git config --local --remove-section submodule.LIFE-RECOVERY 2>nul
if %ERRORLEVEL% equ 0 (
    echo ✅ Config section removed
) else (
    echo ℹ️  Config section not found
)

echo.
echo [4/8] Removing physical directory...
if exist LIFE-RECOVERY (
    rmdir /s /q LIFE-RECOVERY
    echo ✅ Directory removed
) else (
    echo ℹ️  Directory not found
)

echo.
echo [5/8] Cleaning .git/modules...
if exist .git\modules\LIFE-RECOVERY (
    rmdir /s /q .git\modules\LIFE-RECOVERY
    echo ✅ Git modules cleaned
) else (
    echo ℹ️  Git modules not found
)

echo.
echo [6/8] Committing the fix...
git add -A
git commit -m "Fix: Remove all traces of broken LIFE-RECOVERY submodule to fix GitHub Actions" -m "- Removed submodule from git index" -m "- Deleted .gitmodules file" -m "- Cleaned git config" -m "- Removed physical directories" -m "This fixes the GitHub Actions error: fatal: No url found for submodule path 'LIFE-RECOVERY' in .gitmodules"
if %ERRORLEVEL% equ 0 (
    echo ✅ Changes committed
) else (
    echo ℹ️  No changes to commit ^(already fixed^)
)

echo.
echo [7/8] Pushing to GitHub...
git push origin main
if %ERRORLEVEL% equ 0 (
    echo ✅ Changes pushed to GitHub
) else (
    echo ❌ Push failed - check output above
    pause
    exit /b 1
)

echo.
echo [8/8] Verifying fix...
git submodule status
echo.
echo Expected: No submodules listed above
echo.

echo.
echo ════════════════════════════════════════════════
echo  ✅ FIX COMPLETE!
echo ════════════════════════════════════════════════
echo.
echo GitHub Actions should pass on the next run.
echo.
echo 🔍 Verify at:
echo https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions
echo.
echo Wait 1-2 minutes for GitHub to rebuild automatically.
echo.

pause
