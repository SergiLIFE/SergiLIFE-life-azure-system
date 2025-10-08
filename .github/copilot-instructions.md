# Copilot Instructions for L.I.F.E Platform (SergiLIFE-life-azure-system)

Copyright 2025 - Sergio Paya Borrull  
L.I.F.E. Platform - Azure Marketplace Offer ID: `9a600d96-fe1e-420b-902a-a0c42c561adb`  
**Production-Ready:** September 27, 2025 | **Target:** $345K Q4 2025 → $50.7M by 2029  
**🎂 Automated Launch:** October 7, 2025 - 9:00 AM BST

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

**Testing Hierarchy (run in order):**

1. Core algorithm validation: `python experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py`
2. Full test suite: VS Code task `🔬 Run All Tests` or `python -m pytest -v --tb=short`
3. Production readiness: `python production_deployment_test.py` (comprehensive end-to-end)

**Azure Deployment:**

- Setup OIDC: `.\setup-azure-oidc.ps1` (one-time PowerShell script, creates GitHub repo variables)
- Deploy infrastructure: `azd up` (uses `azure.yaml` config, deploys to East US 2)
- GitHub Actions: `.github/workflows/blank.yml` auto-deploys on push to main (OIDC auth, no secrets)
- Validate deployment: Run VS Code task `🚀 Azure Deploy Prep` or `python -c "import azure_config; print('Azure deployment validation...')"`

**Campaign Management (new in Oct 2025):**

- Manual launch: `python campaign_manager.py` (creates tracking infrastructure, generates outreach templates)
- GitHub Actions: Navigate to Actions → "L.I.F.E. Platform - Azure Marketplace Campaign Launcher" → Run workflow
- GitHub CLI: `gh workflow run campaign-launcher.yml --repo SergiLIFE/SergiLIFE-life-azure-system -f campaign_type=marketplace_promotion`
- Campaign types: `marketplace_promotion`, `partner_outreach`, `institution_discovery`, `performance_showcase`
- Tracking data created in: `tracking_data/{kpis,outreach,conversions,analytics}/`
- October 7, 2025 automated launch at 9:00 AM BST (birthday launch, fully automated via GitHub Actions scheduler)

**Benchmarking (auto-run, no user intervention):**

- SOTA comparison: `python sota_benchmark.py` → logs to `logs/life_benchmark.log`
- Neural optimization: Run VS Code task `🧠 Run Autonomous Optimizer` or `python autonomous_optimizer.py` → exports to `results/`
- KPI monitoring: `python autonomous_sota_kpi_monitor.py`

**VS Code Tasks (preferred method):**

All tasks defined in `.vscode/tasks.json` can be run via Command Palette (`Ctrl+Shift+P` → "Run Task"):

- `🧠 Run Autonomous Optimizer` - Full neural processing optimization
- `🔬 Run All Tests` - Complete test suite with pytest
- `🏆 Run SOTA Benchmarks` - State-of-the-art performance comparison
- `✅ Validate L.I.F.E. Environment` - Dependency and component validation
- `🚀 Azure Deploy Prep` - Azure deployment configuration validation

**Key Commands NOT Obvious from Files:**

- EEG test: `python -c "from experimentP2L import LIFEAlgorithmCore; import asyncio; life = LIFEAlgorithmCore(); asyncio.run(life.run_100_cycle_eeg_test())"`
- Import validation: `python -c "import experimentP2L; print(experimentP2L.LIFEAlgorithmCore, experimentP2L.EEGMetrics)"`
- Quick Azure check: `az account show --output table` (requires Azure CLI installed)

## Project-Specific Conventions

**Code Structure Patterns:**

```python
# Always use dataclasses for neural metrics
@dataclass
class EEGMetrics:
    timestamp: datetime
    alpha_power: float
    # ... 8 more required fields

# Enums for state management (never strings)
class LearningStage(Enum):
    ACQUISITION = "acquisition"
    CONSOLIDATION = "consolidation"

# Async for ALL EEG processing
async def process_eeg_stream(self, eeg_data: np.ndarray) -> EEGMetrics:
    # Band power extraction: alpha (8-12Hz), beta (12-30Hz), etc.
    alpha_power = self._calculate_band_power(eeg_data, 8, 12)
```

