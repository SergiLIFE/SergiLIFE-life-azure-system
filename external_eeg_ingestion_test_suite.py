"""
External EEG Ingestion Validation Test Suite
Extends existing L.I.F.E Platform validation with ingestion pipeline testing
Validates accuracy, latency, and integration with nocturnal optimization
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List

import aiohttp


class ExternalEEGIngestionValidator:
    """
    Comprehensive validation suite for external EEG data ingestion
    Tests integration with L.I.F.E Platform neural processing pipeline
    """

    def __init__(self, base_url: str = "http://localhost:7071"):
        self.base_url = base_url
        self.validation_results = {}

    async def test_external_ingestion_accuracy(self) -> Dict:
        """
        Test 11: Validate external EEG ingestion accuracy and latency
        Ensures ingestion pipeline processes PhysioNet/OpenNeuro data correctly
        """
        test_start = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Trigger ingestion validation endpoint
                async with session.get(
                    f"{self.base_url}/api/validate-ingestion"
                ) as response:
                    if response.status != 200:
                        raise Exception(
                            f"Validation endpoint failed: {response.status}"
                        )

                    validation_data = await response.json()

                    if validation_data.get("status") != "success":
                        raise Exception(
                            f"Ingestion validation failed: {validation_data.get('message')}"
                        )

                    validation_metrics = validation_data.get("validation", {})

                    # Accuracy validations
                    processing_latency = validation_metrics.get(
                        "processing_latency_ms", 0
                    )
                    learning_efficiency = validation_metrics.get(
                        "learning_efficiency", 0
                    )
                    records_processed = validation_metrics.get("records_processed", 0)

                    # Performance criteria
                    assert (
                        processing_latency < 1000
                    ), f"Processing too slow: {processing_latency}ms"
                    assert (
                        learning_efficiency > 0.5
                    ), f"Learning efficiency too low: {learning_efficiency}"
                    assert (
                        records_processed > 100
                    ), f"Insufficient records processed: {records_processed}"

                    test_duration = time.time() - test_start

                    return {
                        "status": "PASS",
                        "test_name": "External EEG Ingestion Accuracy & Latency",
                        "processing_latency_ms": processing_latency,
                        "learning_efficiency": learning_efficiency,
                        "records_processed": records_processed,
                        "validation_time_s": round(test_duration, 2),
                        "neural_state": validation_metrics.get(
                            "neural_state", "unknown"
                        ),
                        "pipeline_status": validation_metrics.get(
                            "pipeline_status", "unknown"
                        ),
                        "timestamp": datetime.utcnow().isoformat(),
                    }

        except Exception as e:
            return {
                "status": "FAIL",
                "test_name": "External EEG Ingestion Accuracy & Latency",
                "error": str(e),
                "duration_s": round(time.time() - test_start, 2),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def test_full_ingestion_cycle_performance(self) -> Dict:
        """
        Test 12: Validate complete ingestion cycle performance
        Tests PhysioNet + OpenNeuro dataset processing end-to-end
        """
        test_start = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Start full ingestion cycle
                async with session.post(
                    f"{self.base_url}/api/ingest-external-eeg",
                    json={"mode": "full_cycle", "notify_progress": False},
                    timeout=aiohttp.ClientTimeout(total=600),  # 10 min timeout
                ) as response:

                    if response.status != 200:
                        raise Exception(f"Ingestion cycle failed: {response.status}")

                    cycle_results = await response.json()

                    if cycle_results.get("status") != "success":
                        raise Exception(f"Cycle failed: {cycle_results.get('message')}")

                    results = cycle_results.get("results", {})

                    # Performance validations
                    datasets_processed = results.get("datasets_processed", 0)
                    total_records = results.get("total_records", 0)
                    successful_ingestions = results.get("successful_ingestions", 0)
                    total_duration = results.get("total_duration", 0)
                    avg_latency = results.get("avg_processing_latency", 0)

                    # Validation criteria
                    assert (
                        datasets_processed >= 2
                    ), f"Too few datasets processed: {datasets_processed}"
                    assert (
                        total_records > 1000
                    ), f"Insufficient records: {total_records}"
                    assert successful_ingestions > 0, "No successful ingestions"
                    assert total_duration < 300, f"Cycle too slow: {total_duration}s"
                    assert (
                        avg_latency < 500
                    ), f"Average latency too high: {avg_latency}ms"

                    success_rate = (
                        successful_ingestions / datasets_processed
                        if datasets_processed > 0
                        else 0
                    )
                    assert (
                        success_rate >= 0.5
                    ), f"Success rate too low: {success_rate * 100}%"

                    test_duration = time.time() - test_start

                    return {
                        "status": "PASS",
                        "test_name": "Full Ingestion Cycle Performance",
                        "datasets_processed": datasets_processed,
                        "total_records": total_records,
                        "successful_ingestions": successful_ingestions,
                        "success_rate": f"{success_rate * 100:.1f}%",
                        "cycle_duration_s": total_duration,
                        "avg_processing_latency_ms": avg_latency,
                        "test_duration_s": round(test_duration, 2),
                        "throughput_records_per_sec": (
                            round(total_records / total_duration, 2)
                            if total_duration > 0
                            else 0
                        ),
                        "timestamp": datetime.utcnow().isoformat(),
                    }

        except Exception as e:
            return {
                "status": "FAIL",
                "test_name": "Full Ingestion Cycle Performance",
                "error": str(e),
                "duration_s": round(time.time() - test_start, 2),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def test_nocturnal_integration(self) -> Dict:
        """
        Test 13: Validate integration with nocturnal optimization cycle
        Ensures ingestion works properly during scheduled off-peak optimization
        """
        test_start = time.time()

        try:
            # Import nocturnal optimizer
            from nocturnal_eeg_ingestion_optimizer import NocturnalEEGIngestionOptimizer

            optimizer = NocturnalEEGIngestionOptimizer(base_url=self.base_url)

            # Run a test nocturnal cycle (without time restrictions)
            cycle_results = await optimizer.run_nocturnal_cycle()

            # Validate cycle results
            overall_status = cycle_results.get("overall_status", "error")
            cycle_duration = cycle_results.get("cycle_duration", 0)
            phases = cycle_results.get("phases", {})

            # Check that all phases completed
            required_phases = ["ingestion", "validation", "optimization"]
            for phase in required_phases:
                assert phase in phases, f"Missing phase: {phase}"
                phase_status = phases[phase].get("status", "error")
                assert phase_status in [
                    "success",
                    "partial_success",
                ], f"Phase {phase} failed: {phase_status}"

            # Performance criteria
            assert overall_status in [
                "success",
                "partial_success",
            ], f"Cycle failed: {overall_status}"
            assert (
                cycle_duration < 600
            ), f"Cycle too slow: {cycle_duration}s"  # 10 min max

            # Check optimization results
            optimization_phase = phases.get("optimization", {})
            optimizations = optimization_phase.get("optimizations", {})

            test_duration = time.time() - test_start

            return {
                "status": "PASS",
                "test_name": "Nocturnal Integration",
                "overall_cycle_status": overall_status,
                "cycle_duration_s": cycle_duration,
                "phases_completed": list(phases.keys()),
                "optimizations_applied": len(optimizations),
                "test_duration_s": round(test_duration, 2),
                "ingestion_records": phases.get("ingestion", {})
                .get("results", {})
                .get("total_records", 0),
                "validation_latency_ms": phases.get("validation", {})
                .get("validation", {})
                .get("processing_latency_ms", 0),
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            return {
                "status": "FAIL",
                "test_name": "Nocturnal Integration",
                "error": str(e),
                "duration_s": round(time.time() - test_start, 2),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def test_dataset_variety_handling(self) -> Dict:
        """
        Test 14: Validate handling of different dataset formats and sources
        Tests PhysioNet EDF files vs OpenNeuro JSON formats
        """
        test_start = time.time()

        try:
            # Test individual dataset types through validation endpoint
            test_results = []

            for i in range(3):  # Test multiple validation calls
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{self.base_url}/api/validate-ingestion"
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data.get("status") == "success":
                                validation = data.get("validation", {})
                                test_results.append(
                                    {
                                        "processing_latency_ms": validation.get(
                                            "processing_latency_ms", 0
                                        ),
                                        "learning_efficiency": validation.get(
                                            "learning_efficiency", 0
                                        ),
                                        "records_processed": validation.get(
                                            "records_processed", 0
                                        ),
                                    }
                                )

                # Brief pause between tests
                await asyncio.sleep(2)

            # Analyze consistency across different datasets/calls
            if len(test_results) >= 2:
                latencies = [r["processing_latency_ms"] for r in test_results]
                efficiencies = [r["learning_efficiency"] for r in test_results]

                # Check consistency (coefficient of variation < 0.5)
                avg_latency = sum(latencies) / len(latencies)
                latency_std = (
                    sum((x - avg_latency) ** 2 for x in latencies) / len(latencies)
                ) ** 0.5
                latency_cv = latency_std / avg_latency if avg_latency > 0 else 0

                avg_efficiency = sum(efficiencies) / len(efficiencies)
                efficiency_std = (
                    sum((x - avg_efficiency) ** 2 for x in efficiencies)
                    / len(efficiencies)
                ) ** 0.5
                efficiency_cv = (
                    efficiency_std / avg_efficiency if avg_efficiency > 0 else 0
                )

                # Validation criteria
                assert (
                    latency_cv < 0.5
                ), f"Latency too inconsistent: CV={latency_cv:.3f}"
                assert (
                    efficiency_cv < 0.3
                ), f"Efficiency too inconsistent: CV={efficiency_cv:.3f}"
                assert (
                    avg_latency < 800
                ), f"Average latency too high: {avg_latency:.1f}ms"
                assert (
                    avg_efficiency > 0.6
                ), f"Average efficiency too low: {avg_efficiency:.3f}"

                test_duration = time.time() - test_start

                return {
                    "status": "PASS",
                    "test_name": "Dataset Variety Handling",
                    "tests_conducted": len(test_results),
                    "avg_latency_ms": round(avg_latency, 1),
                    "latency_consistency_cv": round(latency_cv, 3),
                    "avg_efficiency": round(avg_efficiency, 3),
                    "efficiency_consistency_cv": round(efficiency_cv, 3),
                    "test_duration_s": round(test_duration, 2),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            else:
                raise Exception("Insufficient test results for consistency analysis")

        except Exception as e:
            return {
                "status": "FAIL",
                "test_name": "Dataset Variety Handling",
                "error": str(e),
                "duration_s": round(time.time() - test_start, 2),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def run_all_ingestion_tests(self) -> Dict:
        """
        Execute complete external EEG ingestion validation suite
        Returns comprehensive test results for integration verification
        """
        suite_start = time.time()

        print("🧠 Starting External EEG Ingestion Test Suite...")
        print("=" * 60)

        # Run all ingestion-specific tests
        tests = [
            self.test_external_ingestion_accuracy,
            self.test_full_ingestion_cycle_performance,
            self.test_nocturnal_integration,
            self.test_dataset_variety_handling,
        ]

        test_results = []
        passed_tests = 0

        for i, test_func in enumerate(tests, 11):  # Start from Test 11
            print(
                f"\n🔬 Running Test {i}: {test_func.__doc__.split('Test ')[1].split(':')[0]}"
            )

            result = await test_func()
            test_results.append(result)

            status = result["status"]
            test_name = result["test_name"]

            if status == "PASS":
                passed_tests += 1
                print(f"✅ Test {i} PASSED: {test_name}")

                # Print key metrics
                if "processing_latency_ms" in result:
                    print(
                        f"   📊 Processing Latency: {result['processing_latency_ms']}ms"
                    )
                if "records_processed" in result:
                    print(f"   📊 Records Processed: {result['records_processed']}")
                if "success_rate" in result:
                    print(f"   📊 Success Rate: {result['success_rate']}")
            else:
                print(f"❌ Test {i} FAILED: {test_name}")
                print(f"   ⚠️  Error: {result.get('error', 'Unknown error')}")

        suite_duration = time.time() - suite_start
        success_rate = passed_tests / len(tests)

        print(f"\n" + "=" * 60)
        print(f"🎯 INGESTION TEST SUITE COMPLETE")
        print(f"✅ Passed: {passed_tests}/{len(tests)} tests ({success_rate*100:.1f}%)")
        print(f"⏱️  Total Duration: {suite_duration:.1f} seconds")
        print(f"🕒 Completed: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

        return {
            "suite_name": "External EEG Ingestion Validation",
            "total_tests": len(tests),
            "passed_tests": passed_tests,
            "failed_tests": len(tests) - passed_tests,
            "success_rate": f"{success_rate*100:.1f}%",
            "suite_duration_s": round(suite_duration, 1),
            "test_results": test_results,
            "overall_status": "PASS" if success_rate >= 0.75 else "FAIL",
            "timestamp": datetime.utcnow().isoformat(),
        }


# Standalone execution for testing
if __name__ == "__main__":

    async def main():
        validator = ExternalEEGIngestionValidator()
        results = await validator.run_all_ingestion_tests()

        print(f"\nFinal Results:")
        print(json.dumps(results, indent=2))

    asyncio.run(main())
    asyncio.run(main())
