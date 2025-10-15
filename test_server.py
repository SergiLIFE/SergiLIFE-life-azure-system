#!/usr/bin/env python3
"""
🧠 L.I.F.E AI Platform - Server Test Suite
Test the EEG processing server for October 15th strategic partnership demo

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import json
import logging
import os
import sys
import time
from datetime import datetime

import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def test_server_functionality():
    """Test L.I.F.E EEG server functionality"""
    
    server_url = "http://localhost:5000"
    
    print("🧠 L.I.F.E AI Platform - Server Test Suite")
    print("🚀 Strategic Partnership Ready - October 15, 2025")
    print("=" * 60)
    
    # Test 1: Server Health Check
    print("\n📡 Test 1: Server Health Check")
    try:
        response = requests.get(f"{server_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server Online: {data['service']}")
            print(f"📊 Version: {data['version']}")
            print(f"⏰ Status: {data['status']}")
        else:
            print(f"❌ Server returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running")
        print("💡 Please start the server with: python life_eeg_server.py")
        return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Create test EEG file
    print("\n🔬 Test 2: Creating Test EEG File")
    test_eeg_content = """timestamp,channel1,channel2,channel3,channel4
0.000,0.1,-0.2,0.3,-0.1
0.004,0.2,-0.1,0.2,0.0
0.008,-0.1,0.3,-0.2,0.1
0.012,0.0,-0.3,0.1,0.2
0.016,0.3,0.1,-0.1,-0.2
"""
    
    test_filename = "test_eeg_data.csv"
    with open(test_filename, 'w') as f:
        f.write(test_eeg_content)
    print(f"✅ Created test EEG file: {test_filename}")
    
    # Test 3: File Upload
    print("\n📤 Test 3: EEG File Upload")
    try:
        with open(test_filename, 'rb') as f:
            files = {'file': (test_filename, f, 'text/csv')}
            response = requests.post(f"{server_url}/api/upload-eeg", files=files, timeout=30)
        
        if response.status_code == 200:
            upload_data = response.json()
            print(f"✅ Upload successful: {upload_data['filename']}")
            print(f"📊 File size: {upload_data['size_mb']} MB")
            uploaded_filename = upload_data['filename']
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Upload test failed: {e}")
        return False
    
    # Test 4: EEG Processing
    print("\n🧠 Test 4: L.I.F.E EEG Processing")
    try:
        processing_data = {"filename": uploaded_filename}
        response = requests.post(
            f"{server_url}/api/process-eeg",
            json=processing_data,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        if response.status_code == 200:
            analysis_data = response.json()
            print("✅ Processing completed successfully!")
            
            # Display key metrics
            analysis = analysis_data['analysis']
            print(f"🔍 Processing Mode: {analysis.get('processing_mode', 'Standard')}")
            
            if 'neuroplasticity_analysis' in analysis:
                neuro = analysis['neuroplasticity_analysis']
                print(f"🧠 Neuroplasticity Index: {neuro['neuroplasticity_index']}%")
                print(f"📈 Learning Potential: {neuro['learning_potential']}%")
                print(f"🎯 Attention Level: {neuro['attention_level']}%")
            
            if 'ai_insights' in analysis:
                insights = analysis['ai_insights']
                print(f"🤖 Pattern Recognition: {insights['pattern_recognition_accuracy']}%")
                print(f"🔍 Anomaly Detection: {insights['anomaly_detection']}%")
            
            print(f"⏱️ Processing Time: {analysis_data['processing_time']}")
            
        else:
            print(f"❌ Processing failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Processing test failed: {e}")
        return False
    
    # Cleanup
    try:
        os.remove(test_filename)
        print(f"\n🧹 Cleaned up test file: {test_filename}")
    except:
        pass
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED!")
    print("✅ L.I.F.E AI Platform server is ready for October 15th demo")
    print("🚀 Strategic partnership integration complete")
    
    return True

def check_enhanced_processing():
    """Check if enhanced EEG processing is available"""
    print("\n🔬 Enhanced Processing Check")
    try:
        import eeg_processing
        print("✅ Enhanced EEG processing module available")
        
        try:
            import mne
            print("✅ MNE-Python library available")
            print("🧠 Real EEG file formats supported: .edf, .bdf, .set, .cnt")
        except ImportError:
            print("⚠️ MNE-Python not installed - using NumPy fallback")
            
    except ImportError:
        print("⚠️ Enhanced processing module not found - using standard mode")

if __name__ == "__main__":
    print("🧠 L.I.F.E AI Platform - Comprehensive Server Test")
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Strategic Partnership Demo Preparation")
    
    # Check enhanced processing availability
    check_enhanced_processing()
    
    # Wait a moment for server startup
    print("\n⏳ Waiting for server startup...")
    time.sleep(3)
    
    # Run tests
    success = test_server_functionality()
    
    if success:
        print("\n🏆 L.I.F.E AI Platform is READY!")
        print("📋 Next steps:")
        print("   1. Open LIFE_AI_PLATFORM_REAL.html in browser")
        print("   2. Test EEG file upload functionality")
        print("   3. Verify real-time processing results")
        print("   4. Prepare for October 15th strategic meeting")
    else:
        print("\n❌ Tests failed - server needs attention")
        print("💡 Check server logs and restart if needed")
    
    print("\n🎉 Test suite complete!")    print("\n🎉 Test suite complete!")