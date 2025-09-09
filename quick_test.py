#!/usr/bin/env python3
"""
Quick Test Runner for L.I.F.E. Autonomous Optimizer
Run tests and validate autonomous optimization functionality
"""

import subprocess
import sys
import time
from pathlib import Path


def run_tests():
    """Run all available tests for L.I.F.E. platform"""
    print("🧪 L.I.F.E. Quick Test Runner")
    print("=" * 40)

    test_files = [
        "test_autonomous_optimizer.py",
        "test_model_optimizer.py",
        "test_sota_integration.py",
    ]

    results = {}
    total_start = time.time()

    print("🔍 Scanning for test files...")
    available_tests = []
    for test_file in test_files:
        if Path(test_file).exists():
            available_tests.append(test_file)
            print(f"   ✅ Found: {test_file}")
        else:
            print(f"   ⚠️ Missing: {test_file}")

    if not available_tests:
        print("❌ No test files found!")
        return

    print(f"\n🚀 Running {len(available_tests)} test files...")
    print("-" * 40)

    for test_file in available_tests:
        print(f"\n🔬 Testing: {test_file}")
        start_time = time.time()

        try:
            # Run test with timeout
            result = subprocess.run(
                [sys.executable, test_file],
                capture_output=True,
                text=True,
                timeout=120,  # 2 minute timeout
            )

            duration = time.time() - start_time

            if result.returncode == 0:
                print(f"   ✅ PASSED ({duration:.1f}s)")
                results[test_file] = "PASSED"
            else:
                print(f"   ❌ FAILED ({duration:.1f}s)")
                results[test_file] = "FAILED"
                if result.stderr:
                    error_lines = result.stderr.split("\n")[:3]  # First 3 lines
                    for line in error_lines:
                        if line.strip():
                            print(f"      {line[:60]}...")

        except subprocess.TimeoutExpired:
            print(f"   ⏰ TIMEOUT (>120s)")
            results[test_file] = "TIMEOUT"
        except Exception as e:
            print(f"   💥 ERROR: {str(e)[:50]}...")
            results[test_file] = "ERROR"

    # Summary
    total_duration = time.time() - total_start
    print("\n" + "=" * 40)
    print("📊 TEST SUMMARY")
    print("=" * 40)

    passed = sum(1 for r in results.values() if r == "PASSED")
    failed = len(results) - passed

    print(f"✅ Tests Passed: {passed}")
    print(f"❌ Tests Failed: {failed}")
    print(f"⏱️ Total Time: {total_duration:.1f}s")

    if failed == 0:
        print("🏆 ALL TESTS PASSED!")
        print("🚀 L.I.F.E. Autonomous Optimizer is ready!")
    else:
        print("🔧 Some tests failed - review required")

    return results


def quick_syntax_check():
    """Quick syntax check for Python files"""
    print("🔍 Quick Syntax Check")
    print("-" * 30)

    python_files = [
        "autonomous_optimizer.py",
        "model_optimizer.py",
        "sota_benchmark.py",
    ]

    syntax_ok = True

    for py_file in python_files:
        if Path(py_file).exists():
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "py_compile", py_file],
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    print(f"   ✅ {py_file}")
                else:
                    print(f"   ❌ {py_file}")
                    syntax_ok = False
                    if result.stderr:
                        print(f"      {result.stderr.split('File')[0].strip()}")

            except Exception as e:
                print(f"   💥 {py_file}: {e}")
                syntax_ok = False
        else:
            print(f"   ⚠️ {py_file} (not found)")

    if syntax_ok:
        print("🎉 All syntax checks passed!")
    else:
        print("🔧 Some syntax errors found")

    return syntax_ok


def run_specific_test(test_name):
    """Run a specific test file"""
    if not Path(test_name).exists():
        print(f"❌ Test file '{test_name}' not found")
        return False

    print(f"🔬 Running specific test: {test_name}")
    print("-" * 40)

    try:
        result = subprocess.run(
            [sys.executable, test_name], capture_output=True, text=True, timeout=120
        )

        if result.returncode == 0:
            print("✅ TEST PASSED")
            if result.stdout:
                print(result.stdout[-500:])  # Last 500 chars
            return True
        else:
            print("❌ TEST FAILED")
            if result.stderr:
                print(result.stderr[-500:])  # Last 500 chars
            return False

    except subprocess.TimeoutExpired:
        print("⏰ TEST TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 TEST ERROR: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--syntax":
            quick_syntax_check()
        elif sys.argv[1].startswith("test_"):
            run_specific_test(sys.argv[1])
        else:
            print("Usage: python quick_test.py [--syntax | test_filename.py]")
    else:
        run_tests()
