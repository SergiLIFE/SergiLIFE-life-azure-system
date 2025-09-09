"""
L.I.F.E. Platform Autonomous SOTA KPI Configuration
Autonomous monitoring configuration for maintaining champion-level performance
Copyright Sergio Paya Borrull 2025. All Rights Reserved.

Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
KPI thresholds and monitoring parameters for continuous validation
"""

import json
from datetime import datetime
from typing import Dict, List

# SOTA Champion Performance Thresholds (Based on September 9, 2025 achievements)
SOTA_CHAMPION_METRICS = {
    "absolute_best_latency_ms": 0.29,  # Achieved champion latency
    "absolute_best_accuracy": 1.0,  # Perfect BCI accuracy achieved
    "absolute_best_throughput": 745.5,  # Peak ops/sec achieved
    "absolute_best_reliability": 1.0,  # Perfect reliability achieved
    "achievement_date": "2025-09-09",
    "validation_level": "CHAMPION",
}

# Minimum Acceptable Thresholds (Must ALWAYS exceed these)
MINIMUM_PERFORMANCE_THRESHOLDS = {
    "max_latency_ms": 2.0,  # NEVER exceed 2ms
    "min_accuracy": 0.95,  # NEVER below 95%
    "min_throughput_ops_sec": 600,  # NEVER below 600 ops/sec
    "min_reliability": 0.85,  # NEVER below 85%
    "violation_action": "IMMEDIATE_OPTIMIZATION",
}

# Warning Thresholds (Trigger preventive optimization)
WARNING_THRESHOLDS = {
    "latency_warning_ms": 1.5,  # Warning if > 1.5ms
    "accuracy_warning": 0.98,  # Warning if < 98%
    "throughput_warning_ops_sec": 700,  # Warning if < 700 ops/sec
    "reliability_warning": 0.90,  # Warning if < 90%
    "warning_action": "PREVENTIVE_OPTIMIZATION",
}

# Monitoring Intervals Configuration
MONITORING_INTERVALS = {
    "active_mode_seconds": 30,  # 30 sec in active mode
    "sleep_mode_seconds": 300,  # 5 min in sleep mode
    "sota_validation_seconds": 3600,  # 1 hour SOTA validation
    "emergency_check_seconds": 10,  # 10 sec emergency mode
    "mode_switch_check_seconds": 120,  # 2 min mode switch check
}

# Alert and Action Configuration
ALERT_CONFIGURATION = {
    "max_consecutive_degradations": 3,  # Max before emergency action
    "critical_alert_threshold": 5,  # Critical system alert level
    "alert_cool_down_seconds": 300,  # 5 min between similar alerts
    "emergency_recovery_timeout": 600,  # 10 min emergency timeout
}

# Performance Grading Criteria
PERFORMANCE_GRADES = {
    "SOTA_CHAMPION": {
        "latency_max_ms": 0.5,
        "accuracy_min": 0.99,
        "performance_score_min": 0.9,
        "description": "Champion-level SOTA performance",
    },
    "EXCELLENT": {
        "latency_max_ms": 1.0,
        "accuracy_min": 0.98,
        "performance_score_min": 0.85,
        "description": "Excellent performance - near champion",
    },
    "GOOD": {
        "latency_max_ms": 2.0,
        "accuracy_min": 0.95,
        "performance_score_min": 0.7,
        "description": "Good performance - meets minimums",
    },
    "ACCEPTABLE": {
        "latency_max_ms": 5.0,
        "accuracy_min": 0.90,
        "performance_score_min": 0.6,
        "description": "Acceptable - needs monitoring",
    },
    "NEEDS_OPTIMIZATION": {
        "latency_max_ms": 10.0,
        "accuracy_min": 0.80,
        "performance_score_min": 0.4,
        "description": "Performance degraded - optimization required",
    },
    "CRITICAL": {
        "latency_max_ms": float("inf"),
        "accuracy_min": 0.0,
        "performance_score_min": 0.0,
        "description": "Critical performance - emergency action required",
    },
}

