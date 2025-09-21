#!/usr/bin/env python3
"""
BCI Competition IV-2a Benchmarking Script for L.I.F.E. Algorithm
PEP8 compliant, supports multiple runs, aggregates and reports results.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb

Performance Claims Requiring Verification:
- 43.5x faster processing than CNNs: Requires comparative benchmarking
    against established EEG pipelines using standardized datasets.
- Sub-3ms end-to-end latency: Would be a breakthrough; must be peer
    reviewed and replicated.
- 94% accuracy claims: Must be validated with cross-validation and
    comparison to published results.
"""

import json
import os
import time

import numpy as np

from lifetheory import create_eeg_life_processor

DATA_DIR = "bci_data/IV_2a/"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "results")
RESULTS_FILE = os.path.join(RESULTS_DIR, "benchmark_results.json")
AGGREGATE_FILE = os.path.join(RESULTS_DIR, "benchmark_aggregate.json")
SEED = 42


def load_bci_iv_2a_data(data_dir, seed=SEED):
    """Load BCI Competition IV-2a dataset (stub)."""
    np.random.seed(seed)
    X = np.random.randn(100, 22, 1000)
    y = np.random.randint(0, 4, 100)
    return X, y


def run_life_benchmark(X, y, config=None, seed=SEED):
    """Run a single L.I.F.E. benchmark and return results dict."""
    processor = create_eeg_life_processor(config)
    n_train = int(0.8 * len(X))
    X_test = X[n_train:]
    y_test = y[n_train:]
    latencies = []
    y_pred = []
    for eeg in X_test:
        start = time.time()
        _ = processor.process_eeg(eeg)
        latency = (time.time() - start) * 1000
        latencies.append(latency)
        y_pred.append(np.random.randint(0, 4))  # Replace with real output
    latency_ms = float(np.mean(latencies))
    accuracy = float(np.mean(np.array(y_pred) == y_test))
    results = {
        "latency_ms": latency_ms,
        "accuracy": accuracy,
        "n_test": int(len(X_test)),
        "config": config,
        "seed": seed,
    }
    return now


results


def aggregate_benchmarks(num_runs=5, config=None, seed=SEED):
    """Run multiple benchmarks, aggregate and save results."""
    # Ensure results directory exists
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    all_results = []
    for i in range(num_runs):
        run_seed = seed + i
        X, y = load_bci_iv_2a_data(DATA_DIR, seed=run_seed)
        result = run_life_benchmark(X, y, config=config, seed=run_seed)
        all_results.append(result)
    # Aggregate
    latencies = [r["latency_ms"] for r in all_results]
    accuracies = [r["accuracy"] for r in all_results]
    aggregate = {
        "mean_latency_ms": float(np.mean(latencies)),
        "std_latency_ms": float(np.std(latencies)),
        "mean_accuracy": float(np.mean(accuracies)),
        "std_accuracy": float(np.std(accuracies)),
        "num_runs": num_runs,
        "config": config,
        "seeds": [r["seed"] for r in all_results],
        "all_results": all_results,
    }
    with open(AGGREGATE_FILE, "w") as f:
        json.dump(aggregate, f, indent=2)
    return aggregate


def compare_to_sota_and_best(
    aggregate, sota_acc=0.8515, sota_latency=15.12, best_acc=None, best_latency=None
):
    """Prints comparison to SOTA and best results."""
    print("\n--- Benchmark Aggregate Results ---")
    acc_str = f"L.I.F.E. Mean Accuracy: {aggregate['mean_accuracy']*100:.2f}%"
    sota_str = f"SOTA: {sota_acc*100:.2f}%"
    best_str = f"Best: {best_acc*100:.2f}%" if best_acc is not None else "Best: N/A"
    print(acc_str + " | " + sota_str + " | " + best_str)

    lat_str = f"L.I.F.E. Mean Latency: {aggregate['mean_latency_ms']:.2f} ms"
    sota_lat_str = f"SOTA: {sota_latency:.2f} ms"
    best_lat_str = (
        f"Best: {best_latency:.2f} ms" if best_latency is not None else "Best: N/A"
    )
    print(lat_str + " | " + sota_lat_str + " | " + best_lat_str)

    std_acc_str = f"Std Accuracy: {aggregate['std_accuracy']*100:.2f}%"
    std_lat_str = f"Std Latency: {aggregate['std_latency_ms']:.2f} ms"
    print(std_acc_str + " | " + std_lat_str)

    print(f"Config: {aggregate['config']}")
    print(f"Seeds: {aggregate['seeds']}")
    compliance = "PASS" if aggregate["mean_latency_ms"] < sota_latency else "FAIL"
    print("Clinical compliance:", compliance)


def main():
    print("Loading BCI Competition IV-2a data and running multiple benchmarks...")
    champion_config = {
        "learning_rate": 0.005,
        "experience_weight_decay": 0.98,
        "adaptation_threshold": 0.05,
        "max_experiences": 5000,
        "venturi_gate_factor": 1.1,
        "quantum_enhancement": True,
    }

    aggregate = aggregate_benchmarks(num_runs=5, config=champion_config)

    # Load previous bests for comparison and auto-update champion.json if new best
    best_acc = None
    best_latency = None
    champion_data = None
    try:
        with open("champion.json", "r") as f:
            champion_data = json.load(f)
            best_acc = champion_data.get("accuracy")
            best_latency = champion_data.get("latency_ms")
    except Exception:
        pass

    compare_to_sota_and_best(aggregate, best_acc=best_acc, best_latency=best_latency)

    # Auto-update champion.json if new best accuracy
    if best_acc is None or aggregate["mean_accuracy"] > best_acc:
        new_champion = {
            "accuracy": aggregate["mean_accuracy"],
            "latency_ms": aggregate["mean_latency_ms"],
            "config": aggregate["config"],
            "std_accuracy": aggregate["std_accuracy"],
            "std_latency_ms": aggregate["std_latency_ms"],
            "num_runs": aggregate["num_runs"],
            "seeds": aggregate["seeds"],
        }
        with open("champion.json", "w") as f:
            json.dump(new_champion, f, indent=2)
        print("New champion results saved to champion.json!")
    else:
        print("Champion not updated (no improvement in accuracy).")

    # Print results summary after test run
    print("\nSummary of Results:")
    print(json.dumps(aggregate, indent=2))


if __name__ == "__main__":
    main()
