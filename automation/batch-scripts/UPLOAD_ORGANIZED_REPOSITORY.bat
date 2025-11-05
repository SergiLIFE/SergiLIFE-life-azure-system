@echo off
echo === L.I.F.E. PLATFORM REPOSITORY ORGANIZATION - GIT COMMIT ===
echo.

REM Navigate to repository directory
cd /d "c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"

echo Current directory:
cd

echo.
echo === Checking Git Status ===
git status

echo.
echo === Adding organized files ===
git add .

echo.
echo === Committing organized repository ===
git commit -m "Repository Organization Complete - Archive Structure Implemented"

echo.
echo === Pushing to GitHub ===
git push origin main

echo.
echo === ORGANIZATION UPLOADED TO GITHUB ===
echo Your organized repository is now visible on GitHub!
echo No more truncation issues!
echo.
pause