# Autonomous Optimization Triggers
OPTIMIZATION_TRIGGERS = {
    "performance_grade_triggers": ["NEEDS_OPTIMIZATION", "CRITICAL"],
    "consecutive_warnings": 3,
    "accuracy_drop_threshold": 0.05,  # 5% accuracy drop
    "latency_increase_threshold": 2.0,  # 2x latency increase
    "throughput_drop_threshold": 0.3,  # 30% throughput drop
    "auto_optimization_interval_hours": 1,  # Auto-optimize hourly if not champion
}

# KPI Monitoring Modes
MONITORING_MODES = {
    "ACTIVE": {
        "description": "High-frequency monitoring for active optimization",
        "interval_seconds": 30,
        "triggers": ["alerts", "performance_degradation", "user_activity"],
        "optimization_enabled": True,
    },
    "SLEEP": {
        "description": "Low-frequency monitoring for stable performance",
        "interval_seconds": 300,
        "triggers": ["stable_performance", "no_alerts"],
        "optimization_enabled": False,
    },
    "EMERGENCY": {
        "description": "Maximum frequency monitoring for critical issues",
        "interval_seconds": 10,
        "triggers": ["critical_alerts", "system_failures"],
        "optimization_enabled": True,
    },
}

# Azure Integration Configuration
AZURE_INTEGRATION = {
    "marketplace_offer_id": "9a600d96-fe1e-420b-902a-a0c42c561adb",
    "performance_logging_enabled": True,
    "cloud_monitoring_enabled": True,
    "telemetry_upload_interval": 3600,  # 1 hour telemetry upload
    "compliance_validation": True,
}

# System Resource Monitoring
SYSTEM_MONITORING = {
    "cpu_threshold_percent": 80,  # Alert if CPU > 80%
    "memory_threshold_mb": 1024,  # Alert if memory > 1GB
    "disk_threshold_percent": 90,  # Alert if disk > 90%
    "network_monitoring_enabled": True,
}


def get_kpi_configuration() -> Dict:
    """Get complete KPI monitoring configuration"""
    return {
        "sota_champion_metrics": SOTA_CHAMPION_METRICS,
        "minimum_thresholds": MINIMUM_PERFORMANCE_THRESHOLDS,
        "warning_thresholds": WARNING_THRESHOLDS,
        "monitoring_intervals": MONITORING_INTERVALS,
        "alert_configuration": ALERT_CONFIGURATION,
        "performance_grades": PERFORMANCE_GRADES,
        "optimization_triggers": OPTIMIZATION_TRIGGERS,
        "monitoring_modes": MONITORING_MODES,
        "azure_integration": AZURE_INTEGRATION,
        "system_monitoring": SYSTEM_MONITORING,
        "configuration_version": "1.0",
        "last_updated": datetime.now().isoformat(),
    }


def validate_kpi_configuration() -> bool:
    """Validate KPI configuration integrity"""
    config = get_kpi_configuration()

    # Validate champion metrics exist
    if not config["sota_champion_metrics"]["absolute_best_latency_ms"]:
        return False

    # Validate thresholds are logical
    if (
        config["minimum_thresholds"]["max_latency_ms"]
        < config["sota_champion_metrics"]["absolute_best_latency_ms"]
    ):
        return False

    # Validate monitoring intervals
    if config["monitoring_intervals"]["active_mode_seconds"] <= 0:
        return False

    return True


def export_kpi_config_to_file(filename: str = "kpi_config.json"):
    """Export KPI configuration to JSON file"""
    config = get_kpi_configuration()

    with open(filename, "w") as f:
        json.dump(config, f, indent=2)

    print(f"KPI configuration exported to {filename}")


def load_kpi_config_from_file(filename: str = "kpi_config.json") -> Dict:
    """Load KPI configuration from JSON file"""
    try:
        with open(filename, "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Configuration file {filename} not found. Using defaults.")
        return get_kpi_configuration()


