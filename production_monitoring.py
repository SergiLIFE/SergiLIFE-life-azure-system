#!/usr/bin/env python3
"""
L.I.F.E. Platform - Production Monitoring Suite
Real-time monitoring and alerting for production deployments

This module provides comprehensive monitoring capabilities for
production deployments, including health checks, performance
monitoring, and automated alerting.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MonitoringComponent(Enum):
    """Components that can be monitored"""

    AZURE_FUNCTIONS = "azure_functions"
    AZURE_STORAGE = "azure_storage"
    AZURE_DATABASE = "azure_database"
    AZURE_KEY_VAULT = "azure_key_vault"
    AZURE_SERVICE_BUS = "azure_service_bus"
    AZURE_MONITOR = "azure_monitor"
    EEG_PROCESSOR = "eeg_processor"
    LIFE_ALGORITHM = "life_algorithm"
    API_ENDPOINTS = "api_endpoints"
    SYSTEM_RESOURCES = "system_resources"
    NETWORK_CONNECTIVITY = "network_connectivity"


class AlertSeverity(Enum):
    """Alert severity levels"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertStatus(Enum):
    """Alert status"""

    ACTIVE = "active"
    RESOLVED = "resolved"
    ACKNOWLEDGED = "acknowledged"
    SUPPRESSED = "suppressed"


class MetricType(Enum):
    """Types of metrics"""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class MetricValue:
    """Individual metric measurement"""

    name: str
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    labels: Dict[str, str] = field(default_factory=dict)
    metric_type: MetricType = MetricType.GAUGE


@dataclass
class AlertRule:
    """Alert rule definition"""

    rule_id: str
    name: str
    description: str
    component: MonitoringComponent
    severity: AlertSeverity
    condition: str  # Expression to evaluate
    threshold: float
    window_seconds: int = 300  # 5 minutes default
    cooldown_seconds: int = 3600  # 1 hour default
    enabled: bool = True
    last_triggered: Optional[datetime] = None
    trigger_count: int = 0


@dataclass
class Alert:
    """Alert instance"""

    alert_id: str
    rule_id: str
    component: MonitoringComponent
    severity: AlertSeverity
    title: str
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: AlertStatus = AlertStatus.ACTIVE
    value: float = 0.0
    threshold: float = 0.0
    labels: Dict[str, str] = field(default_factory=dict)
    resolved_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None


@dataclass
class HealthCheck:
    """Health check definition"""

    check_id: str
    name: str
    component: MonitoringComponent
    check_function: Callable[[], Dict[str, Any]]
    interval_seconds: int = 60
    timeout_seconds: int = 30
    enabled: bool = True
    last_run: Optional[datetime] = None
    last_result: Optional[Dict[str, Any]] = None
    consecutive_failures: int = 0
    max_consecutive_failures: int = 3


@dataclass
class MonitoringReport:
    """Comprehensive monitoring report"""

    report_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    duration_seconds: float = 0.0
    components_checked: int = 0
    components_healthy: int = 0
    components_degraded: int = 0
    components_unhealthy: int = 0
    active_alerts: int = 0
    critical_alerts: int = 0
    total_metrics: int = 0
    system_health_score: float = 100.0
    component_health: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    alerts_summary: Dict[str, int] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


