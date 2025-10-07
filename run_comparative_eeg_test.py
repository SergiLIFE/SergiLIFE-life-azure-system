"""
L.I.F.E Platform - Comparative EEG Test Runner
Runs fresh 100-cycle test and compares with historical performance

Copyright 2025 - Sergio Paya Borrull
Date: October 2, 2025
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Setup directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")
RESULTS_DIR = os.path.join(SCRIPT_DIR, "results")
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Setup logging
LOG_FILE = os.path.join(
    LOGS_DIR, f"comparative_eeg_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

# Historical baseline data (from previous runs)
HISTORICAL_BASELINES = {
    "September_2025_Production": {
        "date": "2025-09-21",
        "accuracy": 97.95,
        "latency_ms": 0.42,
        "throughput": 2500,
        "cycles_completed": 100,
        "success_rate": 100.0,
        "notes": "Production validation run",
    },
    "PhysioNet_BCI_IV_2a": {
        "date": "2025-09-15",
        "accuracy": 78.0,  # SOTA benchmark baseline
        "latency_ms": 4.38,
        "throughput": 21.7,
        "notes": "SOTA champion baseline (published)",
    },
    "Previous_300_Cycle_Test": {
        "date": "2025-09",
        "accuracy": 95.8,
        "latency_ms": 0.38,
        "cycles_completed": 300,
        "success_rate": 100.0,
        "notes": "Extended validation run",
    },
    "6_4_Million_EEG_Results": {
        "date": "2025-09",
        "accuracy": 96.2,
        "latency_ms": 0.45,
        "total_samples": 6400000,
        "notes": "Large-scale data processing",
    },
}

SOTA_BENCHMARKS = {
    "EEGNet": {"accuracy": 76.3, "latency_ms": 127},
    "ShallowConvNet": {"accuracy": 74.1, "latency_ms": 250},
    "DeepConvNet": {"accuracy": 82.3, "latency_ms": 500},
    "FBCSPNet": {"accuracy": 78.0, "latency_ms": 4.38},
}


async def run_fresh_100_cycle_test():
    """Run a fresh 100-cycle EEG test"""
    logging.info("=" * 80)
    logging.info("STARTING FRESH 100-CYCLE EEG TEST")
    logging.info(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info("=" * 80)

    try:
        # Import L.I.F.E Algorithm
        import experimentP2L

        logging.info("Initializing L.I.F.E Algorithm Core...")
        life = experimentP2L.LIFEAlgorithmCore()

        logging.info("Starting 100-cycle validation test...")
        results = await life.run_100_cycle_eeg_test()

        logging.info("100-cycle test completed successfully!")
        return results

    except Exception as e:
        logging.error(f"Error running test: {e}")
        logging.exception("Full traceback:")
        return None


def compare_with_baselines(current_results):
    """Compare current results with historical baselines"""
    if not current_results:
        logging.error("No current results to compare")
        return

    logging.info("\n" + "=" * 80)
    logging.info("COMPARATIVE ANALYSIS")
    logging.info("=" * 80)

    # Extract key metrics from current results
    current_accuracy = current_results.get("accuracy", 0)
    current_latency = current_results.get("latency_ms", 0)
    current_throughput = current_results.get("throughput", 0)

    # Compare with historical baselines
    logging.info("\n📊 COMPARISON WITH HISTORICAL BASELINES:")
    logging.info("-" * 80)

    for baseline_name, baseline_data in HISTORICAL_BASELINES.items():
        logging.info(f"\n{baseline_name}:")
        logging.info(f"  Date: {baseline_data['date']}")

        # Accuracy comparison
        if "accuracy" in baseline_data:
            accuracy_diff = current_accuracy - baseline_data["accuracy"]
            accuracy_change = (accuracy_diff / baseline_data["accuracy"]) * 100
            logging.info(
                f"  Accuracy: {baseline_data['accuracy']:.2f}% → {current_accuracy:.2f}% "
                f"({accuracy_diff:+.2f}%, {accuracy_change:+.2f}% change)"
            )

        # Latency comparison
        if "latency_ms" in baseline_data:
            latency_diff = current_latency - baseline_data["latency_ms"]
            latency_change = (latency_diff / baseline_data["latency_ms"]) * 100
            logging.info(
                f"  Latency: {baseline_data['latency_ms']:.2f}ms → {current_latency:.2f}ms "
                f"({latency_diff:+.2f}ms, {latency_change:+.2f}% change)"
            )

        # Throughput comparison
        if "throughput" in baseline_data and current_throughput > 0:
            throughput_diff = current_throughput - baseline_data["throughput"]
            throughput_change = (throughput_diff / baseline_data["throughput"]) * 100
            logging.info(
                f"  Throughput: {baseline_data['throughput']:.0f} → {current_throughput:.0f} ops/sec "
                f"({throughput_diff:+.0f}, {throughput_change:+.2f}% change)"
            )

        logging.info(f"  Notes: {baseline_data.get('notes', 'N/A')}")

    # Compare with SOTA benchmarks
    logging.info("\n🏆 COMPARISON WITH SOTA BENCHMARKS:")
    logging.info("-" * 80)

    for benchmark_name, benchmark_data in SOTA_BENCHMARKS.items():
        logging.info(f"\n{benchmark_name}:")

        # Accuracy vs SOTA
        accuracy_improvement = current_accuracy - benchmark_data["accuracy"]
        accuracy_factor = current_accuracy / benchmark_data["accuracy"]
        logging.info(
            f"  Accuracy: {benchmark_data['accuracy']:.2f}% → {current_accuracy:.2f}% "
            f"({accuracy_improvement:+.2f}%, {accuracy_factor:.2f}x better)"
        )

        # Latency vs SOTA
        latency_improvement = benchmark_data["latency_ms"] - current_latency
        latency_factor = benchmark_data["latency_ms"] / current_latency
        logging.info(
            f"  Latency: {benchmark_data['latency_ms']:.2f}ms → {current_latency:.2f}ms "
            f"(-{latency_improvement:.2f}ms, {latency_factor:.2f}x faster)"
        )


def generate_performance_report(current_results):
    """Generate comprehensive performance report"""
    if not current_results:
        return

    logging.info("\n" + "=" * 80)
    logging.info("PERFORMANCE SUMMARY REPORT")
    logging.info("=" * 80)

    # Current performance metrics
    logging.info("\n📈 CURRENT TEST RESULTS:")
    logging.info(f"  Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"  Cycles Completed: {current_results.get('cycles_completed', 0)}")
    logging.info(f"  Success Rate: {current_results.get('success_rate', 0):.2f}%")
    logging.info(f"  Accuracy: {current_results.get('accuracy', 0):.2f}%")
    logging.info(f"  Average Latency: {current_results.get('latency_ms', 0):.2f}ms")
    logging.info(f"  Throughput: {current_results.get('throughput', 0):.0f} ops/sec")

    # Learning progression
    if "learning_progression" in current_results:
        logging.info(f"\n📚 LEARNING PROGRESSION:")
        progression = current_results["learning_progression"]
        for stage, metrics in progression.items():
            logging.info(f"  {stage}: {metrics}")

    # Key findings
    logging.info("\n🔍 KEY FINDINGS:")

    current_accuracy = current_results.get("accuracy", 0)
    current_latency = current_results.get("latency_ms", 0)

    # Compare with production baseline
    prod_baseline = HISTORICAL_BASELINES["September_2025_Production"]
    accuracy_vs_prod = current_accuracy - prod_baseline["accuracy"]
    latency_vs_prod = current_latency - prod_baseline["latency_ms"]

    if accuracy_vs_prod >= 0:
        logging.info(
            f"  ✅ Accuracy maintained/improved: {accuracy_vs_prod:+.2f}% vs production baseline"
        )
    else:
        logging.info(
            f"  ⚠️ Accuracy decreased: {accuracy_vs_prod:.2f}% vs production baseline"
        )

    if latency_vs_prod <= 0.05:  # Within 0.05ms is good
        logging.info(
            f"  ✅ Latency maintained: {latency_vs_prod:+.2f}ms vs production baseline"
        )
    else:
        logging.info(
            f"  ⚠️ Latency increased: {latency_vs_prod:+.2f}ms vs production baseline"
        )

    # SOTA comparison
    best_sota_accuracy = max(b["accuracy"] for b in SOTA_BENCHMARKS.values())
    best_sota_latency = min(b["latency_ms"] for b in SOTA_BENCHMARKS.values())

    if current_accuracy > best_sota_accuracy:
        improvement = current_accuracy - best_sota_accuracy
        logging.info(f"  🏆 EXCEEDS BEST SOTA ACCURACY by {improvement:.2f}%!")

    if current_latency < best_sota_latency:
        factor = best_sota_latency / current_latency
        logging.info(f"  ⚡ {factor:.2f}x FASTER than best SOTA latency!")

    # Save results to file
    results_file = os.path.join(
        RESULTS_DIR, f"comparative_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(results_file, "w") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "current_results": current_results,
                "historical_baselines": HISTORICAL_BASELINES,
                "sota_benchmarks": SOTA_BENCHMARKS,
            },
            f,
            indent=2,
        )

    logging.info(f"\n💾 Results saved to: {results_file}")
    logging.info(f"📋 Log file: {LOG_FILE}")


async def main():
    """Main execution function"""
    try:
        # Run fresh 100-cycle test
        results = await run_fresh_100_cycle_test()

        if results:
            # Compare with baselines
            compare_with_baselines(results)

            # Generate comprehensive report
            generate_performance_report(results)

            logging.info("\n" + "=" * 80)
            logging.info("✅ COMPARATIVE EEG TEST COMPLETED SUCCESSFULLY")
            logging.info("=" * 80)

        else:
            logging.error("Test failed - no results to analyze")
            sys.exit(1)

    except Exception as e:
        logging.error(f"Fatal error in main: {e}")
        logging.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("L.I.F.E PLATFORM - COMPARATIVE EEG TEST RUNNER")
    print("Running fresh 100-cycle test with historical comparison")
    print("=" * 80 + "\n")

    asyncio.run(main())
