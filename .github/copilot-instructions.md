# Copilot Instructions for L.I.F.E Platform (SergiLIFE-life-azure-system)

## Project Overview

- **L.I.F.E.** is a production-ready, Azure-native platform for neuroadaptive learning, leveraging real-time EEG data and adaptive algorithms.
- Major components: EEG processing, adaptive learning engine, Azure integration, enterprise analytics, and compliance modules.
- Key files: `experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py` (core algorithm), `azure_config.py`, `azure_functions_workflow.py`, `autonomous_optimizer.py`, `azure_deployment_manager.py`.

## Architecture & Patterns

- **EEG Data Flow:** Real-time EEG data is processed and fed into adaptive learning models. Results are logged and exported for auditability.
- **Azure Integration:** Uses OIDC authentication (`setup-azure-oidc.ps1`), Azure CLI (`azure.yaml`), and deployment scripts for cloud operations.
- **Validation:** Automated 100-cycle EEG test suite and benchmarking scripts (see `autonomous_sota_kpi_monitor.py`, `sota_benchmark.py`).
- **Evidence Export:** All validation and benchmark results are exported in both human- and machine-readable formats.
- **Compliance:** Encryption, key management, and audit logging are handled via Azure services and `azure_config.py`.

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
  - `python sota_benchmark.py` for SOTA comparisons
  - `python autonomous_sota_kpi_monitor.py` for KPI monitoring

## Project-Specific Conventions

- **Logging:** All logs are Unicode-safe, ASCII-only, and exported for compliance.
- **Directory Structure:** Scripts auto-create required directories and use absolute paths for reproducibility.
- **Naming:** Key scripts and files use descriptive, long-form names for clarity (e.g., `experimentP2L...py`).
- **CI/CD:** See `.github/workflows/blank.yml` for pipeline structure; Azure deployment is automated.
- **Documentation:** Key guides: `README.md`, `AZURE_OIDC_SETUP.md`, `QUICK_START.md`.

## Integration Points

- **Azure:** OIDC authentication, Azure CLI, Key Vault, and monitoring are core to deployment and compliance.
- **APIs:** RESTful endpoints for enterprise integration (see `azure_life_functions.py`).
- **Data:** BCI datasets (e.g., BCI Competition IV-2a) are used for validation and benchmarking.

## Examples

- To run a full validation cycle:
  - `python -c "from experimentP2L import LIFEAlgorithmCore; import asyncio; life = LIFEAlgorithmCore(); asyncio.run(life.run_100_cycle_eeg_test())"`
- To deploy to Azure:
  - `azd up` (after running `setup-azure-oidc.ps1`)

---

For more, see `README.md` and documentation files. If unclear, review the referenced scripts for workflow details.