**Directory Auto-Creation Pattern (critical for reproducibility):**

```python
# Standard across all scripts
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")
RESULTS_DIR = os.path.join(SCRIPT_DIR, "results")
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOGS_DIR, "script_name.log")
```

**Azure Client Initialization (OIDC pattern):**

```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.servicebus import ServiceBusClient

credential = DefaultAzureCredential()  # No secrets needed - uses OIDC
blob_client = BlobServiceClient(
    account_url=f"https://{account_name}.blob.core.windows.net",
    credential=credential
)
servicebus_client = ServiceBusClient(
    fully_qualified_namespace=f"{namespace}.servicebus.windows.net",
    credential=credential
)
```

**Logging Pattern (ASCII-only for compliance):**

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # Always after directory creation
        logging.StreamHandler()
    ]
)
```

**Testing Pattern (100-cycle validation):**

```python
# All neural processing must pass 100-cycle test
async def run_100_cycle_eeg_test(self) -> Dict[str, Any]:
    for cycle in range(100):
        synthetic_eeg = self._generate_test_eeg_data()
        metrics = await self.process_eeg_stream(synthetic_eeg)
        accuracy = self._validate_eeg_processing(synthetic_eeg, metrics)
        assert accuracy > 0.75, f"Cycle {cycle} accuracy below threshold"
```

## Integration Points & Data Flow

**EEG Processing Pipeline:**

1. **Input:** Raw EEG array (channels × time_points) from `_generate_test_eeg_data()` or real sensors
2. **Processing:** Extract 5 frequency bands (delta 0.5-4Hz, theta 4-8Hz, alpha 8-12Hz, beta 12-30Hz, gamma 30-100Hz)
3. **Metrics:** Calculate coherence, attention index, learning efficiency → populate `EEGMetrics` dataclass
4. **Output:** Return typed metrics for adaptive learning session

**Azure Resource Dependencies (production):**

- **Storage Account:** `stlifeplatformprod` (Blob containers for EEG data, results)
- **Key Vault:** `kv-life-platform-prod` (secrets, connection strings)
- **Service Bus:** `sb-life-platform-prod` (message queues for async processing)
- **Functions:** `life-functions-app` (serverless processing, 10-min timeout)
- **Resource Group:** `life-platform-rg` (East US 2 region)

**Venturi Gates System (central orchestrator):**

- **INPUT Gate:** Validates and normalizes incoming EEG data
- **PROCESSING Gate:** Applies neural algorithms (main computation)
- **OUTPUT Gate:** Formats and delivers results
- **Configuration:** `venturi_gates_count: int = 3` in `azure_config.py`
- **Target Latency:** Sub-millisecond (0.38-0.45ms measured)
- **Gate Types (Enum):** SIGNAL_ENHANCEMENT, NOISE_REDUCTION, PATTERN_EXTRACTION, ADAPTIVE_FILTERING

**Campaign Management System (new architecture):**

- **CampaignManager class:** Async operations for campaign launch, metrics tracking, outreach generation
- **Dataclasses:** `CampaignMetrics` (campaign performance), `MarketplaceKPIs` (Azure marketplace metrics)
- **Tracking directories:** Auto-created at `tracking_data/{kpis,outreach,conversions,analytics}/`
- **Target segments:** Educational institutions (1,720 total), healthcare facilities, enterprise partners, research institutions
- **Campaign types:** Marketplace promotion, partner outreach, institution discovery, performance showcase
- **Integration:** GitHub Actions workflow `.github/workflows/campaign-launcher.yml` for automated execution
- **Scheduled launch:** October 7, 2025 at 9:00 AM BST (automated via workflow_dispatch with scheduler)

**External Integrations:**

- **PhysioNet Datasets:** BCI Competition IV-2a for validation (see `azure_eeg_test_framework.py`)
- **Microsoft Graph API:** User management and SSO (enterprise tier)
- **SendGrid (planned):** Email automation for campaign outreach to 1,720+ institutions
- **Partner Center API:** Azure Marketplace offer management (Offer ID: `9a600d96-fe1e-420b-902a-a0c42c561adb`)
- **Domain:** `lifecoach-121.com` for external access
- **Azure Functions:** Serverless execution environment in `life-functions-app/` (eeg-preprocessing, ml-training, quantum-processing)

## Common Pitfalls & Solutions

**Import Issues (common with long filenames):**

```python
# ❌ WRONG: Direct import may fail
from experimentP2L.I.F.E-Learning... import LIFEAlgorithmCore

