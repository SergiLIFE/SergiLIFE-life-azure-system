#!/usr/bin/env python3
"""
Quick Test Launcher for L.I.F.E Platform Validation
Executes the complete testing suite with comprehensive error handling
"""

import os
import sys
import traceback

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required imports are available"""
    try:
        import asyncio
        import json
        import logging
        from datetime import datetime

        import numpy as np
        print("✅ All basic imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def run_manual_component_test():
    """Manual component testing as specified"""
    print("\n🔬 Starting Manual Component Testing...")
    try:
        import asyncio

        from life_integration_testing_guide import LIFEIntegrationTestingGuide
        
        print("✅ Successfully imported LIFEIntegrationTestingGuide")
        
        guide = LIFEIntegrationTestingGuide()
        print("✅ Successfully created testing guide instance")
        
        print("🚀 Running complete validation suite...")
        result = asyncio.run(guide.run_complete_validation_suite())
        
        print(f"✅ Validation completed. Overall result: {result}")
        return result
        
    except Exception as e:
        print(f"❌ Error in manual component test: {e}")
        print(f"❌ Traceback: {traceback.format_exc()}")
        return None

def main():
    """Main execution function"""
    print("🧠 L.I.F.E Platform - Quick Test Launcher")
    print("=" * 60)
    
    # Test imports first
    if not test_imports():
        print("❌ Import test failed. Installing requirements...")
        os.system("pip install numpy asyncio")
        return
    
    # Run manual component test
    result = run_manual_component_test()
    
    if result:
        print("\n🎉 SUCCESS: L.I.F.E Platform validation completed!")
        print(f"📊 Test Results: {result}")
    else:
        print("\n❌ FAILED: Could not complete validation")

if __name__ == "__main__":
    main()if __name__ == "__main__":
    main()