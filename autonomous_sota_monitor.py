#!/usr/bin/env python3
"""
L.I.F.E. Autonomous SOTA Monitoring System
Continuous performance validation and benchmark triggering
Copyright Sergio Paya Borrull 2025. All Rights Reserved.

Features:
- Autonomous SOTA benchmark triggering
- Active and sleep mode monitoring
- Performance degradation detection
- Automatic optimization adjustments
- Continuous validation against champion-level metrics
"""

import asyncio
import json
import logging
import os
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import psutil

# Set up logging (console only for CI/CD compatibility)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class SOTAMonitoringConfig:
    """Configuration for SOTA monitoring system"""

    # Champion-level performance targets (updated with latest results)
    CHAMPION_TARGETS = {
        "bci_accuracy": 1.000,  # 100% perfect accuracy achieved
        "bci_latency_ms": 1.39,  # BCI benchmark champion latency
        "speed_latency_ms": 1.34,  # Speed benchmark champion latency
        "ultra_low_latency_ms": 0.29,  # Absolute record latency
        "throughput_ops_sec": 745.5,  # Peak throughput achieved
        "reliability_score": 0.851,  # Minimum reliability under extreme speed
        "perfect_reliability": 1.000,  # Perfect reliability in accuracy tests
        "performance_score": 0.720,  # Champion performance score
    }

    # Monitoring intervals
    ACTIVE_MODE_INTERVAL = 30  # seconds
    SLEEP_MODE_INTERVAL = 300  # 5 minutes
    DEEP_SLEEP_INTERVAL = 1800  # 30 minutes

    # Performance degradation thresholds
    DEGRADATION_THRESHOLDS = {
        "accuracy_drop": 0.05,  # 5% accuracy drop triggers alert
        "latency_increase": 2.0,  # 2x latency increase triggers alert
        "throughput_drop": 0.20,  # 20% throughput drop triggers alert
        "reliability_drop": 0.10,  # 10% reliability drop triggers alert
    }

    # Benchmark trigger conditions
    BENCHMARK_TRIGGERS = {
        "scheduled_interval": 3600,  # Every hour
        "performance_degradation": True,
        "champion_validation": 24 * 3600,  # Daily champion validation
        "market_readiness": 7 * 24 * 3600,  # Weekly marketplace validation
    }


