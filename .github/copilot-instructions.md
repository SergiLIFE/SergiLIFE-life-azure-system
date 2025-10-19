# Copilot Instructions for L.I.F.E Platform (SergiLIFE-life-azure-system)

Copyright 2025 - Sergio Paya Borrull  
L.I.F.E. Platform - Azure Marketplace Offer ID: `9a600d96-fe1e-420b-902a-a0c42c561adb`  
**Production-Ready:** September 27, 2025 | **Target:** $345K Q4 2025 → $50.7M by 2029  
**🚀 LIVE PLATFORM:** Post-October 2025 Launch | **Status:** OPERATIONAL

## System Architecture

**L.I.F.E.** (Learning Individually from Experience) is a production-ready neuroadaptive learning platform processing real-time EEG data. The system follows a four-layer architecture:

1. **Neural Processing Core** (`experimentP2L...py`, `lifetheory.py`): Processes EEG signals through dataclass-based metrics (`EEGMetrics`, `LearningOutcome`) and enum states (`LearningStage`, `NeuralState`). Uses asyncio for concurrent EEG stream processing.

2. **Venturi Gates System** (`venturi_gates_system.py`): Three-gate orchestrator applying fluid dynamics principles to neural processing. Each gate (INPUT, PROCESSING, OUTPUT) handles specific phases with sub-millisecond latency targets (0.38-0.45ms achieved).

3. **Azure Integration Layer** (`azure_config.py`, `azure_functions_workflow.py`): Production deployment on Azure Functions (10-min timeout), Blob Storage, Service Bus, Key Vault. Uses OIDC auth, no stored secrets. Production subscription: `5c88cef6-f243-497d-98af-6c6086d575ca` (East US 2).

4. **Campaign Automation System** (`campaign_manager.py`, `.github/workflows/campaign-launcher.yml`): Automated marketplace promotion with async campaign execution, KPI tracking, and outreach automation. Targets 1,720 institutions with segmented campaigns (educational, healthcare, enterprise).

**Key Architectural Patterns:**

- All EEG processing is async (`async def process_eeg_stream`)
- Metrics use `@dataclass` for immutability and type safety
- Azure clients initialized with `DefaultAzureCredential()` for OIDC
- Logs/results auto-create directories with absolute paths (`os.path.join(SCRIPT_DIR, "logs")`)
- **Windows-first development:** All paths use Windows conventions (`\` separators, `cmd.exe` commands)
- **No environment files:** All secrets managed through Azure Key Vault and OIDC
- **Campaign automation is async:** All campaign operations use `async def` in `CampaignManager` class

## Critical Developer Workflows

**Initial Setup (Windows):**

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```


# Copilot instructions — L.I.F.E. Platform (concise)

Purpose: help AI coding agents be productive quickly — architecture summary, dev workflows, repo conventions and key files.

- Offer ID: `9a600d96-fe1e-420b-902a-a0c42c561adb` | Production-ready (Sept 27, 2025)

Core architecture (short): Neural Processing Core (EEG dataclasses + async pipeline) → Venturi Gates orchestrator (INPUT/PROCESSING/OUTPUT) → Azure Integration (Blob/ServiceBus/Functions, OIDC) → Campaign Automation (async campaign manager + GitHub Actions).

Essential developer workflows (Windows/CMD):

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

```cmd
# Authenticate with Azure CLI (multi-tenant support):
# 1. Log in without requiring subscriptions (to list tenants):
az login --allow-no-subscriptions
az account tenant list --output table
# 2. Re-login to your specific tenant and set subscription:
az login --tenant e716161a-5e85-4d6d-82f9-96bcdd2e65ac
az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca
```

Quick test commands:
- Core validation (100-cycle): run the LIFE core script or use the helper: python -c "from experimentP2L import LIFEAlgorithmCore; import asyncio; life=LIFEAlgorithmCore(); asyncio.run(life.run_100_cycle_eeg_test())"
- Full tests: Use the VS Code task `🔬 Run All Tests` or `python -m pytest -v --tb=short`
- Run optimizer/benchmarks: `python autonomous_optimizer.py` and `python sota_benchmark.py` (results → `results/` / `logs/`)

Key repo conventions (do not invent):
- All EEG processing is async. Use await or asyncio.run().
- Neural metrics are dataclasses (EEGMetrics, CampaignMetrics). See `experimentP2L*` and `campaign_manager.py`.
- Azure clients use DefaultAzureCredential (OIDC). See `azure_config.py` for account names and `venturi_gates_count` config.
- Windows-first paths and CLI (cmd.exe). Avoid relying on .env files — secrets are in Key Vault.
- Always create `logs`/`results` directories before instantiating file handlers (see pattern using SCRIPT_DIR).

Integration pointers & examples:
- Azure resources: Storage `stlifeplatformprod`, KeyVault `kv-life-platform-prod`, Service Bus `sb-life-platform-prod`, Functions `life-functions-app` (East US 2).
- Long filenames: import modules by their package name (e.g., `import experimentP2L`) instead of trying to import literal hyphenated filenames.
- Campaign workflow: `campaign_manager.py` + `.github/workflows/campaign-launcher.yml`. Tracking output in `tracking_data/{kpis,outreach,conversions,analytics}/`.

Files to check first when making changes:
- `experimentP2L*.py` (core algorithm)
- `azure_config.py`, `azure_functions_workflow.py` (cloud wiring)
- `venturi_gates_system.py` (orchestration)
- `campaign_manager.py` and `.github/workflows/campaign-launcher.yml` (marketing automation)

When editing/adding code, run the 100-cycle core test and `pytest` if you change neural-processing code. Use the VS Code tasks for common runs.

If something isn't discoverable here (credentials, infra deployment scripts, or runtime secrets), ask — repo follows OIDC/Key Vault patterns so do not attempt to add plaintext secrets.

Please review this concise version and tell me if you want any specific examples or more inline snippets added (imports, asyncio patterns, or Azure client templates).
