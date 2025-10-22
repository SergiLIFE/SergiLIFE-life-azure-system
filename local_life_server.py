"""
L.I.F.E Platform - Local Development Server
Creates a local version of the Azure Functions for testing
"""

import logging
from datetime import datetime

from flask import Flask, jsonify, request

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def index():
    """Root endpoint - Platform information"""
    return jsonify(
        {
            "platform": "L.I.F.E (Learning Individually from Experience)",
            "version": "1.0.0",
            "status": "Local Development Mode",
            "timestamp": datetime.utcnow().isoformat(),
            "available_endpoints": [
                "/api/health",
                "/api/health_simple",
                "/api/eeg_processor",
                "/api/platform_info",
            ],
            "note": "This is the local development version. Azure deployment pending authorization.",
        }
    )


@app.route("/api/health")
def health():
    """Health check endpoint - matches Azure Function structure"""
    return jsonify(
        {
            "status": "healthy",
            "app": "L.I.F.E Platform",
            "structure": "local_dev",
            "timestamp": datetime.utcnow().isoformat(),
            "server": "Flask Development Server",
            "azure_status": "Pending Authorization",
        }
    )


@app.route("/api/health_simple")
def health_simple():
    """Simple health check - matches Azure Function structure"""
    return jsonify(
        {
            "status": "healthy",
            "app": "L.I.F.E Platform",
            "endpoint": "health_simple",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Local development endpoint working correctly",
            "deployment_note": "Azure Functions pending authorization approval",
        }
    )


@app.route("/api/eeg_processor", methods=["GET", "POST"])
def eeg_processor():
    """EEG Processing endpoint"""
    if request.method == "GET":
        return jsonify(
            {
                "service": "EEG Neural Processing",
                "status": "ready",
                "algorithms": [
                    "Venturi Gates",
                    "Neural State Detection",
                    "Learning Outcome Analysis",
                ],
                "processing_capacity": "Real-time EEG stream processing",
                "note": "Submit POST request with EEG data for processing",
            }
        )

    elif request.method == "POST":
        # Simulate EEG processing
        eeg_data = request.get_json()

        # Mock processing result
        result = {
            "processing_status": "completed",
            "input_channels": eeg_data.get("channels", 8) if eeg_data else 8,
            "processing_time_ms": 0.42,  # Sub-millisecond as per L.I.F.E specs
            "neural_state": "focused_learning",
            "learning_outcome": {
                "engagement_score": 0.87,
                "comprehension_level": "high",
                "suggested_adaptation": "increase_complexity",
            },
            "venturi_gates": {
                "input_gate": "optimized",
                "processing_gate": "active",
                "output_gate": "clear",
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

        return jsonify(result)


@app.route("/api/platform_info")
def platform_info():
    """Platform information and capabilities"""
    return jsonify(
        {
            "platform_name": "L.I.F.E (Learning Individually from Experience)",
            "copyright": "2025 - Sergio Paya Borrull",
            "azure_marketplace_id": "9a600d96-fe1e-420b-902a-a0c42c561adb",
            "target_revenue": "$345K Q4 2025 → $50.7M by 2029",
            "production_ready": "September 27, 2025",
            "architecture": {
                "neural_processing": "Real-time EEG analysis with sub-millisecond latency",
                "venturi_gates": "Three-gate orchestrator (INPUT/PROCESSING/OUTPUT)",
                "azure_integration": "Functions, Blob Storage, Service Bus, Key Vault",
                "campaign_automation": "Automated marketplace promotion system",
            },
            "deployment_status": {
                "local_development": "✅ Active",
                "azure_functions": "⏳ Pending Authorization",
                "marketplace_listing": "🎯 Ready for Deployment",
            },
            "endpoints": {
                "health_check": "/api/health",
                "eeg_processing": "/api/eeg_processor",
                "platform_info": "/api/platform_info",
            },
        }
    )


def main():
    """Start the local development server"""
    print("=" * 60)
    print("🧠 L.I.F.E PLATFORM - LOCAL DEVELOPMENT SERVER")
    print("=" * 60)
    print("Copyright 2025 - Sergio Paya Borrull")
    print("Azure Marketplace ID: 9a600d96-fe1e-420b-902a-a0c42c561adb")
    print()
    print("🎯 LOCAL ENDPOINTS:")
    print("   • Health Check: http://localhost:5000/api/health")
    print("   • Simple Health: http://localhost:5000/api/health_simple")
    print("   • EEG Processor: http://localhost:5000/api/eeg_processor")
    print("   • Platform Info: http://localhost:5000/api/platform_info")
    print()
    print("📝 NOTE: This is the local development version.")
    print("   Azure Functions deployment pending authorization approval.")
    print()
    print("🚀 Starting server on http://localhost:5000")
    print("   Press Ctrl+C to stop")
    print("=" * 60)

    # Start Flask development server
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()
