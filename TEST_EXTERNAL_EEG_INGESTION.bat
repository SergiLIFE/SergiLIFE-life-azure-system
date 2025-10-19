@echo off
echo ========================================
echo L.I.F.E PLATFORM - EXTERNAL EEG INGESTION TEST
echo ========================================
echo.
echo Testing the new "Ingest External EEG Data" functionality
echo that pulls PhysioNet and OpenNeuro datasets during 
echo nocturnal optimization for pipeline validation.
echo.

REM Test the ingestion engine locally
echo 🧠 Testing External EEG Ingestion Engine...
python external_eeg_ingestion_engine.py
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Ingestion engine test failed
    pause
    exit /b 1
)

echo.
echo ✅ Ingestion engine test completed
echo.

REM Test nocturnal optimizer integration
echo 🌙 Testing Nocturnal Optimizer Integration...
python nocturnal_eeg_ingestion_optimizer.py
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Nocturnal optimizer test failed
    pause
    exit /b 1
)

echo.
echo ✅ Nocturnal optimizer test completed
echo.

REM Test validation suite
echo 🔬 Running Ingestion Validation Test Suite...
python external_eeg_ingestion_test_suite.py
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Validation test suite failed
    pause
    exit /b 1
)

echo.
echo ✅ Validation test suite completed
echo.

REM Open dashboard for visual inspection
echo 🌐 Opening External EEG Ingestion Dashboard...
start external_eeg_ingestion_dashboard.html

echo.
echo ========================================
echo ✅ EXTERNAL EEG INGESTION INTEGRATION COMPLETE
echo ========================================
echo.
echo Your L.I.F.E Platform now includes:
echo.
echo 📊 New "Ingest EEG Data" tab in dashboard
echo 🧠 External dataset processing engine
echo 🌙 Nocturnal optimization integration
echo 🔬 Comprehensive validation test suite
echo ⚡ Azure Function API endpoints
echo.
echo The platform can now automatically pull PhysioNet and
echo OpenNeuro datasets during off-peak hours to validate
echo your EEG processing pipeline accuracy and latency.
echo.
echo Next: Deploy to Azure to enable live ingestion testing
echo Command: DIRECT_AZURE_DEPLOYMENT.bat
echo.
pause