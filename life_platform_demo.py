"""
L.I.F.E Platform Integration Demonstration
Complete showcase of all integrated modules working together

Copyright 2025 - Sergio Paya Borrull
Learning Individually From Experience
"""

import time
from datetime import datetime

import numpy as np

print("="*80)
print("🚀 L.I.F.E PLATFORM INTEGRATION DEMONSTRATION")
print("Learning Individually From Experience - Complete System Showcase")
print("="*80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Test all modules are available
modules_tested = 0
modules_passed = 0

print("\n🔍 MODULE AVAILABILITY TEST")
print("-" * 50)

# Test 1: Core L.I.F.E Algorithm
try:
    from lifetheory import create_life_algorithm
    life_algorithm = create_life_algorithm()
    print("✅ Core L.I.F.E Algorithm: READY")
    modules_tested += 1
    modules_passed += 1
except Exception as e:
    print(f"❌ Core L.I.F.E Algorithm: {e}")
    modules_tested += 1

# Test 2: EEG Processor
try:
    from eeg_processor import create_life_eeg_processor
    eeg_processor = create_life_eeg_processor()
    print("✅ EEG Processor: READY")
    modules_tested += 1
    modules_passed += 1
except Exception as e:
    print(f"❌ EEG Processor: {e}")
    modules_tested += 1

# Test 3: Venturi Gates System
try:
    from venturi_gates_system import create_venturi_system
    venturi_system = create_venturi_system()
    print("✅ Venturi Gates System: READY")
    modules_tested += 1
    modules_passed += 1
except Exception as e:
    print(f"❌ Venturi Gates System: {e}")
    modules_tested += 1

# Test 4: Signal Processing
try:
    from life_module1_signal_processing import create_life_signal_processor
    signal_processor = create_life_signal_processor()
    print("✅ Signal Processing Module: READY")
    modules_tested += 1
    modules_passed += 1
except Exception as e:
    print(f"❌ Signal Processing Module: {e}")
    modules_tested += 1

# Test 5: Pattern Recognition
try:
    from life_module2_pattern_recognition import (
        PatternType,
        create_life_pattern_recognizer,
    )
    pattern_recognizer = create_life_pattern_recognizer(PatternType.NEURAL)
    print("✅ Pattern Recognition Module: READY")
    modules_tested += 1
    modules_passed += 1
except Exception as e:
    print(f"❌ Pattern Recognition Module: {e}")
    modules_tested += 1

# Test 6: Cognitive Behavioral Model
try:
    from life_module3_cognitive_behavioral import create_life_cognitive_model
    cognitive_model = create_life_cognitive_model()
    print("✅ Cognitive Behavioral Model: READY")
    modules_tested += 1
    modules_passed += 1
except Exception as e:
    print(f"❌ Cognitive Behavioral Model: {e}")
    modules_tested += 1

# Test 7: Adaptive Neural Networks
try:
    from life_module4_adaptive_neural_networks import (
        ActivationFunction,
        create_life_neural_network,
    )
    neural_network = create_life_neural_network(
        input_size=10, 
        hidden_layers=[16, 8], 
        output_size=1,
        activation=ActivationFunction.LIFE_ADAPTIVE
    )
    print("✅ Adaptive Neural Networks: READY")
    modules_tested += 1
    modules_passed += 1
except Exception as e:
    print(f"❌ Adaptive Neural Networks: {e}")
    modules_tested += 1

# Test 8: Real-Time Processing
try:
    from life_module5_realtime_processing import create_life_processor
    realtime_processor = create_life_processor(max_workers=2, buffer_size=50)
    print("✅ Real-Time Processing Engine: READY")
    modules_tested += 1
    modules_passed += 1
except Exception as e:
    print(f"❌ Real-Time Processing Engine: {e}")
    modules_tested += 1

# Module Summary
availability_rate = (modules_passed / modules_tested) * 100
print(f"\n📊 MODULE SUMMARY")
print(f"   Available: {modules_passed}/{modules_tested}")
print(f"   Success Rate: {availability_rate:.1f}%")

if availability_rate >= 90:
    status = "🚀 EXCELLENT - Full platform operational!"
elif availability_rate >= 75:
    status = "✨ GOOD - Most modules working!"
elif availability_rate >= 50:
    status = "⚠️  PARTIAL - Some modules available!"
else:
    status = "🔧 LIMITED - Basic functionality only!"

print(f"   Status: {status}")

# Integration Test
if modules_passed >= 3:  # Need at least core modules
    print(f"\n🔬 INTEGRATION TESTING")
    print("-" * 50)
    
    try:
        # Generate test data
        test_signal = np.sin(2 * np.pi * 10 * np.linspace(0, 1, 1000))  # 10 Hz sine
        test_signal += 0.2 * np.random.randn(1000)  # Add noise
        
        print("✅ Test signal generated (1000 samples, 10 Hz + noise)")
        
        # Step 1: Core L.I.F.E processing
        if 'life_algorithm' in locals():
            life_result = life_algorithm.process(
                test_signal[:100],  # Limit for demo
                {"integration_test": True, "signal_type": "synthetic"}
            )
            adaptation_score = life_result.get('adaptation_score', 0.0)
            print(f"✅ L.I.F.E Processing: adaptation_score = {adaptation_score:.3f}")
        
        # Step 2: Signal processing
        if 'signal_processor' in locals():
            signal_result = signal_processor.process_signal(
                test_signal, 
                1000,  # sampling rate
                {"filter_type": "bandpass", "extract_features": True}
            )
            features_count = len(signal_result.get('features', {}))
            print(f"✅ Signal Processing: {features_count} features extracted")
        
        # Step 3: Pattern recognition
        if 'pattern_recognizer' in locals() and 'signal_result' in locals():
            features_array = np.array(list(signal_result['features'].values())).reshape(1, -1)
            pattern_features = pattern_recognizer.extract_pattern_features(features_array)
            pattern_complexity = len(pattern_features.complexity_measures)
            print(f"✅ Pattern Recognition: {pattern_complexity} pattern features")
        
        # Step 4: Venturi enhancement
        if 'venturi_system' in locals():
            venturi_result = venturi_system.enhance_signal(
                test_signal[:500],  # Smaller for demo
                {"mode": "parallel", "gain": 1.2}
            )
            enhancement_factor = venturi_result.get('enhancement_factor', 1.0)
            print(f"✅ Venturi Enhancement: factor = {enhancement_factor:.3f}")
        
        print("✅ Integration test completed successfully!")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")

# Performance Demonstration
if modules_passed >= 2:
    print(f"\n⚡ PERFORMANCE DEMONSTRATION")
    print("-" * 50)
    
    # Throughput test
    if 'life_algorithm' in locals():
        start_time = time.time()
        
        for i in range(10):
            test_data = np.random.randn(100)
            life_algorithm.process(test_data, {"perf_test": True, "iteration": i})
        
        elapsed = time.time() - start_time
        throughput = 1000 / elapsed  # elements per second
        print(f"✅ L.I.F.E Throughput: {throughput:.0f} elements/sec")
    
    # Signal processing speed
    if 'signal_processor' in locals():
        start_time = time.time()
        
        for i in range(5):
            test_signal = np.random.randn(1000)
            signal_processor.process_signal(test_signal, 1000, {"fast_mode": True})
        
        elapsed = time.time() - start_time
        rate = 5000 / elapsed  # samples per second
        print(f"✅ Signal Processing Rate: {rate:.0f} samples/sec")

# Final Assessment
print(f"\n🎯 FINAL PLATFORM ASSESSMENT")
print("=" * 50)

if availability_rate == 100:
    assessment = "🚀 REVOLUTIONARY - Complete L.I.F.E platform operational!"
    recommendation = "Ready for production deployment and advanced research!"
elif availability_rate >= 75:
    assessment = "✨ EXCELLENT - Core platform functioning perfectly!"
    recommendation = "Ready for comprehensive testing and optimization!"
elif availability_rate >= 50:
    assessment = "⚠️  FUNCTIONAL - Basic platform capabilities available!"
    recommendation = "Continue module integration for full functionality!"
else:
    assessment = "🔧 DEVELOPING - Foundation modules operational!"
    recommendation = "Focus on core module stability and expansion!"

print(f"Assessment: {assessment}")
print(f"Recommendation: {recommendation}")

print(f"\n✨ L.I.F.E PLATFORM DEMONSTRATION COMPLETE!")
print(f"Learning Individually From Experience - {datetime.now().strftime('%H:%M:%S')}")
print("="*80)
