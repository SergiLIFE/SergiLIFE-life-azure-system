@echo off
REM L.I.F.E Platform Repository Restructuring Script
REM ===============================================
REM This script helps create the new core repository structure
REM Run this to solve the GitHub "too many files" issue

echo 🎯 L.I.F.E Platform Repository Restructuring
echo ============================================
echo.
echo Problem: Repository has 1,257+ files (GitHub truncating)
echo Solution: Create focused core repository with ~30 essential files
echo.

REM Create the core repository directory
echo 📁 Creating core repository directory...
if not exist "..\life-platform-core" (
    mkdir "..\life-platform-core"
    echo ✅ Created: ..\life-platform-core
) else (
    echo ⚠️  Directory already exists: ..\life-platform-core
)

echo.
echo 📋 Essential files for core repository:
echo.

REM List the essential files that need to be copied
echo Core Algorithm:
echo   - experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py
echo   - lifetheory.py
echo   - venturi_gates_system.py
echo.

echo Platform Files:
echo   - alternative_deployment.py
echo   - life_theory_platform_server.py
echo   - LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
echo.

echo Configuration:
echo   - README.md
echo   - requirements.txt
echo   - azure_config.py
echo   - host.json
echo   - local.settings.json
echo.

echo Azure Integration:
echo   - azure_functions_workflow.py
echo   - function_app.py
echo.

echo Supporting Files:
echo   - LICENSE
echo   - .gitignore
echo   - styles.css
echo.

echo 🚀 Next Steps:
echo 1. Review REPOSITORY_RESTRUCTURING_GUIDE.md
echo 2. Copy essential files to ..\life-platform-core
echo 3. Test core functionality works
echo 4. Create git repository for core
echo 5. Create additional focused repositories as needed
echo.

echo 🎯 This will reduce your repository from 1,257+ files to ~30 core files!
echo.

pause