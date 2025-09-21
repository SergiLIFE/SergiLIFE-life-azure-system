#!/usr/bin/env python3
"""
Simple L.I.F.E Platform Status Check
Quick validation of platform components

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

print("=" * 60)
print("L.I.F.E PLATFORM STATUS CHECK")
print("=" * 60)

# Test basic Python functionality
print("✅ Python execution: OK")

# Test NumPy
try:
    import numpy as np

    print("✅ NumPy available:", np.__version__)
except ImportError:
    print("❌ NumPy not available")

# Test L.I.F.E modules
modules_status = {}

# Test core module
try:
    from lifetheory import create_life_algorithm

    modules_status["lifetheory"] = True
    print("✅ L.I.F.E Theory Core: OK")
except ImportError as e:
    modules_status["lifetheory"] = False
    print("❌ L.I.F.E Theory Core:", str(e))

# Test EEG processor
try:
    from eeg_processor import create_life_eeg_processor

    modules_status["eeg_processor"] = True
    print("✅ EEG Processor: OK")
except ImportError as e:
    modules_status["eeg_processor"] = False
    print("❌ EEG Processor:", str(e))

# Test Venturi system
try:
    from venturi_gates_system import create_venturi_system

    modules_status["venturi_gates"] = True
    print("✅ Venturi Gates System: OK")
except ImportError as e:
    modules_status["venturi_gates"] = False
    print("❌ Venturi Gates System:", str(e))

# Test signal processing
try:
    from life_module1_signal_processing import create_life_signal_processor

    modules_status["signal_processing"] = True
    print("✅ Signal Processing Module: OK")
except ImportError as e:
    modules_status["signal_processing"] = False
    print("❌ Signal Processing Module:", str(e))

# Test pattern recognition
try:
    from life_module2_pattern_recognition import create_life_pattern_recognizer

    modules_status["pattern_recognition"] = True
    print("✅ Pattern Recognition Module: OK")
except ImportError as e:
    modules_status["pattern_recognition"] = False
    print("❌ Pattern Recognition Module:", str(e))

# Summary
print("\n" + "=" * 60)
print("PLATFORM SUMMARY")
print("=" * 60)

total_modules = len(modules_status)
available_modules = sum(modules_status.values())
availability_rate = (
    (available_modules / total_modules) * 100 if total_modules > 0 else 0
)

print(f"Available Modules: {available_modules}/{total_modules}")
print(f"Availability Rate: {availability_rate:.1f}%")

if availability_rate >= 80:
    print("🚀 L.I.F.E Platform Status: EXCELLENT")
elif availability_rate >= 60:
    print("✨ L.I.F.E Platform Status: GOOD")
elif availability_rate >= 40:
    print("⚠️  L.I.F.E Platform Status: PARTIAL")
else:
    print("🔧 L.I.F.E Platform Status: NEEDS SETUP")

print("\n✨ L.I.F.E Platform Check Complete!")
