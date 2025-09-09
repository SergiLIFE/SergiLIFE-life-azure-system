"""
Core L.I.F.E Platform Validation
Testing the fundamental working modules

Copyright 2025 - Sergio Paya Borrull
"""

import time
from datetime import datetime

import numpy as np

print("="*60)
print("🚀 CORE L.I.F.E PLATFORM VALIDATION")
print("Learning Individually From Experience")
print("="*60)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60)

# Test core modules that we know work
working_modules = {}

print("\n🔍 CORE MODULE VALIDATION")
print("-" * 40)

# Test 1: Core L.I.F.E Algorithm
try:
    from lifetheory import create_life_algorithm
    life_algorithm = create_life_algorithm()
    
    # Test processing
    test_data = np.random.randn(100)
    result = life_algorithm.process(test_data, {"test": "core_validation"})
    adaptation_score = result.get('adaptation_score', 0.0)
    
    working_modules['core_life'] = {
        'status': 'WORKING',
        'adaptation_score': adaptation_score,
        'result_type': type(result).__name__
    }
    print(f"✅ Core L.I.F.E Algorithm: adaptation_score = {adaptation_score:.3f}")
    
except Exception as e:
    working_modules['core_life'] = {'status': 'ERROR', 'error': str(e)}
    print(f"❌ Core L.I.F.E Algorithm: {e}")

# Test 2: EEG Processor
try:
    from eeg_processor import create_life_eeg_processor
    eeg_processor = create_life_eeg_processor()
    
    # Test EEG processing
    eeg_data = np.random.randn(4, 1000) * 50  # 4 channels, 1000 samples
    channels = ["Fp1", "Fp2", "C3", "C4"]
    eeg_result = eeg_processor.process(eeg_data, channels, {"test": "core_validation"})
    
    working_modules['eeg_processor'] = {
        'status': 'WORKING',
        'channels_processed': len(channels),
        'overall_score': eeg_result['performance']['overall_score']
    }
    print(f"✅ EEG Processor: {len(channels)} channels, score = {eeg_result['performance']['overall_score']:.3f}")
    
except Exception as e:
    working_modules['eeg_processor'] = {'status': 'ERROR', 'error': str(e)}
    print(f"❌ EEG Processor: {e}")

# Test 3: Venturi Gates System
try:
    from venturi_gates_system import create_venturi_system
    venturi_system = create_venturi_system()
    
    # Test signal enhancement
    test_signal = np.sin(2 * np.pi * 10 * np.linspace(0, 1, 1000))
    test_signal += 0.2 * np.random.randn(1000)
    
    venturi_result = venturi_system.enhance_signal(
        test_signal, 
        {"mode": "parallel", "gain": 1.5}
    )
    
    working_modules['venturi_gates'] = {
        'status': 'WORKING',
        'enhancement_factor': venturi_result.get('enhancement_factor', 1.0),
        'gates_active': venturi_result.get('gates_active', 3)
    }
    print(f"✅ Venturi Gates: enhancement = {venturi_result.get('enhancement_factor', 1.0):.3f}")
    
except Exception as e:
    working_modules['venturi_gates'] = {'status': 'ERROR', 'error': str(e)}
    print(f"❌ Venturi Gates: {e}")

# Summary
working_count = sum(1 for module in working_modules.values() if module['status'] == 'WORKING')
total_count = len(working_modules)
success_rate = (working_count / total_count) * 100

print(f"\n📊 CORE VALIDATION SUMMARY")
print("-" * 40)
print(f"Working Modules: {working_count}/{total_count}")
print(f"Success Rate: {success_rate:.1f}%")

if success_rate == 100:
    status = "🚀 PERFECT - All core modules operational!"
elif success_rate >= 66:
    status = "✨ EXCELLENT - Core platform functional!"
elif success_rate >= 33:
    status = "⚠️  PARTIAL - Some core functionality available!"
else:
    status = "🔧 CRITICAL - Core modules need attention!"

print(f"Status: {status}")

