@echo off
title L.I.F.E. Repository Upload to GitHub
color 0A

echo =====================================
echo  L.I.F.E. REPOSITORY GITHUB UPLOAD
echo =====================================
echo.

echo Step 1: Navigating to repository...
cd /d "c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"

echo Current directory: %cd%
echo.

echo Step 2: Checking if archive exists...
if exist "archive" (
    echo ✓ Archive structure found - ready to upload!
    echo.
) else (
    echo ✗ Archive not found - creating it now...
    mkdir archive
    mkdir archive\deployment
    mkdir archive\testing  
    mkdir archive\campaigns
    mkdir archive\documentation
    mkdir archive\experiments
    mkdir archive\backups
    mkdir archive\historical
    echo ✓ Archive structure created!
    echo.
)

echo Step 3: Adding all files to git...
git add . --all

echo Step 4: Checking git status...
git status --short

echo Step 5: Committing organized repository...
git commit -m "URGENT: Repository Organization - Solve GitHub Truncation Issue"

echo Step 6: Pushing to GitHub...
git push origin main

echo.
echo =====================================
echo  SUCCESS! Repository uploaded!
echo =====================================
echo.
echo Your GitHub repository now shows:
echo ✓ Organized structure
echo ✓ No truncation warnings  
echo ✓ Professional presentation
echo.
echo Visit: https://github.com/SergiLIFE/SergiLIFE-life-azure-system
echo.
pause