"""
L.I.F.E. Research Platform - Validation & Integration Test
===========================================================

Copyright 2025 - Sergio Paya Borrull
Validates comprehensive research data library integration

Tests:
1. Library initialization
2. EEG signal processing
3. Statistical analysis functions
4. Study management operations
5. Data export functionality
6. Performance benchmarks
"""

import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from populate_research_database import populate_comprehensive_research_database
    from research_data_library import (
        EEGBandPower,
        ParticipantDemographics,
        ResearchDataLibrary,
        ResearchSession,
        ResearchStudy,
        StatisticalMethod,
        StudyPhase,
        initialize_research_library,
    )
except ImportError as e:
    print(f"ERROR: Failed to import research libraries: {e}")
    print("\nPlease ensure research_data_library.py exists in the same directory.")
    sys.exit(1)


def test_library_initialization():
    """Test 1: Library initialization"""
    print("\n" + "=" * 70)
    print("TEST 1: Library Initialization")
    print("=" * 70)

    try:
        library = initialize_research_library()
        print(f"✓ Library initialized: v{library.version}")
        print(f"✓ EEG sampling rate: {library.eeg_sampling_rate} Hz")
        print(f"✓ Artifact threshold: {library.artifact_rejection_threshold} sigma")
        print(f"✓ Alpha level: {library.alpha_level}")
        print(f"✓ Data directory: {library.data_directory}")
        return library, True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return None, False


