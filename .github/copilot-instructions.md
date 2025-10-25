# Copilot Instructions for L.I.F.E Platform (SergiLIFE-life-azure-system)

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb

## Project Overview

- **L.I.F.E.** is a production-ready, Azure-native platform for neuroadaptive learning, leveraging real-time EEG data and adaptive algorithms.
- Major components: EEG processing, adaptive learning engine, Azure integration, enterprise analytics, compliance modules, and Venturi system architecture.
- Key files: `experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py` (core algorithm), `azure_config.py`, `azure_functions_workflow.py`, `autonomous_optimizer.py`, `azure_deployment_manager.py`, `production_deployment_test.py` (comprehensive testing suite).
- Core classes: `LIFEAlgorithmCore`, `EEGMetrics`, `LearningOutcome`, `LearningStage`, `NeuralState`, `VenturiGatesSystem`.
- Business model: SaaS with pricing tiers ($15 Basic, $30 Professional, $50 Enterprise); revenue targets $345K Q4 2025 → $50.7M by 2029.
- Version: 2025.1.0-PRODUCTION; Azure Marketplace Offer ID: `9a600d96-fe1e-420b-902a-a0c42c561adb`; Launch: September 27, 2025.
- **Current Status:** ✅ Fully production-ready with 100% test success rate, Azure infrastructure deployed and operational, marketplace certification complete (9/9 sections), ready for launch.

## Repository Structure

- **Core Algorithm:** `experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py` - Main L.I.F.E. algorithm implementation
- **Azure Integration:** `azure_config.py`, `azure_functions_workflow.py`, `azure_deployment_manager.py` - Azure service integration
- **Venturi System:** `venturi_gates_system.py`, `three_venturi_harmonic_calibration.py`, `venturi_batching.py` - Venturi architecture components
- **Testing:** `tests/` directory, `test_*.py` files, `production_deployment_test.py` - Test suites
- **Optimization:** `autonomous_optimizer.py`, `model_optimizer.py`, `performance_analyzer.py` - Performance optimization tools
- **Benchmarking:** `sota_benchmark.py`, `autonomous_sota_kpi_monitor.py` - SOTA comparison and KPI tracking
- **EEG Processing:** `AZURE_EEG_TESTING_SUITE.py`, `real_eeg_physionet_test.py`, `standalone_azure_eeg_test.py` - EEG data processing
- **Documentation:** Markdown files in root (e.g., `README.md`, `AZURE_OIDC_SETUP.md`, `QUICK_START.md`)
- **Configuration:** `.vscode/` (VS Code settings), `.github/workflows/` (CI/CD), `pylintrc` (linting), `requirements.txt` (dependencies)

## Architecture & Patterns

- **EEG Data Flow:** Real-time EEG data is processed and fed into adaptive learning models. Results are logged and exported for auditability.
- **Core Algorithm Structure:** Uses dataclasses (`EEGMetrics`, `LearningOutcome`) and enums (`LearningStage`, `NeuralState`) for neural processing. Implements asyncio for concurrent operations and pandas/numpy for data handling.
- **Azure EEG Testing Framework:** Validates the platform using real PhysioNet datasets (e.g., BCI Competition IV-2a) across multiple neuroadaptive scenarios. Achieves sub-millisecond (0.38–0.45ms) processing and 78–82% accuracy, with transparent benchmarking and evidence export.
- **Azure Integration:** Production-grade use of Azure Functions (serverless, 10-min timeout), Blob Storage (scalable EEG/result storage), and Azure Monitor (real-time health/performance tracking). OIDC authentication (`setup-azure-oidc.ps1`), Azure CLI (`azure.yaml`), and deployment scripts for cloud operations. Production subscription: `5c88cef6-f243-497d-98af-6c6086d575ca` (East US 2), resources include RG `life-platform-rg`, Storage `stlifeplatformprod`, Key Vault `kv-life-platform-prod`, Service Bus `sb-life-platform-prod`, Marketplace Offer `9a600d96-fe1e-420b-902a-a0c42c561adb`.
- **Validation:** Automated 100-cycle EEG test suite, benchmarking scripts (`autonomous_sota_kpi_monitor.py`, `sota_benchmark.py`), and cross-scenario validation (brain cognition, heart-brain coupling, neuroplasticity). Production deployment test suite (`production_deployment_test.py`) validates end-to-end functionality with 100% success rate.
- **Evidence Export:** All validation and benchmark results are exported in both human- and machine-readable formats for auditability and regulatory review.
- **Compliance:** Encryption, key management, and audit logging are handled via Azure services and `azure_config.py`.
- **Scientific Validation:** Ongoing requirements include standardized cross-validation, statistical significance testing, direct comparison with published research, and independent replication for clinical/academic credibility.
- **Venturi Architecture:** 3 Venturi gates as central orchestrator system with fluid dynamics principles for ultra-low latency processing; external domain `lifecoach-121.com`.
- **Production Readiness:** ✅ All components validated, Azure infrastructure deployed and operational, marketplace certification complete, ready for September 27, 2025 launch.