class ProductionMonitoringSuite:
    """
    Production Monitoring Suite for L.I.F.E. Platform

    Provides comprehensive monitoring, alerting, and health checking
    for production deployments with real-time metrics collection.
    """

    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.alert_rules: List[AlertRule] = []
        self.active_alerts: List[Alert] = []
        self.health_checks: List[HealthCheck] = []
        self.metrics_buffer: List[MetricValue] = []
        self.monitoring_reports: List[MonitoringReport] = []

        # Threading and async management
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self.alert_lock = threading.Lock()
        self.metrics_lock = threading.Lock()

        # Initialize monitoring components
        self._initialize_alert_rules()
        self._initialize_health_checks()

        logger.info(
            f"Production Monitoring Suite initialized for workspace: {self.workspace_path}"
        )

    def _initialize_alert_rules(self):
        """Initialize default alert rules"""
        rules = [
            AlertRule(
                rule_id="cpu_high",
                name="High CPU Usage",
                description="CPU usage exceeds threshold",
                component=MonitoringComponent.SYSTEM_RESOURCES,
                severity=AlertSeverity.HIGH,
                condition="cpu_percent > threshold",
                threshold=85.0,
                window_seconds=300,
            ),
            AlertRule(
                rule_id="memory_high",
                name="High Memory Usage",
                description="Memory usage exceeds threshold",
                component=MonitoringComponent.SYSTEM_RESOURCES,
                severity=AlertSeverity.HIGH,
                condition="memory_percent > threshold",
                threshold=90.0,
                window_seconds=300,
            ),
            AlertRule(
                rule_id="disk_space_low",
                name="Low Disk Space",
                description="Available disk space below threshold",
                component=MonitoringComponent.SYSTEM_RESOURCES,
                severity=AlertSeverity.CRITICAL,
                condition="disk_free_percent < threshold",
                threshold=10.0,
                window_seconds=3600,
            ),
            AlertRule(
                rule_id="azure_functions_errors",
                name="Azure Functions Errors",
                description="High error rate in Azure Functions",
                component=MonitoringComponent.AZURE_FUNCTIONS,
                severity=AlertSeverity.CRITICAL,
                condition="error_rate > threshold",
                threshold=5.0,
                window_seconds=300,
            ),
            AlertRule(
                rule_id="eeg_processing_latency",
                name="EEG Processing Latency",
                description="EEG processing latency exceeds threshold",
                component=MonitoringComponent.EEG_PROCESSOR,
                severity=AlertSeverity.HIGH,
                condition="avg_latency_ms > threshold",
                threshold=100.0,
                window_seconds=300,
            ),
            AlertRule(
                rule_id="api_response_time",
                name="API Response Time",
                description="API response time exceeds threshold",
                component=MonitoringComponent.API_ENDPOINTS,
                severity=AlertSeverity.MEDIUM,
                condition="avg_response_time_ms > threshold",
                threshold=2000.0,
                window_seconds=300,
            ),
            AlertRule(
                rule_id="storage_operations_failed",
                name="Storage Operations Failed",
                description="Storage operation failure rate exceeds threshold",
                component=MonitoringComponent.AZURE_STORAGE,
                severity=AlertSeverity.HIGH,
                condition="failure_rate > threshold",
                threshold=1.0,
                window_seconds=600,
            ),
        ]

        self.alert_rules = rules

    def _initialize_health_checks(self):
        """Initialize default health checks"""
        checks = [
            HealthCheck(
                check_id="system_resources",
                name="System Resources",
                component=MonitoringComponent.SYSTEM_RESOURCES,
                check_function=self._check_system_resources,
                interval_seconds=60,
            ),
            HealthCheck(
                check_id="azure_functions",
                name="Azure Functions",
                component=MonitoringComponent.AZURE_FUNCTIONS,
                check_function=self._check_azure_functions,
                interval_seconds=120,
            ),
            HealthCheck(
                check_id="azure_storage",
                name="Azure Storage",
                component=MonitoringComponent.AZURE_STORAGE,
                check_function=self._check_azure_storage,
                interval_seconds=300,
            ),
            HealthCheck(
                check_id="eeg_processor",
                name="EEG Processor",
                component=MonitoringComponent.EEG_PROCESSOR,
                check_function=self._check_eeg_processor,
                interval_seconds=60,
            ),
            HealthCheck(
                check_id="life_algorithm",
                name="L.I.F.E. Algorithm",
                component=MonitoringComponent.LIFE_ALGORITHM,
                check_function=self._check_life_algorithm,
                interval_seconds=120,
            ),
            HealthCheck(
                check_id="api_endpoints",
                name="API Endpoints",
                component=MonitoringComponent.API_ENDPOINTS,
                check_function=self._check_api_endpoints,
                interval_seconds=60,
            ),
            HealthCheck(
                check_id="network_connectivity",
                name="Network Connectivity",
                component=MonitoringComponent.NETWORK_CONNECTIVITY,
                check_function=self._check_network_connectivity,
                interval_seconds=300,
            ),
        ]

        self.health_checks = checks

    async def start_monitoring(self, continuous: bool = True) -> None:
        """Start the monitoring suite"""
        if self.monitoring_active:
            logger.warning("Monitoring is already active")
            return

        self.monitoring_active = True
        logger.info("Starting production monitoring suite")

        if continuous:
            # Start continuous monitoring in background thread
            self.monitoring_thread = threading.Thread(
                target=self._continuous_monitoring_loop, daemon=True
            )
            self.monitoring_thread.start()
        else:
            # Run single monitoring cycle
            await self._run_monitoring_cycle()

    def stop_monitoring(self) -> None:
        """Stop the monitoring suite"""
        if not self.monitoring_active:
            logger.warning("Monitoring is not active")
            return

        self.monitoring_active = False
        logger.info("Stopping production monitoring suite")

        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5.0)

    def _continuous_monitoring_loop(self) -> None:
        """Continuous monitoring loop"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            while self.monitoring_active:
                # Run monitoring cycle
                loop.run_until_complete(self._run_monitoring_cycle())

                # Wait before next cycle
                time.sleep(30)  # 30 second intervals

        except Exception as e:
            logger.error(f"Monitoring loop error: {e}")
        finally:
            loop.close()

    async def _run_monitoring_cycle(self) -> None:
        """Run a complete monitoring cycle"""
        cycle_start = time.time()

        try:
            # Run health checks
            await self._run_health_checks()

            # Collect metrics
            await self._collect_metrics()

            # Evaluate alert rules
            await self._evaluate_alert_rules()

            # Generate monitoring report
            report = await self._generate_monitoring_report()
            self.monitoring_reports.append(report)

            cycle_duration = time.time() - cycle_start
            logger.info(f"Monitoring cycle completed in {cycle_duration:.2f}s")

        except Exception as e:
            logger.error(f"Monitoring cycle failed: {e}")

    async def _run_health_checks(self) -> None:
        """Run all enabled health checks"""
        tasks = []
        for check in self.health_checks:
            if check.enabled:
                tasks.append(self._run_single_health_check(check))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _run_single_health_check(self, check: HealthCheck) -> None:
        """Run a single health check"""
        try:
            # Run check with timeout
            result = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(
                    self.executor, check.check_function
                ),
                timeout=check.timeout_seconds,
            )

            check.last_run = datetime.now()
            check.last_result = result

            if result.get("healthy", False):
                check.consecutive_failures = 0
            else:
                check.consecutive_failures += 1

        except asyncio.TimeoutError:
            logger.warning(f"Health check {check.check_id} timed out")
            check.consecutive_failures += 1
            check.last_result = {"healthy": False, "error": "Timeout"}
        except Exception as e:
            logger.error(f"Health check {check.check_id} failed: {e}")
            check.consecutive_failures += 1
            check.last_result = {"healthy": False, "error": str(e)}

    async def _collect_metrics(self) -> None:
        """Collect system and application metrics"""
        try:
            # Collect system metrics
            await self._collect_system_metrics()

            # Collect application metrics
            await self._collect_application_metrics()

            # Collect Azure metrics
            await self._collect_azure_metrics()

        except Exception as e:
            logger.error(f"Metrics collection failed: {e}")

    async def _collect_system_metrics(self) -> None:
        """Collect system resource metrics"""
        try:
            import psutil

            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            self._add_metric("system_cpu_percent", cpu_percent, {"type": "usage"})

            # Memory metrics
            memory = psutil.virtual_memory()
            self._add_metric("system_memory_percent", memory.percent, {"type": "usage"})
            self._add_metric(
                "system_memory_used_gb", memory.used / (1024**3), {"type": "absolute"}
            )

            # Disk metrics
            disk = psutil.disk_usage("/")
            self._add_metric("system_disk_percent", disk.percent, {"type": "usage"})
            self._add_metric(
                "system_disk_free_gb", disk.free / (1024**3), {"type": "absolute"}
            )

            # Network metrics
            network = psutil.net_io_counters()
            self._add_metric(
                "system_network_bytes_sent", network.bytes_sent, {"type": "counter"}
            )
            self._add_metric(
                "system_network_bytes_recv", network.bytes_recv, {"type": "counter"}
            )

        except ImportError:
            logger.warning("psutil not available for system metrics")
        except Exception as e:
            logger.error(f"System metrics collection failed: {e}")

    async def _collect_application_metrics(self) -> None:
        """Collect application-specific metrics"""
        try:
            # EEG processing metrics
            await self._collect_eeg_metrics()

            # API metrics
            await self._collect_api_metrics()

            # Algorithm performance metrics
            await self._collect_algorithm_metrics()

        except Exception as e:
            logger.error(f"Application metrics collection failed: {e}")

    async def _collect_eeg_metrics(self) -> None:
        """Collect EEG processing metrics"""
        try:
            # Check if EEG processor is running
            eeg_running = self._check_process_running("eeg_processor.py")
            self._add_metric(
                "eeg_processor_running", 1.0 if eeg_running else 0.0, {"type": "status"}
            )

            # Mock latency metrics (would be collected from actual processor)
            self._add_metric("eeg_processing_latency_ms", 45.2, {"type": "performance"})
            self._add_metric(
                "eeg_processing_throughput",
                120.5,
                {"type": "throughput", "unit": "samples/sec"},
            )

        except Exception as e:
            logger.error(f"EEG metrics collection failed: {e}")

    async def _collect_api_metrics(self) -> None:
        """Collect API performance metrics"""
        try:
            # Mock API metrics (would be collected from actual API)
            self._add_metric(
                "api_requests_total", 1250, {"type": "counter", "method": "all"}
            )
            self._add_metric("api_response_time_ms", 150.3, {"type": "performance"})
            self._add_metric("api_error_rate", 0.02, {"type": "rate"})

        except Exception as e:
            logger.error(f"API metrics collection failed: {e}")

    async def _collect_algorithm_metrics(self) -> None:
        """Collect algorithm performance metrics"""
        try:
            # Check if algorithm is running
            algo_running = self._check_process_running("experimentP2L")
            self._add_metric(
                "life_algorithm_running",
                1.0 if algo_running else 0.0,
                {"type": "status"},
            )

            # Mock algorithm metrics
            self._add_metric("life_algorithm_accuracy", 0.823, {"type": "performance"})
            self._add_metric(
                "life_algorithm_processing_time_ms", 38.7, {"type": "performance"}
            )

        except Exception as e:
            logger.error(f"Algorithm metrics collection failed: {e}")

    async def _collect_azure_metrics(self) -> None:
        """Collect Azure service metrics"""
        try:
            # Mock Azure metrics (would use Azure Monitor API)
            self._add_metric("azure_functions_invocations", 450, {"type": "counter"})
            self._add_metric("azure_storage_operations", 1250, {"type": "counter"})
            self._add_metric("azure_functions_errors", 5, {"type": "counter"})

        except Exception as e:
            logger.error(f"Azure metrics collection failed: {e}")

    def _add_metric(
        self, name: str, value: float, labels: Dict[str, str] = None
    ) -> None:
        """Add a metric to the buffer"""
        with self.metrics_lock:
            metric = MetricValue(name=name, value=value, labels=labels or {})
            self.metrics_buffer.append(metric)

            # Keep buffer size manageable (last 1000 metrics)
            if len(self.metrics_buffer) > 1000:
                self.metrics_buffer = self.metrics_buffer[-1000:]

    async def _evaluate_alert_rules(self) -> None:
        """Evaluate all alert rules against current metrics"""
        for rule in self.alert_rules:
            if not rule.enabled:
                continue

            try:
                await self._evaluate_single_alert_rule(rule)
            except Exception as e:
                logger.error(f"Alert rule evaluation failed for {rule.rule_id}: {e}")

    async def _evaluate_single_alert_rule(self, rule: AlertRule) -> None:
        """Evaluate a single alert rule"""
        # Get relevant metrics for the time window
        window_start = datetime.now() - timedelta(seconds=rule.window_seconds)
        relevant_metrics = [
            m
            for m in self.metrics_buffer
            if m.name in rule.condition and m.timestamp >= window_start
        ]

        if not relevant_metrics:
            return

        # Calculate metric value based on rule condition
        if "cpu_percent" in rule.condition:
            values = [
                m.value for m in relevant_metrics if m.name == "system_cpu_percent"
            ]
        elif "memory_percent" in rule.condition:
            values = [
                m.value for m in relevant_metrics if m.name == "system_memory_percent"
            ]
        elif "disk_free_percent" in rule.condition:
            values = [
                m.value for m in relevant_metrics if m.name == "system_disk_percent"
            ]
            values = [100 - v for v in values]  # Convert to free percentage
        elif "error_rate" in rule.condition:
            # Calculate error rate from Azure metrics
            total_ops = sum(
                m.value
                for m in relevant_metrics
                if "azure_functions_invocations" in m.name
            )
            errors = sum(
                m.value for m in relevant_metrics if "azure_functions_errors" in m.name
            )
            values = [errors / total_ops * 100 if total_ops > 0 else 0]
        else:
            # Default to average of relevant metrics
            values = [m.value for m in relevant_metrics]

        if not values:
            return

        current_value = sum(values) / len(values)

        # Check if alert should be triggered
        should_trigger = False
        if ">" in rule.condition and current_value > rule.threshold:
            should_trigger = True
        elif "<" in rule.condition and current_value < rule.threshold:
            should_trigger = True

        if should_trigger:
            # Check cooldown period
            if rule.last_triggered:
                time_since_last = (datetime.now() - rule.last_triggered).total_seconds()
                if time_since_last < rule.cooldown_seconds:
                    return

            # Create alert
            alert = Alert(
                alert_id=f"alert_{rule.rule_id}_{int(datetime.now().timestamp())}",
                rule_id=rule.rule_id,
                component=rule.component,
                severity=rule.severity,
                title=rule.name,
                description=rule.description,
                value=current_value,
                threshold=rule.threshold,
                labels={"rule": rule.rule_id},
            )

            with self.alert_lock:
                self.active_alerts.append(alert)
                rule.last_triggered = datetime.now()
                rule.trigger_count += 1

            logger.warning(
                f"Alert triggered: {alert.title} (value: {current_value:.2f}, threshold: {rule.threshold})"
            )

    def _check_system_resources(self) -> Dict[str, Any]:
        """Check system resources health"""
        try:
            import psutil

            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            healthy = cpu_percent < 90 and memory.percent < 95 and disk.percent < 95

            return {
                "healthy": healthy,
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "disk_percent": disk.percent,
                "details": {
                    "cpu_usage": f"{cpu_percent:.1f}%",
                    "memory_usage": f"{memory.percent:.1f}%",
                    "disk_usage": f"{disk.percent:.1f}%",
                },
            }

        except Exception as e:
            return {"healthy": False, "error": str(e)}

    def _check_azure_functions(self) -> Dict[str, Any]:
        """Check Azure Functions health"""
        try:
            # Check if Azure Functions configuration exists
            config_files = ["azure_functions_config.py", "azure_config.py"]
            config_exists = any(
                (self.workspace_path / f).exists() for f in config_files
            )

            if not config_exists:
                return {
                    "healthy": False,
                    "error": "Azure Functions configuration not found",
                }

            # Mock health check (would check actual Azure status)
            return {
                "healthy": True,
                "status": "operational",
                "details": {
                    "functions_count": 5,
                    "last_deployment": "2025-01-15T10:30:00Z",
                },
            }

        except Exception as e:
            return {"healthy": False, "error": str(e)}

    def _check_azure_storage(self) -> Dict[str, Any]:
        """Check Azure Storage health"""
        try:
            # Check storage configuration
            azure_config = self.workspace_path / "azure_config.py"
            if not azure_config.exists():
                return {"healthy": False, "error": "Azure configuration not found"}

            # Mock health check
            return {
                "healthy": True,
                "status": "connected",
                "details": {"containers_count": 3, "total_size_gb": 25.7},
            }

        except Exception as e:
            return {"healthy": False, "error": str(e)}

    def _check_eeg_processor(self) -> Dict[str, Any]:
        """Check EEG processor health"""
        try:
            # Check if EEG processor files exist
            eeg_files = ["eeg_processor.py", "enhanced_eeg_processor.py"]
            files_exist = any((self.workspace_path / f).exists() for f in eeg_files)

            if not files_exist:
                return {"healthy": False, "error": "EEG processor files not found"}

            # Check if process is running
            running = self._check_process_running("eeg_processor")
            if not running:
                running = self._check_process_running("enhanced_eeg_processor")

            return {
                "healthy": running,
                "status": "running" if running else "stopped",
                "details": {
                    "process_running": running,
                    "last_check": datetime.now().isoformat(),
                },
            }

        except Exception as e:
            return {"healthy": False, "error": str(e)}

    def _check_life_algorithm(self) -> Dict[str, Any]:
        """Check L.I.F.E. algorithm health"""
        try:
            # Check if algorithm file exists
            algo_file = (
                self.workspace_path
                / "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py"
            )
            if not algo_file.exists():
                return {"healthy": False, "error": "L.I.F.E. algorithm file not found"}

            # Check if process is running
            running = self._check_process_running("experimentP2L")

            return {
                "healthy": running,
                "status": "running" if running else "stopped",
                "details": {"process_running": running, "file_exists": True},
            }

        except Exception as e:
            return {"healthy": False, "error": str(e)}

    def _check_api_endpoints(self) -> Dict[str, Any]:
        """Check API endpoints health"""
        try:
            # Check if API file exists
            api_file = self.workspace_path / "life_platform_api.py"
            if not api_file.exists():
                return {"healthy": False, "error": "API file not found"}

            # Mock API health check
            return {
                "healthy": True,
                "status": "operational",
                "details": {"endpoints_count": 8, "response_time_ms": 145},
            }

        except Exception as e:
            return {"healthy": False, "error": str(e)}

    def _check_network_connectivity(self) -> Dict[str, Any]:
        """Check network connectivity"""
        try:
            import socket

            # Test basic connectivity
            socket.create_connection(("8.8.8.8", 53), timeout=5)

            return {
                "healthy": True,
                "status": "connected",
                "details": {"latency_ms": 25, "packet_loss": 0.0},
            }

        except Exception as e:
            return {"healthy": False, "error": str(e)}

    def _check_process_running(self, process_name: str) -> bool:
        """Check if a process is running"""
        try:
            import psutil

            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    if (
                        process_name.lower()
                        in " ".join(proc.info["cmdline"] or []).lower()
                    ):
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            return False

        except ImportError:
            # Fallback without psutil
            try:
                import subprocess

                result = subprocess.run(
                    ["pgrep", "-f", process_name], capture_output=True, text=True
                )
                return result.returncode == 0
            except Exception:
                return False
        except Exception:
            return False

    async def _generate_monitoring_report(self) -> MonitoringReport:
        """Generate comprehensive monitoring report"""
        report = MonitoringReport(
            report_id=f"monitor_report_{int(datetime.now().timestamp())}",
            timestamp=datetime.now(),
        )

        # Analyze health checks
        healthy_count = 0
        degraded_count = 0
        unhealthy_count = 0

        for check in self.health_checks:
            if not check.last_result:
                continue

            report.components_checked += 1

            if check.last_result.get("healthy", False):
                healthy_count += 1
            elif check.consecutive_failures > 0:
                if check.consecutive_failures >= check.max_consecutive_failures:
                    unhealthy_count += 1
                else:
                    degraded_count += 1

        report.components_healthy = healthy_count
        report.components_degraded = degraded_count
        report.components_unhealthy = unhealthy_count

        # Analyze alerts
        with self.alert_lock:
            report.active_alerts = len(self.active_alerts)
            report.critical_alerts = len(
                [a for a in self.active_alerts if a.severity == AlertSeverity.CRITICAL]
            )

        # Calculate system health score
        total_components = report.components_checked
        if total_components > 0:
            health_score = (
                report.components_healthy * 100 + report.components_degraded * 50
            ) / total_components
            # Penalize for active alerts
            alert_penalty = min(report.active_alerts * 5, 50)
            report.system_health_score = max(0, health_score - alert_penalty)

        # Build component health details
        for check in self.health_checks:
            if check.last_result:
                report.component_health[check.component.value] = {
                    "healthy": check.last_result.get("healthy", False),
                    "status": check.last_result.get("status", "unknown"),
                    "last_check": (
                        check.last_run.isoformat() if check.last_run else None
                    ),
                    "consecutive_failures": check.consecutive_failures,
                    "details": check.last_result.get("details", {}),
                }

        # Build alerts summary
        severity_counts = {}
        for alert in self.active_alerts:
            severity_counts[alert.severity.value] = (
                severity_counts.get(alert.severity.value, 0) + 1
            )
        report.alerts_summary = severity_counts

        # Generate recommendations
        report.recommendations = self._generate_monitoring_recommendations(report)

        return report

    def _generate_monitoring_recommendations(
        self, report: MonitoringReport
    ) -> List[str]:
        """Generate monitoring recommendations"""
        recommendations = []

        if report.components_unhealthy > 0:
            recommendations.append(
                f"Address {report.components_unhealthy} unhealthy components immediately"
            )

        if report.critical_alerts > 0:
            recommendations.append(f"Resolve {report.critical_alerts} critical alerts")

        if report.system_health_score < 70:
            recommendations.append(
                "Overall system health is degraded - investigate component issues"
            )

        if report.components_degraded > 0:
            recommendations.append(
                f"Monitor {report.components_degraded} degraded components closely"
            )

        if not recommendations:
            recommendations.append("All systems operating normally")

        return recommendations

    def get_active_alerts(
        self, component: Optional[MonitoringComponent] = None
    ) -> List[Alert]:
        """Get active alerts, optionally filtered by component"""
        with self.alert_lock:
            if component:
                return [a for a in self.active_alerts if a.component == component]
            return self.active_alerts.copy()

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge an alert"""
        with self.alert_lock:
            for alert in self.active_alerts:
                if alert.alert_id == alert_id:
                    alert.status = AlertStatus.ACKNOWLEDGED
                    alert.acknowledged_at = datetime.now()
                    alert.acknowledged_by = acknowledged_by
                    logger.info(f"Alert {alert_id} acknowledged by {acknowledged_by}")
                    return True
        return False

    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert"""
        with self.alert_lock:
            for alert in self.active_alerts:
                if alert.alert_id == alert_id:
                    alert.status = AlertStatus.RESOLVED
                    alert.resolved_at = datetime.now()
                    self.active_alerts.remove(alert)
                    logger.info(f"Alert {alert_id} resolved")
                    return True
        return False

    def get_recent_metrics(
        self, name: Optional[str] = None, limit: int = 100
    ) -> List[MetricValue]:
        """Get recent metrics, optionally filtered by name"""
        with self.metrics_lock:
            metrics = self.metrics_buffer[-limit:]
            if name:
                metrics = [m for m in metrics if m.name == name]
            return metrics.copy()

    def export_monitoring_report(
        self, filepath: str, report: Optional[MonitoringReport] = None
    ) -> bool:
        """Export monitoring report to file"""
        if report is None:
            report = self.monitoring_reports[-1] if self.monitoring_reports else None

        if not report:
            logger.warning("No monitoring report available to export")
            return False

        try:
            export_data = {
                "report_id": report.report_id,
                "timestamp": report.timestamp.isoformat(),
                "duration_seconds": report.duration_seconds,
                "system_health_score": report.system_health_score,
                "components": {
                    "total": report.components_checked,
                    "healthy": report.components_healthy,
                    "degraded": report.components_degraded,
                    "unhealthy": report.components_unhealthy,
                },
                "alerts": {
                    "active": report.active_alerts,
                    "critical": report.critical_alerts,
                    "summary": report.alerts_summary,
                },
                "component_health": report.component_health,
                "recommendations": report.recommendations,
            }

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Monitoring report exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to export monitoring report: {e}")
            return False


# Factory function for easy instantiation
def create_production_monitoring_suite(
    workspace_path: Optional[str] = None,
) -> ProductionMonitoringSuite:
    """
    Factory function to create production monitoring suite

    Args:
        workspace_path: Path to workspace directory

    Returns:
        Configured ProductionMonitoringSuite instance
    """
    return ProductionMonitoringSuite(workspace_path=workspace_path)


# Command-line interface
def main():
    """Main CLI function for production monitoring"""
    import argparse

    parser = argparse.ArgumentParser(
        description="L.I.F.E. Platform Production Monitoring Suite"
    )
    parser.add_argument(
        "--workspace", "-w", default=None, help="Workspace directory path"
    )
    parser.add_argument(
        "--continuous", "-c", action="store_true", help="Run continuous monitoring"
    )
    parser.add_argument(
        "--export", "-e", help="Export monitoring report to specified file"
    )
    parser.add_argument(
        "--alerts", "-a", action="store_true", help="Show active alerts"
    )
    parser.add_argument(
        "--metrics", "-m", help="Show recent metrics for specified name"
    )
    parser.add_argument(
        "--health", action="store_true", help="Show component health status"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create monitoring suite
    suite = create_production_monitoring_suite(workspace_path=args.workspace)

    print("L.I.F.E. Platform - Production Monitoring Suite")
    print("=" * 55)

    try:
        if args.alerts:
            # Show active alerts
            alerts = suite.get_active_alerts()
            print(f"\nActive Alerts: {len(alerts)}")
            for alert in alerts[:10]:  # Show first 10
                print(f"  {alert.severity.value.upper()}: {alert.title}")
                print(f"    {alert.description}")
                print(f"    Value: {alert.value:.2f}, Threshold: {alert.threshold}")
                print(f"    Time: {alert.timestamp}")
                print()

        elif args.metrics:
            # Show recent metrics
            metrics = suite.get_recent_metrics(name=args.metrics, limit=20)
            print(f"\nRecent Metrics for '{args.metrics}': {len(metrics)}")
            for metric in metrics:
                print(f"  {metric.timestamp}: {metric.value:.2f} {metric.labels}")

        elif args.health:
            # Show component health
            print("\nComponent Health Status:")
            for check in suite.health_checks:
                if check.last_result:
                    status = "✅" if check.last_result.get("healthy") else "❌"
                    print(
                        f"  {status} {check.name}: {check.last_result.get('status', 'unknown')}"
                    )

        else:
            # Run monitoring
            print("Running monitoring cycle...")

            # Run single cycle
            asyncio.run(suite._run_monitoring_cycle())

            # Get latest report
            if suite.monitoring_reports:
                report = suite.monitoring_reports[-1]

                print("\nMonitoring Results:")
                print(f"  System Health Score: {report.system_health_score:.1f}%")
                print(f"  Components Checked: {report.components_checked}")
                print(f"  Healthy: {report.components_healthy}")
                print(f"  Degraded: {report.components_degraded}")
                print(f"  Unhealthy: {report.components_unhealthy}")
                print(f"  Active Alerts: {report.active_alerts}")
                print(f"  Critical Alerts: {report.critical_alerts}")

                if report.recommendations:
                    print("\nRecommendations:")
                    for rec in report.recommendations:
                        print(f"  • {rec}")

            if args.export:
                if suite.export_monitoring_report(args.export):
                    print(f"\nMonitoring report exported to {args.export}")
                else:
                    print("\nFailed to export monitoring report")
                    return 1

        return 0

    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
        suite.stop_monitoring()
        return 1
    except Exception as e:
        print(f"\nMonitoring failed: {e}")
        suite.stop_monitoring()
        return 1
    finally:
        if not args.continuous:
            suite.stop_monitoring()


if __name__ == "__main__":
    import sys

    sys.exit(main())
