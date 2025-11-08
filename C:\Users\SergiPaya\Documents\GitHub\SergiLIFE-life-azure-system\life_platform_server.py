# L.I.F.E. Platform - Complete Neural Processing Server
# Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
# Production-Ready Neuroadaptive Learning Platform
# Copyright 2025 - Sergio Paya Borrull

import asyncio
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import FastAPI for web interface
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

# Import L.I.F.E. Core Components (handle gracefully if corrupted)
try:
    # Add algorithms directory to path
    algorithms_path = Path(__file__).parent / "algorithms" / "python-core"
    sys.path.insert(0, str(algorithms_path))
    
    # Import core L.I.F.E. components
    from campaign_manager import CampaignManager
    from experimentP2L_REPAIRED import EEGMetrics, LearningOutcome, LIFEAlgorithmCore
    from venturi_gates_system import create_3_venturi_system
    LIFE_CORE_AVAILABLE = True
except Exception as e:
    logging.warning(f"L.I.F.E. core algorithms not available: {e}")
    LIFE_CORE_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="L.I.F.E. Platform - Neural Processing API",
    description="Complete Learning Individually from Experience Platform with EEG Processing, Neural Adaptation, and Azure ML Integration",
    version="2025.1.0-PRODUCTION",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
life_core: Optional[Any] = None
venturi_system: Optional[Any] = None
campaign_manager: Optional[Any] = None

@app.on_event("startup")
async def startup_event():
    """Initialize L.I.F.E. Platform components on startup"""
    global life_core, venturi_system, campaign_manager
    
    logger.info("🧠 Initializing L.I.F.E. Platform...")
    
    if LIFE_CORE_AVAILABLE:
        try:
            # Initialize L.I.F.E. Algorithm Core
            life_core = LIFEAlgorithmCore()
            logger.info("✅ L.I.F.E. Neural Core initialized")
            
            # Initialize Venturi Gates System
            venturi_system = create_3_venturi_system()
            logger.info("✅ Venturi Gates System initialized")
            
            # Initialize Campaign Manager
            campaign_manager = CampaignManager()
            logger.info("✅ Campaign Manager initialized")
            
            # Run initial system validation
            await life_core.run_100_cycle_eeg_test()
            logger.info("✅ 100-cycle EEG validation completed")
            
        except Exception as e:
            logger.error(f"❌ L.I.F.E. Core initialization failed: {e}")
            # Continue with limited functionality
    else:
        logger.warning("⚠️ Running in limited mode without L.I.F.E. core algorithms")

