#!/usr/bin/env python3
"""
L.I.F.E. Platform - System Health Monitor
Real-time monitoring and health checking for L.I.F.E. Platform components

This module provides comprehensive system health monitoring capabilities,
including real-time metrics collection, health status assessment, and
automated alerting for the L.I.F.E. Platform.

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
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """System health status levels"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"
    DOWN = "down"


class ComponentType(Enum):
    """Types of system components to monitor"""
    CORE_ALGORITHM = "core_algorithm"
    AZURE_FUNCTIONS = "azure_functions"
    DATABASE = "database"
    API_ENDPOINTS = "api_endpoints"
    EEG_PROCESSOR = "eeg_processor"
    AUTONOMOUS_OPTIMIZER = "autonomous_optimizer"
    MONITORING_SYSTEM = "monitoring_system"
    SECURITY_MODULE = "security_module"


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class HealthMetric:
    """Individual health metric"""
    name: str
    value: Any
    unit: str = ""
    status: HealthStatus = HealthStatus.UNKNOWN
    timestamp: datetime = field(default_factory=datetime.now)
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None
    description: str = ""


@dataclass
class ComponentHealth:
    """Health status of a system component"""
    component_type: ComponentType
    component_name: str
    status: HealthStatus = HealthStatus.UNKNOWN
    last_check: datetime = field(default_factory=datetime.now)
    response_time: float = 0.0
    metrics: List[HealthMetric] = field(default_factory=list)
    error_message: str = ""
    dependencies: List[str] = field(default_factory=list)
    version: str = ""
    uptime: float = 0.0


@dataclass
class SystemAlert:
    """System health alert"""
    alert_id: str
    severity: AlertSeverity
    component: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthReport:
    """Comprehensive system health report"""
    report_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    overall_status: HealthStatus = HealthStatus.UNKNOWN
    components: List[ComponentHealth] = field(default_factory=list)
    alerts: List[SystemAlert] = field(default_factory=list)
    system_metrics: List[HealthMetric] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    next_check_scheduled: Optional[datetime] = None


