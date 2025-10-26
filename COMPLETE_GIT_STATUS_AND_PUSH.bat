@echo off
REM Complete Status Check and Push - October 26, 2025

echo ========================================
echo L.I.F.E Platform - Complete Git Status
echo ========================================
echo.

REM Disable pager
git config --global core.pager ""

echo [1/6] Current Branch and Status...
git branch --show-current
echo.

echo [2/6] Checking for uncommitted changes...
git status -s
echo.

echo [3/6] Checking for unpushed commits...
git log --oneline --decorate -10
echo.

echo [4/6] Difference from remote...
git log --oneline origin/main..HEAD
echo.

echo [5/6] Files modified but not staged...
git diff --name-only
echo.

echo [6/6] Files staged but not committed...
git diff --cached --name-only
echo.

echo ========================================
echo Summary:
echo.
git status
echo.
echo ========================================
echo.

set /p ACTION="What would you like to do? [1=Stage All, 2=Commit, 3=Push, 4=Stage+Commit+Push, 5=Exit]: "

if "%ACTION%"=="1" (
    echo.
    echo Staging all changes...
    git add -A
    git status -s
    echo.
    echo ✅ All changes staged
    pause
    goto menu
)

if "%ACTION%"=="2" (
    echo.
    set /p MSG="Commit message: "
    git commit -m "%MSG%"
    echo.
    pause
    goto menu
)

if "%ACTION%"=="3" (
    echo.
    echo Pushing to origin main...
    git push origin main
    echo.
    if errorlevel 1 (
        echo ❌ Push failed. Try: git push origin main --force
    ) else (
        echo ✅ Push successful!
    )
    pause
    goto menu
)

if "%ACTION%"=="4" (
    echo.
    echo [1/3] Staging all changes...
    git add -A
    echo.
    echo [2/3] Committing...
    set /p MSG="Commit message: "
    git commit -m "%MSG%"
    echo.
    echo [3/3] Pushing...
    git push origin main
    echo.
    if errorlevel 1 (
        echo ❌ Push failed
        echo Try: git push origin main --force
    ) else (
        echo ✅ Complete! All changes pushed to GitHub
    )
    pause
)

:menu
echo.
echo ========================================
pause