# Performance Grade Calculator
def calculate_performance_grade(
    latency_ms: float, accuracy: float, performance_score: float
) -> str:
    """Calculate performance grade based on metrics"""

    for grade, criteria in PERFORMANCE_GRADES.items():
        if (
            latency_ms <= criteria["latency_max_ms"]
            and accuracy >= criteria["accuracy_min"]
            and performance_score >= criteria["performance_score_min"]
        ):
            return grade

    return "CRITICAL"


# KPI Threshold Checker
def check_kpi_thresholds(metrics: Dict) -> Dict:
    """Check metrics against all KPI thresholds"""

    results = {
        "champion_status": False,
        "minimum_compliance": True,
        "warnings": [],
        "critical_violations": [],
        "overall_status": "UNKNOWN",
    }

    latency = metrics.get("latency_ms", float("inf"))
    accuracy = metrics.get("accuracy", 0.0)
    throughput = metrics.get("throughput_ops_sec", 0.0)

    # Check champion status
    results["champion_status"] = (
        latency
        <= SOTA_CHAMPION_METRICS["absolute_best_latency_ms"] * 1.1  # 10% tolerance
        and accuracy
        >= SOTA_CHAMPION_METRICS["absolute_best_accuracy"] * 0.99  # 1% tolerance
    )

    # Check minimum compliance
    if latency > MINIMUM_PERFORMANCE_THRESHOLDS["max_latency_ms"]:
        results["critical_violations"].append(
            f"Latency {latency:.2f}ms exceeds maximum {MINIMUM_PERFORMANCE_THRESHOLDS['max_latency_ms']}ms"
        )
        results["minimum_compliance"] = False

    if accuracy < MINIMUM_PERFORMANCE_THRESHOLDS["min_accuracy"]:
        results["critical_violations"].append(
            f"Accuracy {accuracy*100:.1f}% below minimum {MINIMUM_PERFORMANCE_THRESHOLDS['min_accuracy']*100:.1f}%"
        )
        results["minimum_compliance"] = False

    if throughput < MINIMUM_PERFORMANCE_THRESHOLDS["min_throughput_ops_sec"]:
        results["critical_violations"].append(
            f"Throughput {throughput:.1f} below minimum {MINIMUM_PERFORMANCE_THRESHOLDS['min_throughput_ops_sec']}"
        )
        results["minimum_compliance"] = False

    # Check warnings
    if latency > WARNING_THRESHOLDS["latency_warning_ms"]:
        results["warnings"].append(
            f"Latency {latency:.2f}ms above warning threshold {WARNING_THRESHOLDS['latency_warning_ms']}ms"
        )

    if accuracy < WARNING_THRESHOLDS["accuracy_warning"]:
        results["warnings"].append(
            f"Accuracy {accuracy*100:.1f}% below warning threshold {WARNING_THRESHOLDS['accuracy_warning']*100:.1f}%"
        )

    # Determine overall status
    if results["critical_violations"]:
        results["overall_status"] = "CRITICAL"
    elif not results["minimum_compliance"]:
        results["overall_status"] = "VIOLATION"
    elif results["warnings"]:
        results["overall_status"] = "WARNING"
    elif results["champion_status"]:
        results["overall_status"] = "CHAMPION"
    else:
        results["overall_status"] = "GOOD"

    return results


if __name__ == "__main__":
    # Validate and export configuration
    if validate_kpi_configuration():
        print("✅ KPI configuration validation passed")
        export_kpi_config_to_file()

        # Display champion metrics
        print("\n🏆 SOTA Champion Metrics:")
        for key, value in SOTA_CHAMPION_METRICS.items():
            print(f"  {key}: {value}")

        print("\n📊 Performance Grade Criteria:")
        for grade, criteria in PERFORMANCE_GRADES.items():
            print(f"  {grade}: {criteria['description']}")
    else:
        print("❌ KPI configuration validation failed")
