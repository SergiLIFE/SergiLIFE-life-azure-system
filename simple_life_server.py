"""
Simple L.I.F.E Platform Server - Minimal Flask Server
"""

try:
    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.route("/")
    def home():
        return jsonify(
            {
                "platform": "L.I.F.E (Learning Individually from Experience)",
                "status": "Local Development Server Running",
                "message": "Welcome to L.I.F.E Platform - Local Mode",
                "endpoints": ["/api/health", "/api/health_simple"],
            }
        )

    @app.route("/api/health")
    def health():
        return jsonify(
            {
                "status": "healthy",
                "app": "L.I.F.E Platform",
                "mode": "local_development",
                "message": "Health endpoint working locally",
            }
        )

    @app.route("/api/health_simple")
    def health_simple():
        return jsonify(
            {
                "status": "healthy",
                "app": "L.I.F.E Platform",
                "endpoint": "health_simple",
                "message": "Simple health check working locally",
            }
        )

    if __name__ == "__main__":
        print("=" * 50)
        print("🧠 L.I.F.E PLATFORM - STARTING LOCAL SERVER")
        print("=" * 50)
        print("Server will be available at: http://127.0.0.1:5000")
        print("Health endpoints:")
        print("  • http://127.0.0.1:5000/api/health")
        print("  • http://127.0.0.1:5000/api/health_simple")
        print("Press Ctrl+C to stop the server")
        print("=" * 50)

        app.run(host="127.0.0.1", port=5000, debug=True)

except ImportError:
    print("❌ Flask not installed!")
    print("Installing Flask...")
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    print("✅ Flask installed! Please run the script again.")
