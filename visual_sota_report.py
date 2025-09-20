import json
import os

import matplotlib.pyplot as plt

# Load optimizer summary
results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
summary_path = os.path.join(results_dir, "optimizer_summary.json")
if not os.path.exists(summary_path):
    raise FileNotFoundError(f"Summary file not found: {summary_path}")

with open(summary_path, "r", encoding="utf-8") as f:
    summary = json.load(f)

# Extract metrics
perf = summary["performance_metrics"]
labels = ["Average Score", "Best Score", "Average Latency (ms)", "Best Latency (ms)"]
values = [
    perf["average_score"],
    perf["best_score"],
    perf["average_latency"],
    perf["best_latency"],
]

# SOTA comparison (if available)
sota = summary.get("sota_comparison", None)
if isinstance(sota, dict):
    sota_value = sota.get("latency_vs_target", None)
else:
    sota_value = sota

# Plot
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(labels, values, color=["#4CAF50", "#2196F3", "#FFC107", "#FF5722"])
ax.set_title("L.I.F.E. Optimizer SOTA Champion Status")
ax.set_ylabel("Score / Latency (ms)")

# Annotate bars
for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        yval + 0.01,
        f"{yval:.3f}",
        ha="center",
        va="bottom",
    )

# Add SOTA line if available
if sota_value:
    ax.axhline(sota_value, color="red", linestyle="--", label="SOTA Champion")
    ax.legend()

plt.tight_layout()
plt.savefig(os.path.join(results_dir, "sota_champion_status.png"))
plt.show()
plt.show()