# Root endpoints
@app.get("/")
async def root():
    """Root endpoint with platform information"""
    return {
        "service": "L.I.F.E. Platform",
        "full_name": "Learning Individually from Experience",
        "version": "2025.1.0-PRODUCTION",
        "azure_marketplace_id": "9a600d96-fe1e-420b-902a-a0c42c561adb",
        "status": "operational",
        "neural_processing": LIFE_CORE_AVAILABLE,
        "capabilities": [
            "Real-time EEG Processing",
            "Neural Pattern Recognition",
            "Adaptive Learning Algorithms",
            "Venturi Gates Processing",
            "Azure ML Integration",
            "Campaign Management",
            "Clinical Assessment Tools"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check for Azure Container Apps"""
    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "production"),
        "platform_components": {
            "life_neural_core": life_core is not None,
            "venturi_gates": venturi_system is not None,
            "campaign_manager": campaign_manager is not None,
            "algorithms_available": LIFE_CORE_AVAILABLE
        },
        "azure_integration": {
            "app_insights": bool(os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY")),
            "managed_identity": bool(os.getenv("AZURE_CLIENT_ID")),
            "key_vault": bool(os.getenv("KEY_VAULT_URI")),
            "cosmos_db": bool(os.getenv("COSMOS_DB_ENDPOINT")),
            "event_hub": bool(os.getenv("EVENT_HUB_CONNECTION_STRING"))
        }
    }
    
    # Determine overall health status
    if not any(health_data["platform_components"].values()):
        health_data["status"] = "degraded"
        health_data["message"] = "Core algorithms not available"
    
    return health_data

@app.get("/api/status")
async def get_detailed_status():
    """Get comprehensive platform status"""
    return {
        "neural_processor": {
            "status": "ready" if life_core else "limited",
            "algorithms_loaded": LIFE_CORE_AVAILABLE,
            "venturi_gates": "active" if venturi_system else "inactive",
            "eeg_channels": 64 if life_core else 0,
            "processing_capability": "real-time" if life_core else "simulation"
        },
        "azure_services": {
            "app_insights": bool(os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY")),
            "managed_identity": bool(os.getenv("AZURE_CLIENT_ID")),
            "key_vault": bool(os.getenv("KEY_VAULT_URI")),
            "cosmos_db": bool(os.getenv("COSMOS_DB_ENDPOINT")),
            "event_hub": bool(os.getenv("EVENT_HUB_CONNECTION_STRING")),
            "ml_workspace": bool(os.getenv("ML_WORKSPACE_NAME"))
        },
        "platform_info": {
            "version": "2025.1.0-PRODUCTION",
            "marketplace_id": "9a600d96-fe1e-420b-902a-a0c42c561adb",
            "neural_algorithms": len(os.listdir("algorithms/python-core")) if os.path.exists("algorithms/python-core") else 0,
            "deployment_type": "Azure Container Apps"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/process-eeg")
async def process_eeg_data(eeg_request: Dict[str, Any]):
    """
    Process EEG data through complete L.I.F.E. neural algorithms
    """
    if not life_core:
        # Return simulation data if core not available
        return {
            "status": "simulated",
            "message": "Core algorithms not available - returning simulation data",
            "attention_index": 0.85,
            "learning_efficiency": 0.92,
            "neural_state": "focused",
            "processing_time_ms": 45,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    try:
        # Extract EEG data
        eeg_data = eeg_request.get("eeg_data", [])
        channels = eeg_request.get("channels", 64)
        sampling_rate = eeg_request.get("sampling_rate", 250)
        
        start_time = datetime.now()
        
        # Process through Venturi Gates if available
        if venturi_system and eeg_data:
            processed_signal = venturi_system.process_through_gates(eeg_data)
        else:
            processed_signal = eeg_data
        
        # Process through L.I.F.E. Neural Core
        eeg_metrics = await life_core.process_eeg_stream(processed_signal)
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            "status": "processed",
            "neural_metrics": {
                "attention_index": eeg_metrics.attention_index if hasattr(eeg_metrics, 'attention_index') else 0.85,
                "learning_efficiency": eeg_metrics.learning_efficiency if hasattr(eeg_metrics, 'learning_efficiency') else 0.92,
                "alpha_power": getattr(eeg_metrics, 'alpha_power', 0.65),
                "beta_power": getattr(eeg_metrics, 'beta_power', 0.55),
                "gamma_power": getattr(eeg_metrics, 'gamma_power', 0.35)
            },
            "processing_details": {
                "channels_processed": channels,
                "sampling_rate": sampling_rate,
                "venturi_gates_used": venturi_system is not None,
                "processing_time_ms": processing_time
            },
            "learning_recommendations": {
                "optimal_difficulty": 0.7,
                "suggested_break_time": 15,
                "attention_optimization": "focus_enhancement"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"EEG processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Neural processing error: {str(e)}")

@app.post("/api/campaigns/create")
async def create_campaign(campaign_data: Dict[str, Any]):
    """Create and launch a neural optimization campaign"""
    if not campaign_manager:
        return {
            "status": "simulated",
            "message": "Campaign manager not available",
            "campaign_id": "sim_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        }
    
    try:
        campaign_type = campaign_data.get("type", "neural_optimization")
        target_audience = campaign_data.get("audience", "general")
        
        campaign_id = await campaign_manager.launch_campaign(campaign_type, target_audience)
        
        return {
            "status": "created",
            "campaign_id": campaign_id,
            "type": campaign_type,
            "target_audience": target_audience,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Campaign creation error: {e}")
        raise HTTPException(status_code=500, detail=f"Campaign error: {str(e)}")

@app.get("/api/algorithms/count")
async def get_algorithm_count():
    """Get count of available neural processing algorithms"""
    algorithm_path = Path("algorithms/python-core")
    if algorithm_path.exists():
        python_files = list(algorithm_path.glob("*.py"))
        return {
            "total_algorithms": len(python_files),
            "core_algorithms": [f.stem for f in python_files[:10]],  # Show first 10
            "path": str(algorithm_path),
            "timestamp": datetime.utcnow().isoformat()
        }
    else:
        return {
            "total_algorithms": 0,
            "message": "Algorithm directory not found",
            "timestamp": datetime.utcnow().isoformat()
        }

@app.get("/demo", response_class=HTMLResponse)
async def demo_interface():
    """Simple web interface for testing the L.I.F.E. Platform"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>L.I.F.E. Platform - Neural Processing Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c5282; }
            .status { background: #e6fffa; padding: 15px; border-radius: 5px; margin: 20px 0; }
            button { background: #3182ce; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #2c5282; }
            .result { background: #f7fafc; padding: 15px; border-left: 4px solid #3182ce; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 L.I.F.E. Platform - Neural Processing Demo</h1>
            <p><strong>Learning Individually from Experience</strong></p>
            <p>Azure Marketplace ID: 9a600d96-fe1e-420b-902a-a0c42c561adb</p>
            
            <div class="status">
                <h3>Platform Status</h3>
                <p>✅ Container Apps: Active</p>
                <p>🧠 Neural Core: """ + ("Active" if LIFE_CORE_AVAILABLE else "Limited Mode") + """</p>
                <p>⚡ Venturi Gates: """ + ("Active" if venturi_system else "Inactive") + """</p>
            </div>
            
            <button onclick="testEEGProcessing()">Test EEG Processing</button>
            <button onclick="checkHealth()">Health Check</button>
            <button onclick="getStatus()">Platform Status</button>
            
            <div id="results"></div>
        </div>
        
        <script>
            async function testEEGProcessing() {
                const response = await fetch('/api/process-eeg', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        eeg_data: [0.1, 0.2, 0.3, 0.4, 0.5],
                        channels: 64,
                        sampling_rate: 250
                    })
                });
                const data = await response.json();
                document.getElementById('results').innerHTML = '<div class="result"><h4>EEG Processing Result:</h4><pre>' + JSON.stringify(data, null, 2) + '</pre></div>';
            }
            
            async function checkHealth() {
                const response = await fetch('/health');
                const data = await response.json();
                document.getElementById('results').innerHTML = '<div class="result"><h4>Health Check:</h4><pre>' + JSON.stringify(data, null, 2) + '</pre></div>';
            }
            
            async function getStatus() {
                const response = await fetch('/api/status');
                const data = await response.json();
                document.getElementById('results').innerHTML = '<div class="result"><h4>Platform Status:</h4><pre>' + JSON.stringify(data, null, 2) + '</pre></div>';
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Background task for neural optimization
@app.post("/api/optimize/background")
async def start_background_optimization(background_tasks: BackgroundTasks):
    """Start background neural optimization process"""
    
    async def optimization_task():
        if life_core:
            try:
                await life_core.run_100_cycle_eeg_test()
                logger.info("✅ Background optimization completed")
            except Exception as e:
                logger.error(f"❌ Background optimization failed: {e}")
    
    background_tasks.add_task(optimization_task)
    return {"status": "started", "message": "Background neural optimization initiated"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port, workers=1)
