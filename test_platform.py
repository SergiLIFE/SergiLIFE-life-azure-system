#!/usr/bin/env python3
"""
Simple test script for L.I.F.E. Neuroadaptive Learning Platform
Tests basic functionality without Unicode characters
"""

import os
import sys

# Add current directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)


def test_platform_import():
    """Test if platform can be imported"""
    try:
        from neuroadaptive_learning_platform import NeuroadaptiveLearningPlatform

        print("[SUCCESS] Platform import successful")
        return True
    except ImportError as e:
        print(f"[ERROR] Import failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False


def test_basic_functionality():
    """Test basic platform functionality"""
    try:
        from neuroadaptive_learning_platform import (
            IndividualTraits,
            NeuroadaptiveLearningPlatform,
        )

        print("[INFO] Creating platform instance...")
        platform = NeuroadaptiveLearningPlatform()

        print("[INFO] Testing trait creation...")
        traits = IndividualTraits(
            cognitive_style="visual",
            curiosity=0.8,
            resilience=0.7,
            openness=0.9,
            focus_duration=25.0,
            preferred_complexity="medium",
            learning_pace="moderate",
        )

        print("[SUCCESS] Basic functionality test passed")
        return True

    except Exception as e:
        print(f"[ERROR] Basic functionality test failed: {e}")
        return False


if __name__ == "__main__":
    print("Testing L.I.F.E. Neuroadaptive Learning Platform...")
    print("=" * 60)

    import_success = test_platform_import()
    if import_success:
        basic_success = test_basic_functionality()
        if basic_success:
            print("\n[SUCCESS] All tests passed! Platform is ready to run.")
            print("Run: python neuroadaptive_learning_platform.py")
        else:
            print("\n[FAILED] Basic functionality test failed")
    else:
        print("\n[FAILED] Import test failed")

    print("=" * 60)
