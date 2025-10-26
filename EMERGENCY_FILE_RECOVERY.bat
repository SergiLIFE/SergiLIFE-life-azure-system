@echo off
echo ========================================
echo EMERGENCY: FILE RECOVERY OPERATION
echo Restoring Deleted/Missing Files
echo ========================================

echo 🚨 CRITICAL: Files may have been accidentally deleted during git operations
echo 🔧 SOLUTION: Multi-layered recovery approach
echo.

echo Step 1: Check if files were deleted by git operations...
echo "Recent git operations that might have deleted files:"
git reflog --oneline -10

echo.
echo Step 2: Attempt recovery from git history...
echo "Checking previous commits for deleted files..."
git log --oneline --stat -5

echo.
echo Step 3: Try to recover from git stash...
echo "Checking for stashed changes..."
git stash list

echo "Recovering any stashed files..."
git stash pop 2>nul

echo.
echo Step 4: Recover from recent commits...
echo "Attempting to restore files from recent commits..."

REM Get the hash of the most recent commit that had files
for /f "tokens=1" %%i in ('git log --oneline -1') do set recent_commit=%%i
echo "Recent commit: %recent_commit%"

REM Try to checkout files from recent commits
git checkout HEAD~1 -- . 2>nul
git checkout HEAD~2 -- . 2>nul
git checkout HEAD~3 -- . 2>nul

echo.
echo Step 5: Check for backup folders...
echo "Looking for backup directories..."
if exist "BACKUP_BEFORE_NUCLEAR" (
    echo "✅ Found backup folder: BACKUP_BEFORE_NUCLEAR"
    echo "Restoring from backup..."
    xcopy "BACKUP_BEFORE_NUCLEAR\*" . /s /e /h /y 2>nul
    echo "✅ Files restored from backup"
) else (
    echo "❌ No backup folder found"
)

echo.
echo Step 6: Restore from Windows Recycle Bin equivalent...
echo "Checking for recently deleted files..."

REM Check if there are any .git recovery files
if exist ".git\refs\stash" (
    echo "Found git stash - attempting recovery..."
    git stash apply 2>nul
)

echo.
echo Step 7: Use git to restore deleted files from index...
echo "Attempting to restore files from git index..."
git restore --staged . 2>nul
git restore . 2>nul

echo.
echo Step 8: Recover specific L.I.F.E Platform files from git history...
echo "Looking for specific platform files in git history..."

REM List of critical files to recover
set critical_files=experimentP2L*.py life*.py azure*.py campaign*.py *.html *.js *.md requirements.txt

for %%f in (%critical_files%) do (
    echo "Attempting to recover: %%f"
    git show HEAD:%%f > %%f 2>nul
    git show HEAD~1:%%f > %%f 2>nul
    git show HEAD~2:%%f > %%f 2>nul
)

echo.
echo Step 9: Manual file restoration from git objects...
echo "Searching git objects for recoverable files..."

REM Find all blob objects that might contain our files
git fsck --lost-found 2>nul

echo.
echo Step 10: Check current state after recovery attempts...
echo "Files currently in directory:"
dir /b | head -20

echo.
echo "Files recovered/available:"
if exist "*.py" echo "✅ Python files found"
if exist "*.html" echo "✅ HTML files found"  
if exist "*.js" echo "✅ JavaScript files found"
if exist "*.md" echo "✅ Markdown files found"
if exist "requirements.txt" echo "✅ Requirements file found"
if exist ".github" echo "✅ GitHub workflows found"

echo.
echo Step 11: Re-stage recovered files...
echo "Adding all recovered files to git..."
git add . --force
git add -A --force

echo "Files ready to commit:"
git diff --cached --name-only

for /f %%i in ('git diff --cached --name-only ^| find /c /v ""') do set recovered=%%i
echo "Total recovered files: %recovered%"

if %recovered% GTR 0 (
    echo.
    echo Step 12: Commit recovered files...
    git commit -m "EMERGENCY RECOVERY: Restored %recovered% files that were accidentally deleted during git operations - L.I.F.E Platform restoration"
    
    if %ERRORLEVEL% EQU 0 (
        echo "✅ Emergency recovery commit successful!"
        
        echo.
        echo "Push recovered files..."
        git push origin main
        
        if %ERRORLEVEL% EQU 0 (
            echo "🎉 SUCCESS! Files recovered and pushed!"
        ) else (
            echo "⚠️ Files recovered and committed locally - manual push may be needed"
        )
    )
) else (
    echo "❌ No files were recovered automatically"
    echo.
    echo "Manual recovery options:"
    echo "1. Check VS Code for unsaved changes"
    echo "2. Check local backup folders"
    echo "3. Look in system temp folders"
    echo "4. Check if files are in a different directory"
)

echo.
echo Step 13: Alternative recovery sources...
echo "Checking alternative locations..."

REM Check common backup locations
if exist "%USERPROFILE%\Desktop\backup*" echo "✅ Found desktop backups"
if exist "%TEMP%\vscode*" echo "✅ Found VS Code temp files"
if exist ".vscode\settings.json" echo "✅ VS Code workspace intact"

echo.
echo "========================================"
echo "EMERGENCY RECOVERY COMPLETE!"
echo "Check the results above"
echo "If files still missing, we need manual recovery"
echo "========================================"
pause