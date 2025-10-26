@echo off
echo ========================================
echo FILES EXIST - GIT NOT TRACKING THEM
echo Force Git to Recognize All Files
echo ========================================

echo 💡 UNDERSTANDING: Files exist in explorer but git shows them as crossed over
echo 🔧 SOLUTION: Force git to track all existing files
echo.

echo Step 1: Check current git status...
git status --porcelain

echo.
echo Step 2: Check what files actually exist...
echo "Files in directory (first 20):"
dir /b | more +0 | findstr /n "^" | findstr "^[1-9]:" | findstr "^1[0-9]:" > nul && (
    dir /b | more +0 | findstr /n "^" | findstr "^[1-2][0-9]:" 
) || (
    dir /b
)

for /f %%i in ('dir /b ^| find /c /v ""') do set total_files=%%i
echo "Total files in directory: %total_files%"

echo.
echo Step 3: Force git to track ALL existing files...
echo "Adding all files with maximum force..."

REM Reset any git state issues first
git reset --mixed HEAD 2>nul

REM Force add everything
git add . --force
git add -A --force  
git add --all --force
git add * --force 2>nul

REM Add hidden files
git add .* --force 2>nul

echo.
echo Step 4: Check what git now recognizes...
echo "Files git will commit:"
git diff --cached --name-only

for /f %%i in ('git diff --cached --name-only ^| find /c /v ""') do set staged_files=%%i
echo "Files staged by git: %staged_files%"

echo.
echo "Comparison:"
echo "Files in directory: %total_files%"  
echo "Files staged by git: %staged_files%"

if %staged_files% LSS %total_files% (
    echo "⚠️ Git is not tracking all files - investigating..."
    
    echo.
    echo Step 5: Check .gitignore issues...
    if exist ".gitignore" (
        echo "Checking .gitignore patterns..."
        git status --ignored --porcelain
    )
    
    echo.
    echo Step 6: Force add by file patterns...
    for /r %%f in (*) do git add "%%f" --force 2>nul
    
    echo "After force add by pattern:"
    for /f %%i in ('git diff --cached --name-only ^| find /c /v ""') do set final_staged=%%i
    echo "Files now staged: %final_staged%"
    
) else (
    echo "✅ Git is tracking all files correctly!"
)

echo.
echo Step 7: Commit all tracked files...
if %staged_files% GTR 0 (
    git commit -m "FORCE TRACK: All %staged_files% existing files now properly tracked by git - L.I.F.E Platform complete synchronization"
    
    if %ERRORLEVEL% EQU 0 (
        echo "✅ All files committed successfully!"
        
        echo "Push to GitHub..."
        git push origin main
        
        if %ERRORLEVEL% EQU 0 (
            echo "🎉 SUCCESS! All %staged_files% files now tracked and pushed"
        ) else (
            echo "⚠️ Files committed but push failed"
        )
    ) else (
        echo "❌ Commit failed"
    )
) else (
    echo "ℹ️ No files staged - all may already be tracked"
)

echo.
echo Step 8: Final status check...
echo "Final git status:"
git status --porcelain

echo "Recent commit:"
git log --oneline -1

echo.
echo "========================================"
echo "GIT TRACKING OPERATION COMPLETE"
echo "All existing files should now be tracked"
echo "========================================"
pause