# ✅ CORRECT: Use module name with underscores
import experimentP2L
life = experimentP2L.LIFEAlgorithmCore()
```

**Directory Creation (must be before logging setup):**

```python
# ❌ WRONG: Logging before directory exists
logging.FileHandler("logs/file.log")  # Fails if logs/ missing

# ✅ CORRECT: Always create first
os.makedirs("logs", exist_ok=True)
LOG_FILE = os.path.join(SCRIPT_DIR, "logs", "file.log")
```

**Async/Await (EEG processing):**

```python
# ❌ WRONG: Calling async function without await
metrics = life.process_eeg_stream(eeg_data)  # Returns coroutine

# ✅ CORRECT: Use await or asyncio.run()
metrics = await life.process_eeg_stream(eeg_data)
# Or from main: asyncio.run(life.process_eeg_stream(eeg_data))
```

**Testing Sequence (order matters):**

1. Run `experimentP2L...py` first to validate core algorithm
2. Then `production_deployment_test.py` for end-to-end
3. Finally `sota_benchmark.py` for performance comparison
4. Never run `pytest` alone without validating core first

**Module Import Pattern (long filenames):**

```python
# ❌ WRONG: Direct import with hyphens/dots fails
from experimentP2L.I.F.E-Learning-Individually... import LIFEAlgorithmCore

# ✅ CORRECT: Import module, then access class
import experimentP2L
life = experimentP2L.LIFEAlgorithmCore()
metrics = experimentP2L.EEGMetrics(...)
```

## Recent Optimizations (September 2025)

**Production Readiness Achieved:**

- ✅ 100% test success rate across all validation suites
- ✅ Sub-millisecond processing (0.38-0.45ms actual)
- ✅ 78-82% accuracy on real EEG datasets
- ✅ Azure infrastructure fully deployed (East US 2)
- ✅ Marketplace certification complete (9/9 sections)
- ✅ Campaign automation system deployed (October 7, 2025 launch ready)
- ✅ Launch ready: September 27, 2025

**Performance Targets (validated):**

- Processing latency: <1ms (achieved 0.38ms)
- Accuracy: >75% (achieved 78-82%)
- Throughput: 80+ cycles/sec (achieved 80.16)
- Uptime: 99.9% (production SLA)

**Campaign System Updates (October 2025):**

- Automated marketplace promotion targeting 1,720 institutions
- Async campaign execution with real-time KPI tracking
- GitHub Actions integration for scheduled launches
- Outreach automation with segmented templates (educational, healthcare, enterprise)
- Revenue tracking: $345K Q4 2025 target → $50.7M by 2029
- Birthday launch automation: October 7, 2025 at 9:00 AM BST

---

**Quick Reference:**

- **Core Algorithm:** `experimentP2L...py` (500+ lines, production-ready)
- **Azure Config:** `azure_config.py` (enterprise metrics, OIDC setup)
- **Campaign Manager:** `campaign_manager.py` (async campaign execution, KPI tracking)
- **Testing Suite:** `production_deployment_test.py` (comprehensive validation)
- **Benchmarking:** `sota_benchmark.py`, `autonomous_optimizer.py`
- **CI/CD:** `.github/workflows/blank.yml` (OIDC auto-deploy), `.github/workflows/campaign-launcher.yml` (campaign automation)
- **Deployment:** `azd up` after `.\setup-azure-oidc.ps1`

For unclear workflows, check the referenced scripts or ask about specific components. The platform is production-ready and optimized for Azure Marketplace launch with automated campaign management.
