# SOTA Benchmarks and Analysis

This folder consolidates State-of-the-Art (SOTA) benchmark reports and analysis for the L.I.F.E. Platform.

Included:
- SOTA_BENCHMARK_RESULTS_ANALYSIS.md — Detailed performance analysis and methodology
- SOTA_BENCHMARK_RESULTS_ANALYSIS.html — Rendered HTML version
- SOTA_BENCHMARKS.md — Quick reference performance tiers and usage

How to update:
- Keep the Markdown as the single source of truth and regenerate HTML when needed.
- Place new benchmark outputs (CSV/JSON) from automation under `results/benchmarks/`.

Related automation:
- scripts/eeg_100_cycle_benchmark.py — 100-cycle ingestion and optimizer benchmark
- VS Code tasks: "📦 Install EEG Benchmark Deps" and "🏁 100-cycle EEG Benchmark"
