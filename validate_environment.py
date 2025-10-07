#!/usr/bin/env python3
"""
L.I.F.E. Platform Environment Validation
Validates that all core dependencies are properly installed and functional

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import sys
import traceback
from datetime import datetime


def validate_core_imports():
    """Validate all core L.I.F.E. Platform dependencies."""
    print("=" * 80)
    print("L.I.F.E. Platform Environment Validation")
    print("=" * 80)
    print(f"Python Version: {sys.version}")
    print(f"Python Path: {sys.executable}")
    print(f"Validation Time: {datetime.now()}")
    print("-" * 80)
    
    # Core imports test
    imports_to_test = [
        ("numpy", "Core numerical computing"),
        ("pandas", "Data manipulation and analysis"),
        ("scipy", "Scientific computing"),
        ("scikit-learn", "Machine learning"),
        ("tensorflow", "Deep learning framework"),
        ("torch", "PyTorch deep learning"),
        ("mne", "EEG/MEG data processing"),
        ("nilearn", "Neuroimaging data analysis"),
        ("azure.identity", "Azure authentication"),
        ("azure.storage.blob", "Azure Blob Storage"),
        ("azure.functions", "Azure Functions"),
        ("fastapi", "Web framework"),
        ("uvicorn", "ASGI server"),
        ("pytest", "Testing framework"),
        ("psutil", "System monitoring"),
        ("plotly", "Data visualization"),
        ("matplotlib", "Plotting library"),
        ("jupyter", "Jupyter notebooks"),
    ]
    
    success_count = 0
    failed_imports = []
    
    for module_name, description in imports_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name:<20} - {description}")
            success_count += 1
        except Exception as e:
            print(f"❌ {module_name:<20} - FAILED: {str(e)}")
            failed_imports.append((module_name, str(e)))
    
    print("-" * 80)
    print(f"Import Summary: {success_count}/{len(imports_to_test)} successful")
    
    if failed_imports:
        print(f"❌ {len(failed_imports)} imports failed:")
        for module, error in failed_imports:
            print(f"   - {module}: {error}")
        return False
    else:
        print("✅ All core dependencies imported successfully!")
        return True

def validate_life_components():
    """Validate L.I.F.E. Platform specific components."""
    print("\n" + "=" * 80)
    print("L.I.F.E. Platform Components Validation")
    print("=" * 80)
    
    try:
        # Test basic numpy/scientific computing
        import numpy as np
        test_array = np.random.randn(100, 100)
        result = np.linalg.svd(test_array)
        print("✅ NumPy scientific computing - Matrix operations working")
        
        # Test pandas data handling
        import pandas as pd
        df = pd.DataFrame({'A': np.random.randn(100), 'B': np.random.randn(100)})
        correlation = df.corr()
        print("✅ Pandas data analysis - Data manipulation working")
        
        # Test basic ML functionality
        from sklearn.ensemble import RandomForestClassifier
        clf = RandomForestClassifier(n_estimators=10, random_state=42)
        X = np.random.randn(100, 5)
        y = np.random.randint(0, 2, 100)
        clf.fit(X, y)
        print("✅ Scikit-learn ML - Machine learning models working")
        
        # Test TensorFlow (basic)
        import tensorflow as tf
        print(f"✅ TensorFlow {tf.__version__} - Deep learning framework loaded")
        
        # Test PyTorch (basic)
        import torch
        tensor = torch.randn(10, 10)
        print(f"✅ PyTorch {torch.__version__} - Deep learning framework loaded")
        
        # Test Azure SDK
        from azure.identity import DefaultAzureCredential
        print("✅ Azure Identity - Authentication SDK loaded")
        
        print("-" * 80)
        print("✅ All L.I.F.E. Platform components validated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Component validation failed: {str(e)}")
        traceback.print_exc()
        return False

def main():
    """Main validation function."""
    try:
        imports_ok = validate_core_imports()
        components_ok = validate_life_components()
        
        if imports_ok and components_ok:
            print("\n" + "=" * 80)
            print("🎉 L.I.F.E. Platform Environment: READY FOR PRODUCTION!")
            print("🚀 October 7th Launch: All systems operational")
            print("=" * 80)
            return True
        else:
            print("\n" + "=" * 80)
            print("⚠️  Environment validation issues detected")
            print("Please review failed components above")
            print("=" * 80)
            return False
            
    except Exception as e:
        print(f"Critical validation error: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)    sys.exit(0 if success else 1)