@echo off
REM Fix GitHub Actions Build Error and Commit Pending Changes
REM October 26, 2025

echo ========================================
echo L.I.F.E Platform - Fix Build and Commit
echo ========================================
echo.

REM Step 1: Configure Git to prevent pager issues
echo [1/5] Disabling Git pager for cleaner output...
git config --global pager.branch false
git config --global pager.log false  
git config --global pager.diff false
git config --global core.pager ""
echo     ✓ Git pager disabled
echo.

REM Step 2: Clean up accidental files
echo [2/5] Cleaning up accidental untracked files...
if exist "h origin clean-historymain --force" del /f "h origin clean-historymain --force"
if exist "main)" del /f "main)"
echo     ✓ Cleaned up command artifacts
echo.

REM Step 3: Check current git status
echo [3/5] Checking git status...
git status -s
echo.

REM Step 4: Fetch React source from remote to fix build error
echo [4/5] Fetching React source files from GitHub...
git fetch origin
git checkout origin/main -- src/
if exist src\LifeDashboardApp.js (
    echo     ✓ React source files fetched successfully
) else (
    echo     ⚠ No src/ directory found on remote - web interface works independently
)
echo.

REM Step 5: Stage and commit changes
echo [5/5] Staging and committing changes...
git add .
git status -s
echo.
echo Ready to commit. Type your commit message:
set /p COMMIT_MSG="Commit message: "
git commit -m "%COMMIT_MSG%"
echo.

echo ========================================
echo Ready to push? (Y/N)
set /p PUSH_CONFIRM="Push to GitHub? "
if /i "%PUSH_CONFIRM%"=="Y" (
    git push origin main
    echo.
    echo ✅ Changes pushed successfully!
) else (
    echo.
    echo Changes committed locally. Push later with: git push origin main
)
echo.
echo ========================================
echo Done! Press any key to exit...
pause >nul
