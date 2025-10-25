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

## Testing Expectations

- **Always Run Tests Early:** Before making code changes, run existing tests to understand the baseline. Use `python -m pytest -v --tb=short` to run all tests.
- **Test-Driven Development:** When fixing bugs or adding features, write tests first that validate the expected behavior.
- **Continuous Validation:** Run tests after each code change to catch issues early. Don't wait until all changes are complete.
- **Test Coverage:** Maintain or improve test coverage. Use `pytest-cov` for coverage reports: `python -m pytest --cov=. --cov-report=html`
- **Test Types:**
  - Unit tests for individual components (e.g., `test_*.py` files)
  - Integration tests for Azure services (`test_azure_functions.py`)
  - End-to-end tests for complete workflows (`production_deployment_test.py`)
  - Performance tests for benchmarking (`sota_benchmark.py`)
- **Test Isolation:** Tests should be independent and not rely on external state unless testing integration points.
- **Mock External Services:** When testing locally, mock Azure services unless specifically testing integration.

## Code Review Process

- **Self-Review First:** Before requesting review, check your changes for:
  - Code quality and readability
  - Adherence to project conventions
  - No debug code or commented-out sections
  - Proper error handling
  - Security considerations
- **PR Description:** Always provide clear, detailed PR descriptions that include:
  - What problem is being solved
  - How the solution works
  - Testing performed
  - Any breaking changes or migrations needed
- **Small, Focused PRs:** Keep changes minimal and focused on a single issue. Large PRs are harder to review and more likely to introduce bugs.
- **Respond to Feedback:** Address all review comments or provide reasoning if you disagree.
- **Documentation Updates:** Update relevant documentation when changing functionality.

## Security and Compliance Guidelines

- **Never Commit Secrets:** Use Azure Key Vault for secrets, credentials, and API keys. Never hardcode sensitive information.
- **Data Privacy:** Handle EEG data and user information according to GDPR, HIPAA, and other relevant regulations.
- **Encryption:** Use encryption for data at rest (Azure Storage encryption) and in transit (HTTPS/TLS).
- **Input Validation:** Always validate and sanitize user inputs to prevent injection attacks.
- **Dependency Security:** Run security scans before adding new dependencies. Check for known vulnerabilities.
- **Audit Logging:** Ensure all critical operations are logged for compliance and debugging.
- **Access Control:** Implement proper RBAC (Role-Based Access Control) for Azure resources.
- **Code Scanning:** Leverage GitHub's security features and CodeQL scanning.

## Issue and PR Interaction Guidelines

- **Understand the Issue:** Fully read and understand the issue description and comments before starting work.
- **Ask Questions:** If requirements are unclear, ask for clarification in the issue comments using `@mentions`.
- **Link PRs to Issues:** Always reference the issue number in your PR (e.g., "Fixes #123" or "Addresses #456").
- **Progress Updates:** Comment on issues with progress updates, especially for complex or long-running tasks.
- **Breaking Changes:** Clearly document any breaking changes in both PR and issue comments.
- **Testing Evidence:** Provide evidence of testing (screenshots, logs, test results) in PR descriptions.

## Common Pitfalls and Troubleshooting

- **Import Errors:** If modules fail to import, ensure all dependencies are installed: `pip install -r requirements.txt`
- **Azure Authentication:** Most Azure operations require proper OIDC setup. Run `setup-azure-oidc.ps1` first.
- **Environment Variables:** Missing environment variables can cause failures. Check `azure_config.py` for required variables.
- **Path Issues:** Always use absolute paths for file operations. Scripts auto-create `logs/` and `results/` directories.
- **Unicode/Encoding:** All logs must be ASCII-only for compliance. Use proper encoding when handling text.
- **Async Operations:** Many operations use asyncio. Ensure proper async/await usage and event loop management.
- **Azure Rate Limits:** Be mindful of Azure API rate limits. Implement retry logic with exponential backoff.
- **Test Data Location:** EEG test data is in `bci_data/`. Ensure paths are correct when running tests.

## Best Practices for Copilot Interaction

- **Be Specific:** When assigned an issue, Copilot performs best with clear, specific requirements.
- **Incremental Changes:** Make small, verifiable changes. Test frequently.
- **Context Matters:** Copilot will reference this file for guidance. Keep instructions clear and up-to-date.
- **Review Generated Code:** Always review code suggestions for correctness, security, and adherence to project standards.
- **Provide Feedback:** Use PR comments to guide Copilot toward better solutions if initial attempts need refinement.

## Examples

- To run a full validation cycle:
  - `python -c "from experimentP2L import LIFEAlgorithmCore; import asyncio; life = LIFEAlgorithmCore(); asyncio.run(life.run_100_cycle_eeg_test())"`
- To deploy to Azure:
  - `azd up` (after running `setup-azure-oidc.ps1`)
- To run all tests with coverage:
  - `python -m pytest -v --tb=short --cov=. --cov-report=html`
- To check code style:
  - `black --check .` and `flake8 .`

---

For more, see `README.md` and documentation files. If unclear, review the referenced scripts for workflow details.

**Current Status (September 21, 2025):** The L.I.F.E. Platform is fully production-ready with all optimizations completed, Azure infrastructure deployed, and marketplace launch preparation finalized. Ready for September 27, 2025 marketplace launch with Azure Marketplace Offer ID: `9a600d96-fe1e-420b-902a-a0c42c561adb`. 🎉