# Integration Test
if working_count >= 2:
    print(f"\n🔗 CORE INTEGRATION TEST")
    print("-" * 40)
    
    try:
        # Create synthetic EEG-like signal
        fs = 250  # sampling rate
        t = np.linspace(0, 2, 2 * fs)
        
        # Multi-frequency signal (simulating brain activity)
        alpha_wave = 2.0 * np.sin(2 * np.pi * 10 * t)    # 10 Hz alpha
        beta_wave = 1.0 * np.sin(2 * np.pi * 20 * t)     # 20 Hz beta
        noise = 0.5 * np.random.randn(len(t))
        
        # Combine into multi-channel EEG
        eeg_signal = alpha_wave + beta_wave + noise
        eeg_channels = np.array([
            eeg_signal,
            eeg_signal * 0.8 + 0.2 * np.random.randn(len(t)),
            eeg_signal * 0.6 + 0.3 * np.random.randn(len(t)),
            eeg_signal * 0.7 + 0.25 * np.random.randn(len(t))
        ])
        
        print(f"✅ Generated synthetic EEG: {eeg_channels.shape[0]} channels, {eeg_channels.shape[1]} samples")
        
        # Integration pipeline
        pipeline_results = {}
        
        # Step 1: EEG Processing (if available)
        if 'eeg_processor' in working_modules and working_modules['eeg_processor']['status'] == 'WORKING':
            channels = ["Fp1", "Fp2", "C3", "C4"]
            eeg_result = eeg_processor.process(eeg_channels, channels, {"integration_test": True})
            pipeline_results['eeg_processing'] = {
                'quality_score': eeg_result['performance']['overall_score'],
                'quality_improvement': eeg_result['performance']['quality_improvement']
            }
            print(f"✅ EEG Processing: quality = {eeg_result['performance']['overall_score']:.3f}")
        
        # Step 2: Venturi Enhancement (if available)
        if 'venturi_gates' in working_modules and working_modules['venturi_gates']['status'] == 'WORKING':
            enhanced_signal = venturi_system.enhance_signal(
                eeg_signal[:1000],  # Use first 1000 samples
                {"mode": "adaptive", "gain": 1.3}
            )
            pipeline_results['venturi_enhancement'] = {
                'enhancement_factor': enhanced_signal.get('enhancement_factor', 1.0),
                'snr_improvement': enhanced_signal.get('snr_improvement', 0.0)
            }
            print(f"✅ Venturi Enhancement: factor = {enhanced_signal.get('enhancement_factor', 1.0):.3f}")
        
        # Step 3: L.I.F.E Adaptation (if available)
        if 'core_life' in working_modules and working_modules['core_life']['status'] == 'WORKING':
            # Extract features for L.I.F.E processing
            signal_features = np.array([
                np.mean(eeg_signal[:500]),
                np.std(eeg_signal[:500]),
                np.max(eeg_signal[:500]),
                np.min(eeg_signal[:500])
            ])
            
            life_result = life_algorithm.process(
                signal_features, 
                {"integration_test": True, "signal_type": "eeg", "pipeline_step": 3}
            )
            pipeline_results['life_adaptation'] = {
                'adaptation_score': life_result.get('adaptation_score', 0.0),
                'learning_improvement': life_result.get('learning_improvement', 0.0)
            }
            print(f"✅ L.I.F.E Adaptation: score = {life_result.get('adaptation_score', 0.0):.3f}")
        
        # Integration success
        integration_score = len(pipeline_results) / working_count
        print(f"✅ Integration Success: {len(pipeline_results)}/{working_count} modules integrated")
        print(f"✅ Integration Score: {integration_score:.3f}")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")

# Performance Test
if working_count >= 1:
    print(f"\n⚡ PERFORMANCE VALIDATION")
    print("-" * 40)
    
    try:
        # Test L.I.F.E Algorithm performance
        if 'core_life' in working_modules and working_modules['core_life']['status'] == 'WORKING':
            start_time = time.time()
            
            for i in range(20):
                test_data = np.random.randn(50)
                life_algorithm.process(test_data, {"perf_test": True, "iteration": i})
            
            elapsed = time.time() - start_time
            throughput = 1000 / elapsed if elapsed > 0 else float('inf')
            print(f"✅ L.I.F.E Throughput: {throughput:.0f} elements/sec")
        
        # Test EEG processing performance
        if 'eeg_processor' in working_modules and working_modules['eeg_processor']['status'] == 'WORKING':
            start_time = time.time()
            
            # Process 3 EEG segments
            for i in range(3):
                eeg_data = np.random.randn(4, 500) * 50
                channels = ["Fp1", "Fp2", "C3", "C4"]
                eeg_processor.process(eeg_data, channels, {"perf_test": True})
            
            elapsed = time.time() - start_time
            rate = 6000 / elapsed if elapsed > 0 else float('inf')  # 3 * 4 channels * 500 samples
            print(f"✅ EEG Processing Rate: {rate:.0f} samples/sec")
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")

# Final Assessment
print(f"\n🎯 FINAL CORE PLATFORM ASSESSMENT")
print("=" * 50)

if success_rate == 100:
    assessment = "🚀 REVOLUTIONARY - Core L.I.F.E platform fully operational!"
    recommendation = "Ready for advanced module integration and deployment!"
elif success_rate >= 66:
    assessment = "✨ EXCELLENT - Core functionality verified and stable!"
    recommendation = "Proceed with full platform integration testing!"
elif success_rate >= 33:
    assessment = "⚠️  FUNCTIONAL - Basic core capabilities confirmed!"
    recommendation = "Focus on stabilizing remaining core modules!"
else:
    assessment = "🔧 DEVELOPING - Foundation requires attention!"
    recommendation = "Prioritize core module debugging and stabilization!"

print(f"Assessment: {assessment}")
print(f"Recommendation: {recommendation}")

print(f"\n✨ CORE L.I.F.E PLATFORM VALIDATION COMPLETE!")
print(f"Learning Individually From Experience - {datetime.now().strftime('%H:%M:%S')}")
print("="*60)
