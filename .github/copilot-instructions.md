# Copilot Instructions for L.I.F.E Platform (SergiLIFE-life-azure-system)

Copyright 2025 - Sergio Paya Borrull  
L.I.F.E. Platform - Azure Marketplace Offer ID: `9a600d96-fe1e-420b-902a-a0c42c561adb`  
**Production-Ready:** September 27, 2025 | **Target:** $345K Q4 2025 → $50.7M by 2029  
**🚀 LIVE PLATFORM:** Post-October 2025 Launch | **Status:** OPERATIONAL

## System Architecture

**L.I.F.E.** (Learning Individually from Experience) is a production-ready neuroadaptive learning platform processing real-time EEG data. The system follows a multi-layer architecture:

1. **Neural Processing Core** (`algorithms/python-core/experimentP2L_REPAIRED.py`): Processes EEG signals through dataclass-based metrics (`EEGMetrics`, `LearningOutcome`, `UserTraits`) and enum states (`LearningStage`, `NeuralState`). All EEG processing is async with sub-millisecond targets.

2. **Venturi Gates System** (`algorithms/python-core/venturi_gates_system.py`): Three-gate fluid dynamics orchestrator (SIGNAL_ACCELERATION, NOISE_REDUCTION, PATTERN_EXPANSION) applying Venturi principles to neural processing. Sub-millisecond latency: 0.38-0.45ms per gate.

3. **Azure Integration Layer** (`azure_functions/function_app.py`, `algorithms/python-core/azure_config.py`): Production Azure Functions with marketplace webhook handling (`marketplace-webhook`, `connection-webhook`, `health` endpoints), OIDC authentication, and no stored secrets. Resources: `life-functions-app`, `stlifeplatformprod`, `kv-life-platform-prod`.

4. **Campaign Automation System** (`algorithms/python-core/campaign_manager.py`): Async campaign execution with KPI tracking, targeting 1,720 institutions across educational, healthcare, and enterprise segments.

5. **Azure Marketplace Integration** (`marketplace_integration_setup.py`, `AZURE_MARKETPLACE_INTEGRATION_GUIDE.md`): Full SaaS fulfillment API with subscription lifecycle management, landing pages, and Partner Center configuration.

**Key Architectural Patterns:**

- **All neural processing is async** (`async def process_eeg_stream`, `await` for neural operations)
- **Dataclass-based metrics** for immutability: `UserTraits`, `EEGMetrics`, `LearningOutcome`
- **OIDC-only authentication** via `DefaultAzureCredential()` - no connection strings
- **Windows-first development** with `cmd.exe` commands and `\` path separators
- **Auto-directory creation** pattern: `os.makedirs(LOGS_DIR, exist_ok=True)` before file operations
- **Bicep Infrastructure as Code** in `infra/` - all Azure resources defined declaratively
- **Marketplace webhook pattern** - SaaS fulfillment handled via Azure Functions v2 model

## Essential Developer Workflows

**Initial Setup (Windows):**
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Azure Authentication (Multi-tenant):**
```cmd
# 1. Login without subscription requirements to list tenants:
az login --allow-no-subscriptions
az account tenant list --output table
# 2. Login to specific tenant and set subscription:
az login --tenant e716161a-5e85-4d6d-82f9-96bcdd2e65ac
az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca
```

**Core Testing & Validation:**
- **Primary test suite:** Use VS Code task `🔬 Run All Tests` (`python -m pytest -v --tb=short`)
- **Platform validation:** Use VS Code task `🔧 Validate L.I.F.E. Environment`
- **Azure connection check:** Use VS Code task `� Flawless Connection Validator`
- **Platform server:** Use VS Code task `🧠 Launch L.I.F.E Theory Platform`
- **Full ecosystem test:** Use VS Code task `⚡ Ultimate Full-Cycle Ecosystem Test` (if available)
- **Marketplace integration:** `python marketplace_integration_setup.py`

## Key Repository Conventions

**Critical Patterns (Do Not Invent):**
- **All EEG processing is async:** Use `async def` and `await` for neural operations
- **Dataclass-based metrics:** `UserTraits`, `EEGMetrics`, `LearningOutcome` in `experimentP2L_REPAIRED.py`
- **OIDC-only Azure auth:** `DefaultAzureCredential()` - no connection strings or `.env` files
- **Windows-first development:** Use `cmd.exe` commands and `\` path separators
- **Auto-create directories:** Always `os.makedirs(LOGS_DIR, exist_ok=True)` before file operations

**Azure Resources (East US 2):**
- Functions: `life-functions-app` (marketplace webhooks in `azure_functions/function_app.py`)
- Storage: `stlifeplatformprod` 
- Key Vault: `kv-life-platform-prod`
- Service Bus: `sb-life-platform-prod`

**Campaign System:**
- Async operations in `algorithms/python-core/campaign_manager.py`
- Tracking data: `tracking_data/{kpis,outreach,conversions,analytics}/`

## VS Code Task Automation

**Frequently Used Tasks:**
- `🔬 Run All Tests` - Full pytest suite
- `⚡ Ultimate Full-Cycle Ecosystem Test` - Complete system validation
- `🚀 Run Autonomous Optimizer` - Performance benchmarking  
- `🧠 Launch L.I.F.E Theory Platform` - Local platform server
- `🔧 Azure Deploy Prep` - Connection validation

**Testing Hierarchy:**
1. **Neural core test:** VS Code task or direct Python import from `algorithms/python-core/`
2. **Azure integration:** `🔧 Flawless Connection Validator` task
3. **Full ecosystem:** `python ULTIMATE_FULL_CYCLE_ECOSYSTEM_TEST.py`

## Essential Development Patterns

**Async Neural Processing (CRITICAL):**
```python
# All EEG processing must be async - found in experimentP2L_REPAIRED.py
async def process_eeg_stream(self, eeg_data: np.ndarray) -> EEGMetrics:
    # Use await for neural operations
    alpha_power = await self._calculate_band_power(eeg_data, 8, 12)
    attention_index = await self._calculate_attention_index(alpha_power, beta_power)
    return metrics

