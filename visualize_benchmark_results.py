import json
import matplotlib.pyplot as plt
import numpy as np

AGGREGATE_FILE = 'benchmark_aggregate.json'


def plot_benchmark_results(aggregate_file=AGGREGATE_FILE):
    with open(aggregate_file, 'r') as f:
        data = json.load(f)
    accuracies = [r['accuracy'] for r in data['all_results']]
    latencies = [r['latency_ms'] for r in data['all_results']]
    runs = np.arange(1, len(accuracies) + 1)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(runs, np.array(accuracies) * 100, marker='o', label='Accuracy (%)')
    plt.axhline(data['mean_accuracy'] * 100, color='g', linestyle='--', label='Mean Accuracy')
    plt.xlabel('Run')
    plt.ylabel('Accuracy (%)')
    plt.title('Benchmark Accuracy per Run')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(runs, latencies, marker='o', color='orange', label='Latency (ms)')
    plt.axhline(data['mean_latency_ms'], color='r', linestyle='--', label='Mean Latency')
    plt.xlabel('Run')
    plt.ylabel('Latency (ms)')
    plt.title('Benchmark Latency per Run')
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_benchmark_results()
