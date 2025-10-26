@echo off
echo ========================================
echo CROSSED-OVER CHANGES: .gitignore Issue Fix
echo Recovering Files Ignored by .gitignore
echo ========================================

echo 🔍 DIAGNOSIS: Files may be ignored by .gitignore rules
echo 🔧 SOLUTION: Force add ignored files and fix gitignore issues
echo.

echo Step 1: Check what files are being ignored...
echo "Files currently ignored by git:"
git status --ignored --porcelain

echo.
echo Step 2: Backup current .gitignore...
copy .gitignore .gitignore.backup 2>nul

echo Step 3: Temporarily disable problematic .gitignore rules...
echo "Commenting out recovery folder ignores..."

REM Create a new gitignore without the problematic rules
(
echo # Recovery folders ^(temporarily re-enabled for recovery^)
echo # LIFE-RECOVERY/
echo # SergiLIFE-RECOVERED/
echo.
) > .gitignore.temp

REM Append the rest of the gitignore
more +4 .gitignore >> .gitignore.temp 2>nul

REM Replace the gitignore
move .gitignore.temp .gitignore 2>nul

echo Step 4: Force add ALL files including previously ignored ones...
git add . --force
git add -A --force
git add --all --force

REM Specifically target the recovery folders
git add LIFE-RECOVERY/ --force 2>nul
git add SergiLIFE-RECOVERED/ --force 2>nul

REM Add all files with force flag to override gitignore
git add * --force 2>nul

echo.
echo Step 5: Add files by explicit patterns...
for /r %%f in (*.py) do git add "%%f" --force 2>nul
for /r %%f in (*.js) do git add "%%f" --force 2>nul
for /r %%f in (*.html) do git add "%%f" --force 2>nul
for /r %%f in (*.css) do git add "%%f" --force 2>nul
for /r %%f in (*.md) do git add "%%f" --force 2>nul
for /r %%f in (*.txt) do git add "%%f" --force 2>nul
for /r %%f in (*.json) do git add "%%f" --force 2>nul
for /r %%f in (*.yml) do git add "%%f" --force 2>nul
for /r %%f in (*.bat) do git add "%%f" --force 2>nul

echo.
echo Step 6: Check recovery results...
echo "Files now staged:"
git diff --cached --name-only

echo.
for /f %%i in ('git diff --cached --name-only ^| find /c /v ""') do set staged=%%i
echo "Total recovered files: %staged%"

if %staged% GTR 0 (
    echo.
    echo Step 7: Commit the recovered files...
    git commit -m "GITIGNORE FIX: Recover all %staged% crossed-over changes - fixed .gitignore conflicts and restored complete L.I.F.E Platform"
    
    if %ERRORLEVEL% EQU 0 (
        echo "✅ Recovery commit successful!"
        
        echo.
        echo Step 8: Push recovered changes...
        git push origin main
        
        if %ERRORLEVEL% EQU 0 (
            echo "🎉 SUCCESS! All crossed-over changes recovered!"
            echo "✅ %staged% files restored and pushed"
            echo "✅ .gitignore conflicts resolved"
            echo "✅ Complete platform synchronized"
        ) else (
            echo "⚠️ Files committed but push failed - trying force push..."
            git push origin main --force
        )
    ) else (
        echo "❌ Commit failed"
    )
    
) else (
    echo "⚠️ No files were staged - deeper investigation needed"
    
    echo.
    echo "Advanced diagnostics:"
    echo "Repository status:"
    git status --porcelain
    
    echo.
    echo "Ignored files:"
    git status --ignored --porcelain
    
    echo.
    echo "Files in current directory:"
    dir /b | head -10
)

echo.
echo Step 9: Restore original .gitignore if needed...
if exist ".gitignore.backup" (
    echo "Restore original .gitignore? (y/n)"
    set /p restore_choice=""
    if /I "%restore_choice%"=="y" (
        move .gitignore.backup .gitignore
        echo "✅ Original .gitignore restored"
    )
)

echo.
echo "========================================"
echo "GITIGNORE FIX COMPLETE!"
echo "Crossed-over changes recovery attempted"
echo "========================================"
pause