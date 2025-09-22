#!/usr/bin/env python3
"""
L.I.F.E. Platform - KPI Configuration System
Key Performance Indicators configuration and monitoring framework

This module provides comprehensive KPI configuration for the L.I.F.E. Platform,
including performance metrics, business metrics, and technical indicators.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KPICategory(Enum):
    """KPI categories for organization"""

    PERFORMANCE = "performance"
    BUSINESS = "business"
    TECHNICAL = "technical"
    COMPLIANCE = "compliance"
    USER_EXPERIENCE = "user_experience"
    FINANCIAL = "financial"


class KPIPriority(Enum):
    """KPI priority levels"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class KPIStatus(Enum):
    """KPI status indicators"""

    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    OFF_TRACK = "off_track"
    ACHIEVED = "achieved"


@dataclass
class KPITarget:
    """KPI target configuration"""

    value: Union[float, int]
    unit: str
    timeframe: str  # e.g., "monthly", "quarterly", "yearly"
    comparison: str = "greater_than"  # greater_than, less_than, equal_to
    tolerance: float = 0.05  # 5% tolerance for target achievement


@dataclass
class KPIThreshold:
    """KPI threshold configuration"""

    warning: Union[float, int]
    critical: Union[float, int]
    direction: str = (
        "ascending"  # ascending (higher better) or descending (lower better)
    )


@dataclass
class KPIConfig:
    """Complete KPI configuration"""

    id: str
    name: str
    description: str
    category: KPICategory
    priority: KPIPriority
    target: KPITarget
    threshold: KPIThreshold
    calculation_method: str
    data_source: str
    update_frequency: str  # e.g., "real_time", "hourly", "daily"
    owner: str
    tags: List[str] = field(default_factory=list)
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class KPIMeasurement:
    """KPI measurement data point"""

    kpi_id: str
    value: Union[float, int]
    timestamp: datetime
    status: KPIStatus
    metadata: Dict[str, Any] = field(default_factory=dict)


