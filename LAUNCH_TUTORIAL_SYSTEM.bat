@echo off
REM 🎮 L.I.F.E. Platform - Self-Guided Tutorial System Launcher
REM Enhanced Tab Navigation with Back/Forward Controls
REM Copyright 2025 - Sergio Paya Borrull

echo.
echo ================================================================
echo 🎮 L.I.F.E. Platform - Self-Guided Tutorial System
echo ================================================================
echo 🎯 Enhanced Tab Navigation with Back/Forward Controls  
echo 📊 Complete Step Tracking and Progress Persistence
echo 🔄 Non-Linear Navigation with Jump-to-Step Capability
echo ================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo 📥 Please install Python from https://python.org
    pause
    exit /b 1
)

REM Install required dependencies if needed
echo 📦 Installing required dependencies...
pip install asyncio >nul 2>&1

REM Run the tutorial system
echo 🚀 Launching Self-Guided Tutorial System...
echo.
python SELF_GUIDED_TUTORIAL_SYSTEM.py

REM Check if tutorial ran successfully
if %errorlevel% equ 0 (
    echo.
    echo ✅ Tutorial system completed successfully!
) else (
    echo.
    echo ❌ Tutorial system encountered an error
    echo 📋 Check the error messages above for details
)

echo.
echo 🎉 Thank you for using the L.I.F.E. Platform Tutorial System!
echo 🚀 Your progress has been saved automatically
echo.
pause