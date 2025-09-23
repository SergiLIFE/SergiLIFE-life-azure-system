import json
from datetime import datetime
from pathlib import Path

import numpy as np

print("🧠 L.I.F.E. Azure EEG Testing - Environment Check")
print("=" * 60)

try:
    # Test NumPy
    print("✅ NumPy available:", np.__version__)
    
    # Test basic functionality
    data = np.random.randn(10, 5)
    print("✅ NumPy operations working")
    
    # Test file operations
    test_dir = Path("test_output")
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / "test.json"
    with open(test_file, 'w') as f:
        json.dump({"test": "success", "timestamp": datetime.now().isoformat()}, f)
    
    print("✅ File operations working")
    print(f"✅ Test file created: {test_file}")
    
    # Test the main EEG testing functionality
    print("\n🚀 Starting Azure EEG Testing...")
    
    # Import and run the simple tester
    exec(open('AZURE_EEG_SIMPLE_TESTER.py').read())
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()    traceback.print_exc()