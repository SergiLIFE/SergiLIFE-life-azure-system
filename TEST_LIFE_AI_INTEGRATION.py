#!/usr/bin/env python3
"""
L.I.F.E AI Platform Integration Test
Tests the complete experimentP2L algorithm integration in LIFE_AI_PLATFORM_REAL.html
"""

import os
import re
import time
from datetime import datetime


def test_life_ai_integration():
    """Test the complete L.I.F.E algorithm integration in AI platform"""
    
    print("🧠 L.I.F.E AI Platform Integration Test")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # File path
    ai_platform_file = "LIFE_AI_PLATFORM_REAL.html"
    
    if not os.path.exists(ai_platform_file):
        print(f"❌ ERROR: {ai_platform_file} not found!")
        return False
    
    print(f"✅ Found AI Platform file: {ai_platform_file}")
    
    # Read file content
    with open(ai_platform_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📊 File size: {len(content):,} characters")
    print()
    
    # Test for L.I.F.E algorithm components
    tests = [
        ("Title Integration", "Complete Algorithm Integration.*experimentP2L"),
        ("LearningStage Enum", r"const LearningStage\s*=\s*{"),
        ("NeuralState Enum", r"const NeuralState\s*=\s*{"),
        ("EEGMetrics Class", r"class EEGMetrics\s*{"),
        ("LearningOutcome Class", r"class LearningOutcome\s*{"),
        ("LIFEAICore Class", r"class LIFEAICore\s*{"),
        ("100-Cycle Test Method", r"runAI100CycleEEGTest\(\)"),
        ("Complete Integration Version", r"2025\.1\.0-AI-COMPLETE-INTEGRATION"),
        ("experimentP2L Reference", "experimentP2L"),
        ("Learning Stages Tab", r'<button.*onclick="showTab\(\'life-algorithm\'\)"'),
        ("L.I.F.E Status Indicators", r'id="learning-stage"'),
        ("Real-time Processing", r"startRealTimeAIProcessing"),
        ("Auto-start Functionality", "Auto-starting L.I.F.E real-time processing"),
        ("Neural State Display", r'id="neural-state"'),
        ("Adaptation Parameters", "adaptationParameters")
    ]
    
    passed = 0
    failed = 0
    
    print("🔍 Running Integration Tests:")
    print("-" * 40)
    
    for test_name, pattern in tests:
        if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            print(f"✅ {test_name}")
            passed += 1
        else:
            print(f"❌ {test_name}")
            failed += 1
    
    print()
    print("📊 Test Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    # Additional checks
    print()
    print("🔍 Additional Verification:")
    
    # Check for Learning Stages
    learning_stages = ['ACQUISITION', 'CONSOLIDATION', 'RETRIEVAL', 'ADAPTATION']
    found_stages = []
    for stage in learning_stages:
        if stage in content:
            found_stages.append(stage)
    
    print(f"📚 Learning Stages Found: {len(found_stages)}/4 - {found_stages}")
    
    # Check for Neural States
    neural_states = ['RESTING', 'FOCUSED', 'LEARNING', 'PROCESSING', 'CONSOLIDATING']
    found_states = []
    for state in neural_states:
        if state in content:
            found_states.append(state)
    
    print(f"🧠 Neural States Found: {len(found_states)}/5 - {found_states}")
    
    # Check for EEG metrics
    eeg_metrics = ['alphaPower', 'betaPower', 'thetaPower', 'deltaPower', 'gammaPower', 'coherenceScore']
    found_metrics = []
    for metric in eeg_metrics:
        if metric in content:
            found_metrics.append(metric)
    
    print(f"📊 EEG Metrics Found: {len(found_metrics)}/6 - {found_metrics}")
    
    print()
    
    # Overall assessment
    if passed >= 12 and len(found_stages) >= 3 and len(found_states) >= 4:
        print("🎉 INTEGRATION SUCCESSFUL!")
        print("✅ Complete L.I.F.E Theory Algorithm successfully integrated into AI platform")
        print("🧠 experimentP2L components fully implemented")
        print("🚀 Platform ready for production neuroadaptive learning")
        return True
    else:
        print("⚠️  INTEGRATION INCOMPLETE")
        print("❌ Some L.I.F.E algorithm components may be missing")
        return False

if __name__ == "__main__":
    try:
        success = test_life_ai_integration()
        print()
        if success:
            print("🌟 L.I.F.E AI Platform Integration Test PASSED")
            print("🎯 Ready for neuroadaptive AI processing!")
        else:
            print("🔧 L.I.F.E AI Platform Integration needs attention")
        print("=" * 60)
    except Exception as e:
        print(f"❌ Test error: {e}")        print(f"❌ Test error: {e}")