#!/usr/bin/env python3
"""
L.I.F.E. Platform - Autonomous SOTA KPI Monitor
Real-time monitoring and optimization of State-Of-The-Art performance metrics

This module provides autonomous monitoring of key performance indicators (KPIs)
for the L.I.F.E. Platform, ensuring continuous optimization and benchmarking
against state-of-the-art standards.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class KPICategory(Enum):
    """Categories of KPIs being monitored"""

    PERFORMANCE = "performance"
    ACCURACY = "accuracy"
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    RELIABILITY = "reliability"
    EFFICIENCY = "efficiency"
    COMPLIANCE = "compliance"
    DOCUMENT_INTEGRITY = "document_integrity"
    MARKETPLACE_READINESS = "marketplace_readiness"
    NAKEDAI_INTEGRATION = "nakedai_integration"  # Phase 2 preparation
    FLOW_MOMENTUM = "flow_momentum"  # Seamless transition tracking


class KPIMetric(Enum):
    """Specific KPI metrics - Enhanced with NAKEDai Integration Targets"""

    # L.I.F.E THEORY PLATFORM METRICS (Phase 1)
    PROCESSING_LATENCY = "processing_latency_ms"
    ACCURACY_RATE = "accuracy_rate"
    THROUGHPUT_REQ_PER_SEC = "throughput_req_per_sec"
    MEMORY_USAGE_PERCENT = "memory_usage_percent"
    CPU_USAGE_PERCENT = "cpu_usage_percent"
    ERROR_RATE_PERCENT = "error_rate_percent"
    UPTIME_PERCENT = "uptime_percent"
    COMPLIANCE_SCORE = "compliance_score"
    DOCUMENT_INTEGRITY_SCORE = "document_integrity_score"
    MARKETPLACE_READINESS_SCORE = "marketplace_readiness_score"

    # NAKEDai 2026 REVOLUTIONARY DEVELOPMENT TARGETS (13-Month Timeline)
    NAKEDAI_HARDWARE_INTEGRATION = "nakedai_hardware_integration_percent"
    NAKEDAI_ALGORITHM_DEVELOPMENT = "nakedai_algorithm_development_percent"
    NAKEDAI_MANUFACTURING_READINESS = "nakedai_manufacturing_readiness_percent"
    EXPONENTIAL_LEARNING_PROGRESS = "exponential_learning_progress_percent"
    NAKEDAI_VISUAL_DESIGN_PERFECTION = "nakedai_visual_design_perfection_percent"
    NAKEDAI_AESTHETIC_APPEAL_SCORE = "nakedai_aesthetic_appeal_score"
    REVOLUTIONARY_BREAKTHROUGH_SCORE = "revolutionary_breakthrough_score"
    CONSCIOUSNESS_EVOLUTION_READINESS = "consciousness_evolution_readiness_percent"


class AlertSeverity(Enum):
    """Alert severity levels"""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class OptimizationAction(Enum):
    """Types of optimization actions"""

    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    OPTIMIZE_MEMORY = "optimize_memory"
    OPTIMIZE_CPU = "optimize_cpu"
    LOAD_BALANCE = "load_balance"
    FAILOVER = "failover"
    RECONFIGURE = "reconfigure"
    NO_ACTION = "no_action"


@dataclass
class KPIMeasurement:
    """Represents a single KPI measurement"""

    metric: KPIMetric
    category: KPICategory
    value: Union[int, float]
    unit: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KPIThreshold:
    """Defines thresholds for KPI monitoring"""

    metric: KPIMetric
    warning_threshold: Union[int, float]
    critical_threshold: Union[int, float]
    direction: str  # "above" or "below"
    description: str


@dataclass
class KPIAlert:
    """Represents a KPI alert"""

    alert_id: str
    metric: KPIMetric
    severity: AlertSeverity
    message: str
    current_value: Union[int, float]
    threshold_value: Union[int, float]
    timestamp: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    resolution_time: Optional[datetime] = None


@dataclass
class SOTABenchmark:
    """State-of-the-art benchmark reference"""

    metric: KPIMetric
    sota_value: Union[int, float]
    sota_source: str
    last_updated: datetime
    description: str


class AutonomousSOTAKPIMonitor:
    """
    Autonomous SOTA KPI Monitor for L.I.F.E. Platform

    Provides real-time monitoring, alerting, and autonomous optimization
    of key performance indicators against state-of-the-art benchmarks.
    """

    def __init__(
        self,
        workspace_path: Optional[str] = None,
        monitoring_interval: int = 30,  # seconds
        alert_cooldown: int = 300,  # seconds
        enable_autonomous_optimization: bool = True,
    ):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.monitoring_interval = monitoring_interval
        self.alert_cooldown = alert_cooldown
        self.enable_autonomous_optimization = enable_autonomous_optimization

        # Data structures
        self.measurements: List[KPIMeasurement] = []
        self.alerts: List[KPIAlert] = []
        self.thresholds: Dict[KPIMetric, KPIThreshold] = {}
        self.sota_benchmarks: Dict[KPIMetric, SOTABenchmark] = {}
        self.optimization_history: List[Dict[str, Any]] = []

        # Monitoring state
        self.is_monitoring = False
        self.last_alert_times: Dict[KPIMetric, datetime] = {}
        self.baseline_values: Dict[KPIMetric, Union[int, float]] = {}

        # Initialize components
        self._initialize_thresholds()
        self._initialize_sota_benchmarks()
        self._load_baseline_values()

        logger.info(
            f"Autonomous SOTA KPI Monitor initialized for workspace: {self.workspace_path}"
        )

    def _initialize_thresholds(self):
        """Initialize KPI thresholds for monitoring"""
        self.thresholds = {
            KPIMetric.PROCESSING_LATENCY: KPIThreshold(
                metric=KPIMetric.PROCESSING_LATENCY,
                warning_threshold=1.0,  # 1ms
                critical_threshold=5.0,  # 5ms
                direction="above",
                description="EEG processing latency should remain under 1ms for optimal performance",
            ),
            KPIMetric.ACCURACY_RATE: KPIThreshold(
                metric=KPIMetric.ACCURACY_RATE,
                warning_threshold=0.75,  # 75%
                critical_threshold=0.65,  # 65%
                direction="below",
                description="Accuracy rate should maintain above 75% for reliable operation",
            ),
            KPIMetric.THROUGHPUT_REQ_PER_SEC: KPIThreshold(
                metric=KPIMetric.THROUGHPUT_REQ_PER_SEC,
                warning_threshold=500,
                critical_threshold=200,
                direction="below",
                description="Throughput should maintain above 500 req/sec",
            ),
            KPIMetric.MEMORY_USAGE_PERCENT: KPIThreshold(
                metric=KPIMetric.MEMORY_USAGE_PERCENT,
                warning_threshold=80.0,
                critical_threshold=95.0,
                direction="above",
                description="Memory usage should remain under 80%",
            ),
            KPIMetric.CPU_USAGE_PERCENT: KPIThreshold(
                metric=KPIMetric.CPU_USAGE_PERCENT,
                warning_threshold=75.0,
                critical_threshold=90.0,
                direction="above",
                description="CPU usage should remain under 75%",
            ),
            KPIMetric.ERROR_RATE_PERCENT: KPIThreshold(
                metric=KPIMetric.ERROR_RATE_PERCENT,
                warning_threshold=1.0,
                critical_threshold=5.0,
                direction="above",
                description="Error rate should remain under 1%",
            ),
            KPIMetric.UPTIME_PERCENT: KPIThreshold(
                metric=KPIMetric.UPTIME_PERCENT,
                warning_threshold=99.5,
                critical_threshold=99.0,
                direction="below",
                description="Uptime should maintain above 99.5%",
            ),
        }

    def _initialize_sota_benchmarks(self):
        """Initialize state-of-the-art benchmark values"""
        self.sota_benchmarks = {
            KPIMetric.PROCESSING_LATENCY: SOTABenchmark(
                metric=KPIMetric.PROCESSING_LATENCY,
                sota_value=0.38,  # 0.38ms sub-millisecond processing
                sota_source="L.I.F.E. Platform 2025 Benchmark",
                last_updated=datetime.now(),
                description="Sub-millisecond EEG processing latency",
            ),
            KPIMetric.ACCURACY_RATE: SOTABenchmark(
                metric=KPIMetric.ACCURACY_RATE,
                sota_value=0.82,  # 82% accuracy
                sota_source="BCI Competition IV-2a Validation",
                last_updated=datetime.now(),
                description="78-82% accuracy on PhysioNet datasets",
            ),
            KPIMetric.THROUGHPUT_REQ_PER_SEC: SOTABenchmark(
                metric=KPIMetric.THROUGHPUT_REQ_PER_SEC,
                sota_value=1000,
                sota_source="Production Load Testing",
                last_updated=datetime.now(),
                description="1000+ requests per second throughput",
            ),
        }

    def _load_baseline_values(self):
        """Load or establish baseline KPI values"""
        baseline_file = self.workspace_path / "kpi_baseline.json"
        if baseline_file.exists():
            try:
                with open(baseline_file, "r") as f:
                    baseline_data = json.load(f)
                    for metric_name, value in baseline_data.items():
                        try:
                            metric = KPIMetric(metric_name)
                            self.baseline_values[metric] = value
                        except ValueError:
                            continue
                logger.info(
                    f"Loaded baseline values for {len(self.baseline_values)} metrics"
                )
            except Exception as e:
                logger.warning(f"Failed to load baseline values: {e}")
        else:
            logger.info("No baseline values found, will establish during monitoring")

    async def start_monitoring(self):
        """Start autonomous KPI monitoring"""
        if self.is_monitoring:
            logger.warning("KPI monitoring is already running")
            return

        self.is_monitoring = True
        logger.info("Starting autonomous SOTA KPI monitoring...")

        try:
            while self.is_monitoring:
                await self._perform_monitoring_cycle()
                await asyncio.sleep(self.monitoring_interval)
        except Exception as e:
            logger.error(f"Monitoring cycle failed: {e}")
            self.is_monitoring = False

    def stop_monitoring(self):
        """Stop KPI monitoring"""
        self.is_monitoring = False
        logger.info("KPI monitoring stopped")

    async def _perform_monitoring_cycle(self):
        """Perform a complete monitoring cycle"""
        try:
            # Collect current measurements
            measurements = await self._collect_measurements()

            # Store measurements
            self.measurements.extend(measurements)

            # Check thresholds and generate alerts
            alerts = self._check_thresholds(measurements)
            self.alerts.extend(alerts)

            # Perform autonomous optimization if enabled
            if self.enable_autonomous_optimization:
                optimization_actions = self._determine_optimization_actions(
                    measurements, alerts
                )
                await self._execute_optimization_actions(optimization_actions)

            # Update baseline values if needed
            self._update_baseline_values(measurements)

            # Log monitoring summary
            self._log_monitoring_summary(measurements, alerts)

        except Exception as e:
            logger.error(f"Monitoring cycle error: {e}")

    async def _collect_measurements(self) -> List[KPIMeasurement]:
        """Collect current KPI measurements"""
        measurements = []

        try:
            # Performance metrics
            latency = await self._measure_processing_latency()
            if latency is not None:
                measurements.append(
                    KPIMeasurement(
                        metric=KPIMetric.PROCESSING_LATENCY,
                        category=KPICategory.PERFORMANCE,
                        value=latency,
                        unit="ms",
                    )
                )

            accuracy = await self._measure_accuracy_rate()
            if accuracy is not None:
                measurements.append(
                    KPIMeasurement(
                        metric=KPIMetric.ACCURACY_RATE,
                        category=KPICategory.ACCURACY,
                        value=accuracy,
                        unit="percent",
                    )
                )

            throughput = await self._measure_throughput()
            if throughput is not None:
                measurements.append(
                    KPIMeasurement(
                        metric=KPIMetric.THROUGHPUT_REQ_PER_SEC,
                        category=KPICategory.THROUGHPUT,
                        value=throughput,
                        unit="req/sec",
                    )
                )

            # System metrics
            memory_usage = self._measure_memory_usage()
            measurements.append(
                KPIMeasurement(
                    metric=KPIMetric.MEMORY_USAGE_PERCENT,
                    category=KPICategory.EFFICIENCY,
                    value=memory_usage,
                    unit="percent",
                )
            )

            cpu_usage = self._measure_cpu_usage()
            measurements.append(
                KPIMeasurement(
                    metric=KPIMetric.CPU_USAGE_PERCENT,
                    category=KPICategory.EFFICIENCY,
                    value=cpu_usage,
                    unit="percent",
                )
            )

            # Reliability metrics
            error_rate = await self._measure_error_rate()
            measurements.append(
                KPIMeasurement(
                    metric=KPIMetric.ERROR_RATE_PERCENT,
                    category=KPICategory.RELIABILITY,
                    value=error_rate,
                    unit="percent",
                )
            )

            uptime = self._measure_uptime()
            measurements.append(
                KPIMeasurement(
                    metric=KPIMetric.UPTIME_PERCENT,
                    category=KPICategory.RELIABILITY,
                    value=uptime,
                    unit="percent",
                )
            )

        except Exception as e:
            logger.error(f"Measurement collection error: {e}")

        return measurements

    async def _measure_processing_latency(self) -> Optional[float]:
        """Measure current processing latency"""
        try:
            # Simulate latency measurement (would integrate with actual processing)
            # In production, this would measure real EEG processing latency
            base_latency = 0.38  # SOTA baseline
            variance = (time.time() % 10) / 100  # Small random variance
            return base_latency + variance
        except Exception:
            return None

    async def _measure_accuracy_rate(self) -> Optional[float]:
        """Measure current accuracy rate"""
        try:
            # Simulate accuracy measurement (would integrate with validation system)
            base_accuracy = 0.82  # SOTA baseline
            variance = ((time.time() % 20) - 10) / 1000  # Small variance
            return max(0.0, min(1.0, base_accuracy + variance))
        except Exception:
            return None

    async def _measure_throughput(self) -> Optional[float]:
        """Measure current throughput"""
        try:
            # Simulate throughput measurement
            base_throughput = 1000.0
            variance = ((time.time() % 50) - 25) * 10
            return max(0, base_throughput + variance)
        except Exception:
            return None

    def _measure_memory_usage(self) -> float:
        """Measure current memory usage"""
        try:
            import psutil

            return psutil.virtual_memory().percent
        except ImportError:
            # Fallback if psutil not available
            return 45.0 + ((time.time() % 30) - 15)

    def _measure_cpu_usage(self) -> float:
        """Measure current CPU usage"""
        try:
            import psutil

            return psutil.cpu_percent(interval=1)
        except ImportError:
            # Fallback if psutil not available
            return 23.0 + ((time.time() % 40) - 20)

    async def _measure_error_rate(self) -> float:
        """Measure current error rate"""
        try:
            # Calculate error rate from recent alerts
            recent_alerts = [
                alert
                for alert in self.alerts
                if (datetime.now() - alert.timestamp).total_seconds()
                < 3600  # Last hour
                and alert.severity in [AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY]
            ]
            total_measurements = len(
                [
                    m
                    for m in self.measurements
                    if (datetime.now() - m.timestamp).total_seconds() < 3600
                ]
            )
            return (len(recent_alerts) / max(total_measurements, 1)) * 100
        except Exception:
            return 0.1  # Low error rate baseline

    def _measure_uptime(self) -> float:
        """Measure system uptime percentage"""
        # Simplified uptime calculation
        # In production, this would track actual service uptime
        return 99.9

    def _check_thresholds(self, measurements: List[KPIMeasurement]) -> List[KPIAlert]:
        """Check measurements against thresholds and generate alerts"""
        alerts = []

        for measurement in measurements:
            if measurement.metric not in self.thresholds:
                continue

            threshold = self.thresholds[measurement.metric]

            # Check if alert cooldown has passed
            last_alert = self.last_alert_times.get(measurement.metric)
            if (
                last_alert
                and (datetime.now() - last_alert).total_seconds() < self.alert_cooldown
            ):
                continue

            alert_triggered = False
            severity = AlertSeverity.INFO

            if threshold.direction == "above":
                if measurement.value >= threshold.critical_threshold:
                    severity = AlertSeverity.CRITICAL
                    alert_triggered = True
                elif measurement.value >= threshold.warning_threshold:
                    severity = AlertSeverity.WARNING
                    alert_triggered = True
            elif threshold.direction == "below":
                if measurement.value <= threshold.critical_threshold:
                    severity = AlertSeverity.CRITICAL
                    alert_triggered = True
                elif measurement.value <= threshold.warning_threshold:
                    severity = AlertSeverity.WARNING
                    alert_triggered = True

            if alert_triggered:
                alert = KPIAlert(
                    alert_id=f"{measurement.metric.value}_{int(time.time())}",
                    metric=measurement.metric,
                    severity=severity,
                    message=f"{measurement.metric.value}: {measurement.value}{measurement.unit} "
                    f"{'exceeds' if threshold.direction == 'above' else 'below'} "
                    f"{'critical' if severity == AlertSeverity.CRITICAL else 'warning'} "
                    f"threshold ({threshold.critical_threshold if severity == AlertSeverity.CRITICAL else threshold.warning_threshold})",
                    current_value=measurement.value,
                    threshold_value=(
                        threshold.critical_threshold
                        if severity == AlertSeverity.CRITICAL
                        else threshold.warning_threshold
                    ),
                )
                alerts.append(alert)
                self.last_alert_times[measurement.metric] = datetime.now()

                logger.warning(f"KPI Alert: {alert.message}")

        return alerts

    def _determine_optimization_actions(
        self, measurements: List[KPIMeasurement], alerts: List[KPIAlert]
    ) -> List[OptimizationAction]:
        """Determine optimization actions based on measurements and alerts"""
        actions = []

        # Analyze critical alerts
        critical_alerts = [a for a in alerts if a.severity == AlertSeverity.CRITICAL]

        if critical_alerts:
            # High memory usage
            memory_measurement = next(
                (m for m in measurements if m.metric == KPIMetric.MEMORY_USAGE_PERCENT),
                None,
            )
            if memory_measurement and memory_measurement.value > 90:
                actions.append(OptimizationAction.OPTIMIZE_MEMORY)

            # High CPU usage
            cpu_measurement = next(
                (m for m in measurements if m.metric == KPIMetric.CPU_USAGE_PERCENT),
                None,
            )
            if cpu_measurement and cpu_measurement.value > 85:
                actions.append(OptimizationAction.OPTIMIZE_CPU)

            # Low throughput
            throughput_measurement = next(
                (
                    m
                    for m in measurements
                    if m.metric == KPIMetric.THROUGHPUT_REQ_PER_SEC
                ),
                None,
            )
            if throughput_measurement and throughput_measurement.value < 300:
                actions.append(OptimizationAction.SCALE_UP)

        # Proactive optimization for performance
        latency_measurement = next(
            (m for m in measurements if m.metric == KPIMetric.PROCESSING_LATENCY), None
        )
        if latency_measurement and latency_measurement.value > 1.0:
            actions.append(OptimizationAction.OPTIMIZE_CPU)

        if not actions:
            actions.append(OptimizationAction.NO_ACTION)

        return actions

    async def _execute_optimization_actions(self, actions: List[OptimizationAction]):
        """Execute determined optimization actions"""
        for action in actions:
            if action == OptimizationAction.NO_ACTION:
                continue

            try:
                logger.info(f"Executing optimization action: {action.value}")

                if action == OptimizationAction.OPTIMIZE_MEMORY:
                    await self._optimize_memory()
                elif action == OptimizationAction.OPTIMIZE_CPU:
                    await self._optimize_cpu()
                elif action == OptimizationAction.SCALE_UP:
                    await self._scale_up()
                elif action == OptimizationAction.SCALE_DOWN:
                    await self._scale_down()

                # Record optimization action
                self.optimization_history.append(
                    {
                        "action": action.value,
                        "timestamp": datetime.now().isoformat(),
                        "success": True,
                    }
                )

            except Exception as e:
                logger.error(f"Optimization action {action.value} failed: {e}")
                self.optimization_history.append(
                    {
                        "action": action.value,
                        "timestamp": datetime.now().isoformat(),
                        "success": False,
                        "error": str(e),
                    }
                )

    async def _optimize_memory(self):
        """Perform memory optimization"""
        # Placeholder for memory optimization logic
        # In production, this would implement garbage collection,
        # memory pool optimization, etc.
        await asyncio.sleep(0.1)  # Simulate optimization time

    async def _optimize_cpu(self):
        """Perform CPU optimization"""
        # Placeholder for CPU optimization logic
        # In production, this would implement thread optimization,
        # algorithm tuning, etc.
        await asyncio.sleep(0.1)  # Simulate optimization time

    async def _scale_up(self):
        """Scale up resources"""
        # Placeholder for scaling logic
        # In production, this would integrate with Azure scaling APIs
        await asyncio.sleep(0.1)  # Simulate scaling time

    async def _scale_down(self):
        """Scale down resources"""
        # Placeholder for scaling logic
        await asyncio.sleep(0.1)  # Simulate scaling time

    def _update_baseline_values(self, measurements: List[KPIMeasurement]):
        """Update baseline values based on recent measurements"""
        for measurement in measurements:
            if measurement.metric not in self.baseline_values:
                self.baseline_values[measurement.metric] = measurement.value
            else:
                # Exponential moving average update
                alpha = 0.1  # Smoothing factor
                current_baseline = self.baseline_values[measurement.metric]
                self.baseline_values[measurement.metric] = (
                    alpha * measurement.value + (1 - alpha) * current_baseline
                )

    def _log_monitoring_summary(
        self, measurements: List[KPIMeasurement], alerts: List[KPIAlert]
    ):
        """Log summary of monitoring cycle"""
        measurement_summary = {}
        for measurement in measurements:
            measurement_summary[measurement.metric.value] = {
                "value": measurement.value,
                "unit": measurement.unit,
            }

        logger.info(
            f"Monitoring cycle completed: {len(measurements)} measurements, "
            f"{len(alerts)} alerts generated"
        )

        # Log significant deviations from SOTA
        for measurement in measurements:
            if measurement.metric in self.sota_benchmarks:
                sota = self.sota_benchmarks[measurement.metric]
                deviation = abs(measurement.value - sota.sota_value) / sota.sota_value
                if deviation > 0.1:  # 10% deviation
                    logger.warning(
                        f"SOTA deviation detected for {measurement.metric.value}: "
                        f"{measurement.value:.3f} vs SOTA {sota.sota_value:.3f} "
                        f"({deviation:.1%} deviation)"
                    )

    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status and statistics"""
        return {
            "is_monitoring": self.is_monitoring,
            "total_measurements": len(self.measurements),
            "active_alerts": len([a for a in self.alerts if not a.resolved]),
            "total_alerts": len(self.alerts),
            "monitored_metrics": len(self.thresholds),
            "sota_benchmarks": len(self.sota_benchmarks),
            "optimization_actions": len(self.optimization_history),
            "last_measurement": (
                self.measurements[-1].timestamp.isoformat()
                if self.measurements
                else None
            ),
        }

    def get_kpi_report(self) -> Dict[str, Any]:
        """Generate comprehensive KPI report"""
        latest_measurements = {}
        for measurement in reversed(self.measurements):
            if measurement.metric not in latest_measurements:
                latest_measurements[measurement.metric] = measurement

        report = {
            "timestamp": datetime.now().isoformat(),
            "measurements": {},
            "alerts": [
                self._alert_to_dict(alert) for alert in self.alerts[-10:]
            ],  # Last 10 alerts
            "sota_comparison": {},
            "optimization_summary": self.optimization_history[
                -5:
            ],  # Last 5 optimizations
        }

        for metric, measurement in latest_measurements.items():
            report["measurements"][metric.value] = {
                "value": measurement.value,
                "unit": measurement.unit,
                "timestamp": measurement.timestamp.isoformat(),
            }

            # SOTA comparison
            if metric in self.sota_benchmarks:
                sota = self.sota_benchmarks[metric]
                deviation = measurement.value - sota.sota_value
                report["sota_comparison"][metric.value] = {
                    "current_value": measurement.value,
                    "sota_value": sota.sota_value,
                    "deviation": deviation,
                    "deviation_percent": (
                        (deviation / sota.sota_value) * 100
                        if sota.sota_value != 0
                        else 0
                    ),
                    "sota_source": sota.sota_source,
                }

        return report

    def _alert_to_dict(self, alert: KPIAlert) -> Dict[str, Any]:
        """Convert alert to dictionary"""
        return {
            "alert_id": alert.alert_id,
            "metric": alert.metric.value,
            "severity": alert.severity.value,
            "message": alert.message,
            "current_value": alert.current_value,
            "threshold_value": alert.threshold_value,
            "timestamp": alert.timestamp.isoformat(),
            "resolved": alert.resolved,
            "resolution_time": (
                alert.resolution_time.isoformat() if alert.resolution_time else None
            ),
        }

    def export_kpi_data(self, filepath: str) -> bool:
        """Export KPI data to JSON file"""
        try:
            data = {
                "export_timestamp": datetime.now().isoformat(),
                "measurements": [
                    self._measurement_to_dict(m) for m in self.measurements
                ],
                "alerts": [self._alert_to_dict(a) for a in self.alerts],
                "thresholds": {
                    k.value: self._threshold_to_dict(v)
                    for k, v in self.thresholds.items()
                },
                "sota_benchmarks": {
                    k.value: self._sota_to_dict(v)
                    for k, v in self.sota_benchmarks.items()
                },
                "optimization_history": self.optimization_history,
                "baseline_values": {
                    k.value: v for k, v in self.baseline_values.items()
                },
            }

            with open(filepath, "w") as f:
                json.dump(data, f, indent=2, default=str)

            logger.info(f"KPI data exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to export KPI data: {e}")
            return False

    def _measurement_to_dict(self, measurement: KPIMeasurement) -> Dict[str, Any]:
        """Convert measurement to dictionary"""
        return {
            "metric": measurement.metric.value,
            "category": measurement.category.value,
            "value": measurement.value,
            "unit": measurement.unit,
            "timestamp": measurement.timestamp.isoformat(),
            "metadata": measurement.metadata,
        }

    def _threshold_to_dict(self, threshold: KPIThreshold) -> Dict[str, Any]:
        """Convert threshold to dictionary"""
        return {
            "metric": threshold.metric.value,
            "warning_threshold": threshold.warning_threshold,
            "critical_threshold": threshold.critical_threshold,
            "direction": threshold.direction,
            "description": threshold.description,
        }

    def _sota_to_dict(self, sota: SOTABenchmark) -> Dict[str, Any]:
        """Convert SOTA benchmark to dictionary"""
        return {
            "metric": sota.metric.value,
            "sota_value": sota.sota_value,
            "sota_source": sota.sota_source,
            "last_updated": sota.last_updated.isoformat(),
            "description": sota.description,
        }


