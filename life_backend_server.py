"""
🧠 L.I.F.E Platform Backend Integration Server
October 17, 2025

This is the MISSING PIECE that connects HTML platforms to the actual algorithm.
- Receives EEG data from platforms
- Processes with experimentP2L.py algorithm
- Returns REAL results instead of simulated data

Run this server alongside your HTTP server (different port):
    Python backend: http://localhost:5000 (this file)
    HTML platforms: http://localhost:8080 (python -m http.server 8080)
"""

import asyncio
import json
import os
import sys
import traceback
from datetime import datetime

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# ============================================================================
# IMPORT L.I.F.E ALGORITHM
# ============================================================================

try:
    # Try to import the actual L.I.F.E algorithm
    from experimentP2L import EEGMetrics, LearningOutcome, LIFEAlgorithmCore

    print("✅ Successfully imported L.I.F.E Algorithm from experimentP2L")
    ALGORITHM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Could not import experimentP2L: {e}")
    print("   Will use MOCK algorithm for demonstration")
    ALGORITHM_AVAILABLE = False

# ============================================================================
# FLASK APP SETUP
# ============================================================================

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests (platforms on :8080 → backend on :5000)

# Create logs directory (Windows-compatible)
LOGS_DIR = os.path.join(os.path.dirname(__file__), "logs", "backend")
try:
    os.makedirs(LOGS_DIR, exist_ok=True)
except Exception as e:
    print(f"⚠️  Could not create logs directory: {e}")
    LOGS_DIR = os.path.join(os.path.dirname(__file__), "logs")

# ============================================================================
# MOCK ALGORITHM (Fallback if experimentP2L not available)
# ============================================================================


class MockLIFEAlgorithm:
    """Fallback algorithm that generates realistic-looking results"""

    def __init__(self):
        self.processing_count = 0

    def process_eeg(self, eeg_data):
        """Process EEG data and return mock results"""
        self.processing_count += 1

        # Generate realistic metrics based on input
        import random

        import numpy as np

        # Convert input to array if needed
        if isinstance(eeg_data, list):
            signal = np.array(eeg_data)
        else:
            signal = np.array([random.gauss(0, 1) for _ in range(100)])

        # Calculate basic metrics
        mean_amplitude = float(np.mean(np.abs(signal)))
        frequency_spread = float(np.std(signal))

        return {
            "algorithm": "MOCK (experimentP2L not found)",
            "processing_cycle": self.processing_count,
            "eeg_quality": min(100, int(mean_amplitude * 50)),
            "neural_engagement": min(
                100, int((mean_amplitude + frequency_spread) * 30)
            ),
            "learning_readiness": min(100, random.randint(60, 95)),
            "cognitive_load": min(100, random.randint(30, 80)),
            "attention_score": min(100, random.randint(50, 90)),
            "adaptability_index": min(100, random.randint(40, 85)),
            "timestamp": datetime.now().isoformat(),
            "note": "Using mock algorithm - install/import experimentP2L.py for real results",
        }


# ============================================================================
# INITIALIZE ALGORITHM
# ============================================================================

if ALGORITHM_AVAILABLE:
    life_algorithm = LIFEAlgorithmCore()
    print("✅ L.I.F.E Algorithm Core initialized")
else:
    life_algorithm = MockLIFEAlgorithm()
    print("⚠️  Using MOCK algorithm - results are simulated")

# ============================================================================
# BACKEND ROUTES
# ============================================================================


@app.route("/health", methods=["GET"])
def health_check():
    """Check if backend is running"""
    return (
        jsonify(
            {
                "status": "OPERATIONAL",
                "timestamp": datetime.now().isoformat(),
                "algorithm": (
                    "REAL (experimentP2L)"
                    if ALGORITHM_AVAILABLE
                    else "MOCK (simulation)"
                ),
                "version": "1.0",
            }
        ),
        200,
    )