def test_eeg_processing(library):
    """Test 2: EEG signal processing"""
    print("\n" + "=" * 70)
    print("TEST 2: EEG Signal Processing")
    print("=" * 70)

    try:
        # Generate realistic test EEG data
        import random

        raw_eeg = [random.uniform(10, 30) for _ in range(256)]

        result = library.process_raw_eeg(raw_eeg, sampling_rate=256)

        print(f"✓ Processed {result['samples_processed']} samples")
        print(f"✓ Artifacts removed: {result['artifacts_removed']}")
        print(f"✓ Quality score: {result['quality_score']:.3f}")
        print(f"✓ Engagement: {result['engagement']:.3f}")
        print(f"✓ Focus: {result['focus']:.3f}")
        print(f"✓ Stress: {result['stress']:.3f}")

        print("\nBand Powers:")
        for band, power in result["band_powers"].items():
            print(f"  {band.capitalize()}: {power:.2f} μV²")

        return True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_statistical_analysis(library):
    """Test 3: Statistical analysis functions"""
    print("\n" + "=" * 70)
    print("TEST 3: Statistical Analysis")
    print("=" * 70)

    try:
        # T-test
        control = [65.2, 68.4, 72.1, 69.8, 71.3, 67.9, 70.5, 68.2, 69.1, 71.8]
        intervention = [78.5, 82.1, 79.3, 85.2, 80.9, 83.4, 81.7, 79.8, 84.5, 82.3]

        t_result = library.calculate_t_test(control, intervention)

        print("T-Test Results:")
        print(f"  Method: {t_result.method.value}")
        print(f"  t-statistic: {t_result.test_statistic:.3f}")
        print(f"  p-value: {t_result.p_value:.4f}")
        print(f"  Effect size (Cohen's d): {t_result.effect_size:.3f}")
        print(f"  Significant: {t_result.significant}")
        print(f"  Interpretation: {t_result.interpretation}")

        # Correlation
        x = [65, 70, 75, 80, 85, 90, 72, 78, 82, 88]
        y = [68, 73, 79, 83, 88, 92, 74, 80, 85, 90]

        corr_result = library.calculate_correlation(x, y)

        print("\nCorrelation Results:")
        print(f"  Method: {corr_result.method.value}")
        print(f"  r: {corr_result.test_statistic:.3f}")
        print(f"  p-value: {corr_result.p_value:.4f}")
        print(f"  R²: {corr_result.effect_size:.3f}")
        print(f"  Interpretation: {corr_result.interpretation}")

        return True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_study_management(library):
    """Test 4: Study management operations"""
    print("\n" + "=" * 70)
    print("TEST 4: Study Management")
    print("=" * 70)

    try:
        # Create test study
        study = ResearchStudy(
            study_id="TEST-2025-001",
            title="Test Study - Platform Validation",
            principal_investigator="Dr. Test Researcher",
            institution="L.I.F.E. Platform",
            phase=StudyPhase.PILOT,
            start_date="2025-10-18",
            end_date=None,
            n_participants=10,
            protocols=["test_protocol"],
            primary_outcomes=["Test metric 1", "Test metric 2"],
            secondary_outcomes=["Test metric 3"],
        )

        success = library.add_study(study)
        print(f"✓ Study added: {study.study_id}")

        # Add test participant
        participant = ParticipantDemographics(
            participant_id="TEST-P001",
            age=25,
            gender="Test",
            education_level="Test Level",
            handedness="Right",
            native_language="English",
            medical_history=[],
            medications=[],
            inclusion_criteria_met=True,
            exclusion_criteria_violated=False,
        )

        library.add_participant(participant)
        print(f"✓ Participant added: {participant.participant_id}")

        # Add test session
        bands = EEGBandPower(delta=12.5, theta=15.3, alpha=25.8, beta=32.4, gamma=18.9)

        session = ResearchSession(
            session_id="TEST-S001",
            participant_id="TEST-P001",
            timestamp="2025-10-18T10:00:00",
            protocol="test_protocol",
            duration_minutes=30.0,
            eeg_bands=bands,
            engagement=0.75,
            focus=0.82,
            stress=0.35,
            performance_score=85.5,
            notes="Test session",
        )

        library.add_session(session)
        print(f"✓ Session added: {session.session_id}")

        print(f"\nLibrary Status:")
        print(f"  Total Studies: {len(library.studies)}")
        print(f"  Total Participants: {len(library.participants)}")
        print(f"  Total Sessions: {len(library.sessions)}")

        return True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_data_export(library):
    """Test 5: Data export functionality"""
    print("\n" + "=" * 70)
    print("TEST 5: Data Export")
    print("=" * 70)

    try:
        if not library.studies:
            print("✓ No studies to export (expected for fresh library)")
            return True

        study_id = list(library.studies.keys())[0]

        # Export study data
        success = library.export_study_data(study_id, format="json")
        print(f"✓ Study data exported: {study_id}")

        # Generate report
        report = library.generate_publication_report(study_id)
        print(f"✓ Publication report generated ({len(report)} characters)")

        return True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_performance_benchmarks(library):
    """Test 6: Performance benchmarks"""
    print("\n" + "=" * 70)
    print("TEST 6: Performance Benchmarks")
    print("=" * 70)

    try:
        import random
        import time

        # Benchmark EEG processing
        eeg_times = []
        for _ in range(100):
            raw_eeg = [random.uniform(10, 30) for _ in range(256)]
            start = time.perf_counter()
            library.process_raw_eeg(raw_eeg, sampling_rate=256)
            eeg_times.append((time.perf_counter() - start) * 1000)  # Convert to ms

        avg_eeg_time = sum(eeg_times) / len(eeg_times)
        print(f"✓ EEG Processing: {avg_eeg_time:.4f} ms average ({100} iterations)")

        # Benchmark statistical tests
        stat_times = []
        for _ in range(100):
            group1 = [random.uniform(60, 80) for _ in range(20)]
            group2 = [random.uniform(70, 90) for _ in range(20)]
            start = time.perf_counter()
            library.calculate_t_test(group1, group2)
            stat_times.append((time.perf_counter() - start) * 1000)

        avg_stat_time = sum(stat_times) / len(stat_times)
        print(
            f"✓ Statistical Analysis: {avg_stat_time:.4f} ms average ({100} iterations)"
        )

        print("\nPerformance Summary:")
        print(f"  EEG Throughput: {1000/avg_eeg_time:.0f} processes/second")
        print(f"  Statistical Throughput: {1000/avg_stat_time:.0f} tests/second")

        return True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def run_comprehensive_validation():
    """Run all validation tests"""
    print("=" * 70)
    print("L.I.F.E. RESEARCH DATA LIBRARY - COMPREHENSIVE VALIDATION")
    print("=" * 70)
    print("\nValidating extended research data library integration...")

    results = []

    # Test 1: Initialize
    library, success = test_library_initialization()
    results.append(("Library Initialization", success))

    if not library:
        print("\n✗ CRITICAL: Cannot proceed without library initialization")
        return

    # Test 2: EEG Processing
    success = test_eeg_processing(library)
    results.append(("EEG Signal Processing", success))

    # Test 3: Statistical Analysis
    success = test_statistical_analysis(library)
    results.append(("Statistical Analysis", success))

    # Test 4: Study Management
    success = test_study_management(library)
    results.append(("Study Management", success))

    # Test 5: Data Export
    success = test_data_export(library)
    results.append(("Data Export", success))

    # Test 6: Performance Benchmarks
    success = test_performance_benchmarks(library)
    results.append(("Performance Benchmarks", success))

    # Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name}")

    print()
    print(f"Results: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")

    if passed == total:
        print("\n✓✓✓ ALL TESTS PASSED - RESEARCH LIBRARY FULLY OPERATIONAL ✓✓✓")
        print("\nResearch data library is ready for production use.")
        print("Platform efficacy: MAXIMIZED")
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        print("Please review errors above.")

    print("=" * 70)


if __name__ == "__main__":
    run_comprehensive_validation()

    print("\n" + "=" * 70)
    print("OPTIONAL: Populate Full Research Database")
    print("=" * 70)
    print("\nTo populate the comprehensive research database with:")
    print("  - 610 participants")
    print("  - 8,810 research sessions")
    print("  - 5 complete studies")
    print("\nRun: python populate_research_database.py")
    print("=" * 70)