## Developer Workflows

- **Setup:**
  - `python -m venv venv; .\venv\Scripts\activate; pip install -r requirements.txt`
- **Run Core Algorithm:**
  - `python experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py`
- **Testing:**
  - Use VS Code tasks: `🔬 Run All Tests` or `🧪 Test Autonomous Optimizer`
  - Manual: `python -m pytest -v --tb=short`
  - Production validation: `python production_deployment_test.py` (comprehensive end-to-end testing)
- **Azure Deployment:**
  - `azd up` (after OIDC setup)
  - Validate with `python -c "import azure_config; print('Azure deployment validation...')"`
- **Benchmarking:**
  - `python sota_benchmark.py` for SOTA comparisons (autonomous execution, logs to `logs/life_benchmark.log`)
  - `python autonomous_sota_kpi_monitor.py` for KPI monitoring
- **Optimization:**
  - `python autonomous_optimizer.py` for neural processing optimization (creates `logs/` and `results/` directories automatically)
- **Production Validation:**
  - Run `production_deployment_test.py` for complete system validation before marketplace launch

## Project-Specific Conventions

- **Logging:** All logs are Unicode-safe, ASCII-only, and exported for compliance. Scripts auto-create `logs/` directory with absolute paths (e.g., `logs/life_benchmark.log`, `logs/autonomous_optimizer.log`).
- **Directory Structure:** Scripts auto-create required directories (`logs/`, `results/`) and use absolute paths for reproducibility.
- **Naming:** Key scripts and files use descriptive, long-form names for clarity (e.g., `experimentP2L...py`).
- **CI/CD:** See `.github/workflows/blank.yml` for pipeline structure; Azure deployment is automated.
- **Documentation:** Key guides: `README.md`, `AZURE_OIDC_SETUP.md`, `QUICK_START.md`.
- **Code Structure:** Use dataclasses for data structures (`EEGMetrics`, `LearningOutcome`), enums for states (`LearningStage`, `NeuralState`), asyncio for concurrency, numpy/pandas for data processing.

## Code Style & Quality

- **Formatting:** Use Black for code formatting (line length: 100). Configuration in `pylintrc`.
- **Linting:** Run `pylint` with project-specific rules (see `pylintrc`). Also use `flake8` for additional checks.
- **Type Hints:** Use type hints for function parameters and return values. Run `mypy` for type checking.
- **Testing Standards:**
  - Place tests in `tests/` directory or colocate with prefix `test_*.py`
  - Use pytest for all tests with descriptive test names: `test_<functionality>_<scenario>_<expected_outcome>`
  - Aim for >80% code coverage on new features
  - Use `pytest-asyncio` for async tests, `pytest-mock` for mocking
  - Test files should mirror the structure of the code they test
- **Error Handling:**
  - Use specific exception types (avoid bare `except:`)
  - Log errors with context using structured logging
  - Implement retry logic for Azure service calls with exponential backoff
  - Always clean up resources in `finally` blocks or use context managers

## Security Guidelines

- **Secrets Management:**
  - Never commit credentials, API keys, or secrets to git
  - Use Azure Key Vault for production secrets (see `azure_config.py`)
  - Use environment variables or `.env` files for local development (add `.env` to `.gitignore`)
- **Data Privacy:**
  - EEG data must be anonymized before processing
  - Follow HIPAA and GDPR compliance requirements
  - Encrypt sensitive data at rest and in transit
- **Azure Security:**
  - Use Managed Identities for Azure resource authentication
  - Follow least-privilege principle for RBAC assignments
  - Enable Azure Monitor for security audit logging

## Troubleshooting

- **Common Issues:**
  - **Import Errors:** Ensure virtual environment is activated and all dependencies installed
  - **Azure Auth Failures:** Run `az login` and verify subscription access
  - **EEG Processing Errors:** Check that PhysioNet datasets are available and properly formatted
  - **Test Failures:** Run individual test files to isolate issues: `pytest -v test_<specific>.py`
