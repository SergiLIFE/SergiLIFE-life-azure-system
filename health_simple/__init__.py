import json
import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Health check endpoint called")

    try:
        health_data = {
            "status": "healthy",
            "platform": "L.I.F.E. Platform",
            "version": "1.0.0",
            "message": "Function App is running successfully",
        }

        return func.HttpResponse(
            json.dumps(health_data, indent=2),
            status_code=200,
            mimetype="application/json",
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"status": "error", "message": str(e)}),
            status_code=500,
            mimetype="application/json",
        )
