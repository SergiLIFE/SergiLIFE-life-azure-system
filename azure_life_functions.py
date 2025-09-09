"""
Azure Functions Integration for L.I.F.E Theory
HTTP triggers for EEG processing and Venturi enhancement

Copyright 2025 - Sergio Paya Borrull
"""

import json
import logging
import traceback
from datetime import datetime
from typing import Any, Dict, List

import azure.functions as func
import numpy as np

# Import L.I.F.E Theory components
from eeg_processor import create_eeg_processor
from lifetheory import create_life_algorithm
from venturi_gates_system import create_3_venturi_system

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global processors (initialized once for better performance)
eeg_processor = None
venturi_system = None
life_algorithm = None


def initialize_processors():
    """Initialize processors on first use"""
    global eeg_processor, venturi_system, life_algorithm

    if eeg_processor is None:
        logger.info("Initializing L.I.F.E Theory processors...")

        # Create EEG processor with optimized configuration
        eeg_config = {
            "sampling_rate": 250.0,
            "learning_rate": 0.005,
            "venturi_factor": 1.2,
            "max_experiences": 1000,  # Reduced for Azure Functions
        }
        eeg_processor = create_eeg_processor(eeg_config)

        # Create Venturi system
        venturi_system = create_3_venturi_system()

        # Create general L.I.F.E algorithm
        life_config = {
            "learning_rate": 0.01,
            "max_experiences": 1000,
            "venturi_gate_factor": 1.2,
        }
        life_algorithm = create_life_algorithm(life_config)

        logger.info("L.I.F.E Theory processors initialized successfully")


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Main Azure Functions entry point"""
    try:
        # Initialize processors if needed
        initialize_processors()

        # Get request method and route
        method = req.method
        route = req.route_params.get("route", "status")

        logger.info(f"Processing {method} request for route: {route}")

        # Route requests to appropriate handlers
        if route == "process-eeg":
            return process_eeg_endpoint(req)
        elif route == "venturi-enhance":
            return venturi_enhance_endpoint(req)
        elif route == "life-process":
            return life_process_endpoint(req)
        elif route == "status":
            return status_endpoint(req)
        elif route == "health":
            return health_check_endpoint(req)
        else:
            return func.HttpResponse(
                json.dumps({"error": f"Unknown route: {route}"}),
                status_code=404,
                mimetype="application/json",
            )

    except Exception as e:
        logger.error(f"Error in main handler: {str(e)}")
        logger.error(traceback.format_exc())

        return func.HttpResponse(
            json.dumps(
                {
                    "error": "Internal server error",
                    "message": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            status_code=500,
            mimetype="application/json",
        )


def process_eeg_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """Process EEG data through L.I.F.E Theory pipeline"""
    try:
        if req.method != "POST":
            return func.HttpResponse(
                json.dumps({"error": "Method not allowed. Use POST."}),
                status_code=405,
                mimetype="application/json",
            )

        # Parse request body
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                json.dumps({"error": "Invalid JSON in request body"}),
                status_code=400,
                mimetype="application/json",
            )

        # Validate request structure
        if not req_body or "eeg_data" not in req_body:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'eeg_data' in request body"}),
                status_code=400,
                mimetype="application/json",
            )

        # Extract parameters
        eeg_data = np.array(req_body["eeg_data"])
        channels = req_body.get("channels", None)
        context = req_body.get("context", {})

        # Validate EEG data
        if eeg_data.ndim != 2:
            return func.HttpResponse(
                json.dumps({"error": "EEG data must be 2D array (channels x samples)"}),
                status_code=400,
                mimetype="application/json",
            )

        # Process EEG data
        logger.info(f"Processing EEG data: {eeg_data.shape}")
        results = eeg_processor.process(eeg_data, channels, context)

        # Convert numpy arrays to lists for JSON serialization
        serializable_results = make_json_serializable(results)

        # Add metadata
        serializable_results.update(
            {
                "processed_by": "L.I.F.E Theory EEG Processor",
                "azure_function": "process-eeg",
                "processing_time": datetime.now().isoformat(),
            }
        )

        logger.info(f"EEG processing completed successfully")

        return func.HttpResponse(
            json.dumps(serializable_results),
            status_code=200,
            mimetype="application/json",
        )

    except Exception as e:
        logger.error(f"Error in EEG processing: {str(e)}")
        return func.HttpResponse(
            json.dumps(
                {
                    "error": "EEG processing failed",
                    "message": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            status_code=500,
            mimetype="application/json",
        )


def venturi_enhance_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """Apply Venturi enhancement to signal data"""
    try:
        if req.method != "POST":
            return func.HttpResponse(
                json.dumps({"error": "Method not allowed. Use POST."}),
                status_code=405,
                mimetype="application/json",
            )

        # Parse request
        req_body = req.get_json()
        if not req_body or "signal" not in req_body:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'signal' in request body"}),
                status_code=400,
                mimetype="application/json",
            )

        signal = np.array(req_body["signal"])
        context = req_body.get("context", {})
        processing_mode = req_body.get("mode", "serial")  # 'serial' or 'parallel'

        # Validate signal
        if signal.ndim != 1:
            return func.HttpResponse(
                json.dumps({"error": "Signal must be 1D array"}),
                status_code=400,
                mimetype="application/json",
            )

        logger.info(
            f"Applying Venturi enhancement: {len(signal)} samples, mode: {processing_mode}"
        )

        # Apply Venturi processing
        if processing_mode == "parallel":
            results = venturi_system.process_parallel_gates(signal, context)
        else:
            results = venturi_system.process_through_gates(signal, context)

        # Make results JSON serializable
        serializable_results = make_json_serializable(results)

        # Add metadata
        serializable_results.update(
            {
                "processed_by": "Venturi Gates System",
                "azure_function": "venturi-enhance",
                "processing_mode": processing_mode,
                "processing_time": datetime.now().isoformat(),
            }
        )

        logger.info("Venturi enhancement completed successfully")

        return func.HttpResponse(
            json.dumps(serializable_results),
            status_code=200,
            mimetype="application/json",
        )

    except Exception as e:
        logger.error(f"Error in Venturi enhancement: {str(e)}")
        return func.HttpResponse(
            json.dumps(
                {
                    "error": "Venturi enhancement failed",
                    "message": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            status_code=500,
            mimetype="application/json",
        )


def life_process_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """Process data through core L.I.F.E algorithm"""
    try:
        if req.method != "POST":
            return func.HttpResponse(
                json.dumps({"error": "Method not allowed. Use POST."}),
                status_code=405,
                mimetype="application/json",
            )

        # Parse request
        req_body = req.get_json()
        if not req_body or "data" not in req_body:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'data' in request body"}),
                status_code=400,
                mimetype="application/json",
            )

        data = np.array(req_body["data"])
        context = req_body.get("context", {})

        logger.info(f"Processing data through L.I.F.E algorithm: {data.shape}")

        # Process through L.I.F.E algorithm
        processed_data = life_algorithm.process(data, context)

        # Get performance metrics
        metrics = life_algorithm.get_performance_metrics()

        # Prepare results
        results = {
            "processed_data": processed_data.tolist(),
            "performance_metrics": metrics,
            "input_shape": list(data.shape),
            "output_shape": list(processed_data.shape),
        }

        # Add metadata
        results.update(
            {
                "processed_by": "L.I.F.E Theory Algorithm",
                "azure_function": "life-process",
                "processing_time": datetime.now().isoformat(),
            }
        )

        logger.info("L.I.F.E processing completed successfully")

        return func.HttpResponse(
            json.dumps(results), status_code=200, mimetype="application/json"
        )

    except Exception as e:
        logger.error(f"Error in L.I.F.E processing: {str(e)}")
        return func.HttpResponse(
            json.dumps(
                {
                    "error": "L.I.F.E processing failed",
                    "message": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            status_code=500,
            mimetype="application/json",
        )


def status_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """Get system status and metrics"""
    try:
        # Initialize processors if needed
        initialize_processors()

        # Collect status from all components
        status = {
            "system": "L.I.F.E Theory Azure Functions",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "components": {},
        }

        # EEG processor status
        if eeg_processor:
            eeg_status = eeg_processor.get_processor_status()
            status["components"]["eeg_processor"] = eeg_status

        # Venturi system status
        if venturi_system:
            venturi_status = venturi_system.get_system_status()
            status["components"]["venturi_system"] = venturi_status

        # L.I.F.E algorithm status
        if life_algorithm:
            life_metrics = life_algorithm.get_performance_metrics()
            status["components"]["life_algorithm"] = life_metrics

        # System capabilities
        status["capabilities"] = {
            "eeg_processing": True,
            "venturi_enhancement": True,
            "life_algorithm": True,
            "real_time_processing": True,
            "adaptive_learning": True,
            "quantum_enhancement": False,  # Not implemented in this version
        }

        return func.HttpResponse(
            json.dumps(status), status_code=200, mimetype="application/json"
        )

    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        return func.HttpResponse(
            json.dumps(
                {
                    "system": "L.I.F.E Theory Azure Functions",
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            status_code=500,
            mimetype="application/json",
        )


def health_check_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """Simple health check endpoint"""
    try:
        # Quick health check
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime": "running",
            "version": "1.0.0",
        }

        return func.HttpResponse(
            json.dumps(health_status), status_code=200, mimetype="application/json"
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps(
                {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            status_code=500,
            mimetype="application/json",
        )


def make_json_serializable(obj: Any) -> Any:
    """Convert numpy arrays and other non-serializable objects to JSON-compatible format"""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: make_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [make_json_serializable(item) for item in obj]
    else:
        return obj


# Example usage for local testing
def test_local_eeg_processing():
    """Test EEG processing locally"""
    print("Testing L.I.F.E Theory EEG processing locally...")

    # Initialize processors
    initialize_processors()

    # Create test EEG data
    channels = 4
    samples = 1000
    eeg_data = np.random.randn(channels, samples) * 50  # Typical EEG amplitude
    channel_names = ["Fp1", "Fp2", "C3", "C4"]

    # Process EEG data
    results = eeg_processor.process(eeg_data, channel_names, {"test": "local"})

    print(f"Processing completed:")
    print(f"  Channels: {len(results['channels'])}")
    print(f"  Performance: {results['performance']['overall_score']:.3f}")
    print(f"  Quality improvement: {results['performance']['quality_improvement']:.3f}")

    return results


def test_local_venturi_enhancement():
    """Test Venturi enhancement locally"""
    print("Testing Venturi enhancement locally...")

    # Initialize processors
    initialize_processors()

    # Create test signal
    t = np.linspace(0, 1, 1000)
    signal = np.sin(2 * np.pi * 10 * t) + 0.3 * np.random.randn(1000)

    # Apply Venturi enhancement
    results = venturi_system.process_through_gates(signal)

    print(f"Venturi enhancement completed:")
    print(f"  System efficiency: {results['system_efficiency']:.3f}")
    print(f"  Gates processed: {len(results['gate_outputs'])}")

    return results


if __name__ == "__main__":
    # Local testing
    print("L.I.F.E Theory Azure Functions - Local Testing")
    print("=" * 50)

    # Test EEG processing
    eeg_results = test_local_eeg_processing()

    print()

    # Test Venturi enhancement
    venturi_results = test_local_venturi_enhancement()

    print("\nLocal testing completed successfully!")
    print("Ready for Azure Functions deployment.")
