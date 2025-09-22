"""
L.I.F.E. Platform - Autonomous SOTA KPI Demo
Copyright 2025 - Sergio Paya Borrull

Demonstration of autonomous SOTA (State-of-the-Art) KPI monitoring system
for the L.I.F.E. Platform neuroadaptive learning system.

This demo showcases real-time performance monitoring, KPI tracking,
and autonomous optimization triggers for the L.I.F.E. Platform.
"""

import asyncio
import json
import logging
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import List


@dataclass
class KPIMetrics:
    """KPI metrics data structure"""

    timestamp: datetime
    performance_score: float
    accuracy: float
    latency_ms: float
    memory_usage_mb: float
    cpu_usage_percent: float
    throughput_events_per_sec: float


@dataclass
class SOTABenchmark:
    """SOTA benchmark data structure"""

    model_name: str
    benchmark_score: float
    benchmark_date: datetime
    dataset: str
    improvement_percentage: float


class AutonomousSOTAKPIDemo:
    """Demonstration of autonomous SOTA KPI monitoring system"""

    def __init__(self):
        self.kpi_history: List[KPIMetrics] = []
        self.sota_benchmarks: List[SOTABenchmark] = []
        self.monitoring_active = False
        self.kpi_thresholds = {
            "performance_score": 0.85,
            "accuracy": 0.82,
            "latency_ms": 500.0,
            "memory_usage_mb": 1024.0,
            "cpu_usage_percent": 80.0,
            "throughput_events_per_sec": 100.0,
        }

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

        # Initialize demo data
        self._initialize_demo_data()

    def _initialize_demo_data(self):
        """Initialize demo KPI data and SOTA benchmarks"""
        # Initialize SOTA benchmarks
        self.sota_benchmarks = [
            SOTABenchmark(
                model_name="LIFE-v1.0",
                benchmark_score=0.78,
                benchmark_date=datetime.now() - timedelta(days=30),
                dataset="BCI Competition IV-2a",
                improvement_percentage=0.0,
            ),
            SOTABenchmark(
                model_name="LIFE-v1.1",
                benchmark_score=0.81,
                benchmark_date=datetime.now() - timedelta(days=15),
                dataset="BCI Competition IV-2a",
                improvement_percentage=3.85,
            ),
            SOTABenchmark(
                model_name="LIFE-v1.2",
                benchmark_score=0.83,
                benchmark_date=datetime.now() - timedelta(days=7),
                dataset="BCI Competition IV-2a",
                improvement_percentage=2.47,
            ),
        ]

        # Generate initial KPI history
        base_time = datetime.now() - timedelta(hours=24)
        for i in range(24):
            timestamp = base_time + timedelta(hours=i)
            # Simulate realistic KPI values with some variation
            performance = 0.82 + (i * 0.005) + (0.02 * (i % 3 - 1))
            accuracy = 0.79 + (i * 0.003) + (0.015 * (i % 4 - 2))
            latency = 450 + (i * 5) + (20 * (i % 2))
            memory = 850 + (i * 10) + (50 * (i % 3))
            cpu = 65 + (i * 2) + (10 * (i % 5))
            throughput = 95 + (i * 3) + (15 * (i % 4))

            kpi = KPIMetrics(
                timestamp=timestamp,
                performance_score=min(performance, 0.95),
                accuracy=min(accuracy, 0.88),
                latency_ms=min(latency, 600),
                memory_usage_mb=min(memory, 1200),
                cpu_usage_percent=min(cpu, 90),
                throughput_events_per_sec=min(throughput, 150),
            )
            self.kpi_history.append(kpi)

    async def _simulate_real_time_kpi(self) -> KPIMetrics:
        """Simulate real-time KPI generation"""
        # Add some realistic variation to current KPIs
        last_kpi = self.kpi_history[-1] if self.kpi_history else None

        if last_kpi:
            # Simulate gradual improvement with noise
            performance = last_kpi.performance_score + (
                0.001 * (1 if time.time() % 2 > 1 else -1)
            )
            accuracy = last_kpi.accuracy + (
                0.0005 * (1 if time.time() % 3 > 1.5 else -1)
            )
            latency = last_kpi.latency_ms + (2 * (1 if time.time() % 4 > 2 else -1))
            memory = last_kpi.memory_usage_mb + (
                5 * (1 if time.time() % 5 > 2.5 else -1)
            )
            cpu = last_kpi.cpu_usage_percent + (1 * (1 if time.time() % 6 > 3 else -1))
            throughput = last_kpi.throughput_events_per_sec + (
                2 * (1 if time.time() % 7 > 3.5 else -1)
            )
        else:
            # Default values if no history
            performance = 0.84
            accuracy = 0.81
            latency = 480
            memory = 920
            cpu = 72
            throughput = 110

        # Ensure values stay within reasonable bounds
        kpi = KPIMetrics(
            timestamp=datetime.now(),
            performance_score=max(0.75, min(performance, 0.95)),
            accuracy=max(0.70, min(accuracy, 0.90)),
            latency_ms=max(300, min(latency, 800)),
            memory_usage_mb=max(500, min(memory, 1500)),
            cpu_usage_percent=max(30, min(cpu, 95)),
            throughput_events_per_sec=max(50, min(throughput, 200)),
        )

        self.kpi_history.append(kpi)
        return kpi

    def _check_kpi_thresholds(self, kpi: KPIMetrics) -> List[str]:
        """Check if KPI values are below thresholds"""
        alerts = []

        if kpi.performance_score < self.kpi_thresholds["performance_score"]:
            alerts.append(".2f")

        if kpi.accuracy < self.kpi_thresholds["accuracy"]:
            alerts.append(".2f")

        if kpi.latency_ms > self.kpi_thresholds["latency_ms"]:
            alerts.append(".1f")

        if kpi.memory_usage_mb > self.kpi_thresholds["memory_usage_mb"]:
            alerts.append(".1f")

        if kpi.cpu_usage_percent > self.kpi_thresholds["cpu_usage_percent"]:
            alerts.append(".1f")

        if (
            kpi.throughput_events_per_sec
            < self.kpi_thresholds["throughput_events_per_sec"]
        ):
            alerts.append(".1f")

        return alerts

    def _calculate_sota_improvement(self, current_kpi: KPIMetrics) -> float:
        """Calculate improvement over last SOTA benchmark"""
        if not self.sota_benchmarks:
            return 0.0

        last_sota = max(self.sota_benchmarks, key=lambda x: x.benchmark_date)
        improvement = (
            (current_kpi.performance_score - last_sota.benchmark_score)
            / last_sota.benchmark_score
        ) * 100
        return improvement

    async def _autonomous_optimization_trigger(self, alerts: List[str]) -> bool:
        """Determine if autonomous optimization should be triggered"""
        if len(alerts) >= 2:  # Trigger if 2+ KPIs are outside thresholds
            self.logger.info(
                "🚨 Autonomous optimization triggered due to multiple KPI alerts"
            )
            return True

        # Check for critical single KPI issues
        critical_alerts = [
            alert for alert in alerts if "latency" in alert or "memory" in alert
        ]
        if critical_alerts:
            self.logger.info(
                "🚨 Autonomous optimization triggered due to critical KPI alert"
            )
            return True

        return False

    async def run_kpi_monitoring_demo(self, duration_minutes: int = 5):
        """Run the KPI monitoring demonstration"""
        print("🧠 L.I.F.E. Platform - Autonomous SOTA KPI Demo")
        print("=" * 60)
        print(f"Monitoring KPIs for {duration_minutes} minutes...")
        print()

        self.monitoring_active = True
        start_time = datetime.now()
        monitoring_end = start_time + timedelta(minutes=duration_minutes)

        print("📊 Initial KPI Thresholds:")
        for key, value in self.kpi_thresholds.items():
            print(f"  {key}: {value:.2f}")
        print()

        print("🎯 SOTA Benchmarks:")
        for benchmark in self.sota_benchmarks[-3:]:  # Show last 3
            print(
                f"  {benchmark.model_name}: {benchmark.benchmark_score:.3f} "
                f"({benchmark.improvement_percentage:+.2f}%) - {benchmark.dataset}"
            )
        print()

        optimization_triggers = 0

        try:
            while datetime.now() < monitoring_end and self.monitoring_active:
                # Generate new KPI data
                current_kpi = await self._simulate_real_time_kpi()

                # Check thresholds
                alerts = self._check_kpi_thresholds(current_kpi)

                # Calculate SOTA improvement
                sota_improvement = self._calculate_sota_improvement(current_kpi)

                # Display current status
                print(
                    f"📈 {current_kpi.timestamp.strftime('%H:%M:%S')} - "
                    f"Perf: {current_kpi.performance_score:.3f} | "
                    f"Acc: {current_kpi.accuracy:.3f} | "
                    f"Lat: {current_kpi.latency_ms:.1f}ms | "
                    f"SOTA Δ: {sota_improvement:+.2f}%"
                )

                if alerts:
                    print(f"   ⚠️  Alerts: {', '.join(alerts)}")

                    # Check for autonomous optimization trigger
                    if await self._autonomous_optimization_trigger(alerts):
                        optimization_triggers += 1
                        print("   🤖 AUTONOMOUS OPTIMIZATION TRIGGERED!")
                        # Simulate optimization (brief pause)
                        await asyncio.sleep(0.5)

                # Brief pause between readings
                await asyncio.sleep(2)

        except KeyboardInterrupt:
            self.logger.info("Demo interrupted by user")
        finally:
            self.monitoring_active = False

        # Final summary
        print()
        print("📋 Demo Summary:")
        print(
            f"   Duration: {(datetime.now() - start_time).total_seconds() / 60:.1f} minutes"
        )
        print(f"   KPI Readings: {len(self.kpi_history)}")
        print(f"   Optimization Triggers: {optimization_triggers}")
        print(
            f"   Final SOTA Improvement: {self._calculate_sota_improvement(self.kpi_history[-1]):+.2f}%"
        )

        # Export results
        await self._export_demo_results()

    async def _export_demo_results(self):
        """Export demo results to JSON file"""
        results = {
            "demo_metadata": {
                "timestamp": datetime.now().isoformat(),
                "platform": "L.I.F.E. v2025.1.0",
                "demo_type": "Autonomous SOTA KPI Monitoring",
            },
            "kpi_history": [
                asdict(kpi) for kpi in self.kpi_history[-50:]
            ],  # Last 50 readings
            "sota_benchmarks": [
                asdict(benchmark) for benchmark in self.sota_benchmarks
            ],
            "thresholds": self.kpi_thresholds,
            "final_metrics": {
                "total_readings": len(self.kpi_history),
                "current_performance": (
                    self.kpi_history[-1].performance_score if self.kpi_history else 0
                ),
                "current_accuracy": (
                    self.kpi_history[-1].accuracy if self.kpi_history else 0
                ),
                "sota_improvement": (
                    self._calculate_sota_improvement(self.kpi_history[-1])
                    if self.kpi_history
                    else 0
                ),
            },
        }

        filename = f"demo_kpi_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(results, f, indent=2, default=str)

        self.logger.info(f"Demo results exported to {filename}")
        print(f"💾 Results exported to {filename}")

    def stop_monitoring(self):
        """Stop the KPI monitoring"""
        self.monitoring_active = False
        self.logger.info("KPI monitoring stopped")


async def main():
    """Main demo function"""
    print("🧠 L.I.F.E. Platform - Autonomous SOTA KPI Monitoring Demo")
    print("Copyright 2025 - Sergio Paya Borrull")
    print()

    demo = AutonomousSOTAKPIDemo()

    try:
        # Run demo for 3 minutes (can be adjusted)
        await demo.run_kpi_monitoring_demo(duration_minutes=3)
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    finally:
        demo.stop_monitoring()


if __name__ == "__main__":
    asyncio.run(main())