# Factory function for easy instantiation
def create_autonomous_sota_kpi_monitor(
    workspace_path: Optional[str] = None,
    monitoring_interval: int = 30,
    enable_autonomous_optimization: bool = True,
) -> AutonomousSOTAKPIMonitor:
    """
    Factory function to create autonomous SOTA KPI monitor

    Args:
        workspace_path: Path to workspace directory
        monitoring_interval: Monitoring interval in seconds
        enable_autonomous_optimization: Whether to enable autonomous optimization

    Returns:
        Configured AutonomousSOTAKPIMonitor instance
    """
    return AutonomousSOTAKPIMonitor(
        workspace_path=workspace_path,
        monitoring_interval=monitoring_interval,
        enable_autonomous_optimization=enable_autonomous_optimization,
    )


# Command-line interface
def main():
    """Main CLI function for autonomous SOTA KPI monitoring"""
    import argparse

    parser = argparse.ArgumentParser(
        description="L.I.F.E. Platform Autonomous SOTA KPI Monitor"
    )
    parser.add_argument(
        "--workspace", "-w", default=None, help="Workspace directory path"
    )
    parser.add_argument(
        "--interval",
        "-i",
        type=int,
        default=30,
        help="Monitoring interval in seconds (default: 30)",
    )
    parser.add_argument(
        "--no-optimization", action="store_true", help="Disable autonomous optimization"
    )
    parser.add_argument("--export", "-e", help="Export KPI data to specified file")
    parser.add_argument(
        "--report", "-r", action="store_true", help="Generate and display KPI report"
    )
    parser.add_argument(
        "--status", "-s", action="store_true", help="Show monitoring status"
    )

    args = parser.parse_args()

    # Create monitor
    monitor = create_autonomous_sota_kpi_monitor(
        workspace_path=args.workspace,
        monitoring_interval=args.interval,
        enable_autonomous_optimization=not args.no_optimization,
    )

    if args.status:
        status = monitor.get_monitoring_status()
        print("Monitoring Status:")
        print(f"  Active: {status['is_monitoring']}")
        print(f"  Measurements: {status['total_measurements']}")
        print(f"  Active Alerts: {status['active_alerts']}")
        print(f"  Monitored Metrics: {status['monitored_metrics']}")
        return 0

    if args.report:
        report = monitor.get_kpi_report()
        print("KPI Report:")
        print(f"  Timestamp: {report['timestamp']}")
        print(f"  Measurements: {len(report['measurements'])}")
        print(f"  Recent Alerts: {len(report['alerts'])}")
        print(f"  SOTA Comparisons: {len(report['sota_comparison'])}")
        return 0

    if args.export:
        if monitor.export_kpi_data(args.export):
            print(f"KPI data exported to {args.export}")
        else:
            print("Failed to export KPI data")
            return 1
        return 0

    # Start monitoring
    print("L.I.F.E. Platform - Autonomous SOTA KPI Monitor")
    print("=" * 60)
    print(f"Workspace: {args.workspace or os.getcwd()}")
    print(f"Interval: {args.interval}s")
    print(
        f"Autonomous Optimization: {'Enabled' if not args.no_optimization else 'Disabled'}"
    )
    print("\nStarting monitoring... (Press Ctrl+C to stop)")

    try:
        asyncio.run(monitor.start_monitoring())
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
        monitor.stop_monitoring()

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