# Venturi Gates integration for sub-millisecond processing
venturi_system = create_3_venturi_system()
processed_signal = venturi_system.process_through_gates(eeg_signal)
```

**Dataclass Usage Pattern:**
```python
# All metrics are immutable dataclasses - see experimentP2L_REPAIRED.py
@dataclass
class UserTraits:
    user_id: str
    curiosity: float  # 0.0-1.0
    persistence: float
    openness: float
    processing_speed: float
    learning_efficiency: float

@dataclass 
class EEGMetrics:
    attention_index: float
    learning_efficiency: float
```

**Azure Functions Deployment:**
```cmd
# Deploy with remote build - handles Python version differences
az functionapp deployment source config-zip --name life-functions-app --resource-group life-platform-prod --src deployment.zip --build remote

# Test marketplace webhooks after deployment
curl -X POST https://life-functions-app.azurewebsites.net/api/marketplace-webhook \
  -H "Content-Type: application/json" \
  -d '{"subscriptionId":"test123","action":"Subscribe","planId":"life-individual"}'
```

**Marketplace Integration Pattern:**
```python
# Azure Functions v2 model with SaaS fulfillment - see azure_functions/function_app.py
@app.route(route="marketplace-webhook", auth_level=func.AuthLevel.FUNCTION, methods=["POST"])
async def marketplace_webhook(req: func.HttpRequest) -> func.HttpResponse:
    webhook_data = req.get_json()
    subscription_id = webhook_data.get("subscriptionId")
    action = webhook_data.get("action")  # Subscribe, Unsubscribe, ChangePlan
    
    if action == "Subscribe":
        result = await provision_life_platform_access(subscription_id, plan_id)
    # Handle lifecycle events and provision L.I.F.E. platform access
```

**Campaign Manager (Async Pattern):**
```python
# All campaign operations are async - see campaign_manager.py
async def launch_campaign(self, campaign_type: str, target_audience: str) -> str:
    campaign_id = await self._create_campaign_metadata()
    await self.generate_outreach_campaign(target_audience)
    return campaign_id
```

## File Structure & Key Locations

**Core Algorithm Files:**
- `algorithms/python-core/experimentP2L_REPAIRED.py` - Main L.I.F.E algorithm with dataclasses
- `algorithms/python-core/venturi_gates_system.py` - 3-gate fluid dynamics orchestrator
- `algorithms/python-core/azure_config.py` - OIDC-only Azure configuration

**Azure Integration:**
- `azure_functions/function_app.py` - Marketplace webhook handlers (`@app.route` with Python v2 model)
- `infra/main.bicep` - Infrastructure as Code for production deployment
- `marketplace_integration_setup.py` - Automated marketplace setup and configuration
- `AZURE_MARKETPLACE_INTEGRATION_GUIDE.md` - Complete integration documentation

**Infrastructure & Deployment:**
- `infra/` - Complete Bicep templates for multi-environment deployment
- `azure_functions_requirements.txt` - Specific dependencies for Azure Functions runtime
- Automated deployment via `automation/batch-scripts/` for Windows workflows

**Testing & Validation:**
- Use VS Code tasks for common workflows - avoid manual terminal commands
- Directory auto-creation: `os.makedirs(LOGS_DIR, exist_ok=True)` before file operations
- Campaign tracking: `tracking_data/{kpis,outreach,conversions,analytics}/`

**Deployment Notes:**
- Python 3.11 required in Azure (local may be 3.13)  
- OIDC authentication only - no connection strings or environment files
- All secrets in Azure Key Vault: `kv-life-platform-prod`

**Current Project State (November 2025):**
- Core files may have encoding issues - handle gracefully when reading
- Many VS Code tasks defined in `.vscode/tasks.json` - prefer tasks over manual commands
- Marketplace integration actively developed via `marketplace_integration_setup.py`
- Bicep infrastructure templates exist in `infra/` directory
- Multiple demo and validation scripts available in root directory

## Critical Development Guidelines

**Testing Requirements:**
- **Always** run 100-cycle EEG test before committing neural processing changes
- Use VS Code tasks over manual terminal commands for consistency
- Run `ULTIMATE_FULL_CYCLE_ECOSYSTEM_TEST.py` for comprehensive system validation
- Marketplace webhook testing: Use curl commands from `AZURE_MARKETPLACE_INTEGRATION_GUIDE.md`

**Import Patterns:**
- Long filenames: `from algorithms.python_core import experimentP2L_REPAIRED`
- Venturi system: `from algorithms.python_core.venturi_gates_system import create_3_venturi_system`
- Azure integration: `from azure_functions.function_app import app`

**Deployment Checklist:**
1. Validate environment: VS Code task `🔧 Flawless Connection Validator`
2. Test neural core: Direct Python import with async validation
3. Deploy to staging: Use Bicep templates in `infra/`
4. Marketplace integration: Follow `marketplace_integration_setup.py` workflow
5. Production deployment: Remote build with Azure CLI
