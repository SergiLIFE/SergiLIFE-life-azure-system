#!/usr/bin/env python3
"""
Simple test to check autonomous_optimizer import
"""

import os
import sys

print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

try:
    print("Attempting to import autonomous_optimizer...")
    import autonomous_optimizer

    print("✅ Import successful!")

    print("Attempting to create AutonomousOptimizer...")
    optimizer = autonomous_optimizer.AutonomousOptimizer()
    print("✅ AutonomousOptimizer created successfully!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