class SystemHealthMonitor:
    """
    System Health Monitor for L.I.F.E. Platform

    Provides real-time monitoring and health assessment of all
    platform components with automated alerting capabilities.
    """

    def __init__(self, workspace_path: Optional[str] = None, check_interval: int = 60):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.check_interval = check_interval  # seconds
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.last_report: Optional[HealthReport] = None
        self.alerts: List[SystemAlert] = []
        self.health_history: List[HealthReport] = []

        # Component configurations
        self.component_configs = {
            ComponentType.CORE_ALGORITHM: {
                "check_function": self._check_core_algorithm_health,
                "timeout": 30,
                "critical_threshold": 60  # seconds
            },
            ComponentType.AZURE_FUNCTIONS: {
                "check_function": self._check_azure_functions_health,
                "timeout": 45,
                "critical_threshold": 120  # seconds
            },
            ComponentType.API_ENDPOINTS: {
                "check_function": self._check_api_endpoints_health,
                "timeout": 15,
                "critical_threshold": 30  # seconds
            },
            ComponentType.EEG_PROCESSOR: {
                "check_function": self._check_eeg_processor_health,
                "timeout": 20,
                "critical_threshold": 45  # seconds
            },
            ComponentType.AUTONOMOUS_OPTIMIZER: {
                "check_function": self._check_autonomous_optimizer_health,
                "timeout": 25,
                "critical_threshold": 60  # seconds
            },
            ComponentType.MONITORING_SYSTEM: {
                "check_function": self._check_monitoring_system_health,
                "timeout": 10,
                "critical_threshold": 15  # seconds
            }
        }

        logger.info(f"System Health Monitor initialized for workspace: {self.workspace_path}")

    async def start_monitoring(self) -> None:
        """Start continuous health monitoring"""
        if self.is_monitoring:
            logger.warning("Health monitoring already running")
            return

        self.is_monitoring = True
        logger.info("Starting system health monitoring...")

        # Initial health check
        await self.perform_health_check()

        # Start monitoring thread
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self.monitor_thread.start()

    def stop_monitoring(self) -> None:
        """Stop health monitoring"""
        if not self.is_monitoring:
            logger.warning("Health monitoring not running")
            return

        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)

        logger.info("System health monitoring stopped")

    def _monitoring_loop(self) -> None:
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Run health check in event loop
                asyncio.run(self.perform_health_check())
            except Exception as e:
                logger.error(f"Health check failed: {e}")

            # Wait for next check
            time.sleep(self.check_interval)

    async def perform_health_check(self) -> HealthReport:
        """Perform comprehensive health check"""
        report = HealthReport(
            report_id=f"health_{int(time.time())}",
            timestamp=datetime.now()
        )

        try:
            # Check system-level metrics
            report.system_metrics = await self._collect_system_metrics()

            # Check individual components
            component_tasks = []
            for component_type, config in self.component_configs.items():
                task = self._check_component_health(component_type, config)
                component_tasks.append(task)

            component_results = await asyncio.gather(*component_tasks, return_exceptions=True)

            for result in component_results:
                if isinstance(result, Exception):
                    logger.error(f"Component health check failed: {result}")
                    continue
                report.components.append(result)

            # Determine overall status
            report.overall_status = self._calculate_overall_status(report.components)

            # Generate alerts
            new_alerts = self._generate_alerts(report)
            report.alerts.extend(new_alerts)
            self.alerts.extend(new_alerts)

            # Generate recommendations
            report.recommendations = self._generate_health_recommendations(report)

            # Schedule next check
            report.next_check_scheduled = datetime.now() + timedelta(seconds=self.check_interval)

            # Store report
            self.last_report = report
            self.health_history.append(report)

            # Keep only last 100 reports
            if len(self.health_history) > 100:
                self.health_history = self.health_history[-100:]

            logger.info(f"Health check completed. Overall status: {report.overall_status.value}")

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            report.overall_status = HealthStatus.CRITICAL

        return report

    async def _collect_system_metrics(self) -> List[HealthMetric]:
        """Collect system-level health metrics"""
        metrics = []

        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_status = (HealthStatus.CRITICAL if cpu_percent > 90
                         else HealthStatus.WARNING if cpu_percent > 75
                         else HealthStatus.HEALTHY)

            metrics.append(HealthMetric(
                name="cpu_usage",
                value=cpu_percent,
                unit="%",
                status=cpu_status,
                threshold_warning=75.0,
                threshold_critical=90.0,
                description="CPU utilization percentage"
            ))

            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_status = (HealthStatus.CRITICAL if memory_percent > 90
                           else HealthStatus.WARNING if memory_percent > 80
                           else HealthStatus.HEALTHY)

            metrics.append(HealthMetric(
                name="memory_usage",
                value=memory_percent,
                unit="%",
                status=memory_status,
                threshold_warning=80.0,
                threshold_critical=90.0,
                description="Memory utilization percentage"
            ))

            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_status = (HealthStatus.CRITICAL if disk_percent > 95
                          else HealthStatus.WARNING if disk_percent > 85
                          else HealthStatus.HEALTHY)

            metrics.append(HealthMetric(
                name="disk_usage",
                value=disk_percent,
                unit="%",
                status=disk_status,
                threshold_warning=85.0,
                threshold_critical=95.0,
                description="Disk utilization percentage"
            ))

            # Network connections
            net_connections = len(psutil.net_connections())
            metrics.append(HealthMetric(
                name="network_connections",
                value=net_connections,
                unit="connections",
                status=HealthStatus.HEALTHY,
                description="Active network connections"
            ))

        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
            metrics.append(HealthMetric(
                name="system_metrics_error",
                value=str(e),
                status=HealthStatus.CRITICAL,
                description="Error collecting system metrics"
            ))

        return metrics

    async def _check_component_health(self, component_type: ComponentType, config: Dict[str, Any]) -> ComponentHealth:
        """Check health of a specific component"""
        component = ComponentHealth(
            component_type=component_type,
            component_name=component_type.value.replace('_', ' ').title()
        )

        start_time = time.time()

        try:
            # Execute health check function with timeout
            check_function = config["check_function"]
            timeout = config["timeout"]

            result = await asyncio.wait_for(
                check_function(),
                timeout=timeout
            )

            component.status = result.get("status", HealthStatus.UNKNOWN)
            component.metrics = result.get("metrics", [])
            component.error_message = result.get("error", "")
            component.version = result.get("version", "")
            component.uptime = result.get("uptime", 0.0)
            component.dependencies = result.get("dependencies", [])

        except asyncio.TimeoutError:
            component.status = HealthStatus.CRITICAL
            component.error_message = f"Health check timed out after {config['timeout']} seconds"
        except Exception as e:
            component.status = HealthStatus.CRITICAL
            component.error_message = f"Health check failed: {str(e)}"

        component.response_time = time.time() - start_time
        component.last_check = datetime.now()

        return component

    async def _check_core_algorithm_health(self) -> Dict[str, Any]:
        """Check core algorithm health"""
        result = {
            "status": HealthStatus.UNKNOWN,
            "metrics": [],
            "version": "",
            "uptime": 0.0,
            "dependencies": ["numpy", "pandas", "asyncio"]
        }

        try:
            # Check if core algorithm file exists
            core_file = self.workspace_path / "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py"
            if not core_file.exists():
                result["status"] = HealthStatus.DOWN
                result["error"] = "Core algorithm file not found"
                return result

            # Try to import and check basic functionality
            sys.path.insert(0, str(self.workspace_path))
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("life_algorithm", core_file)
                life_module = importlib.util.module_from_spec(spec)

                # Basic import test
                spec.loader.exec_module(life_module)

                # Check for required classes
                required_classes = ['LIFEAlgorithmCore', 'EEGMetrics', 'LearningOutcome']
                missing_classes = []

                for cls in required_classes:
                    if not hasattr(life_module, cls):
                        missing_classes.append(cls)

                if missing_classes:
                    result["status"] = HealthStatus.CRITICAL
                    result["error"] = f"Missing required classes: {', '.join(missing_classes)}"
                else:
                    result["status"] = HealthStatus.HEALTHY
                    result["version"] = getattr(life_module, '__version__', '1.0.0')

                    # Add performance metrics
                    result["metrics"] = [
                        HealthMetric(
                            name="algorithm_classes_loaded",
                            value=len(required_classes),
                            unit="classes",
                            status=HealthStatus.HEALTHY,
                            description="Number of core algorithm classes loaded"
                        )
                    ]

            finally:
                if str(self.workspace_path) in sys.path:
                    sys.path.remove(str(self.workspace_path))

        except Exception as e:
            result["status"] = HealthStatus.CRITICAL
            result["error"] = f"Core algorithm health check failed: {str(e)}"

        return result

    async def _check_azure_functions_health(self) -> Dict[str, Any]:
        """Check Azure Functions health"""
        result = {
            "status": HealthStatus.UNKNOWN,
            "metrics": [],
            "version": "",
            "uptime": 0.0,
            "dependencies": ["azure-functions", "azure-identity"]
        }

        try:
            # Check if Azure Functions file exists
            functions_file = self.workspace_path / "azure_functions_workflow.py"
            if not functions_file.exists():
                result["status"] = HealthStatus.DOWN
                result["error"] = "Azure Functions workflow file not found"
                return result

            # Basic syntax and import check
            with open(functions_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for Azure Functions patterns
            required_patterns = ['azure.functions', 'func.', 'HttpRequest', 'HttpResponse']
            found_patterns = sum(1 for pattern in required_patterns if pattern in content)

            if found_patterns >= len(required_patterns) * 0.8:  # 80% coverage
                result["status"] = HealthStatus.HEALTHY
                result["metrics"] = [
                    HealthMetric(
                        name="functions_patterns_found",
                        value=found_patterns,
                        unit="patterns",
                        status=HealthStatus.HEALTHY,
                        description="Azure Functions code patterns detected"
                    )
                ]
            else:
                result["status"] = HealthStatus.WARNING
                result["error"] = f"Missing Azure Functions patterns: {len(required_patterns) - found_patterns} not found"

        except Exception as e:
            result["status"] = HealthStatus.CRITICAL
            result["error"] = f"Azure Functions health check failed: {str(e)}"

        return result

    async def _check_api_endpoints_health(self) -> Dict[str, Any]:
        """Check API endpoints health"""
        result = {
            "status": HealthStatus.UNKNOWN,
            "metrics": [],
            "version": "",
            "uptime": 0.0,
            "dependencies": ["fastapi", "uvicorn", "requests"]
        }

        try:
            # Check if API file exists
            api_file = self.workspace_path / "life_platform_api.py"
            if not api_file.exists():
                result["status"] = HealthStatus.DOWN
                result["error"] = "API endpoints file not found"
                return result

            # Basic structure check
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for API patterns
            api_patterns = ['FastAPI', '@app.', 'HTTPException', 'pydantic']
            found_patterns = sum(1 for pattern in api_patterns if pattern in content)

            if found_patterns >= len(api_patterns) * 0.7:  # 70% coverage
                result["status"] = HealthStatus.HEALTHY
                result["metrics"] = [
                    HealthMetric(
                        name="api_patterns_found",
                        value=found_patterns,
                        unit="patterns",
                        status=HealthStatus.HEALTHY,
                        description="API framework patterns detected"
                    )
                ]
            else:
                result["status"] = HealthStatus.WARNING
                result["error"] = f"Incomplete API implementation: {len(api_patterns) - found_patterns} patterns missing"

        except Exception as e:
            result["status"] = HealthStatus.CRITICAL
            result["error"] = f"API endpoints health check failed: {str(e)}"

        return result

    async def _check_eeg_processor_health(self) -> Dict[str, Any]:
        """Check EEG processor health"""
        result = {
            "status": HealthStatus.UNKNOWN,
            "metrics": [],
            "version": "",
            "uptime": 0.0,
            "dependencies": ["numpy", "scipy", "mne"]
        }

        try:
            # Check if EEG processor file exists
            eeg_file = self.workspace_path / "eeg_processor.py"
            if not eeg_file.exists():
                result["status"] = HealthStatus.DOWN
                result["error"] = "EEG processor file not found"
                return result

            # Basic functionality check
            with open(eeg_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for EEG processing patterns
            eeg_patterns = ['EEG', 'signal', 'filter', 'fft', 'numpy']
            found_patterns = sum(1 for pattern in eeg_patterns if pattern.lower() in content.lower())

            if found_patterns >= len(eeg_patterns) * 0.6:  # 60% coverage
                result["status"] = HealthStatus.HEALTHY
                result["metrics"] = [
                    HealthMetric(
                        name="eeg_patterns_found",
                        value=found_patterns,
                        unit="patterns",
                        status=HealthStatus.HEALTHY,
                        description="EEG processing patterns detected"
                    )
                ]
            else:
                result["status"] = HealthStatus.WARNING
                result["error"] = f"Limited EEG processing capabilities: {len(eeg_patterns) - found_patterns} patterns missing"

        except Exception as e:
            result["status"] = HealthStatus.CRITICAL
            result["error"] = f"EEG processor health check failed: {str(e)}"

        return result

    async def _check_autonomous_optimizer_health(self) -> Dict[str, Any]:
        """Check autonomous optimizer health"""
        result = {
            "status": HealthStatus.UNKNOWN,
            "metrics": [],
            "version": "",
            "uptime": 0.0,
            "dependencies": ["numpy", "pandas", "scikit-learn"]
        }

        try:
            # Check if optimizer file exists
            optimizer_file = self.workspace_path / "autonomous_optimizer.py"
            if not optimizer_file.exists():
                result["status"] = HealthStatus.DOWN
                result["error"] = "Autonomous optimizer file not found"
                return result

            # Basic structure check
            with open(optimizer_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for optimization patterns
            opt_patterns = ['optimize', 'autonomous', 'KPI', 'benchmark', 'asyncio']
            found_patterns = sum(1 for pattern in opt_patterns if pattern.lower() in content.lower())

            if found_patterns >= len(opt_patterns) * 0.7:  # 70% coverage
                result["status"] = HealthStatus.HEALTHY
                result["metrics"] = [
                    HealthMetric(
                        name="optimizer_patterns_found",
                        value=found_patterns,
                        unit="patterns",
                        status=HealthStatus.HEALTHY,
                        description="Autonomous optimization patterns detected"
                    )
                ]
            else:
                result["status"] = HealthStatus.WARNING
                result["error"] = f"Incomplete optimization features: {len(opt_patterns) - found_patterns} patterns missing"

        except Exception as e:
            result["status"] = HealthStatus.CRITICAL
            result["error"] = f"Autonomous optimizer health check failed: {str(e)}"

        return result

    async def _check_monitoring_system_health(self) -> Dict[str, Any]:
        """Check monitoring system health"""
        result = {
            "status": HealthStatus.HEALTHY,
            "metrics": [],
            "version": "1.0.0",
            "uptime": time.time(),  # System uptime
            "dependencies": ["psutil", "asyncio"]
        }

        # Add monitoring-specific metrics
        result["metrics"] = [
            HealthMetric(
                name="monitoring_checks_performed",
                value=len(self.health_history) if self.health_history else 0,
                unit="checks",
                status=HealthStatus.HEALTHY,
                description="Number of health checks performed"
            ),
            HealthMetric(
                name="active_alerts",
                value=len([a for a in self.alerts if not a.resolved]),
                unit="alerts",
                status=HealthStatus.HEALTHY,
                description="Number of active alerts"
            )
        ]

        return result

    def _calculate_overall_status(self, components: List[ComponentHealth]) -> HealthStatus:
        """Calculate overall system health status"""
        if not components:
            return HealthStatus.UNKNOWN

        # Count status levels
        status_counts = {}
        for component in components:
            status = component.status.value
            status_counts[status] = status_counts.get(status, 0) + 1

        # Determine overall status
        if status_counts.get(HealthStatus.CRITICAL.value, 0) > 0:
            return HealthStatus.CRITICAL
        elif status_counts.get(HealthStatus.WARNING.value, 0) > 0:
            return HealthStatus.WARNING
        elif status_counts.get(HealthStatus.DOWN.value, 0) > 0:
            return HealthStatus.WARNING
        elif all(c.status == HealthStatus.HEALTHY for c in components):
            return HealthStatus.HEALTHY
        else:
            return HealthStatus.UNKNOWN

    def _generate_alerts(self, report: HealthReport) -> List[SystemAlert]:
        """Generate alerts based on health report"""
        alerts = []

        # Check component status changes
        if self.last_report:
            for component in report.components:
                prev_component = None
                for prev_comp in self.last_report.components:
                    if prev_comp.component_type == component.component_type:
                        prev_component = prev_comp
                        break

                if prev_component and prev_component.status != component.status:
                    if component.status in [HealthStatus.CRITICAL, HealthStatus.DOWN]:
                        severity = AlertSeverity.CRITICAL
                    elif component.status == HealthStatus.WARNING:
                        severity = AlertSeverity.WARNING
                    else:
                        severity = AlertSeverity.INFO

                    alert = SystemAlert(
                        alert_id=f"alert_{int(time.time())}_{component.component_type.value}",
                        severity=severity,
                        component=component.component_name,
                        message=f"Status changed from {prev_component.status.value} to {component.status.value}",
                        metadata={
                            "previous_status": prev_component.status.value,
                            "current_status": component.status.value,
                            "response_time": component.response_time
                        }
                    )
                    alerts.append(alert)

        # Check system metrics for alerts
        for metric in report.system_metrics:
            if metric.status == HealthStatus.CRITICAL:
                alert = SystemAlert(
                    alert_id=f"alert_{int(time.time())}_system_{metric.name}",
                    severity=AlertSeverity.CRITICAL,
                    component="System",
                    message=f"Critical system metric: {metric.name} = {metric.value}{metric.unit}",
                    metadata={
                        "metric_name": metric.name,
                        "metric_value": metric.value,
                        "threshold_critical": metric.threshold_critical
                    }
                )
                alerts.append(alert)
            elif metric.status == HealthStatus.WARNING:
                alert = SystemAlert(
                    alert_id=f"alert_{int(time.time())}_system_{metric.name}",
                    severity=AlertSeverity.WARNING,
                    component="System",
                    message=f"Warning system metric: {metric.name} = {metric.value}{metric.unit}",
                    metadata={
                        "metric_name": metric.name,
                        "metric_value": metric.value,
                        "threshold_warning": metric.threshold_warning
                    }
                )
                alerts.append(alert)

        return alerts

    def _generate_health_recommendations(self, report: HealthReport) -> List[str]:
        """Generate health recommendations"""
        recommendations = []

        # Check overall status
        if report.overall_status == HealthStatus.CRITICAL:
            recommendations.append("Immediate attention required - critical components are failing")
        elif report.overall_status == HealthStatus.WARNING:
            recommendations.append("Review warning conditions to prevent potential issues")

        # Check component-specific issues
        for component in report.components:
            if component.status == HealthStatus.DOWN:
                recommendations.append(f"Restore {component.component_name} - component is completely down")
            elif component.status == HealthStatus.CRITICAL:
                recommendations.append(f"Fix critical issues in {component.component_name}")
            elif component.response_time > 30:  # Slow response
                recommendations.append(f"Optimize performance of {component.component_name} (response time: {component.response_time:.2f}s)")

        # Check system metrics
        for metric in report.system_metrics:
            if metric.status == HealthStatus.CRITICAL:
                recommendations.append(f"Address critical system issue: high {metric.name.replace('_', ' ')}")
            elif metric.status == HealthStatus.WARNING:
                recommendations.append(f"Monitor {metric.name.replace('_', ' ')} levels")

        # General recommendations
        if len(report.alerts) > 5:
            recommendations.append("High number of alerts - review system configuration")

        if not recommendations:
            recommendations.append("System health is good - continue monitoring")

        return recommendations

    def get_current_health_status(self) -> Optional[HealthReport]:
        """Get the most recent health report"""
        return self.last_report

    def get_active_alerts(self) -> List[SystemAlert]:
        """Get all active (unresolved) alerts"""
        return [alert for alert in self.alerts if not alert.resolved]

    def resolve_alert(self, alert_id: str) -> bool:
        """Mark an alert as resolved"""
        for alert in self.alerts:
            if alert.alert_id == alert_id and not alert.resolved:
                alert.resolved = True
                alert.resolved_at = datetime.now()
                logger.info(f"Alert {alert_id} resolved")
                return True
        return False

    def export_health_report(self, filepath: str, report: Optional[HealthReport] = None) -> bool:
        """Export health report to file"""
        if report is None:
            report = self.last_report

        if not report:
            logger.warning("No health report available to export")
            return False

        try:
            export_data = {
                "report_id": report.report_id,
                "timestamp": report.timestamp.isoformat(),
                "overall_status": report.overall_status.value,
                "components": [
                    {
                        "type": comp.component_type.value,
                        "name": comp.component_name,
                        "status": comp.status.value,
                        "last_check": comp.last_check.isoformat(),
                        "response_time": comp.response_time,
                        "error_message": comp.error_message,
                        "metrics": [
                            {
                                "name": metric.name,
                                "value": metric.value,
                                "unit": metric.unit,
                                "status": metric.status.value,
                                "description": metric.description
                            }
                            for metric in comp.metrics
                        ]
                    }
                    for comp in report.components
                ],
                "system_metrics": [
                    {
                        "name": metric.name,
                        "value": metric.value,
                        "unit": metric.unit,
                        "status": metric.status.value,
                        "description": metric.description
                    }
                    for metric in report.system_metrics
                ],
                "alerts": [
                    {
                        "id": alert.alert_id,
                        "severity": alert.severity.value,
                        "component": alert.component,
                        "message": alert.message,
                        "timestamp": alert.timestamp.isoformat(),
                        "resolved": alert.resolved
                    }
                    for alert in report.alerts
                ],
                "recommendations": report.recommendations
            }

            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Health report exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to export health report: {e}")
            return False


# Factory function for easy instantiation
def create_system_health_monitor(workspace_path: Optional[str] = None, check_interval: int = 60) -> SystemHealthMonitor:
    """
    Factory function to create system health monitor

    Args:
        workspace_path: Path to workspace directory
        check_interval: Health check interval in seconds

    Returns:
        Configured SystemHealthMonitor instance
    """
    return SystemHealthMonitor(workspace_path=workspace_path, check_interval=check_interval)


# Command-line interface
def main():
    """Main CLI function for system health monitoring"""
    import argparse

    parser = argparse.ArgumentParser(
        description="L.I.F.E. Platform System Health Monitor"
    )
    parser.add_argument(
        "--workspace",
        "-w",
        default=None,
        help="Workspace directory path"
    )
    parser.add_argument(
        "--check-interval",
        "-i",
        type=int,
        default=60,
        help="Health check interval in seconds (default: 60)"
    )
    parser.add_argument(
        "--export",
        "-e",
        help="Export health report to specified file"
    )
    parser.add_argument(
        "--continuous",
        "-c",
        action="store_true",
        help="Run continuous monitoring (press Ctrl+C to stop)"
    )
    parser.add_argument(
        "--resolve-alert",
        "-r",
        help="Resolve alert with specified ID"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create health monitor
    monitor = create_system_health_monitor(
        workspace_path=args.workspace,
        check_interval=args.check_interval
    )

    print("L.I.F.E. Platform - System Health Monitor")
    print("=" * 50)
    print(f"Workspace: {args.workspace or os.getcwd()}")
    print(f"Check Interval: {args.check_interval} seconds")

    try:
        if args.resolve_alert:
            if monitor.resolve_alert(args.resolve_alert):
                print(f"Alert {args.resolve_alert} resolved successfully")
            else:
                print(f"Failed to resolve alert {args.resolve_alert}")
            return 0

        if args.continuous:
            print("\nStarting continuous health monitoring...")
            print("Press Ctrl+C to stop")

            asyncio.run(monitor.start_monitoring())

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping monitoring...")
                monitor.stop_monitoring()

        else:
            # Single health check
            print("\nPerforming health check...")
            report = asyncio.run(monitor.perform_health_check())

            print("\nHealth Check Results:")
            print(f"  Overall Status: {report.overall_status.value.upper()}")
            print(f"  Components Checked: {len(report.components)}")
            print(f"  Active Alerts: {len(report.alerts)}")

            if report.components:
                print("\nComponent Status:")
                for comp in report.components:
                    status_icon = {
                        HealthStatus.HEALTHY: "✅",
                        HealthStatus.WARNING: "⚠️",
                        HealthStatus.CRITICAL: "❌",
                        HealthStatus.DOWN: "🔴",
                        HealthStatus.UNKNOWN: "❓"
                    }.get(comp.status, "❓")

                    print(f"  {status_icon} {comp.component_name}: {comp.status.value} ({comp.response_time:.2f}s)")

            if report.system_metrics:
                print("\nSystem Metrics:")
                for metric in report.system_metrics:
                    status_icon = {
                        HealthStatus.HEALTHY: "✅",
                        HealthStatus.WARNING: "⚠️",
                        HealthStatus.CRITICAL: "❌"
                    }.get(metric.status, "❓")

                    print(f"  {status_icon} {metric.name}: {metric.value}{metric.unit}")

            if report.alerts:
                print("\nActive Alerts:")
                for alert in report.alerts[:5]:  # Show first 5
                    severity_icon = {
                        AlertSeverity.INFO: "ℹ️",
                        AlertSeverity.WARNING: "⚠️",
                        AlertSeverity.ERROR: "❌",
                        AlertSeverity.CRITICAL: "🚨"
                    }.get(alert.severity, "❓")

                    print(f"  {severity_icon} {alert.component}: {alert.message}")

            if report.recommendations:
                print("\nRecommendations:")
                for rec in report.recommendations:
                    print(f"  • {rec}")

        if args.export:
            if monitor.export_health_report(args.export):
                print(f"\nHealth report exported to {args.export}")
            else:
                print("\nFailed to export health report")
                return 1

        # Return appropriate exit code
        if monitor.last_report and monitor.last_report.overall_status == HealthStatus.CRITICAL:
            print("\n❌ Critical health issues detected")
            return 1
        elif monitor.last_report and monitor.last_report.overall_status == HealthStatus.WARNING:
            print("\n⚠️ Health warnings detected")
            return 1
        else:
            print("\n✅ System health is good")
            return 0

    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
        monitor.stop_monitoring()
        return 1
    except Exception as e:
        print(f"\nHealth monitoring failed: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())    sys.exit(main())