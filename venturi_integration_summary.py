#!/usr/bin/env python3
"""
Venturi Integration Summary - Performance Reporting and System Analytics
L.I.F.E. Platform comprehensive integration summary and performance analytics

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import json
import logging
import random
import statistics
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# import numpy as np  # Temporarily commented out due to space constraints

logger = logging.getLogger(__name__)


@dataclass
class SystemMetric:
    """Individual system performance metric"""

    component: str
    metric_name: str
    value: float
    timestamp: datetime
    unit: str
    status: str  # 'normal', 'warning', 'critical'


@dataclass
class IntegrationSummary:
    """Summary of system integration status"""

    timestamp: datetime
    overall_status: str
    component_status: Dict[str, str]
    performance_metrics: Dict[str, float]
    alerts: List[str]
    recommendations: List[str]


class VenturiIntegrationSummarizer:
    """
    Comprehensive integration summary and performance reporting system
    Aggregates data from all Venturi components for system-wide analytics
    """

    def __init__(
        self,
        metrics_db_path: str = "venturi_metrics.json",
        summary_db_path: str = "integration_summaries.json",
    ):
        self.metrics_db_path = Path(metrics_db_path)
        self.summary_db_path = Path(summary_db_path)

        self.metrics: List[SystemMetric] = []
        self.summaries: List[IntegrationSummary] = []

        self.load_data()

    def load_data(self) -> None:
        """Load metrics and summary data from disk"""
        # Load metrics
        if self.metrics_db_path.exists():
            try:
                with open(self.metrics_db_path, "r") as f:
                    data = json.load(f)
                    for metric_data in data.get("metrics", []):
                        # Convert timestamp string back to datetime
                        metric_data["timestamp"] = datetime.fromisoformat(
                            metric_data["timestamp"]
                        )
                        metric = SystemMetric(**metric_data)
                        self.metrics.append(metric)
                logger.info(f"Loaded {len(self.metrics)} system metrics")
            except Exception as e:
                logger.error(f"Failed to load metrics database: {e}")

        # Load summaries
        if self.summary_db_path.exists():
            try:
                with open(self.summary_db_path, "r") as f:
                    data = json.load(f)
                    for summary_data in data.get("summaries", []):
                        # Convert timestamp string back to datetime
                        summary_data["timestamp"] = datetime.fromisoformat(
                            summary_data["timestamp"]
                        )
                        summary = IntegrationSummary(**summary_data)
                        self.summaries.append(summary)
                logger.info(f"Loaded {len(self.summaries)} integration summaries")
            except Exception as e:
                logger.error(f"Failed to load summaries database: {e}")

    def save_data(self) -> None:
        """Save metrics and summary data to disk"""
        # Save metrics
        metrics_data = {
            "last_updated": datetime.now().isoformat(),
            "metrics": [
                {**metric.__dict__, "timestamp": metric.timestamp.isoformat()}
                for metric in self.metrics[-1000:]  # Keep last 1000 metrics
            ],
        }

        try:
            with open(self.metrics_db_path, "w") as f:
                json.dump(metrics_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")

        # Save summaries
        summaries_data = {
            "last_updated": datetime.now().isoformat(),
            "summaries": [
                {**summary.__dict__, "timestamp": summary.timestamp.isoformat()}
                for summary in self.summaries[-100:]  # Keep last 100 summaries
            ],
        }

        try:
            with open(self.summary_db_path, "w") as f:
                json.dump(summaries_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save summaries: {e}")

    def record_metric(
        self,
        component: str,
        metric_name: str,
        value: float,
        unit: str = "",
        status: str = "normal",
    ) -> None:
        """Record a new system metric"""
        metric = SystemMetric(
            component=component,
            metric_name=metric_name,
            value=value,
            timestamp=datetime.now(),
            unit=unit,
            status=status,
        )

        self.metrics.append(metric)

        # Auto-save periodically (every 10 metrics)
        if len(self.metrics) % 10 == 0:
            self.save_data()

        logger.debug(f"Recorded metric: {component}.{metric_name} = {value} {unit}")

    def generate_integration_summary(self) -> IntegrationSummary:
        """Generate comprehensive integration summary"""
        now = datetime.now()

        # Analyze component status
        component_status = self._analyze_component_status()

        # Calculate performance metrics
        performance_metrics = self._calculate_performance_metrics()

        # Generate alerts
        alerts = self._generate_alerts(component_status, performance_metrics)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            component_status, performance_metrics
        )

        # Determine overall status
        overall_status = self._determine_overall_status(component_status, alerts)

        summary = IntegrationSummary(
            timestamp=now,
            overall_status=overall_status,
            component_status=component_status,
            performance_metrics=performance_metrics,
            alerts=alerts,
            recommendations=recommendations,
        )

        self.summaries.append(summary)
        self.save_data()

        logger.info(f"Generated integration summary: {overall_status}")

        return summary

    def _analyze_component_status(self) -> Dict[str, str]:
        """Analyze status of each system component"""
        component_status = {}
        recent_metrics = self._get_recent_metrics(hours=1)

        # Group metrics by component
        component_metrics = defaultdict(list)
        for metric in recent_metrics:
            component_metrics[metric.component].append(metric)

        # Analyze each component
        for component, metrics in component_metrics.items():
            if not metrics:
                component_status[component] = "unknown"
                continue

            # Check for critical issues
            critical_count = sum(1 for m in metrics if m.status == "critical")
            warning_count = sum(1 for m in metrics if m.status == "warning")
            normal_count = sum(1 for m in metrics if m.status == "normal")

            total_metrics = len(metrics)

            if critical_count > 0:
                status = "critical"
            elif warning_count / total_metrics > 0.3:  # >30% warnings
                status = "warning"
            elif normal_count / total_metrics > 0.8:  # >80% normal
                status = "healthy"
            else:
                status = "degraded"

            component_status[component] = status

        return component_status

    def _calculate_performance_metrics(self) -> Dict[str, float]:
        """Calculate key performance metrics across the system"""
        recent_metrics = self._get_recent_metrics(hours=24)

        if not recent_metrics:
            return {}

        metrics_summary = {}

        # Overall system efficiency
        efficiency_metrics = [
            m for m in recent_metrics if "efficiency" in m.metric_name.lower()
        ]
        if efficiency_metrics:
            metrics_summary["system_efficiency"] = sum(
                m.value for m in efficiency_metrics
            ) / len(efficiency_metrics)

        # Average processing latency
        latency_metrics = [
            m for m in recent_metrics if "latency" in m.metric_name.lower()
        ]
        if latency_metrics:
            metrics_summary["avg_processing_latency"] = sum(
                m.value for m in latency_metrics
            ) / len(latency_metrics)

        # Throughput metrics
        throughput_metrics = [
            m for m in recent_metrics if "throughput" in m.metric_name.lower()
        ]
        if throughput_metrics:
            metrics_summary["avg_throughput"] = sum(
                m.value for m in throughput_metrics
            ) / len(throughput_metrics)

        # Error rates
        error_metrics = [m for m in recent_metrics if "error" in m.metric_name.lower()]
        if error_metrics:
            metrics_summary["error_rate"] = sum(m.value for m in error_metrics) / len(
                error_metrics
            )

        # Resource utilization
        cpu_metrics = [m for m in recent_metrics if "cpu" in m.metric_name.lower()]
        if cpu_metrics:
            metrics_summary["avg_cpu_utilization"] = sum(
                m.value for m in cpu_metrics
            ) / len(cpu_metrics)

        memory_metrics = [
            m for m in recent_metrics if "memory" in m.metric_name.lower()
        ]
        if memory_metrics:
            metrics_summary["avg_memory_utilization"] = sum(
                m.value for m in memory_metrics
            ) / len(memory_metrics)

        return metrics_summary

    def _generate_alerts(
        self, component_status: Dict[str, str], performance_metrics: Dict[str, float]
    ) -> List[str]:
        """Generate system alerts based on current status"""
        alerts = []

        # Component status alerts
        critical_components = [
            comp for comp, status in component_status.items() if status == "critical"
        ]
        if critical_components:
            alerts.append(
                f"🚨 CRITICAL: Components failing - {', '.join(critical_components)}"
            )

        warning_components = [
            comp for comp, status in component_status.items() if status == "warning"
        ]
        if warning_components:
            alerts.append(
                f"⚠️  WARNING: Components degraded - {', '.join(warning_components)}"
            )

        # Performance alerts
        if "system_efficiency" in performance_metrics:
            efficiency = performance_metrics["system_efficiency"]
            if efficiency < 0.7:
                alerts.append(
                    f"⚠️  LOW EFFICIENCY: System efficiency at {efficiency:.1%}"
                )

        if "error_rate" in performance_metrics:
            error_rate = performance_metrics["error_rate"]
            if error_rate > 0.05:  # >5% error rate
                alerts.append(f"🚨 HIGH ERROR RATE: {error_rate:.1%} errors detected")

        if "avg_cpu_utilization" in performance_metrics:
            cpu_usage = performance_metrics["avg_cpu_utilization"]
            if cpu_usage > 0.9:  # >90% CPU
                alerts.append(f"⚠️  HIGH CPU USAGE: {cpu_usage:.1%} CPU utilization")

        return alerts

    def _generate_recommendations(
        self, component_status: Dict[str, str], performance_metrics: Dict[str, float]
    ) -> List[str]:
        """Generate system improvement recommendations"""
        recommendations = []

        # Component-specific recommendations
        for component, status in component_status.items():
            if status == "critical":
                recommendations.append(
                    f"🔧 IMMEDIATE: Investigate and repair {component}"
                )
            elif status == "warning":
                recommendations.append(
                    f"🔍 MONITOR: Keep close watch on {component} performance"
                )

        # Performance-based recommendations
        if "system_efficiency" in performance_metrics:
            efficiency = performance_metrics["system_efficiency"]
            if efficiency < 0.8:
                recommendations.append(
                    "⚡ OPTIMIZE: Run Venturi batching optimization to improve efficiency"
                )

        if "avg_processing_latency" in performance_metrics:
            latency = performance_metrics["avg_processing_latency"]
            if latency > 0.1:  # >100ms
                recommendations.append(
                    "🏃‍♂️ SPEED UP: Consider parallel processing or caching optimizations"
                )

        if "error_rate" in performance_metrics:
            error_rate = performance_metrics["error_rate"]
            if error_rate > 0.02:  # >2%
                recommendations.append(
                    "🐛 DEBUG: Run resilience tests to identify error sources"
                )

        # General recommendations
        if not recommendations:
            recommendations.append(
                "✅ SYSTEM HEALTHY: All components operating normally"
            )

        return recommendations

    def _determine_overall_status(
        self, component_status: Dict[str, str], alerts: List[str]
    ) -> str:
        """Determine overall system status"""
        if any(status == "critical" for status in component_status.values()):
            return "CRITICAL"

        critical_alerts = sum(1 for alert in alerts if "🚨 CRITICAL" in alert)
        if critical_alerts > 0:
            return "CRITICAL"

        warning_components = sum(
            1 for status in component_status.values() if status == "warning"
        )
        warning_alerts = sum(1 for alert in alerts if "⚠️" in alert)

        if warning_components > 0 or warning_alerts > 0:
            return "WARNING"

        if all(
            status in ["healthy", "unknown"] for status in component_status.values()
        ):
            return "HEALTHY"

        return "DEGRADED"

    def _get_recent_metrics(self, hours: int = 24) -> List[SystemMetric]:
        """Get metrics from the last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [m for m in self.metrics if m.timestamp > cutoff]

    def get_comprehensive_report(self) -> str:
        """Generate comprehensive system report"""
        if not self.summaries:
            return "No integration summaries available. Run generate_integration_summary() first."

        latest_summary = self.summaries[-1]

        report_lines = []
        report_lines.append("VENTURI INTEGRATION SUMMARY REPORT")
        report_lines.append("=" * 50)
        report_lines.append(
            f"Generated: {latest_summary.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        report_lines.append(f"Overall Status: {latest_summary.overall_status}")
        report_lines.append("")

        # Component Status
        report_lines.append("COMPONENT STATUS")
        report_lines.append("-" * 20)
        for component, status in latest_summary.component_status.items():
            status_icon = {
                "healthy": "✅",
                "warning": "⚠️",
                "critical": "🚨",
                "degraded": "🟡",
                "unknown": "❓",
            }.get(status, "❓")
            report_lines.append(f"{status_icon} {component}: {status.upper()}")
        report_lines.append("")

        # Performance Metrics
        report_lines.append("PERFORMANCE METRICS")
        report_lines.append("-" * 20)
        for metric, value in latest_summary.performance_metrics.items():
            if "rate" in metric or "utilization" in metric:
                report_lines.append(f"• {metric}: {value:.1%}")
            elif "latency" in metric:
                report_lines.append(f"• {metric}: {value:.3f}s")
            else:
                report_lines.append(f"• {metric}: {value:.3f}")
        report_lines.append("")

        # Alerts
        if latest_summary.alerts:
            report_lines.append("ACTIVE ALERTS")
            report_lines.append("-" * 15)
            for alert in latest_summary.alerts:
                report_lines.append(f"• {alert}")
            report_lines.append("")

        # Recommendations
        if latest_summary.recommendations:
            report_lines.append("RECOMMENDATIONS")
            report_lines.append("-" * 15)
            for rec in latest_summary.recommendations:
                report_lines.append(f"• {rec}")
            report_lines.append("")

        # Historical Summary
        if len(self.summaries) > 1:
            report_lines.append("HISTORICAL TREND (Last 7 Summaries)")
            report_lines.append("-" * 35)

            recent_summaries = self.summaries[-7:]
            status_counts = defaultdict(int)

            for summary in recent_summaries:
                status_counts[summary.overall_status] += 1

            for status, count in status_counts.items():
                percentage = count / len(recent_summaries) * 100
                report_lines.append(f"• {status}: {count} times ({percentage:.1f}%)")

        return "\n".join(report_lines)

    def add_sample_metrics(self) -> None:
        """Add sample metrics for demonstration"""
        components = [
            "venturi_gates",
            "venturi_batching",
            "venturi_resilience",
            "venturi_research",
        ]

        for component in components:
            # Add normal metrics
            self.record_metric(component, "efficiency", random.uniform(0.8, 0.95))
            self.record_metric(
                component, "latency", random.uniform(0.02, 0.08), "seconds"
            )
            self.record_metric(
                component, "throughput", random.uniform(100, 500), "ops/sec"
            )
            self.record_metric(component, "error_rate", random.uniform(0.001, 0.01))
            self.record_metric(component, "cpu_utilization", random.uniform(0.3, 0.7))
            self.record_metric(
                component, "memory_utilization", random.uniform(0.4, 0.8)
            )

        logger.info("Added sample metrics for demonstration")


# Global integration summarizer instance
integration_summarizer = VenturiIntegrationSummarizer()


def generate_system_report() -> None:
    """Generate and display comprehensive system report"""
    print("📊 Venturi Integration Summary")
    print("=" * 40)

    # Add sample data if no metrics exist
    if not integration_summarizer.metrics:
        integration_summarizer.add_sample_metrics()

    # Generate summary
    summary = integration_summarizer.generate_integration_summary()

    print(f"Overall Status: {summary.overall_status}")
    print(f"Components: {len(summary.component_status)}")
    print(f"Active Alerts: {len(summary.alerts)}")
    print(f"Recommendations: {len(summary.recommendations)}")

    # Show detailed report
    report = integration_summarizer.get_comprehensive_report()
    print(f"\n📋 Full Report ({len(report.split())} lines)")
    print("-" * 40)
    print(report)


if __name__ == "__main__":
    generate_system_report()
