import asyncio
import json
import logging
import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import the test script
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import azure.functions as func


async def run_physionet_test():
    """Run the PhysioNet test in the cloud"""
    try:
        # Import the test module
        from real_eeg_physionet_test import RealEEGDataTester

        # Create tester instance
        tester = RealEEGDataTester()

        # Run comprehensive test
        logging.info("Starting PhysioNet test in Azure Functions")
        report = await tester.run_comprehensive_test_suite()

        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "report": report
        }

    except Exception as e:
        logging.error(f"Test failed: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function entry point"""
    logging.info('PhysioNet test function triggered')

    try:
        # Run the test asynchronously
        result = asyncio.run(run_physionet_test())

        # Return the result
        return func.HttpResponse(
            json.dumps(result, indent=2),
            mimetype="application/json",
            status_code=200 if result["status"] == "success" else 500
        )

    except Exception as e:
        logging.error(f"Function error: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }),
            mimetype="application/json",
            status_code=500
        )        )