import json
import logging
from datetime import datetime, timezone

import azure.functions as func

app = func.FunctionApp()


@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"])
async def health_check(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(
            {"status": "healthy", "platform": "L.I.F.E Platform", "version": "2.0.0"}
        ),
        mimetype="application/json",
    )


@app.route(route="eeg/process", auth_level=func.AuthLevel.FUNCTION, methods=["POST"])
async def eeg_processor(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"status": "success", "message": "EEG processor ready"}),
        mimetype="application/json",
    )