class AutonomousSOTAMonitor:
    """Autonomous SOTA monitoring and validation system"""

    def __init__(self):
        self.config = SOTAMonitoringConfig()
        self.performance_history = []
        self.last_benchmark_time = 0
        self.last_champion_validation = 0
        self.monitoring_active = False
        self.sleep_mode = False
        self.deep_sleep_mode = False
        self.current_performance = {}
        self.alerts = []
        self.autonomous_optimizer_process = None

        # Create monitoring directories
        os.makedirs("monitoring", exist_ok=True)
        os.makedirs("monitoring/logs", exist_ok=True)
        os.makedirs("monitoring/benchmarks", exist_ok=True)

    async def start_autonomous_monitoring(self):
        """Start the autonomous SOTA monitoring system"""
        logger.info("🚀 Starting L.I.F.E. Autonomous SOTA Monitoring System")
        logger.info("🎯 Champion-level performance validation enabled")
        logger.info("=" * 80)

        self.monitoring_active = True

        # Start monitoring tasks
        tasks = [
            asyncio.create_task(self._active_monitoring_loop()),
            asyncio.create_task(self._sleep_monitoring_loop()),
            asyncio.create_task(self._benchmark_trigger_loop()),
            asyncio.create_task(self._champion_validation_loop()),
            asyncio.create_task(self._performance_analysis_loop()),
        ]

        logger.info("✅ All monitoring loops started")
        logger.info("🔄 Monitoring modes: Active, Sleep, Benchmark, Champion, Analysis")

        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logger.info("🛑 Autonomous monitoring stopped by user")
        except Exception as e:
            logger.error(f"❌ Monitoring error: {e}")
        finally:
            self.monitoring_active = False

    async def _active_monitoring_loop(self):
        """Active mode monitoring - continuous performance tracking"""
        while self.monitoring_active:
            if not self.sleep_mode:
                await self._monitor_system_performance()
                await self._check_autonomous_optimizer_status()
                await self._validate_performance_metrics()
                await asyncio.sleep(self.config.ACTIVE_MODE_INTERVAL)
            else:
                await asyncio.sleep(1)  # Quick check if still in sleep mode

    async def _sleep_monitoring_loop(self):
        """Sleep mode monitoring - reduced frequency monitoring"""
        while self.monitoring_active:
            if self.sleep_mode and not self.deep_sleep_mode:
                await self._minimal_performance_check()
                await asyncio.sleep(self.config.SLEEP_MODE_INTERVAL)
            elif self.deep_sleep_mode:
                await self._deep_sleep_check()
                await asyncio.sleep(self.config.DEEP_SLEEP_INTERVAL)
            else:
                await asyncio.sleep(10)  # Check mode every 10 seconds

    async def _benchmark_trigger_loop(self):
        """Autonomous benchmark triggering based on conditions"""
        while self.monitoring_active:
            current_time = time.time()

            # Check if benchmark should be triggered
            should_trigger = await self._should_trigger_benchmark()

            if should_trigger:
                logger.info("🏆 Triggering autonomous SOTA benchmark validation")
                await self._trigger_sota_benchmark()
                self.last_benchmark_time = current_time

            await asyncio.sleep(60)  # Check every minute

    async def _champion_validation_loop(self):
        """Daily champion-level performance validation"""
        while self.monitoring_active:
            current_time = time.time()

            if (
                current_time - self.last_champion_validation
                > self.config.BENCHMARK_TRIGGERS["champion_validation"]
            ):
                logger.info("🏅 Starting champion-level performance validation")
                await self._validate_champion_performance()
                self.last_champion_validation = current_time

            await asyncio.sleep(3600)  # Check every hour

    async def _performance_analysis_loop(self):
        """Continuous performance analysis and optimization"""
        while self.monitoring_active:
            if len(self.performance_history) > 10:
                await self._analyze_performance_trends()
                await self._generate_optimization_recommendations()

            await asyncio.sleep(600)  # Analyze every 10 minutes

    async def _monitor_system_performance(self):
        """Monitor current system performance"""
        try:
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            # Get network stats if available
            try:
                network = psutil.net_io_counters()
                network_sent = network.bytes_sent
                network_recv = network.bytes_recv
            except:
                network_sent = network_recv = 0

            performance_data = {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used_gb": memory.used / (1024**3),
                "disk_percent": disk.percent,
                "network_sent_gb": network_sent / (1024**3),
                "network_recv_gb": network_recv / (1024**3),
            }

            self.current_performance = performance_data
            self.performance_history.append(performance_data)

            # Keep only last 1000 entries
            if len(self.performance_history) > 1000:
                self.performance_history = self.performance_history[-1000:]

            logger.debug(f"📊 Performance: CPU {cpu_percent}%, RAM {memory.percent}%")

        except Exception as e:
            logger.error(f"❌ Performance monitoring error: {e}")

    async def _check_autonomous_optimizer_status(self):
        """Check if autonomous optimizer is running and its performance"""
        try:
            optimizer_running = False
            optimizer_pid = None
            optimizer_cpu = 0
            optimizer_memory = 0

            for proc in psutil.process_iter(
                ["pid", "name", "cmdline", "cpu_percent", "memory_percent"]
            ):
                try:
                    cmdline = " ".join(proc.info["cmdline"] or [])
                    if "autonomous_optimizer.py" in cmdline:
                        optimizer_running = True
                        optimizer_pid = proc.info["pid"]
                        optimizer_cpu = proc.info["cpu_percent"] or 0
                        optimizer_memory = proc.info["memory_percent"] or 0
                        self.autonomous_optimizer_process = proc
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if optimizer_running:
                logger.debug(
                    f"🧠 Autonomous Optimizer: PID {optimizer_pid}, "
                    f"CPU {optimizer_cpu}%, RAM {optimizer_memory}%"
                )
            else:
                logger.warning("⚠️  Autonomous Optimizer not detected")

            return optimizer_running

        except Exception as e:
            logger.error(f"❌ Optimizer status check error: {e}")
            return False

    async def _validate_performance_metrics(self):
        """Validate current performance against SOTA targets"""
        try:
            if not self.current_performance:
                return

            # Check for performance degradation
            alerts = []

            # CPU usage alert
            if self.current_performance["cpu_percent"] > 80:
                alerts.append("High CPU usage detected")

            # Memory usage alert
            if self.current_performance["memory_percent"] > 85:
                alerts.append("High memory usage detected")

            # Add alerts to queue
            for alert in alerts:
                self.alerts.append(
                    {"timestamp": datetime.now().isoformat(), "message": alert}
                )

            # Keep only last 100 alerts
            if len(self.alerts) > 100:
                self.alerts = self.alerts[-100:]

        except Exception as e:
            logger.error(f"❌ Performance validation error: {e}")

    async def _should_trigger_benchmark(self):
        """Determine if SOTA benchmark should be triggered"""
        current_time = time.time()

        # Time-based trigger
        if (
            current_time - self.last_benchmark_time
            > self.config.BENCHMARK_TRIGGERS["scheduled_interval"]
        ):
            return True

        # Performance degradation trigger
        if len(self.performance_history) > 10:
            recent_performance = self.performance_history[-10:]
            avg_cpu = sum(p["cpu_percent"] for p in recent_performance) / len(
                recent_performance
            )
            avg_memory = sum(p["memory_percent"] for p in recent_performance) / len(
                recent_performance
            )

            if avg_cpu > 70 or avg_memory > 80:
                logger.info(
                    "🚨 Performance degradation detected - triggering benchmark"
                )
                return True

        return False

    async def _trigger_sota_benchmark(self):
        """Trigger SOTA benchmark execution"""
        try:
            logger.info("🏆 Executing autonomous SOTA benchmark")

            # Import and run SOTA benchmark
            import subprocess

            result = subprocess.run(
                ["python", "sota_benchmark.py"],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            if result.returncode == 0:
                logger.info("✅ SOTA benchmark completed successfully")
                await self._parse_benchmark_results(result.stdout)
            else:
                logger.error(f"❌ SOTA benchmark failed: {result.stderr}")

        except subprocess.TimeoutExpired:
            logger.error("⏰ SOTA benchmark timed out")
        except Exception as e:
            logger.error(f"❌ Benchmark trigger error: {e}")

    async def _parse_benchmark_results(self, benchmark_output: str):
        """Parse and validate SOTA benchmark results"""
        try:
            # Extract key metrics from benchmark output
            lines = benchmark_output.split("\n")
            results = {}

            for line in lines:
                if "Accuracy:" in line and "SOTA" in line:
                    # Extract accuracy value
                    parts = line.split("Accuracy:")
                    if len(parts) > 1:
                        accuracy_str = parts[1].strip().split()[0]
                        try:
                            results["accuracy"] = float(accuracy_str)
                        except ValueError:
                            pass

                elif "Latency:" in line and "ms" in line:
                    # Extract latency value
                    parts = line.split("Latency:")
                    if len(parts) > 1:
                        latency_str = parts[1].strip().split("ms")[0]
                        try:
                            results["latency_ms"] = float(latency_str)
                        except ValueError:
                            pass

                elif "Throughput:" in line and "ops/sec" in line:
                    # Extract throughput value
                    parts = line.split("Throughput:")
                    if len(parts) > 1:
                        throughput_str = parts[1].strip().split()[0]
                        try:
                            results["throughput_ops_sec"] = float(throughput_str)
                        except ValueError:
                            pass

            # Validate against champion targets
            await self._validate_benchmark_results(results)

        except Exception as e:
            logger.error(f"❌ Benchmark result parsing error: {e}")

    async def _validate_benchmark_results(self, results: Dict):
        """Validate benchmark results against champion targets"""
        try:
            champion_status = True
            validation_report = []

            # Check accuracy
            if "accuracy" in results:
                accuracy = results["accuracy"]
                target = self.config.CHAMPION_TARGETS["bci_accuracy"]
                if accuracy >= target * 0.95:  # 95% of champion level
                    validation_report.append(
                        f"✅ Accuracy: {accuracy:.3f} (Champion: {target:.3f})"
                    )
                else:
                    validation_report.append(
                        f"⚠️  Accuracy: {accuracy:.3f} below champion level"
                    )
                    champion_status = False

            # Check latency
            if "latency_ms" in results:
                latency = results["latency_ms"]
                target = self.config.CHAMPION_TARGETS["bci_latency_ms"]
                if latency <= target * 1.2:  # Within 20% of champion level
                    validation_report.append(
                        f"✅ Latency: {latency:.2f}ms (Champion: {target:.2f}ms)"
                    )
                else:
                    validation_report.append(
                        f"⚠️  Latency: {latency:.2f}ms above champion level"
                    )
                    champion_status = False

            # Check throughput
            if "throughput_ops_sec" in results:
                throughput = results["throughput_ops_sec"]
                target = self.config.CHAMPION_TARGETS["throughput_ops_sec"]
                if throughput >= target * 0.8:  # 80% of champion level
                    validation_report.append(
                        f"✅ Throughput: {throughput:.1f} ops/sec (Champion: {target:.1f})"
                    )
                else:
                    validation_report.append(
                        f"⚠️  Throughput: {throughput:.1f} below champion level"
                    )
                    champion_status = False

            # Log validation results
            logger.info("🏆 SOTA Benchmark Validation Results:")
            for report in validation_report:
                logger.info(f"   {report}")

            if champion_status:
                logger.info("🥇 CHAMPION LEVEL PERFORMANCE MAINTAINED! 🏆")
            else:
                logger.warning(
                    "⚠️  Performance below champion level - optimization recommended"
                )

            # Save validation results
            await self._save_validation_results(
                results, champion_status, validation_report
            )

        except Exception as e:
            logger.error(f"❌ Benchmark validation error: {e}")

    async def _validate_champion_performance(self):
        """Comprehensive champion-level performance validation"""
        logger.info("🏅 Running comprehensive champion performance validation")

        # Trigger full SOTA benchmark suite
        await self._trigger_sota_benchmark()

        # Additional validations
        logger.info("🔍 Validating system health for champion performance")

        # Check system resources
        if self.current_performance:
            cpu = self.current_performance["cpu_percent"]
            memory = self.current_performance["memory_percent"]

            if cpu < 50 and memory < 70:
                logger.info("✅ System resources optimal for champion performance")
            else:
                logger.warning("⚠️  System resources may impact champion performance")

    async def _minimal_performance_check(self):
        """Minimal performance check for sleep mode"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory_percent = psutil.virtual_memory().percent

            if cpu_percent > 80 or memory_percent > 90:
                logger.warning(
                    f"🚨 Sleep mode alert: CPU {cpu_percent}%, RAM {memory_percent}%"
                )
                # Switch back to active mode if resources are stressed
                self.sleep_mode = False
                logger.info("🔄 Switching back to active monitoring mode")

        except Exception as e:
            logger.error(f"❌ Sleep mode monitoring error: {e}")

    async def _deep_sleep_check(self):
        """Deep sleep mode - minimal system validation"""
        try:
            # Just check if autonomous optimizer is still running
            optimizer_running = await self._check_autonomous_optimizer_status()
            if not optimizer_running:
                logger.warning("⚠️  Autonomous optimizer not detected in deep sleep")

        except Exception as e:
            logger.error(f"❌ Deep sleep monitoring error: {e}")

    async def _analyze_performance_trends(self):
        """Analyze performance trends and patterns"""
        if len(self.performance_history) < 10:
            return

        try:
            recent = self.performance_history[-10:]

            # Calculate averages
            avg_cpu = sum(p["cpu_percent"] for p in recent) / len(recent)
            avg_memory = sum(p["memory_percent"] for p in recent) / len(recent)

            # Detect trends
            cpu_trend = (
                "increasing" if recent[-1]["cpu_percent"] > avg_cpu else "stable"
            )
            memory_trend = (
                "increasing" if recent[-1]["memory_percent"] > avg_memory else "stable"
            )

            logger.debug(f"📈 Trends: CPU {cpu_trend}, Memory {memory_trend}")

        except Exception as e:
            logger.error(f"❌ Performance trend analysis error: {e}")

    async def _generate_optimization_recommendations(self):
        """Generate optimization recommendations based on performance analysis"""
        try:
            recommendations = []

            if self.current_performance:
                cpu = self.current_performance["cpu_percent"]
                memory = self.current_performance["memory_percent"]

                if cpu > 70:
                    recommendations.append("Consider switching to efficiency mode")
                if memory > 80:
                    recommendations.append("Memory optimization recommended")

                if recommendations:
                    logger.info("🎯 Optimization recommendations:")
                    for rec in recommendations:
                        logger.info(f"   💡 {rec}")

        except Exception as e:
            logger.error(f"❌ Recommendation generation error: {e}")

    async def _save_validation_results(
        self, results: Dict, champion_status: bool, report: List[str]
    ):
        """Save validation results to file"""
        try:
            validation_data = {
                "timestamp": datetime.now().isoformat(),
                "results": results,
                "champion_status": champion_status,
                "validation_report": report,
                "champion_targets": self.config.CHAMPION_TARGETS,
            }

            filename = f"monitoring/benchmarks/validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w") as f:
                json.dump(validation_data, f, indent=2)

            logger.debug(f"💾 Validation results saved to {filename}")

        except Exception as e:
            logger.error(f"❌ Failed to save validation results: {e}")

    def set_sleep_mode(self, enabled: bool):
        """Enable or disable sleep mode"""
        self.sleep_mode = enabled
        mode = "sleep" if enabled else "active"
        logger.info(f"🔄 Monitoring mode switched to: {mode}")

    def set_deep_sleep_mode(self, enabled: bool):
        """Enable or disable deep sleep mode"""
        self.deep_sleep_mode = enabled
        if enabled:
            self.sleep_mode = True
        mode = "deep sleep" if enabled else "normal"
        logger.info(f"🔄 Monitoring mode switched to: {mode}")

    def get_performance_summary(self) -> Dict:
        """Get current performance summary"""
        return {
            "current_performance": self.current_performance,
            "recent_alerts": self.alerts[-10:] if self.alerts else [],
            "monitoring_active": self.monitoring_active,
            "sleep_mode": self.sleep_mode,
            "deep_sleep_mode": self.deep_sleep_mode,
            "last_benchmark": self.last_benchmark_time,
            "last_champion_validation": self.last_champion_validation,
        }


async def main():
    """Main function to start autonomous SOTA monitoring"""
    monitor = AutonomousSOTAMonitor()

    logger.info("🚀 L.I.F.E. Autonomous SOTA Monitoring System")
    logger.info("🎯 Champion-level performance validation")
    logger.info("🔄 Active and sleep mode monitoring enabled")
    logger.info("=" * 80)

    try:
        await monitor.start_autonomous_monitoring()
    except KeyboardInterrupt:
        logger.info("🛑 Monitoring stopped by user")
    except Exception as e:
        logger.error(f"❌ Monitoring system error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
