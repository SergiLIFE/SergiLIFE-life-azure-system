#!/usr/bin/env python3
"""Test script for three_venturi_harmonic_calibration imports"""

try:
    import asyncio
    import json
    import logging
    import math
    import os
    import statistics
    from datetime import datetime
    from typing import Any, Dict, List, Optional

    import numpy as np
    print("✅ Basic imports successful")

    # Test Venturi imports
    try:
        from venturi_gates_system import (VenturiGate, VenturiGateConfig,
                                          VenturiGatesSystem, VenturiGateType)
        print("✅ Venturi system imports successful")
    except ImportError:
        print("⚠️  Venturi system not available, using mock implementation")
        class MockVenturiGateType:
            SIGNAL_ENHANCEMENT = "signal_enhancement"
            NOISE_REDUCTION = "noise_reduction"
            PATTERN_EXTRACTION = "pattern_extraction"
        VenturiGateType = MockVenturiGateType

    # Test the main class import
    from three_venturi_harmonic_calibration import \
        ThreeVenturiHarmonicCalibrator
    print("✅ ThreeVenturiHarmonicCalibrator import successful")

    # Test basic instantiation
    calibrator = ThreeVenturiHarmonicCalibrator()
    print("✅ Calibrator instantiation successful")

    print("🎉 All tests passed!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()