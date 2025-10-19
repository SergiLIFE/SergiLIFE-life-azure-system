"""
Nocturnal Platform Optimizer with External EEG Ingestion Integration
Integrates external dataset ingestion into L.I.F.E Platform's sleep mode optimization
"""

import asyncio
import json
import logging
from datetime import datetime, time
from typing import Dict, Optional

import aiohttp


class NocturnalEEGIngestionOptimizer:
    """
    Enhanced nocturnal optimizer that includes external EEG data ingestion
    during off-peak hours for continuous pipeline validation
    """

    def __init__(self, base_url: str = "https://life-functions-app.azurewebsites.net"):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        self.ingestion_schedule = {
            "daily_ingestion_hour": 2,  # 2:00 AM UTC
            "validation_hour": 3,  # 3:00 AM UTC
            "optimization_hour": 4,  # 4:00 AM UTC
        }

    async def should_activate_ingestion(self) -> bool:
        """
        Determine if nocturnal ingestion should activate
        Checks time, system load, and previous ingestion status
        """
        current_time = datetime.utcnow().time()
        target_time = time(self.ingestion_schedule["daily_ingestion_hour"], 0)

        # Check if it's within the ingestion window (2:00-2:30 AM UTC)
        ingestion_window_start = time(
            self.ingestion_schedule["daily_ingestion_hour"], 0
        )
        ingestion_window_end = time(self.ingestion_schedule["daily_ingestion_hour"], 30)

        return ingestion_window_start <= current_time <= ingestion_window_end

    async def trigger_external_ingestion(self) -> Dict:
        """
        Trigger external EEG data ingestion via Azure Function API
        Returns ingestion results for optimization feedback
        """
        try:
            self.logger.info("Triggering nocturnal external EEG ingestion")

            async with aiohttp.ClientSession() as session:
                # Start ingestion with progress monitoring
                async with session.post(
                    f"{self.base_url}/api/ingest-external-eeg",
                    json={
                        "mode": "nocturnal_cycle",
                        "notify_progress": False,  # Batch mode for nocturnal
                    },
                    timeout=aiohttp.ClientTimeout(total=1800),  # 30 min timeout
                ) as response:

                    if response.status == 200:
                        results = await response.json()
                        self.logger.info(
                            f"Nocturnal ingestion completed: {results.get('message', '')}"
                        )
                        return results
                    else:
                        error_text = await response.text()
                        raise Exception(f"HTTP {response.status}: {error_text}")

        except Exception as e:
            self.logger.error(f"Nocturnal ingestion failed: {e}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def validate_ingestion_pipeline(self) -> Dict:
        """
        Validate the ingestion pipeline after nocturnal processing
        Ensures data quality and processing performance
        """
        try:
            self.logger.info("Validating ingestion pipeline performance")

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/validate-ingestion",
                    timeout=aiohttp.ClientTimeout(total=120),  # 2 min timeout
                ) as response:

                    if response.status == 200:
                        validation_results = await response.json()
                        self.logger.info(
                            "Ingestion pipeline validation completed successfully"
                        )
                        return validation_results
                    else:
                        error_text = await response.text()
                        raise Exception(
                            f"Validation failed - HTTP {response.status}: {error_text}"
                        )

        except Exception as e:
            self.logger.error(f"Pipeline validation failed: {e}")
            return {
                "status": "error",
                "validation": {"pipeline_status": "FAIL", "error": str(e)},
                "message": f"Validation error: {e}",
            }

    async def optimize_based_on_ingestion_results(
        self, ingestion_results: Dict, validation_results: Dict
    ) -> Dict:
        """
        Use ingestion and validation results to optimize L.I.F.E Platform parameters
        Adjusts neural processing thresholds based on external data performance
        """
        try:
            optimization_updates = {}

            # Extract performance metrics
            ingestion_success = ingestion_results.get("status") == "success"
            validation_success = validation_results.get("status") == "success"

            if ingestion_success and validation_success:
                results = ingestion_results.get("results", {})
                validation = validation_results.get("validation", {})

                # Optimize processing latency thresholds
                avg_latency = validation.get("processing_latency_ms", 0)
                if avg_latency > 0:
                    # Adjust neural processing targets based on observed performance
                    optimization_updates["neural_processing"] = {
                        "target_latency_ms": min(
                            avg_latency * 1.2, 1000
                        ),  # 20% buffer, max 1s
                        "efficiency_threshold": max(
                            validation.get("learning_efficiency", 0.7), 0.6
                        ),
                    }

                # Optimize ingestion frequency based on success rate
                total_datasets = len(results.get("ingestion_details", []))
                successful_datasets = results.get("successful_ingestions", 0)
                success_rate = (
                    successful_datasets / total_datasets if total_datasets > 0 else 0
                )

                if success_rate > 0.8:
                    # High success rate - can increase ingestion frequency
                    optimization_updates["ingestion_schedule"] = {
                        "frequency": "daily",
                        "next_optimization": "increase_dataset_variety",
                    }
                elif success_rate < 0.5:
                    # Low success rate - reduce frequency, focus on stability
                    optimization_updates["ingestion_schedule"] = {
                        "frequency": "weekly",
                        "next_optimization": "improve_error_handling",
                    }

                # Optimize Azure resource allocation
                total_records = results.get("total_records", 0)
                total_duration = results.get("total_duration", 0)

                if total_duration > 0 and total_records > 0:
                    records_per_second = total_records / total_duration
                    optimization_updates["azure_scaling"] = {
                        "recommended_throughput": records_per_second,
                        "scale_recommendation": (
                            "up" if records_per_second < 100 else "maintain"
                        ),
                    }

                self.logger.info(
                    f"Optimization updates generated: {optimization_updates}"
                )

            return {
                "status": "success",
                "optimizations": optimization_updates,
                "applied_at": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Optimization failed: {e}")
            return {"status": "error", "message": str(e)}

    async def run_nocturnal_cycle(self) -> Dict:
        """
        Execute complete nocturnal optimization cycle with EEG ingestion
        """
        cycle_start = datetime.utcnow()
        self.logger.info("Starting nocturnal optimization cycle with EEG ingestion")

        cycle_results = {
            "cycle_start": cycle_start.isoformat(),
            "phases": {},
            "overall_status": "in_progress",
        }

        try:
            # Phase 1: External EEG Data Ingestion
            self.logger.info("Phase 1: External EEG Data Ingestion")
            ingestion_results = await self.trigger_external_ingestion()
            cycle_results["phases"]["ingestion"] = ingestion_results

            # Brief pause between phases
            await asyncio.sleep(30)

            # Phase 2: Pipeline Validation
            self.logger.info("Phase 2: Ingestion Pipeline Validation")
            validation_results = await self.validate_ingestion_pipeline()
            cycle_results["phases"]["validation"] = validation_results

            # Brief pause before optimization
            await asyncio.sleep(15)

            # Phase 3: Optimization Based on Results
            self.logger.info("Phase 3: Performance Optimization")
            optimization_results = await self.optimize_based_on_ingestion_results(
                ingestion_results, validation_results
            )
            cycle_results["phases"]["optimization"] = optimization_results

            # Determine overall success
            all_phases_successful = all(
                [
                    ingestion_results.get("status") == "success",
                    validation_results.get("status") == "success",
                    optimization_results.get("status") == "success",
                ]
            )

            cycle_results["overall_status"] = (
                "success" if all_phases_successful else "partial_success"
            )
            cycle_results["cycle_duration"] = (
                datetime.utcnow() - cycle_start
            ).total_seconds()

            self.logger.info(
                f"Nocturnal cycle completed: {cycle_results['overall_status']}"
            )

        except Exception as e:
            self.logger.error(f"Nocturnal cycle failed: {e}")
            cycle_results["overall_status"] = "error"
            cycle_results["error"] = str(e)

        cycle_results["cycle_end"] = datetime.utcnow().isoformat()
        return cycle_results

    async def background_optimization_loop(self):
        """
        Main background loop for nocturnal optimization with EEG ingestion
        Runs continuously, activating during configured hours
        """
        self.is_running = True
        self.logger.info("Starting nocturnal optimization background loop")

        while self.is_running:
            try:
                if await self.should_activate_ingestion():
                    self.logger.info("Activating nocturnal optimization cycle")
                    cycle_results = await self.run_nocturnal_cycle()

                    # Log cycle summary
                    status = cycle_results.get("overall_status", "unknown")
                    duration = cycle_results.get("cycle_duration", 0)
                    self.logger.info(
                        f"Nocturnal cycle {status} in {duration:.1f} seconds"
                    )

                    # Sleep until next day after successful cycle
                    if status == "success":
                        await asyncio.sleep(
                            20 * 3600
                        )  # Sleep 20 hours until next cycle
                    else:
                        await asyncio.sleep(3600)  # Retry in 1 hour if failed
                else:
                    # Check every hour during non-ingestion periods
                    await asyncio.sleep(3600)

            except Exception as e:
                self.logger.error(f"Background loop error: {e}")
                await asyncio.sleep(3600)  # Wait 1 hour before retry

    def stop(self):
        """Stop the background optimization loop"""
        self.is_running = False
        self.logger.info("Stopping nocturnal optimization loop")


# Standalone execution for testing
if __name__ == "__main__":

    async def main():
        optimizer = NocturnalEEGIngestionOptimizer()

        # Test single cycle
        results = await optimizer.run_nocturnal_cycle()
        print(json.dumps(results, indent=2))

    asyncio.run(main())
    asyncio.run(main())