- **Performance Issues:**
  - Check system resources with `Performance Monitor` VS Code task
  - Review logs in `logs/` directory for bottlenecks
  - Use `sota_benchmark.py` to compare performance against baselines
- **Debugging:**
  - Use VS Code debugger with launch configurations in `.vscode/launch.json`
  - Add breakpoints in key processing loops for EEG data flow
  - Use `python -m pdb` for command-line debugging

## Integration Points

- **Azure:** OIDC authentication, Azure CLI, Key Vault, and monitoring are core to deployment and compliance. Services include Blob Storage (EEG data), Service Bus (messaging), Monitor (logs/metrics), Functions (serverless processing).
- **APIs:** RESTful endpoints for enterprise integration (see `azure_life_functions.py`).
- **Data:** BCI datasets (e.g., BCI Competition IV-2a) are used for validation and benchmarking.
- **External Domain:** `lifecoach-121.com` for external access.

## Recent Optimizations & Validations (September 2025)

### ✅ **Production Readiness Achievements**

- ✅ **Component Import Issues Resolved** - All core modules validated for correct imports
- ✅ **Full Integration Tests** - Comprehensive testing with real Azure resources completed
- ✅ **Production Deployment Validation** - Azure infrastructure fully operational and validated
- ✅ **Marketplace Launch Preparation** - Documentation, pricing, and offer configuration finalized
- ✅ **Azure Resources Deployed** - Function App, Storage, Key Vault, Service Bus operational in East US 2
- ✅ **Enterprise Security** - RBAC, encryption, and compliance configurations active
- ✅ **Venturi System Integration** - All Venturi modules tested and operational
- ✅ **EEG Data Validation** - Real PhysioNet datasets processed successfully

### 📊 **Performance Metrics (Latest Validation)**

```
✅ Production Deployment Test Results
   ├── Core Algorithm Test: PASSED
   ├── Azure Functions Test: PASSED
   ├── EEG Data Pipeline Test: PASSED
   ├── Enterprise Analytics Test: PASSED
   ├── Security & Compliance Test: PASSED
   ├── Performance Benchmarking: PASSED
   ├── Overall Status: PRODUCTION_READY
   └── Success Rate: 100.0%
```

### 🎯 **Launch Readiness Status**

- **Marketplace Certification:** 9/9 sections complete ✅
- **Azure Infrastructure:** Fully deployed and operational ✅
- **Code Optimization:** Production deployment tests passed ✅
- **Documentation:** Complete and ready for customers ✅
- **Launch Date:** September 27, 2025 (6 days remaining) 🚀

## Examples

- To run a full validation cycle:
  - `python -c "from experimentP2L import LIFEAlgorithmCore; import asyncio; life = LIFEAlgorithmCore(); asyncio.run(life.run_100_cycle_eeg_test())"`
- To deploy to Azure:
  - `azd up` (after running `setup-azure-oidc.ps1`)

---

For more, see `README.md` and documentation files. If unclear, review the referenced scripts for workflow details.

## Collaboration Guidelines

- **Pull Requests:** Keep PRs focused and small. Include clear descriptions and link to related issues.
- **Commit Messages:** Use conventional commits format: `type(scope): description` (e.g., `feat(eeg): add new processing algorithm`)
- **Code Reviews:** All code requires review before merging. Focus on correctness, performance, and maintainability.
- **Issue Tracking:** Use GitHub Issues for bugs and features. Label appropriately (bug, enhancement, documentation, etc.).
- **Breaking Changes:** Document in CHANGELOG.md and increment version appropriately (following semver).

## Performance Requirements

- **Latency:** Target sub-millisecond processing (<1ms) for EEG data
- **Accuracy:** Maintain 78-82% accuracy benchmarks in neuroadaptive scenarios
- **Scalability:** Design for 3,000-85,000 concurrent users
- **Reliability:** 99.9% uptime SLA for Enterprise tier
- **Resource Usage:** Optimize for efficient Azure resource consumption to control costs

**Current Status (September 21, 2025):** The L.I.F.E. Platform is fully production-ready with all optimizations completed, Azure infrastructure deployed, and marketplace launch preparation finalized. Ready for September 27, 2025 marketplace launch with Azure Marketplace Offer ID: `9a600d96-fe1e-420b-902a-a0c42c561adb`. 🎉
