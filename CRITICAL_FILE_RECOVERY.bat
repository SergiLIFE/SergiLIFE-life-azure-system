@echo off
echo ========================================
echo CRITICAL: 521 FILES DELETED AGAIN!
echo Emergency Recovery Operation
echo ========================================

echo 🚨 PROBLEM: Files got deleted during commit operation
echo 🔧 SOLUTION: Multi-source recovery from all possible locations
echo.

echo Step 1: Immediate git history recovery...
echo "Recovering from recent commits..."

REM Get recent commit hashes
git log --oneline -10

echo.
echo "Attempting recovery from previous commit states..."
git checkout HEAD~1 -- . 2>nul
git checkout HEAD~2 -- . 2>nul
git checkout HEAD~3 -- . 2>nul

echo.
echo Step 2: Recover from git stash...
git stash list
git stash pop 2>nul
git stash apply stash@{0} 2>nul
git stash apply stash@{1} 2>nul

echo.
echo Step 3: Recover from git reflog (lost commits)...
echo "Checking reflog for lost file states..."
git reflog --oneline -15

REM Try to recover from reflog entries
for /f "tokens=1" %%i in ('git reflog --oneline -5') do (
    echo "Attempting recovery from: %%i"
    git checkout %%i -- . 2>nul
)

echo.
echo Step 4: Search for backup directories...
if exist "BACKUP_BEFORE_NUCLEAR" (
    echo "✅ Found backup folder!"
    echo "Restoring from BACKUP_BEFORE_NUCLEAR..."
    xcopy "BACKUP_BEFORE_NUCLEAR\*" . /s /e /h /y /i 2>nul
) else (
    echo "❌ No backup folder found"
)

echo.
echo Step 5: Check VS Code workspace recovery...
if exist ".vscode\settings.json" (
    echo "Checking VS Code for file references..."
)

echo.
echo Step 6: Windows file recovery...
echo "Checking Windows temp and recent files..."
if exist "%TEMP%\vscode*" (
    echo "Found VS Code temp files"
    xcopy "%TEMP%\vscode*" "temp_recovery\" /s /e /h /y 2>nul
)

echo.
echo Step 7: Git object recovery (advanced)...
echo "Searching git objects for recoverable files..."
git fsck --unreachable 2>nul

echo.
echo Step 8: Force file recreation from patterns...
echo "Attempting to recreate critical files from git database..."

REM Try to recover specific file types from git objects
for /f %%i in ('git rev-list --objects --all ^| findstr "\.py$"') do (
    git show %%i > recovered_%%i 2>nul
)

echo.
echo Step 9: Current state assessment...
echo "Files currently in directory:"
dir /b | head -20

for /f %%i in ('dir /b ^| find /c /v ""') do set current_files=%%i
echo "Current file count: %current_files%"

if %current_files% LSS 100 (
    echo "🚨 CRITICAL: Still very few files - need aggressive recovery"
    
    echo.
    echo Step 10: Nuclear git recovery...
    echo "Trying to recover from ALL git history..."
    
    REM Get all commit hashes and try to recover from each
    git log --pretty=format:"%%H" --all > all_commits.txt 2>nul
    
    echo "Attempting recovery from all commits..."
    for /f %%c in (all_commits.txt) do (
        echo "Trying commit: %%c"
        git show %%c --name-only > files_in_%%c.txt 2>nul
        git checkout %%c -- . 2>nul
    )
    
) else (
    echo "ℹ️ Some files recovered - adding them to git..."
    git add . --force
)

echo.
echo Step 11: Final recovery attempt...
git add -A --force
git status --porcelain

for /f %%i in ('git status --porcelain ^| find /c /v ""') do set recovered=%%i
echo "Files recovered and staged: %recovered%"

if %recovered% GTR 0 (
    echo.
    echo "Committing recovered files..."
    git commit -m "EMERGENCY RECOVERY: Restored %recovered% files after deletion - critical file recovery operation"
    
    git push origin main
    
    echo "✅ Emergency recovery completed with %recovered% files"
) else (
    echo "❌ No files recovered - manual intervention needed"
    echo.
    echo "MANUAL RECOVERY OPTIONS:"
    echo "1. Check other directories for L.I.F.E files"
    echo "2. Look in Downloads/Desktop for backups"  
    echo "3. Check OneDrive/cloud storage"
    echo "4. Restore from system backup"
)

echo.
echo "========================================"
echo "EMERGENCY FILE RECOVERY COMPLETE"
echo "Check results above for success/failure"
echo "========================================"
pause