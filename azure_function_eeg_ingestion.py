"""
Azure Function for External EEG Data Ingestion
Integrates with L.I.F.E Platform nocturnal optimization cycle
Provides REST API for frontend dashboard integration
"""

import asyncio
import json
import logging
from datetime import datetime

import azure.functions as func

from external_eeg_ingestion_engine import (ExternalEEGIngestionEngine,
                                           main_ingestion_handler)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="IngestExternalEEG")
@app.route(route="ingest-external-eeg", methods=["POST"])
async def ingest_external_eeg_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function endpoint for external EEG data ingestion
    Supports both one-time and scheduled ingestion cycles
    """
    try:
        # Parse request parameters
        request_body = {}
        if req.get_body():
            try:
                request_body = req.get_json() or {}
            except ValueError:
                pass
        
        mode = request_body.get('mode', 'full_cycle')
        notify_progress = request_body.get('notify_progress', False)
        
        logger.info(f"Starting external EEG ingestion - Mode: {mode}, Progress notifications: {notify_progress}")
        
        # Initialize ingestion engine
        ingestion_engine = ExternalEEGIngestionEngine()
        
        if notify_progress:
            # Stream progress updates for real-time dashboard
            return await stream_ingestion_progress(ingestion_engine, req)
        else:
            # Standard batch processing
            results = await ingestion_engine.run_full_ingestion_cycle()
            
            return func.HttpResponse(
                body=json.dumps({
                    "status": "success",
                    "message": f"Successfully processed {results['datasets_processed']} datasets",
                    "results": results,
                    "timestamp": datetime.utcnow().isoformat()
                }),
                mimetype="application/json",
                status_code=200
            )
            
    except Exception as e:
        logger.error(f"External EEG ingestion failed: {e}", exc_info=True)
        return func.HttpResponse(
            body=json.dumps({
                "status": "error",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }),
            mimetype="application/json",
            status_code=500
        )

async def stream_ingestion_progress(ingestion_engine, req):
    """
    Stream real-time progress updates to frontend dashboard
    Uses Server-Sent Events for live updates
    """
    
    async def progress_generator():
        """Generator for streaming progress updates"""
        try:
            # Start ingestion with progress callbacks
            results = {"datasets_processed": 0, "total_records": 0}
            
            # Send initial status
            yield json.dumps({
                "type": "cycle_start",
                "message": "Starting external EEG ingestion cycle",
                "timestamp": datetime.utcnow().isoformat()
            }) + "\n"
            
            # Process each dataset with progress updates
            for i, dataset in enumerate(ingestion_engine.datasets):
                # Dataset start notification
                yield json.dumps({
                    "type": "dataset_start", 
                    "dataset_name": dataset.name,
                    "dataset_type": dataset.dataset_type,
                    "progress_percentage": int((i / len(ingestion_engine.datasets)) * 100)
                }) + "\n"
                
                try:
                    # Simulate dataset processing with progress
                    dataset_start = datetime.utcnow()
                    
                    # Fetch dataset
                    if dataset.dataset_type == 'physionet':
                        eeg_data = await ingestion_engine.fetch_physionet_dataset(dataset)
                    else:
                        eeg_data = await ingestion_engine.fetch_openneuro_dataset(dataset)
                    
                    if eeg_data is not None:
                        # Process data
                        metrics = await ingestion_engine.process_external_eeg_data(eeg_data, dataset)
                        
                        # Store results
                        storage_success = await ingestion_engine.store_ingested_data(metrics, dataset)
                        
                        # Calculate processing stats
                        processing_time = (datetime.utcnow() - dataset_start).total_seconds()
                        records_processed = eeg_data.shape[1] if len(eeg_data.shape) > 1 else len(eeg_data)
                        
                        results["datasets_processed"] += 1
                        results["total_records"] += records_processed
                        
                        # Send success update
                        yield json.dumps({
                            "type": "dataset_complete",
                            "dataset_name": dataset.name,
                            "records": records_processed,
                            "latency": round(metrics.processing_latency, 2),
                            "processing_time": round(processing_time, 2),
                            "storage_success": storage_success,
                            "learning_efficiency": round(metrics.learning_efficiency, 3)
                        }) + "\n"
                        
                    else:
                        # Send error update
                        yield json.dumps({
                            "type": "dataset_error",
                            "dataset_name": dataset.name,
                            "error": "Failed to fetch dataset"
                        }) + "\n"
                        
                except Exception as e:
                    # Send error update
                    yield json.dumps({
                        "type": "dataset_error",
                        "dataset_name": dataset.name,
                        "error": str(e)
                    }) + "\n"
                
                # Progress update
                progress = int(((i + 1) / len(ingestion_engine.datasets)) * 100)
                yield json.dumps({
                    "type": "dataset_progress",
                    "progress_percentage": progress
                }) + "\n"
            
            # Send final summary
            yield json.dumps({
                "type": "cycle_complete",
                "summary": f"Processed {results['datasets_processed']} datasets, {results['total_records']} total records",
                "stats": ingestion_engine.ingestion_stats,
                "results": results
            }) + "\n"
            
        except Exception as e:
            yield json.dumps({
                "type": "error",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }) + "\n"
    
    # Create response with streaming content
    return func.HttpResponse(
        body=progress_generator(),
        mimetype="application/x-ndjson",  # Newline-delimited JSON
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        status_code=200
    )

@app.function_name(name="GetIngestionStats")
@app.route(route="ingestion-stats", methods=["GET"])
async def get_ingestion_stats(req: func.HttpRequest) -> func.HttpResponse:
    """
    Get current ingestion statistics for dashboard display
    """
    try:
        # Initialize engine to access stats
        ingestion_engine = ExternalEEGIngestionEngine()
        
        return func.HttpResponse(
            body=json.dumps({
                "status": "success",
                "stats": ingestion_engine.ingestion_stats,
                "timestamp": datetime.utcnow().isoformat()
            }),
            mimetype="application/json",
            status_code=200
        )
        
    except Exception as e:
        logger.error(f"Failed to get ingestion stats: {e}")
        return func.HttpResponse(
            body=json.dumps({
                "status": "error",
                "message": str(e)
            }),
            mimetype="application/json", 
            status_code=500
        )

@app.function_name(name="ScheduledIngestion")
@app.schedule(schedule="0 0 2 * * *", arg_name="mytimer", run_on_startup=False)
async def scheduled_external_ingestion(mytimer: func.TimerRequest) -> None:
    """
    Scheduled function for nocturnal EEG data ingestion
    Runs daily at 2:00 AM UTC during off-peak hours
    """
    try:
        logger.info("Starting scheduled external EEG ingestion cycle")
        
        # Run ingestion cycle
        results = await main_ingestion_handler(None)
        
        if results['status'] == 'success':
            logger.info(f"Scheduled ingestion completed successfully: {results['message']}")
        else:
            logger.error(f"Scheduled ingestion failed: {results['message']}")
            
    except Exception as e:
        logger.error(f"Scheduled ingestion error: {e}", exc_info=True)

@app.function_name(name="ValidateIngestionPipeline") 
@app.route(route="validate-ingestion", methods=["GET"])
async def validate_ingestion_pipeline(req: func.HttpRequest) -> func.HttpResponse:
    """
    Validation endpoint to test ingestion pipeline accuracy and latency
    Used by testing suites to verify external data processing
    """
    try:
        validation_start = datetime.utcnow()
        
        # Initialize ingestion engine
        ingestion_engine = ExternalEEGIngestionEngine()
        
        # Run lightweight validation cycle (single dataset)
        test_dataset = ingestion_engine.datasets[0]  # Use first dataset for validation
        
        # Test dataset fetching
        if test_dataset.dataset_type == 'physionet':
            eeg_data = await ingestion_engine.fetch_physionet_dataset(test_dataset)
        else:
            eeg_data = await ingestion_engine.fetch_openneuro_dataset(test_dataset)
        
        if eeg_data is None:
            raise Exception("Failed to fetch validation dataset")
        
        # Test processing pipeline
        metrics = await ingestion_engine.process_external_eeg_data(eeg_data, test_dataset)
        
        # Test storage (without actually storing)
        # storage_test = await ingestion_engine.store_ingested_data(metrics, test_dataset)
        
        validation_time = (datetime.utcnow() - validation_start).total_seconds()
        
        validation_results = {
            "pipeline_status": "PASS",
            "dataset_fetch": "SUCCESS",
            "neural_processing": "SUCCESS", 
            "processing_latency_ms": round(metrics.processing_latency, 2),
            "validation_time_s": round(validation_time, 2),
            "records_processed": eeg_data.shape[1] if len(eeg_data.shape) > 1 else len(eeg_data),
            "learning_efficiency": round(metrics.learning_efficiency, 3),
            "neural_state": metrics.neural_state.value,
            "timestamp": validation_start.isoformat()
        }
        
        # Validation criteria
        assert metrics.processing_latency < 1000, f"Processing too slow: {metrics.processing_latency}ms"
        assert metrics.learning_efficiency > 0.5, f"Learning efficiency too low: {metrics.learning_efficiency}"
        assert validation_time < 60, f"Validation too slow: {validation_time}s"
        
        return func.HttpResponse(
            body=json.dumps({
                "status": "success",
                "validation": validation_results,
                "message": "Ingestion pipeline validation passed"
            }),
            mimetype="application/json",
            status_code=200
        )
        
    except Exception as e:
        logger.error(f"Ingestion validation failed: {e}")
        return func.HttpResponse(
            body=json.dumps({
                "status": "error",
                "validation": {
                    "pipeline_status": "FAIL",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                },
                "message": f"Validation failed: {e}"
            }),
            mimetype="application/json",
            status_code=500
        )                "message": f"Validation failed: {e}"
            }),
            mimetype="application/json",
            status_code=500
        )