class KPIConfigurationManager:
    """
    Manages KPI configurations for the L.I.F.E. Platform

    Provides centralized configuration management for all KPIs,
    including performance targets, thresholds, and monitoring settings.
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.kpis: Dict[str, KPIConfig] = {}
        self.measurements: Dict[str, List[KPIMeasurement]] = {}
        self._load_default_configurations()

        logger.info(f"KPI Configuration Manager initialized with {len(self.kpis)} KPIs")

    def _load_default_configurations(self):
        """Load default KPI configurations for L.I.F.E. Platform"""
        default_kpis = [
            # Performance KPIs
            KPIConfig(
                id="latency_ms",
                name="Processing Latency",
                description="Average EEG signal processing latency (ms)",
                category=KPICategory.PERFORMANCE,
                priority=KPIPriority.CRITICAL,
                target=KPITarget(value=0.9, unit="ms", timeframe="real_time"),
                threshold=KPIThreshold(warning=1.5, critical=2.0),
                calculation_method="average",
                data_source="performance_monitor",
                update_frequency="real_time",
                owner="Platform Team",
                tags=["latency", "performance", "real_time"],
            ),
            KPIConfig(
                id="accuracy_percent",
                name="Classification Accuracy",
                description="EEG pattern classification accuracy percentage",
                category=KPICategory.PERFORMANCE,
                priority=KPIPriority.CRITICAL,
                target=KPITarget(value=82.0, unit="%", timeframe="monthly"),
                threshold=KPIThreshold(warning=75.0, critical=70.0),
                calculation_method="weighted_average",
                data_source="accuracy_ensemble_classifier",
                update_frequency="daily",
                owner="ML Team",
                tags=["accuracy", "classification", "ml"],
            ),
            KPIConfig(
                id="throughput_ops_sec",
                name="Processing Throughput",
                description="Number of EEG processing operations per second",
                category=KPICategory.PERFORMANCE,
                priority=KPIPriority.HIGH,
                target=KPITarget(value=80.16, unit="ops/sec", timeframe="real_time"),
                threshold=KPIThreshold(warning=60.0, critical=40.0),
                calculation_method="rate",
                data_source="performance_monitor",
                update_frequency="real_time",
                owner="Platform Team",
                tags=["throughput", "performance", "scalability"],
            ),
            # Business KPIs
            KPIConfig(
                id="monthly_revenue",
                name="Monthly Recurring Revenue",
                description="Monthly recurring revenue from subscriptions",
                category=KPICategory.BUSINESS,
                priority=KPIPriority.CRITICAL,
                target=KPITarget(value=50000, unit="USD", timeframe="monthly"),
                threshold=KPIThreshold(warning=35000, critical=25000),
                calculation_method="sum",
                data_source="billing_system",
                update_frequency="daily",
                owner="Business Team",
                tags=["revenue", "business", "financial"],
            ),
            KPIConfig(
                id="user_acquisition",
                name="Monthly Active Users",
                description="Number of monthly active users",
                category=KPICategory.BUSINESS,
                priority=KPIPriority.HIGH,
                target=KPITarget(value=1000, unit="users", timeframe="monthly"),
                threshold=KPIThreshold(warning=750, critical=500),
                calculation_method="count_unique",
                data_source="user_analytics",
                update_frequency="daily",
                owner="Growth Team",
                tags=["users", "growth", "engagement"],
            ),
            KPIConfig(
                id="customer_satisfaction",
                name="Customer Satisfaction Score",
                description="Average customer satisfaction rating (1-5 scale)",
                category=KPICategory.BUSINESS,
                priority=KPIPriority.HIGH,
                target=KPITarget(value=4.5, unit="score", timeframe="monthly"),
                threshold=KPIThreshold(warning=4.0, critical=3.5),
                calculation_method="average",
                data_source="survey_system",
                update_frequency="weekly",
                owner="Customer Success",
                tags=["satisfaction", "feedback", "retention"],
            ),
            # Technical KPIs
            KPIConfig(
                id="uptime_percent",
                name="Platform Uptime",
                description="Percentage of time the platform is operational",
                category=KPICategory.TECHNICAL,
                priority=KPIPriority.CRITICAL,
                target=KPITarget(value=99.9, unit="%", timeframe="monthly"),
                threshold=KPIThreshold(
                    warning=99.5, critical=99.0, direction="ascending"
                ),
                calculation_method="uptime_percentage",
                data_source="monitoring_system",
                update_frequency="real_time",
                owner="DevOps Team",
                tags=["uptime", "reliability", "availability"],
            ),
            KPIConfig(
                id="error_rate",
                name="Application Error Rate",
                description="Percentage of requests that result in errors",
                category=KPICategory.TECHNICAL,
                priority=KPIPriority.HIGH,
                target=KPITarget(value=0.1, unit="%", timeframe="daily"),
                threshold=KPIThreshold(
                    warning=1.0, critical=5.0, direction="descending"
                ),
                calculation_method="error_percentage",
                data_source="application_logs",
                update_frequency="hourly",
                owner="DevOps Team",
                tags=["errors", "reliability", "monitoring"],
            ),
            KPIConfig(
                id="memory_usage_mb",
                name="Memory Usage",
                description="Average memory usage in megabytes",
                category=KPICategory.TECHNICAL,
                priority=KPIPriority.MEDIUM,
                target=KPITarget(
                    value=512, unit="MB", timeframe="real_time", comparison="less_than"
                ),
                threshold=KPIThreshold(
                    warning=1024, critical=2048, direction="descending"
                ),
                calculation_method="average",
                data_source="system_monitor",
                update_frequency="real_time",
                owner="DevOps Team",
                tags=["memory", "resources", "optimization"],
            ),
            # Compliance KPIs
            KPIConfig(
                id="audit_compliance",
                name="Audit Compliance Score",
                description="Percentage compliance with regulatory audit requirements",
                category=KPICategory.COMPLIANCE,
                priority=KPIPriority.CRITICAL,
                target=KPITarget(value=100.0, unit="%", timeframe="quarterly"),
                threshold=KPIThreshold(warning=95.0, critical=90.0),
                calculation_method="compliance_score",
                data_source="audit_system",
                update_frequency="weekly",
                owner="Compliance Team",
                tags=["compliance", "audit", "regulatory"],
            ),
            KPIConfig(
                id="data_security_score",
                name="Data Security Score",
                description="Security posture assessment score",
                category=KPICategory.COMPLIANCE,
                priority=KPIPriority.HIGH,
                target=KPITarget(value=95.0, unit="score", timeframe="monthly"),
                threshold=KPIThreshold(warning=85.0, critical=75.0),
                calculation_method="security_assessment",
                data_source="security_monitor",
                update_frequency="daily",
                owner="Security Team",
                tags=["security", "compliance", "risk"],
            ),
            # User Experience KPIs
            KPIConfig(
                id="response_time",
                name="API Response Time",
                description="Average API response time in milliseconds",
                category=KPICategory.USER_EXPERIENCE,
                priority=KPIPriority.HIGH,
                target=KPITarget(
                    value=200, unit="ms", timeframe="real_time", comparison="less_than"
                ),
                threshold=KPIThreshold(
                    warning=500, critical=1000, direction="descending"
                ),
                calculation_method="percentile_95",
                data_source="api_monitor",
                update_frequency="real_time",
                owner="Engineering Team",
                tags=["response_time", "api", "user_experience"],
            ),
            KPIConfig(
                id="user_session_duration",
                name="Average Session Duration",
                description="Average user session duration in minutes",
                category=KPICategory.USER_EXPERIENCE,
                priority=KPIPriority.MEDIUM,
                target=KPITarget(value=15.0, unit="minutes", timeframe="daily"),
                threshold=KPIThreshold(warning=10.0, critical=5.0),
                calculation_method="average",
                data_source="analytics_platform",
                update_frequency="daily",
                owner="Product Team",
                tags=["engagement", "retention", "user_experience"],
            ),
        ]

        for kpi in default_kpis:
            self.kpis[kpi.id] = kpi
            self.measurements[kpi.id] = []

    def get_kpi_config(self, kpi_id: str) -> Optional[KPIConfig]:
        """Get KPI configuration by ID"""
        return self.kpis.get(kpi_id)

    def get_kpis_by_category(self, category: KPICategory) -> List[KPIConfig]:
        """Get all KPIs in a specific category"""
        return [kpi for kpi in self.kpis.values() if kpi.category == category]

    def get_kpis_by_priority(self, priority: KPIPriority) -> List[KPIConfig]:
        """Get all KPIs with a specific priority"""
        return [kpi for kpi in self.kpis.values() if kpi.priority == priority]

    def add_kpi(self, kpi_config: KPIConfig) -> bool:
        """Add a new KPI configuration"""
        if kpi_config.id in self.kpis:
            logger.warning(f"KPI {kpi_config.id} already exists")
            return False

        self.kpis[kpi_config.id] = kpi_config
        self.measurements[kpi_config.id] = []
        logger.info(f"Added new KPI: {kpi_config.name}")
        return True

    def update_kpi(self, kpi_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing KPI configuration"""
        if kpi_id not in self.kpis:
            logger.warning(f"KPI {kpi_id} not found")
            return False

        kpi = self.kpis[kpi_id]
        for key, value in updates.items():
            if hasattr(kpi, key):
                setattr(kpi, key, value)

        kpi.updated_at = datetime.now()
        logger.info(f"Updated KPI: {kpi_id}")
        return True

    def remove_kpi(self, kpi_id: str) -> bool:
        """Remove a KPI configuration"""
        if kpi_id not in self.kpis:
            logger.warning(f"KPI {kpi_id} not found")
            return False

        del self.kpis[kpi_id]
        del self.measurements[kpi_id]
        logger.info(f"Removed KPI: {kpi_id}")
        return True

    def record_measurement(self, measurement: KPIMeasurement) -> bool:
        """Record a KPI measurement"""
        if measurement.kpi_id not in self.kpis:
            logger.warning(f"KPI {measurement.kpi_id} not found")
            return False

        self.measurements[measurement.kpi_id].append(measurement)

        # Keep only recent measurements (last 1000 per KPI)
        if len(self.measurements[measurement.kpi_id]) > 1000:
            self.measurements[measurement.kpi_id].pop(0)

        logger.debug(
            f"Recorded measurement for KPI {measurement.kpi_id}: {measurement.value}"
        )
        return True

    def get_kpi_status(self, kpi_id: str) -> Optional[KPIStatus]:
        """Get current status of a KPI"""
        if kpi_id not in self.measurements or not self.measurements[kpi_id]:
            return None

        kpi_config = self.kpis[kpi_id]
        latest_measurement = self.measurements[kpi_id][-1]

        # Determine status based on thresholds and target
        value = latest_measurement.value
        target = kpi_config.target.value
        tolerance = kpi_config.target.tolerance

        # Check if within tolerance of target
        if abs(value - target) / target <= tolerance:
            return KPIStatus.ON_TRACK
        elif abs(value - target) / target <= tolerance * 2:
            return KPIStatus.AT_RISK
        else:
            return KPIStatus.OFF_TRACK

    def get_kpi_trend(self, kpi_id: str, hours: int = 24) -> Dict[str, Any]:
        """Get KPI trend analysis for the specified time period"""
        if kpi_id not in self.measurements:
            return {"error": "KPI not found"}

        measurements = self.measurements[kpi_id]
        cutoff_time = datetime.now() - timedelta(hours=hours)

        recent_measurements = [m for m in measurements if m.timestamp >= cutoff_time]

        if not recent_measurements:
            return {"error": "No recent measurements"}

        values = [m.value for m in recent_measurements]

        return {
            "kpi_id": kpi_id,
            "period_hours": hours,
            "measurement_count": len(values),
            "current_value": values[-1],
            "average_value": sum(values) / len(values),
            "min_value": min(values),
            "max_value": max(values),
            "trend_direction": "increasing" if values[-1] > values[0] else "decreasing",
            "volatility": 0.0,  # np.std(values) if len(values) > 1 else 0
        }

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get comprehensive dashboard summary of all KPIs"""
        summary = {
            "total_kpis": len(self.kpis),
            "kpis_by_category": {},
            "kpis_by_status": {},
            "critical_kpis": [],
            "at_risk_kpis": [],
            "overall_health_score": 0.0,
        }

        # Initialize category and status counters
        for category in KPICategory:
            summary["kpis_by_category"][category.value] = 0
        for status in KPIStatus:
            summary["kpis_by_status"][status.value] = 0

        total_score = 0
        scored_kpis = 0

        for kpi_id, kpi_config in self.kpis.items():
            if not kpi_config.enabled:
                continue

            # Count by category
            summary["kpis_by_category"][kpi_config.category.value] += 1

            # Get status and count
            status = self.get_kpi_status(kpi_id)
            if status:
                summary["kpis_by_status"][status.value] += 1

                # Track critical and at-risk KPIs
                if kpi_config.priority == KPIPriority.CRITICAL:
                    if status == KPIStatus.AT_RISK:
                        summary["at_risk_kpis"].append(kpi_id)
                    elif status == KPIStatus.OFF_TRACK:
                        summary["critical_kpis"].append(kpi_id)

                # Calculate health score contribution
                status_score = {
                    KPIStatus.ACHIEVED: 1.0,
                    KPIStatus.ON_TRACK: 0.9,
                    KPIStatus.AT_RISK: 0.6,
                    KPIStatus.OFF_TRACK: 0.3,
                }.get(status, 0.5)

                priority_weight = {
                    KPIPriority.CRITICAL: 1.0,
                    KPIPriority.HIGH: 0.8,
                    KPIPriority.MEDIUM: 0.6,
                    KPIPriority.LOW: 0.4,
                }.get(kpi_config.priority, 0.5)

                total_score += status_score * priority_weight
                scored_kpis += 1

        # Calculate overall health score
        if scored_kpis > 0:
            summary["overall_health_score"] = total_score / scored_kpis

        return summary

    def export_config(self, filepath: str) -> bool:
        """Export KPI configurations to JSON file"""
        try:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "kpi_count": len(self.kpis),
                "kpis": {},
            }

            for kpi_id, kpi_config in self.kpis.items():
                export_data["kpis"][kpi_id] = {
                    "id": kpi_config.id,
                    "name": kpi_config.name,
                    "description": kpi_config.description,
                    "category": kpi_config.category.value,
                    "priority": kpi_config.priority.value,
                    "target": {
                        "value": kpi_config.target.value,
                        "unit": kpi_config.target.unit,
                        "timeframe": kpi_config.target.timeframe,
                    },
                    "threshold": {
                        "warning": kpi_config.threshold.warning,
                        "critical": kpi_config.threshold.critical,
                    },
                    "calculation_method": kpi_config.calculation_method,
                    "data_source": kpi_config.data_source,
                    "update_frequency": kpi_config.update_frequency,
                    "owner": kpi_config.owner,
                    "tags": kpi_config.tags,
                    "enabled": kpi_config.enabled,
                }

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Exported KPI configuration to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to export KPI configuration: {e}")
            return False

    def import_config(self, filepath: str) -> bool:
        """Import KPI configurations from JSON file"""
        try:
            with open(filepath, "r") as f:
                import_data = json.load(f)

            imported_count = 0
            for kpi_id, kpi_data in import_data.get("kpis", {}).items():
                # Convert string enums back to enum objects
                kpi_config = KPIConfig(
                    id=kpi_data["id"],
                    name=kpi_data["name"],
                    description=kpi_data["description"],
                    category=KPICategory(kpi_data["category"]),
                    priority=KPIPriority(kpi_data["priority"]),
                    target=KPITarget(**kpi_data["target"]),
                    threshold=KPIThreshold(**kpi_data["threshold"]),
                    calculation_method=kpi_data["calculation_method"],
                    data_source=kpi_data["data_source"],
                    update_frequency=kpi_data["update_frequency"],
                    owner=kpi_data["owner"],
                    tags=kpi_data["tags"],
                    enabled=kpi_data["enabled"],
                )

                if self.add_kpi(kpi_config):
                    imported_count += 1

            logger.info(f"Imported {imported_count} KPI configurations from {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to import KPI configuration: {e}")
            return False


# Factory function for easy instantiation
def create_kpi_manager(config_path: Optional[str] = None) -> KPIConfigurationManager:
    """
    Factory function to create a KPI configuration manager

    Args:
        config_path: Optional path to configuration file

    Returns:
        Configured KPIConfigurationManager instance
    """
    return KPIConfigurationManager(config_path)


# Example usage and demonstration
def demonstrate_kpi_config():
    """Demonstrate the KPI configuration system"""
    print("📊 KPI Configuration System Demonstration")
    print("=" * 60)

    # Create KPI manager
    kpi_manager = create_kpi_manager()

    print(f"📋 Loaded {len(kpi_manager.kpis)} default KPIs")

    # Display KPIs by category
    print("\n🏷️ KPIs by Category:")
    for category in KPICategory:
        kpis = kpi_manager.get_kpis_by_category(category)
        print(f"  {category.value.title()}: {len(kpis)} KPIs")

    # Display critical KPIs
    print("\n🚨 Critical Priority KPIs:")
    critical_kpis = kpi_manager.get_kpis_by_priority(KPIPriority.CRITICAL)
    for kpi in critical_kpis[:5]:  # Show first 5
        print(
            f"  • {kpi.name} ({kpi.id}) - Target: {kpi.target.value}{kpi.target.unit}"
        )

    # Simulate some measurements
    print("\n📈 Simulating KPI Measurements...")
    import random

    # Simulate measurements for key KPIs
    test_kpis = ["latency_ms", "accuracy_percent", "throughput_ops_sec"]

    for kpi_id in test_kpis:
        kpi_config = kpi_manager.get_kpi_config(kpi_id)
        if kpi_config:
            # Generate realistic measurement values
            value = 0.0  # Default value
            if kpi_id == "latency_ms":
                value = random.uniform(0.5, 1.2)  # Around target of 0.9ms
            elif kpi_id == "accuracy_percent":
                value = random.uniform(78, 85)  # Around target of 82%
            elif kpi_id == "throughput_ops_sec":
                value = random.uniform(75, 85)  # Around target of 80.16

            measurement = KPIMeasurement(
                kpi_id=kpi_id,
                value=value,
                timestamp=datetime.now(),
                status=KPIStatus.ON_TRACK,
            )

            kpi_manager.record_measurement(measurement)
            status = kpi_manager.get_kpi_status(kpi_id)
            status_str = status.value if status else "unknown"
            name = kpi_config.name
            unit = kpi_config.target.unit
            print(f"  {name}: {value:.2f}{unit} - Status: {status_str}")

    # Get dashboard summary
    print("\n📊 Dashboard Summary:")
    summary = kpi_manager.get_dashboard_summary()
    print(f"  Total KPIs: {summary['total_kpis']}")
    print(f"  Overall Health Score: {summary['overall_health_score']:.2f}")
    print(f"  Critical Issues: {len(summary['critical_kpis'])}")
    print(f"  At Risk KPIs: {len(summary['at_risk_kpis'])}")

    # Export configuration
    print("\n💾 Exporting KPI Configuration...")
    export_success = kpi_manager.export_config("kpi_config_export.json")
    if export_success:
        print("  ✅ Configuration exported successfully")
    else:
        print("  ❌ Export failed")

    print("\n🎉 KPI Configuration demonstration completed successfully!")


if __name__ == "__main__":
    # Run demonstration
    demonstrate_kpi_config()
