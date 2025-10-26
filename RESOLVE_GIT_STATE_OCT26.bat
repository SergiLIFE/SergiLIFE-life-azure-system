@echo off
echo ========================================
echo L.I.F.E Platform - Git State Resolution
echo October 26, 2025 - Final Status Check
echo ========================================
echo.

echo [1/8] Current Branch and Status...
git branch --show-current
echo.

echo [2/8] Repository state check...
if exist .git\rebase-merge (
    echo ❌ REBASE IN PROGRESS - Will abort
    git rebase --abort
    echo ✅ Rebase aborted
) else if exist .git\rebase-apply (
    echo ❌ REBASE APPLY IN PROGRESS - Will abort
    git rebase --abort
    echo ✅ Rebase aborted
) else (
    echo ✅ No rebase in progress
)
echo.

echo [3/8] Checking for merge conflicts...
git status --porcelain | findstr "^UU\|^AA\|^DD"
if %ERRORLEVEL% EQU 0 (
    echo ❌ Merge conflicts detected
) else (
    echo ✅ No merge conflicts
)
echo.

echo [4/8] Full git status...
git status
echo.

echo [5/8] Recent commits...
git log --oneline -5
echo.

echo [6/8] Remote status comparison...
git fetch origin main
git log --oneline main..origin/main
if %ERRORLEVEL% EQU 0 (
    echo ✅ Remote fetch successful
) else (
    echo ❌ Remote fetch failed
)
echo.

echo [7/8] Staged/unstaged files...
echo "Staged files:"
git diff --cached --name-only
echo.
echo "Unstaged files:"
git diff --name-only
echo.
echo "Untracked files:"
git ls-files --others --exclude-standard
echo.

echo [8/8] Final resolution actions...
echo.
echo "Choose your action:"
echo "1. Clean state and force push all changes"
echo "2. Abort all operations and start fresh"
echo "3. Continue rebase if in progress"
echo "4. Just show status and exit"
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo "🚀 Executing clean state and force push..."
    git add -A
    git commit -m "Fix: Resolve all pending changes and git state - October 26, 2025"
    git push origin main --force
    echo "✅ Force push completed"
) else if "%choice%"=="2" (
    echo.
    echo "🔄 Resetting to clean state..."
    git reset --hard origin/main
    echo "✅ Repository reset to match remote"
) else if "%choice%"=="3" (
    echo.
    echo "⏭️ Continuing rebase..."
    git rebase --continue
    echo "✅ Rebase continued"
) else (
    echo.
    echo "📊 Status check complete - no actions taken"
)

echo.
echo "========================================"
echo "Git State Resolution Complete"
echo "========================================"
pause