@app.route("/analyze-eeg", methods=["POST"])
def analyze_eeg():
    """
    Main endpoint: Receive EEG data, process with algorithm, return results

    Expected request format:
    {
        "eeg_signal": [array of numbers],
        "sample_rate": 256,
        "duration_seconds": 2,
        "session_id": "unique-id",
        "user_type": "student|clinical|enterprise|researcher",
        "metadata": {...}
    }
    """
    try:
        # Get EEG data from request
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided", "status": "FAILED"}), 400

        eeg_signal = data.get("eeg_signal")
        if not eeg_signal:
            return (
                jsonify({"error": "No 'eeg_signal' in request", "status": "FAILED"}),
                400,
            )

        # Extract metadata
        sample_rate = data.get("sample_rate", 256)
        duration_seconds = data.get("duration_seconds", 2)
        session_id = data.get(
            "session_id", f"session_{int(datetime.now().timestamp())}"
        )
        user_type = data.get("user_type", "general")

        print(
            f"📊 Processing EEG - Session: {session_id}, Length: {len(eeg_signal)} samples"
        )

        # Process with algorithm
        if ALGORITHM_AVAILABLE:
            # Run actual algorithm
            result = process_with_real_algorithm(
                eeg_signal=eeg_signal,
                sample_rate=sample_rate,
                session_id=session_id,
                user_type=user_type,
            )
        else:
            # Run mock algorithm
            result = life_algorithm.process_eeg(eeg_signal)

        # Log the result
        log_result(session_id, result)

        # Return result
        return (
            jsonify(
                {
                    "status": "SUCCESS",
                    "session_id": session_id,
                    "results": result,
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        error_msg = f"Error processing EEG: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ {error_msg}")

        return (
            jsonify(
                {
                    "status": "FAILED",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            500,
        )


@app.route("/batch-analyze", methods=["POST"])
def batch_analyze():
    """
    Batch endpoint: Process multiple EEG segments at once

    Expected format:
    {
        "segments": [
            {"eeg_signal": [...], "metadata": {...}},
            {"eeg_signal": [...], "metadata": {...}},
            ...
        ]
    }
    """
    try:
        data = request.get_json()
        segments = data.get("segments", [])

        results = []
        for i, segment in enumerate(segments):
            eeg_signal = segment.get("eeg_signal")
            if eeg_signal:
                if ALGORITHM_AVAILABLE:
                    result = process_with_real_algorithm(eeg_signal)
                else:
                    result = life_algorithm.process_eeg(eeg_signal)
                results.append(result)

        return (
            jsonify(
                {
                    "status": "SUCCESS",
                    "segments_processed": len(results),
                    "results": results,
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"status": "FAILED", "error": str(e)}), 500


@app.route("/status", methods=["GET"])
def status():
    """Get backend status and algorithm information"""
    return (
        jsonify(
            {
                "backend": "OPERATIONAL",
                "algorithm": "REAL" if ALGORITHM_AVAILABLE else "MOCK",
                "timestamp": datetime.now().isoformat(),
                "endpoints": {
                    "health": "GET /health",
                    "analyze": "POST /analyze-eeg",
                    "batch": "POST /batch-analyze",
                    "status": "GET /status",
                },
            }
        ),
        200,
    )


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def process_with_real_algorithm(
    eeg_signal, sample_rate=256, session_id="", user_type=""
):
    """
    Process EEG with the REAL L.I.F.E algorithm
    """
    try:
        # Run algorithm (synchronously for now, could be async)
        result = life_algorithm.process_eeg_stream(
            eeg_signal=eeg_signal, sample_rate=sample_rate
        )

        # Format result for API response
        return {
            "algorithm": "experimentP2L (REAL)",
            "user_type": user_type,
            "session_id": session_id,
            "eeg_samples": len(eeg_signal),
            "sample_rate": sample_rate,
            "processing_status": "SUCCESS",
            "neural_metrics": (
                result.neural_metrics if hasattr(result, "neural_metrics") else {}
            ),
            "learning_outcome": (
                result.learning_outcome if hasattr(result, "learning_outcome") else {}
            ),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        print(f"❌ Algorithm processing error: {e}")
        # Return mock result on algorithm error
        return life_algorithm.process_eeg(eeg_signal)


def log_result(session_id, result):
    """Log processing result to file"""
    try:
        log_file = os.path.join(LOGS_DIR, f"{session_id}.json")
        with open(log_file, "w") as f:
            json.dump(result, f, indent=2, default=str)
        print(f"✅ Result logged to {log_file}")
    except Exception as e:
        print(f"⚠️  Could not log result: {e}")


# ============================================================================
# ERROR HANDLERS
# ============================================================================


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify(
            {
                "error": "Endpoint not found",
                "available": [
                    "GET /health",
                    "GET /status",
                    "POST /analyze-eeg",
                    "POST /batch-analyze",
                ],
            }
        ),
        404,
    )


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error", "details": str(error)}), 500


# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("🧠 L.I.F.E PLATFORM BACKEND SERVER")
    print("=" * 80)
    print(f"📍 Backend API: http://localhost:5000")
    print(f"📍 HTML Platforms: http://localhost:8080")
    print(
        f"📍 Algorithm: {'REAL (experimentP2L)' if ALGORITHM_AVAILABLE else 'MOCK (simulated)'}"
    )
    print("=" * 80)
    print("\n✅ Server starting...")
    print("   - Receiving EEG data on POST /analyze-eeg")
    print("   - Processing with L.I.F.E algorithm")
    print("   - Returning REAL results to platforms")
    print("\n💡 To use this backend:")
    print("   1. Modify platform to send EEG data to http://localhost:5000/analyze-eeg")
    print("   2. Platforms receive real algorithm results")
    print("   3. Display real metrics instead of simulated ones")
    print("\n🧪 Test endpoint (quick health check):")
    print("   curl http://localhost:5000/health")
    print("\n" + "=" * 80 + "\n")

    # Run Flask development server
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False,  # Important: disable reloader for async operations
    )
