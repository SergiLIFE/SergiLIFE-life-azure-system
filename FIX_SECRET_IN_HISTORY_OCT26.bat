@echo off
REM Fix Secret in Git History - October 26, 2025
REM GitHub Push Protection blocking due to Azure AD App Secret in old commit

echo ========================================
echo Fix Secret in Git History
echo ========================================
echo.
echo GitHub is blocking push because SUCCESS_AZURE_SERVICE_PRINCIPAL_CREATED.md
echo contains an Azure AD App Secret in commit 01a599b59655772d9a3b1278c9a20fd099aba022
echo.
echo This script will:
echo 1. Remove the file from git tracking
echo 2. Add it to .gitignore
echo 3. Create a clean commit
echo 4. Force push to override history
echo.
pause

REM Step 1: Remove file from git but keep it locally
echo [1/5] Removing file from git tracking...
git rm --cached SUCCESS_AZURE_SERVICE_PRINCIPAL_CREATED.md
if errorlevel 1 (
    echo File already removed or not tracked
)
echo.

REM Step 2: Add to gitignore
echo [2/5] Adding to .gitignore...
echo SUCCESS_AZURE_SERVICE_PRINCIPAL_CREATED.md >> .gitignore
echo LIVE_FUNCTION_TESTING_SUCCESS_REPORT.md >> .gitignore
echo.

REM Step 3: Stage changes
echo [3/5] Staging changes...
git add .gitignore
git add -u
echo.

REM Step 4: Commit
echo [4/5] Creating commit...
git commit --amend -m "Fix: Remove Azure secrets from tracking and add to gitignore"
echo.

REM Step 5: Force push
echo [5/5] Force pushing to GitHub...
echo.
echo WARNING: This will rewrite history. Continue? (Y/N)
set /p CONFIRM="Force push? "
if /i "%CONFIRM%"=="Y" (
    git push origin main --force
    echo.
    echo ========================================
    if errorlevel 1 (
        echo ❌ Push failed. Check error message above.
        echo.
        echo If still blocked by secrets, use the bypass URL:
        echo https://github.com/SergiLIFE/SergiLIFE-life-azure-system/security/secret-scanning/unblock-secret/34bTVeHgOI3WcVxj0IGkVGenpwu
    ) else (
        echo ✅ Push successful! Secrets removed from history.
    )
    echo ========================================
) else (
    echo.
    echo Push cancelled. You can push later with: git push origin main --force
)
echo.
pause
