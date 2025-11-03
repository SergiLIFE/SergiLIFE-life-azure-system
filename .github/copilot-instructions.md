# Copilot Instructions for L.I.F.E Platform

**Repository:** SergiLIFE-life-azure-system  
**Copyright:** 2025 - Sergio Paya Borrull  
**Azure Marketplace Offer ID:** `9a600d96-fe1e-420b-902a-a0c42c561adb`  
**Status:** Production-Ready (September 27, 2025) | OPERATIONAL

## System Architecture

**L.I.F.E.** (Learning Individually from Experience) is a production-ready neuroadaptive learning platform processing real-time EEG data. The system follows a four-layer architecture:

1. **Neural Processing Core** (`experimentP2L*.py`, `lifetheory.py`): Processes EEG signals through dataclass-based metrics (`EEGMetrics`, `LearningOutcome`) and enum states (`LearningStage`, `NeuralState`). Uses asyncio for concurrent EEG stream processing.

2. **Venturi Gates System** (`venturi_gates_system.py`): Three-gate orchestrator applying fluid dynamics principles to neural processing. Each gate (INPUT, PROCESSING, OUTPUT) handles specific phases with sub-millisecond latency targets (0.38-0.45ms achieved).

3. **Azure Integration Layer** (`azure_config.py`, `azure_functions_workflow.py`): Production deployment on Azure Functions (10-min timeout), Blob Storage, Service Bus, Key Vault. Uses OIDC auth, no stored secrets. Production subscription: `5c88cef6-f243-497d-98af-6c6086d575ca` (East US 2).

4. **Campaign Automation System** (`campaign_manager.py`, `.github/workflows/campaign-launcher.yml`): Automated marketplace promotion with async campaign execution, KPI tracking, and outreach automation. Targets 1,720 institutions with segmented campaigns (educational, healthcare, enterprise).

## Key Architectural Patterns

- **All EEG processing is async**: Use `async def process_eeg_stream` pattern with `await` or `asyncio.run()`
- **Metrics use `@dataclass`**: For immutability and type safety (e.g., `EEGMetrics`, `CampaignMetrics`)
- **Azure clients use OIDC**: Initialize with `DefaultAzureCredential()` - no stored secrets
- **Directory auto-creation**: Logs/results directories created with absolute paths using `os.path.join(SCRIPT_DIR, "logs")`
- **Windows-first development**: All paths use Windows conventions (`\` separators, `cmd.exe` commands)
- **No environment files**: All secrets managed through Azure Key Vault and OIDC
- **Campaign automation is async**: All campaign operations use `async def` in `CampaignManager` class

## Setup and Development Workflows

### Initial Setup (Windows)

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Azure CLI Authentication (multi-tenant support)

```cmd
# 1. Log in without requiring subscriptions (to list tenants):
az login --allow-no-subscriptions
az account tenant list --output table

# 2. Re-login to your specific tenant and set subscription:
az login --tenant e716161a-5e85-4d6d-82f9-96bcdd2e65ac
az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca
```

## Testing and Validation

### Quick Test Commands

- **Core validation (100-cycle)**: 
  ```cmd
  python -c "from experimentP2L import LIFEAlgorithmCore; import asyncio; life=LIFEAlgorithmCore(); asyncio.run(life.run_100_cycle_eeg_test())"
  ```

- **Full test suite**: 
  ```cmd
  python -m pytest -v --tb=short
  ```
  Or use VS Code task: `🔬 Run All Tests`

- **Optimizer/Benchmarks**: 
  ```cmd
  python autonomous_optimizer.py
  python sota_benchmark.py
  ```
  Results written to `results/` and `logs/` directories.

### VS Code Tasks

The repository includes comprehensive VS Code tasks for common operations:
- `🚀 Ultimate Full-Cycle Ecosystem Test` - Complete system validation
- `🔬 Run All Tests` - Full pytest suite
- `🧠 Run Autonomous Optimizer` - Neural processing optimization
- `🏆 Run SOTA Benchmarks` - Performance benchmarks

## Repository Conventions

### Critical Rules (DO NOT INVENT)

- **Async patterns**: All EEG processing must be async. Use `async/await` within async functions, `asyncio.run()` for top-level entry points
- **Dataclasses for metrics**: See `experimentP2L*.py` and `campaign_manager.py` for examples
- **OIDC authentication**: Use `DefaultAzureCredential()` - see `azure_config.py`
- **Windows paths**: Use `cmd.exe` commands, `\` separators, avoid POSIX assumptions
- **No .env files**: Secrets are in Azure Key Vault only
- **Directory creation**: Always create `logs`/`results` directories before file handlers (see SCRIPT_DIR pattern)

### Azure Resources

- **Storage Account**: `stlifeplatformprod`
- **Key Vault**: `kv-life-platform-prod`
- **Service Bus**: `sb-life-platform-prod`
- **Functions App**: `life-functions-app`
- **Region**: East US 2

### Module Imports

For long filenames, import by package name (e.g., `import experimentP2L`) instead of literal hyphenated filenames.

### Campaign Workflow

- Main files: `campaign_manager.py` + `.github/workflows/campaign-launcher.yml`
- Tracking data: `tracking_data/{kpis,outreach,conversions,analytics}/`

## Key Files to Check First

When making changes, review these files first:
- **Core Algorithm**: `experimentP2L*.py`
- **Cloud Integration**: `azure_config.py`, `azure_functions_workflow.py`
- **Orchestration**: `venturi_gates_system.py`
- **Marketing Automation**: `campaign_manager.py`, `.github/workflows/campaign-launcher.yml`

## Validation Protocol

When editing/adding code:
1. Run the 100-cycle core test for neural-processing changes
2. Run `pytest` for any code modifications
3. Use VS Code tasks for common validation runs
4. Check that logs/results directories are created before writing files

## Security Notes

- All credentials and secrets must use Azure Key Vault
- Never add plaintext secrets to code or configuration files
- Use OIDC/Key Vault patterns throughout
- If credentials are needed but not discoverable, ask rather than inventing solutions
