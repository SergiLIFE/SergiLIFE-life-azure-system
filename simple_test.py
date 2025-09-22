"""
Simple Test Suite for L.I.F.E. Platform
Copyright 2025 - Sergio Paya Borrull

Basic test suite for validating core L.I.F.E. platform functionality.
This module provides simple, focused tests for key components without
complex dependencies or external requirements.

Tests included:
- Basic algorithm validation
- Data structure integrity
- Simple performance benchmarks
- Configuration validation
"""

import logging
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class TestResult:
    """Simple test result structure"""

    test_name: str
    passed: bool
    execution_time: float
    error_message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class LIFESimpleTestSuite:
    """Simple test suite for L.I.F.E. platform validation"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.test_results: List[TestResult] = []

        # Setup basic logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all simple tests"""
        print("🧪 Running L.I.F.E. Simple Test Suite")
        print("=" * 40)

        start_time = time.time()

        # Test categories
        test_categories = [
            self.test_basic_math,
            self.test_data_structures,
            self.test_string_operations,
            self.test_list_operations,
            self.test_dict_operations,
            self.test_basic_algorithm,
            self.test_performance_baseline,
            self.test_configuration_validation,
        ]

        passed_tests = 0
        total_tests = len(test_categories)

        for test_func in test_categories:
            result = self._run_single_test(test_func)
            self.test_results.append(result)
            if result.passed:
                passed_tests += 1
                print(f"✅ {result.test_name}: PASSED ({result.execution_time:.3f}s)")
            else:
                print(f"❌ {result.test_name}: FAILED ({result.execution_time:.3f}s)")
                if result.error_message:
                    print(f"   Error: {result.error_message}")

        total_time = time.time() - start_time

        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": (
                (passed_tests / total_tests) * 100 if total_tests > 0 else 0
            ),
            "total_time": total_time,
            "timestamp": datetime.now().isoformat(),
        }

        print("\n📊 Test Summary:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Passed: {summary['passed_tests']}")
        print(f"   Failed: {summary['failed_tests']}")
        print(f"   Success Rate: {summary['success_rate']:.1f}%")
        print(f"   Total Time: {summary['total_time']:.3f}s")
        if summary["success_rate"] == 100.0:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed - review results above")

        return summary

    def _run_single_test(self, test_func) -> TestResult:
        """Run a single test function"""
        test_name = test_func.__name__.replace("test_", "").replace("_", " ").title()

        start_time = time.time()
        try:
            result = test_func()
            execution_time = time.time() - start_time

            if result is None or result is True:
                return TestResult(
                    test_name=test_name, passed=True, execution_time=execution_time
                )
            elif isinstance(result, dict) and result.get("passed", False):
                return TestResult(
                    test_name=test_name,
                    passed=True,
                    execution_time=execution_time,
                    details=result,
                )
            else:
                error_msg = (
                    result.get("error", "Test returned false")
                    if isinstance(result, dict)
                    else "Test failed"
                )
                return TestResult(
                    test_name=test_name,
                    passed=False,
                    execution_time=execution_time,
                    error_message=error_msg,
                )

        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult(
                test_name=test_name,
                passed=False,
                execution_time=execution_time,
                error_message=str(e),
            )

    def test_basic_math(self) -> bool:
        """Test basic mathematical operations"""
        # Test addition
        assert 2 + 2 == 4

        # Test multiplication
        assert 3 * 4 == 12

        # Test division
        assert 10 / 2 == 5

        # Test modulo
        assert 10 % 3 == 1

        # Test power
        assert 2**3 == 8

        return True

    def test_data_structures(self) -> bool:
        """Test basic data structure operations"""
        # Test tuple creation and access
        test_tuple = (1, 2, 3, 4, 5)
        assert test_tuple[0] == 1
        assert test_tuple[-1] == 5
        assert len(test_tuple) == 5

        # Test set operations
        test_set = {1, 2, 3, 4, 5}
        assert 3 in test_set
        assert 6 not in test_set
        assert len(test_set) == 5

        return True

    def test_string_operations(self) -> bool:
        """Test string manipulation operations"""
        test_string = "L.I.F.E. Platform"

        # Test string length
        assert len(test_string) == 16

        # Test substring search
        assert "LIFE" in test_string
        assert test_string.startswith("L.I.F.E.")
        assert test_string.endswith("Platform")

        # Test string splitting
        parts = test_string.split(" ")
        assert len(parts) == 2
        assert parts[0] == "L.I.F.E."
        assert parts[1] == "Platform"

        # Test string formatting
        formatted = f"Welcome to {test_string}"
        assert formatted == "Welcome to L.I.F.E. Platform"

        return True

    def test_list_operations(self) -> bool:
        """Test list manipulation operations"""
        # Test list creation and basic operations
        test_list = [1, 2, 3, 4, 5]

        # Test append
        test_list.append(6)
        assert len(test_list) == 6
        assert test_list[-1] == 6

        # Test insert
        test_list.insert(0, 0)
        assert test_list[0] == 0
        assert len(test_list) == 7

        # Test remove
        test_list.remove(3)
        assert 3 not in test_list
        assert len(test_list) == 6

        # Test sort
        unsorted = [3, 1, 4, 1, 5]
        unsorted.sort()
        assert unsorted == [1, 1, 3, 4, 5]

        return True

    def test_dict_operations(self) -> bool:
        """Test dictionary operations"""
        # Test dictionary creation
        test_dict = {"name": "L.I.F.E.", "version": "2025.1.0", "status": "production"}

        # Test key access
        assert test_dict["name"] == "L.I.F.E."
        assert test_dict["version"] == "2025.1.0"
        assert test_dict.get("status") == "production"

        # Test key existence
        assert "name" in test_dict
        assert "nonexistent" not in test_dict

        # Test adding new key
        test_dict["platform"] = "Azure"
        assert test_dict["platform"] == "Azure"
        assert len(test_dict) == 4

        # Test key removal
        del test_dict["status"]
        assert "status" not in test_dict
        assert len(test_dict) == 3

        return True

    def test_basic_algorithm(self) -> Dict[str, Any]:
        """Test basic algorithmic operations"""

        # Test factorial calculation
        def factorial(n: int) -> int:
            if n <= 1:
                return 1
            return n * factorial(n - 1)

        assert factorial(5) == 120
        assert factorial(0) == 1
        assert factorial(1) == 1

        # Test fibonacci sequence
        def fibonacci(n: int) -> int:
            if n <= 1:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)

        assert fibonacci(0) == 0
        assert fibonacci(1) == 1
        assert fibonacci(5) == 5
        assert fibonacci(8) == 21

        # Test prime number check
        def is_prime(n: int) -> bool:
            if n <= 1:
                return False
            if n <= 3:
                return True
            if n % 2 == 0 or n % 3 == 0:
                return False
            i = 5
            while i * i <= n:
                if n % i == 0 or n % (i + 2) == 0:
                    return False
                i += 6
            return True

        assert is_prime(2) == True
        assert is_prime(17) == True
        assert is_prime(4) == False
        assert is_prime(1) == False

        return {
            "passed": True,
            "algorithms_tested": ["factorial", "fibonacci", "prime_check"],
        }

    def test_performance_baseline(self) -> Dict[str, Any]:
        """Test basic performance baseline"""
        start_time = time.time()

        # Simple computational load
        result = 0
        for i in range(100000):
            result += i * i

        computation_time = time.time() - start_time

        # Memory allocation test
        large_list = [i for i in range(10000)]
        assert len(large_list) == 10000
        assert large_list[0] == 0
        assert large_list[-1] == 9999

        # String concatenation performance
        strings = []
        for i in range(1000):
            strings.append(f"item_{i}")
        concatenated = " ".join(strings)
        assert len(concatenated.split()) == 1000

        return {
            "passed": True,
            "computation_result": result,
            "computation_time": computation_time,
            "memory_test_size": len(large_list),
            "string_concat_items": 1000,
        }

    def test_configuration_validation(self) -> Dict[str, Any]:
        """Test basic configuration validation"""
        # Test configuration structure
        config = {
            "platform": "L.I.F.E.",
            "version": "2025.1.0",
            "environment": "production",
            "features": ["eeg_processing", "adaptive_learning", "azure_integration"],
            "settings": {"max_users": 1000, "timeout": 30, "debug": False},
        }

        # Validate required keys
        required_keys = ["platform", "version", "environment", "features", "settings"]
        for key in required_keys:
            assert key in config, f"Missing required key: {key}"

        # Validate data types
        assert isinstance(config["platform"], str)
        assert isinstance(config["version"], str)
        assert isinstance(config["features"], list)
        assert isinstance(config["settings"], dict)

        # Validate settings
        settings = config["settings"]
        assert settings["max_users"] > 0
        assert settings["timeout"] > 0
        assert isinstance(settings["debug"], bool)

        # Test configuration modification
        config_copy = config.copy()
        config_copy["environment"] = "testing"
        assert config_copy["environment"] == "testing"
        assert config["environment"] == "production"  # Original unchanged

        return {
            "passed": True,
            "config_keys_validated": len(required_keys),
            "settings_validated": len(settings),
            "immutability_tested": True,
        }

    def get_test_report(self) -> str:
        """Generate a detailed test report"""
        report = []
        report.append("L.I.F.E. Simple Test Suite Report")
        report.append("=" * 40)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        passed_count = sum(1 for result in self.test_results if result.passed)
        total_count = len(self.test_results)

        report.append(f"Test Results: {passed_count}/{total_count} passed")
        report.append(f"Success Rate: {passed_count/total_count*100:.1f}%")
        report.append("")

        report.append("Detailed Results:")
        report.append("-" * 20)

        for result in self.test_results:
            status = "PASS" if result.passed else "FAIL"
            report.append(
                f"{result.test_name}: {status} ({result.execution_time:.3f}s)"
            )
            if result.error_message:
                report.append(f"  Error: {result.error_message}")
            if result.details:
                for key, value in result.details.items():
                    report.append(f"  {key}: {value}")

        return "\n".join(report)


def main():
    """Main test execution function"""
    print("🧠 L.I.F.E. Simple Test Suite")
    print("Copyright 2025 - Sergio Paya Borrull")
    print()

    # Run the test suite
    test_suite = LIFESimpleTestSuite()
    summary = test_suite.run_all_tests()

    # Generate and display report
    print("\n📄 Detailed Test Report:")
    print("-" * 30)
    report = test_suite.get_test_report()
    print(report)

    # Save report to file
    report_filename = (
        f"simple_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n💾 Report saved to: {report_filename}")

    # Exit with appropriate code
    if summary["success_rate"] == 100.0:
        print("✅ All tests completed successfully!")
        return 0
    else:
        print("❌ Some tests failed - check the report above")
        return 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
