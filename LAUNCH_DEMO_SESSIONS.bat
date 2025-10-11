@echo off
REM L.I.F.E. Platform - Three Demo Sessions Quick Launcher
REM October 15, 2025

echo.
echo ========================================================
echo  L.I.F.E. Platform - Three Demo Sessions Launcher
echo  October 15, 2025 - Healthcare Professional Demos
echo ========================================================
echo.
echo Available Sessions:
echo.
echo  1. Clinical Professionals (09:00-09:45 BST)
echo     - 17 participants - Neurology, Psychiatry, Pediatrics
echo     - Focus: Clinical workflow optimization
echo     - Tier: Professional ($75,000/year)
echo.
echo  2. Research ^& IT Leadership (11:00-11:45 BST)  
echo     - 6 participants - Research Directors, IT Managers
echo     - Focus: Enterprise capabilities and research
echo     - Tier: Enterprise ($250,000/year)
echo.
echo  3. Executive ^& Strategic Overview (14:00-14:30 BST)
echo     - 23 participants - All attendees combined
echo     - Focus: Strategic value and ROI analysis
echo     - Tier: Both tiers with custom options
echo.
echo ========================================================

:menu
echo.
echo Select demo session to launch:
echo.
echo [1] Clinical Professionals Session
echo [2] Research ^& IT Leadership Session  
echo [3] Executive ^& Strategic Overview Session
echo [A] Launch ALL sessions (3 browser tabs)
echo [S] Start server only
echo [Q] Quit
echo.
set /p choice="Enter your choice (1-3, A, S, Q): "

if /i "%choice%"=="1" goto session1
if /i "%choice%"=="2" goto session2
if /i "%choice%"=="3" goto session3
if /i "%choice%"=="A" goto allsessions
if /i "%choice%"=="S" goto serveronly
if /i "%choice%"=="Q" goto quit

echo Invalid choice. Please try again.
goto menu

:session1
echo.
echo ======================================
echo  Launching Session 1: Clinical Professionals
echo ======================================
python session_launcher.py 1
pause
goto menu

:session2
echo.
echo ======================================
echo  Launching Session 2: Research ^& IT Leadership
echo ======================================
python session_launcher.py 2
pause
goto menu

:session3
echo.
echo ======================================
echo  Launching Session 3: Executive ^& Strategic Overview
echo ======================================
python session_launcher.py 3
pause
goto menu

:allsessions
echo.
echo ======================================
echo  Launching ALL Three Sessions
echo  (Opens 3 browser tabs)
echo ======================================
python session_launcher.py all
pause
goto menu

:serveronly
echo.
echo ======================================
echo  Starting Demo Server Only
echo ======================================
python session_launcher.py
pause
goto menu

:quit
echo.
echo Thank you for using L.I.F.E. Platform Demo Sessions!
echo Demo server may continue running in background.
echo.
pause
exit
