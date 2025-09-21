# Copilot Instructions for L.I.F.E Platform (SergiLIFE-life-azure-system)

## Project Overview

- **L.I.F.E.** is a production-ready, Azure-native platform for neuroadaptive learning, leveraging real-time EEG data and adaptive algorithms.
- Major components: EEG processing, adaptive learning engine, Azure integration, enterprise analytics, and compliance modules.
- Key files: `experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py` (core algorithm), `azure_config.py`, `azure_functions_workflow.py`, `autonomous_optimizer.py`, `azure_deployment_manager.py`.
- Core classes: `LIFEAlgorithmCore`, `EEGMetrics`, `LearningOutcome`, `LearningStage`, `NeuralState`.
- Business model: SaaS with pricing tiers ($15 Basic, $30 Professional, $50 Enterprise); revenue targets $345K Q4 2025 → $50.7M by 2029.
- Version: 2025.1.0-PRODUCTION; Azure Marketplace Offer ID: `9a600d96-fe1e-420b-902a-a0c42c561adb`; Launch: September 27, 2025.

## Architecture & Patterns

- **EEG Data Flow:** Real-time EEG data is processed and fed into adaptive learning models. Results are logged and exported for auditability.
- **Core Algorithm Structure:** Uses dataclasses (`EEGMetrics`, `LearningOutcome`) and enums (`LearningStage`, `NeuralState`) for neural processing. Implements asyncio for concurrent operations and pandas/numpy for data handling.
- **Azure EEG Testing Framework:** Validates the platform using real PhysioNet datasets (e.g., BCI Competition IV-2a) across multiple neuroadaptive scenarios. Achieves sub-millisecond (0.38–0.45ms) processing and 78–82% accuracy, with transparent benchmarking and evidence export.
- **Azure Integration:** Production-grade use of Azure Functions (serverless, 10-min timeout), Blob Storage (scalable EEG/result storage), and Azure Monitor (real-time health/performance tracking). OIDC authentication (`setup-azure-oidc.ps1`), Azure CLI (`azure.yaml`), and deployment scripts for cloud operations. Production subscription: `5c88cef6-f243-497d-98af-6c6086d575ca` (East US 2), resources include RG `life-platform-rg`, Storage `stlifeplatformprod`, Key Vault `kv-life-platform-prod`, Service Bus `sb-life-platform-prod`, Marketplace Offer `9a600d96-fe1e-420b-902a-a0c42c561adb`.
- **Validation:** Automated 100-cycle EEG test suite, benchmarking scripts (`autonomous_sota_kpi_monitor.py`, `sota_benchmark.py`), and cross-scenario validation (brain cognition, heart-brain coupling, neuroplasticity).
- **Evidence Export:** All validation and benchmark results are exported in both human- and machine-readable formats for auditability and regulatory review.
- **Compliance:** Encryption, key management, and audit logging are handled via Azure services and `azure_config.py`.
- **Scientific Validation:** Ongoing requirements include standardized cross-validation, statistical significance testing, direct comparison with published research, and independent replication for clinical/academic credibility.
- **Venturi Architecture:** 3 Venturi gates as central orchestrator system; external domain `lifecoach-121.com`.

## Developer Workflows

- **Setup:**
  - `python -m venv venv; .\venv\Scripts\activate; pip install -r requirements.txt`
- **Run Core Algorithm:**
  - `python experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py`
- **Testing:**
  - Use VS Code tasks: `🔬 Run All Tests` or `🧪 Test Autonomous Optimizer`
  - Manual: `python -m pytest -v --tb=short`
- **Azure Deployment:**
  - `azd up` (after OIDC setup)
  - Validate with `python -c "import azure_config; print('Azure deployment validation...')"`
- **Benchmarking:**
  - `python sota_benchmark.py` for SOTA comparisons (autonomous execution, logs to `logs/life_benchmark.log`)
  - `python autonomous_sota_kpi_monitor.py` for KPI monitoring
- **Optimization:**
  - `python autonomous_optimizer.py` for neural processing optimization (creates `logs/` and `results/` directories automatically)

## Project-Specific Conventions

- **Logging:** All logs are Unicode-safe, ASCII-only, and exported for compliance. Scripts auto-create `logs/` directory with absolute paths (e.g., `logs/life_benchmark.log`, `logs/autonomous_optimizer.log`).
- **Directory Structure:** Scripts auto-create required directories (`logs/`, `results/`) and use absolute paths for reproducibility.
- **Naming:** Key scripts and files use descriptive, long-form names for clarity (e.g., `experimentP2L...py`).
- **CI/CD:** See `.github/workflows/blank.yml` for pipeline structure; Azure deployment is automated.
- **Documentation:** Key guides: `README.md`, `AZURE_OIDC_SETUP.md`, `QUICK_START.md`.
- **Code Structure:** Use dataclasses for data structures (`EEGMetrics`, `LearningOutcome`), enums for states (`LearningStage`, `NeuralState`), asyncio for concurrency, numpy/pandas for data processing.

## Integration Points

- **Azure:** OIDC authentication, Azure CLI, Key Vault, and monitoring are core to deployment and compliance. Services include Blob Storage (EEG data), Service Bus (messaging), Monitor (logs/metrics), Functions (serverless processing).
- **APIs:** RESTful endpoints for enterprise integration (see `azure_life_functions.py`).
- **Data:** BCI datasets (e.g., BCI Competition IV-2a) are used for validation and benchmarking.
- **External Domain:** `lifecoach-121.com` for external access.

## Examples

- To run a full validation cycle:
  - `python -c "from experimentP2L import LIFEAlgorithmCore; import asyncio; life = LIFEAlgorithmCore(); asyncio.run(life.run_100_cycle_eeg_test())"`
- To deploy to Azure:
  - `azd up` (after running `setup-azure-oidc.ps1`)

---

For more, see `README.md` and documentation files. If unclear, review the referenced scripts for workflow details.
