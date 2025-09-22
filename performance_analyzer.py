#!/usr/bin/env python3
"""
L.I.F.E. Platform - Performance Analyzer
Advanced performance analysis and optimization for neuroadaptive systems

This module provides comprehensive performance analysis capabilities
for the L.I.F.E. Platform, including real-time metrics collection,
bottleneck identification, and automated optimization recommendations.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import os
import statistics
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class PerformanceMetric(Enum):
    """Performance metrics to track"""

    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    DISK_IO = "disk_io"
    NETWORK_IO = "network_io"
    EEG_PROCESSING_LATENCY = "eeg_processing_latency"
    ALGORITHM_EXECUTION_TIME = "algorithm_execution_time"
    API_RESPONSE_TIME = "api_response_time"
    DATABASE_QUERY_TIME = "database_query_time"
    CACHE_HIT_RATE = "cache_hit_rate"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    MEMORY_LEAKS = "memory_leaks"
    THREAD_CONTENTION = "thread_contention"


class PerformanceThreshold(Enum):
    """Performance threshold levels"""

    EXCELLENT = "excellent"
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"


class AnalysisType(Enum):
    """Types of performance analysis"""

    REAL_TIME = "real_time"
    HISTORICAL = "historical"
    COMPARATIVE = "comparative"
    PREDICTIVE = "predictive"
    BOTTLENECK = "bottleneck"


@dataclass
class PerformanceSample:
    """Individual performance measurement"""

    metric: PerformanceMetric
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    labels: Dict[str, str] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceThresholdConfig:
    """Configuration for performance thresholds"""

    metric: PerformanceMetric
    excellent_max: float
    good_max: float
    warning_max: float
    critical_max: float
    unit: str = ""
    description: str = ""


@dataclass
class PerformanceAnalysis:
    """Performance analysis result"""

    analysis_id: str
    analysis_type: AnalysisType
    timestamp: datetime = field(default_factory=datetime.now)
    duration_seconds: float = 0.0
    metrics_analyzed: int = 0
    bottlenecks_identified: int = 0
    recommendations: List[str] = field(default_factory=list)
    performance_score: float = 100.0
    summary: Dict[str, Any] = field(default_factory=dict)
    detailed_results: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OptimizationRecommendation:
    """Performance optimization recommendation"""

    recommendation_id: str
    title: str
    description: str
    impact: str  # high, medium, low
    effort: str  # high, medium, low
    category: str
    implementation_steps: List[str] = field(default_factory=list)
    expected_improvement: Dict[str, float] = field(default_factory=dict)
    priority: int = 1  # 1-5, 1 being highest


class PerformanceAnalyzer:
    """
    Performance Analyzer for L.I.F.E. Platform

    Provides comprehensive performance monitoring, analysis, and
    optimization recommendations for neuroadaptive systems.
    """

    def __init__(
        self, workspace_path: Optional[str] = None, sampling_interval: float = 1.0
    ):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.sampling_interval = sampling_interval

        # Performance data storage
        self.performance_samples: List[PerformanceSample] = []
        self.analysis_history: List[PerformanceAnalysis] = []
        self.threshold_configs: Dict[PerformanceMetric, PerformanceThresholdConfig] = {}

        # Real-time monitoring
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self.executor = ThreadPoolExecutor(max_workers=4)

        # Initialize thresholds
        self._initialize_thresholds()

        logger.info(
            f"Performance Analyzer initialized for workspace: {self.workspace_path}"
        )

    def _initialize_thresholds(self):
        """Initialize performance thresholds"""
        thresholds = [
            PerformanceThresholdConfig(
                metric=PerformanceMetric.CPU_USAGE,
                excellent_max=50.0,
                good_max=70.0,
                warning_max=85.0,
                critical_max=95.0,
                unit="%",
                description="CPU utilization percentage",
            ),
            PerformanceThresholdConfig(
                metric=PerformanceMetric.MEMORY_USAGE,
                excellent_max=60.0,
                good_max=75.0,
                warning_max=90.0,
                critical_max=95.0,
                unit="%",
                description="Memory utilization percentage",
            ),
            PerformanceThresholdConfig(
                metric=PerformanceMetric.EEG_PROCESSING_LATENCY,
                excellent_max=25.0,
                good_max=50.0,
                warning_max=100.0,
                critical_max=200.0,
                unit="ms",
                description="EEG processing latency",
            ),
            PerformanceThresholdConfig(
                metric=PerformanceMetric.ALGORITHM_EXECUTION_TIME,
                excellent_max=30.0,
                good_max=60.0,
                warning_max=120.0,
                critical_max=300.0,
                unit="ms",
                description="Algorithm execution time",
            ),
            PerformanceThresholdConfig(
                metric=PerformanceMetric.API_RESPONSE_TIME,
                excellent_max=100.0,
                good_max=500.0,
                warning_max=2000.0,
                critical_max=5000.0,
                unit="ms",
                description="API response time",
            ),
            PerformanceThresholdConfig(
                metric=PerformanceMetric.ERROR_RATE,
                excellent_max=0.1,
                good_max=1.0,
                warning_max=5.0,
                critical_max=10.0,
                unit="%",
                description="Error rate percentage",
            ),
            PerformanceThresholdConfig(
                metric=PerformanceMetric.THROUGHPUT,
                excellent_max=float("inf"),  # Higher is better
                good_max=float("inf"),
                warning_max=50.0,
                critical_max=10.0,
                unit="req/sec",
                description="Request throughput",
            ),
        ]

        for threshold in thresholds:
            self.threshold_configs[threshold.metric] = threshold

    def start_real_time_monitoring(self) -> None:
        """Start real-time performance monitoring"""
        if self.monitoring_active:
            logger.warning("Performance monitoring is already active")
            return

        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop, daemon=True
        )
        self.monitoring_thread.start()

        logger.info("Real-time performance monitoring started")

    def stop_monitoring(self) -> None:
        """Stop performance monitoring"""
        if not self.monitoring_active:
            logger.warning("Performance monitoring is not active")
            return

        self.monitoring_active = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5.0)

        logger.info("Performance monitoring stopped")

    def _monitoring_loop(self) -> None:
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect performance metrics
                asyncio.run(self._collect_performance_metrics())

                # Sleep for sampling interval
                time.sleep(self.sampling_interval)

            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(5.0)  # Brief pause on error

    async def _collect_performance_metrics(self) -> None:
        """Collect current performance metrics"""
        try:
            # System metrics
            await self._collect_system_metrics()

            # Application metrics
            await self._collect_application_metrics()

            # Clean up old samples (keep last 24 hours)
            cutoff_time = datetime.now() - timedelta(hours=24)
            self.performance_samples = [
                sample
                for sample in self.performance_samples
                if sample.timestamp > cutoff_time
            ]

        except Exception as e:
            logger.error(f"Metrics collection failed: {e}")

    async def _collect_system_metrics(self) -> None:
        """Collect system-level performance metrics"""
        try:
            import psutil

            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self._add_sample(PerformanceMetric.CPU_USAGE, cpu_percent)

            # Memory metrics
            memory = psutil.virtual_memory()
            self._add_sample(PerformanceMetric.MEMORY_USAGE, memory.percent)

            # Disk I/O
            disk_io = psutil.disk_io_counters()
            if disk_io:
                read_bytes_per_sec = disk_io.read_bytes / self.sampling_interval
                write_bytes_per_sec = disk_io.write_bytes / self.sampling_interval
                self._add_sample(
                    PerformanceMetric.DISK_IO,
                    read_bytes_per_sec + write_bytes_per_sec,
                    {"type": "combined", "unit": "bytes/sec"},
                )

            # Network I/O
            network_io = psutil.net_io_counters()
            if network_io:
                bytes_per_sec = (
                    network_io.bytes_sent + network_io.bytes_recv
                ) / self.sampling_interval
                self._add_sample(
                    PerformanceMetric.NETWORK_IO, bytes_per_sec, {"unit": "bytes/sec"}
                )

        except ImportError:
            logger.warning("psutil not available for system metrics")
        except Exception as e:
            logger.error(f"System metrics collection failed: {e}")

    async def _collect_application_metrics(self) -> None:
        """Collect application-specific performance metrics"""
        try:
            # EEG processing metrics
            await self._collect_eeg_metrics()

            # Algorithm metrics
            await self._collect_algorithm_metrics()

            # API metrics
            await self._collect_api_metrics()

        except Exception as e:
            logger.error(f"Application metrics collection failed: {e}")

    async def _collect_eeg_metrics(self) -> None:
        """Collect EEG processing performance metrics"""
        try:
            # Check if EEG processor is running
            eeg_running = self._check_process_running("eeg_processor")

            if eeg_running:
                # Mock EEG processing metrics (would be collected from actual processor)
                latency = 42.3  # milliseconds
                throughput = 118.7  # samples per second

                self._add_sample(
                    PerformanceMetric.EEG_PROCESSING_LATENCY, latency, {"unit": "ms"}
                )
                self._add_sample(
                    PerformanceMetric.THROUGHPUT,
                    throughput,
                    {"component": "eeg_processor", "unit": "samples/sec"},
                )

        except Exception as e:
            logger.error(f"EEG metrics collection failed: {e}")

    async def _collect_algorithm_metrics(self) -> None:
        """Collect algorithm performance metrics"""
        try:
            # Check if algorithm is running
            algo_running = self._check_process_running("experimentP2L")

            if algo_running:
                # Mock algorithm metrics
                execution_time = 35.2  # milliseconds
                accuracy = 0.824  # accuracy score

                self._add_sample(
                    PerformanceMetric.ALGORITHM_EXECUTION_TIME,
                    execution_time,
                    {"unit": "ms"},
                )
                # Note: Accuracy might be tracked separately as it's not a performance metric

        except Exception as e:
            logger.error(f"Algorithm metrics collection failed: {e}")

    async def _collect_api_metrics(self) -> None:
        """Collect API performance metrics"""
        try:
            # Mock API metrics (would be collected from actual API monitoring)
            response_time = 145.3  # milliseconds
            error_rate = 0.02  # 0.02%
            throughput = 85.4  # requests per second

            self._add_sample(
                PerformanceMetric.API_RESPONSE_TIME, response_time, {"unit": "ms"}
            )
            self._add_sample(PerformanceMetric.ERROR_RATE, error_rate, {"unit": "%"})
            self._add_sample(
                PerformanceMetric.THROUGHPUT,
                throughput,
                {"component": "api", "unit": "req/sec"},
            )

        except Exception as e:
            logger.error(f"API metrics collection failed: {e}")

    def _add_sample(
        self,
        metric: PerformanceMetric,
        value: float,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Add a performance sample"""
        sample = PerformanceSample(metric=metric, value=value, labels=labels or {})
        self.performance_samples.append(sample)

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

    def get_current_performance_status(self) -> Dict[str, Any]:
        """Get current performance status"""
        status = {
            "timestamp": datetime.now(),
            "overall_health": "unknown",
            "metrics": {},
            "alerts": [],
            "recommendations": [],
        }

        # Get latest samples for each metric
        latest_samples = {}
        for sample in reversed(self.performance_samples):
            if sample.metric not in latest_samples:
                latest_samples[sample.metric] = sample

        # Evaluate each metric
        health_scores = []
        alerts = []

        for metric, sample in latest_samples.items():
            threshold = self.threshold_configs.get(metric)
            if threshold:
                level = self._evaluate_threshold(sample.value, threshold)

                status["metrics"][metric.value] = {
                    "value": sample.value,
                    "unit": threshold.unit,
                    "level": level.value,
                    "timestamp": sample.timestamp,
                }

                # Calculate health score contribution
                if level == PerformanceThreshold.EXCELLENT:
                    health_scores.append(100)
                elif level == PerformanceThreshold.GOOD:
                    health_scores.append(75)
                elif level == PerformanceThreshold.WARNING:
                    health_scores.append(50)
                elif level == PerformanceThreshold.CRITICAL:
                    health_scores.append(0)
                    alerts.append(
                        f"CRITICAL: {metric.value} is at {sample.value}{threshold.unit}"
                    )

        # Calculate overall health
        if health_scores:
            status["overall_health"] = (
                "healthy" if statistics.mean(health_scores) >= 75 else "degraded"
            )
        else:
            status["overall_health"] = "no_data"

        status["alerts"] = alerts
        status["recommendations"] = self._generate_quick_recommendations(status)

        return status

    def _evaluate_threshold(
        self, value: float, threshold: PerformanceThresholdConfig
    ) -> PerformanceThreshold:
        """Evaluate a value against performance thresholds"""
        # For metrics where higher is better (like throughput)
        if threshold.metric in [
            PerformanceMetric.THROUGHPUT,
            PerformanceMetric.CACHE_HIT_RATE,
        ]:
            if value >= threshold.excellent_max:
                return PerformanceThreshold.EXCELLENT
            elif value >= threshold.good_max:
                return PerformanceThreshold.GOOD
            elif value >= threshold.warning_max:
                return PerformanceThreshold.WARNING
            else:
                return PerformanceThreshold.CRITICAL
        else:
            # For metrics where lower is better (most metrics)
            if value <= threshold.excellent_max:
                return PerformanceThreshold.EXCELLENT
            elif value <= threshold.good_max:
                return PerformanceThreshold.GOOD
            elif value <= threshold.warning_max:
                return PerformanceThreshold.WARNING
            else:
                return PerformanceThreshold.CRITICAL

    def _generate_quick_recommendations(self, status: Dict[str, Any]) -> List[str]:
        """Generate quick performance recommendations"""
        recommendations = []

        for metric_name, metric_data in status["metrics"].items():
            level = metric_data["level"]

            if level in ["warning", "critical"]:
                metric_enum = PerformanceMetric(metric_name)

                if metric_enum == PerformanceMetric.CPU_USAGE:
                    recommendations.append(
                        "Consider optimizing CPU-intensive operations or scaling resources"
                    )
                elif metric_enum == PerformanceMetric.MEMORY_USAGE:
                    recommendations.append(
                        "Monitor for memory leaks and consider memory optimization"
                    )
                elif metric_enum == PerformanceMetric.EEG_PROCESSING_LATENCY:
                    recommendations.append(
                        "Optimize EEG processing pipeline for lower latency"
                    )
                elif metric_enum == PerformanceMetric.API_RESPONSE_TIME:
                    recommendations.append(
                        "Review API endpoints for performance bottlenecks"
                    )

        if not recommendations:
            recommendations.append("Performance is within acceptable ranges")

        return recommendations

    async def perform_comprehensive_analysis(
        self,
        analysis_type: AnalysisType = AnalysisType.BOTTLENECK,
        time_window_hours: int = 1,
    ) -> PerformanceAnalysis:
        """Perform comprehensive performance analysis"""
        analysis = PerformanceAnalysis(
            analysis_id=f"perf_analysis_{int(datetime.now().timestamp())}",
            analysis_type=analysis_type,
            timestamp=datetime.now(),
        )

        start_time = time.time()

        try:
            # Filter samples by time window
            cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
            relevant_samples = [
                sample
                for sample in self.performance_samples
                if sample.timestamp >= cutoff_time
            ]

            analysis.metrics_analyzed = len(relevant_samples)

            if analysis_type == AnalysisType.BOTTLENECK:
                bottlenecks = await self._analyze_bottlenecks(relevant_samples)
                analysis.bottlenecks_identified = len(bottlenecks)
                analysis.detailed_results["bottlenecks"] = bottlenecks

            elif analysis_type == AnalysisType.HISTORICAL:
                historical_analysis = await self._analyze_historical_trends(
                    relevant_samples
                )
                analysis.detailed_results["historical"] = historical_analysis

            elif analysis_type == AnalysisType.COMPARATIVE:
                comparative_analysis = await self._analyze_comparative_performance(
                    relevant_samples
                )
                analysis.detailed_results["comparative"] = comparative_analysis

            # Generate recommendations
            analysis.recommendations = (
                await self._generate_optimization_recommendations(analysis)
            )

            # Calculate performance score
            analysis.performance_score = self._calculate_performance_score(
                relevant_samples
            )

            # Generate summary
            analysis.summary = self._generate_analysis_summary(analysis)

        except Exception as e:
            logger.error(f"Performance analysis failed: {e}")
            analysis.detailed_results["error"] = str(e)

        analysis.duration_seconds = time.time() - start_time
        self.analysis_history.append(analysis)

        return analysis

    async def _analyze_bottlenecks(
        self, samples: List[PerformanceSample]
    ) -> List[Dict[str, Any]]:
        """Analyze performance bottlenecks"""
        bottlenecks = []

        # Group samples by metric
        metric_samples = {}
        for sample in samples:
            if sample.metric not in metric_samples:
                metric_samples[sample.metric] = []
            metric_samples[sample.metric].append(sample.value)

        # Analyze each metric for bottlenecks
        for metric, values in metric_samples.items():
            if len(values) < 10:  # Need minimum samples
                continue

            threshold = self.threshold_configs.get(metric)
            if not threshold:
                continue

            # Calculate statistics
            avg_value = statistics.mean(values)
            max_value = max(values)
            std_dev = statistics.stdev(values) if len(values) > 1 else 0

            # Check for performance issues
            issues = []

            if metric in [
                PerformanceMetric.THROUGHPUT,
                PerformanceMetric.CACHE_HIT_RATE,
            ]:
                # Higher is better
                if avg_value < threshold.warning_max:
                    issues.append(
                        f"Average value ({avg_value:.2f}) below warning threshold"
                    )
            else:
                # Lower is better
                if avg_value > threshold.warning_max:
                    issues.append(
                        f"Average value ({avg_value:.2f}) above warning threshold"
                    )

            if std_dev > avg_value * 0.5:  # High variability
                issues.append(f"High variability (std dev: {std_dev:.2f})")

            if max_value > threshold.critical_max:
                issues.append(
                    f"Peak value ({max_value:.2f}) exceeds critical threshold"
                )

            if issues:
                bottlenecks.append(
                    {
                        "metric": metric.value,
                        "average": avg_value,
                        "maximum": max_value,
                        "standard_deviation": std_dev,
                        "issues": issues,
                        "severity": (
                            "high"
                            if any("critical" in issue.lower() for issue in issues)
                            else "medium"
                        ),
                    }
                )

        return bottlenecks

    async def _analyze_historical_trends(
        self, samples: List[PerformanceSample]
    ) -> Dict[str, Any]:
        """Analyze historical performance trends"""
        trends = {}

        # Group by metric and time periods
        metric_data = {}
        for sample in samples:
            metric = sample.metric
            if metric not in metric_data:
                metric_data[metric] = []
            metric_data[metric].append((sample.timestamp, sample.value))

        for metric, data in metric_data.items():
            if len(data) < 20:  # Need enough data points
                continue

            # Sort by time
            data.sort(key=lambda x: x[0])

            # Calculate trend
            values = [x[1] for x in data]
            timestamps = [x[0] for x in data]

            # Simple linear trend
            if len(values) > 1:
                trend_slope = self._calculate_trend_slope(values)
                trend_direction = "improving" if trend_slope < 0 else "degrading"

                trends[metric.value] = {
                    "trend_direction": trend_direction,
                    "trend_slope": trend_slope,
                    "average": statistics.mean(values),
                    "data_points": len(values),
                }

        return trends

    async def _analyze_comparative_performance(
        self, samples: List[PerformanceSample]
    ) -> Dict[str, Any]:
        """Analyze comparative performance against benchmarks"""
        comparative = {}

        # Define benchmarks (these would be configurable)
        benchmarks = {
            PerformanceMetric.CPU_USAGE: {
                "excellent": 30.0,
                "good": 50.0,
                "poor": 80.0,
            },
            PerformanceMetric.MEMORY_USAGE: {
                "excellent": 40.0,
                "good": 60.0,
                "poor": 85.0,
            },
            PerformanceMetric.EEG_PROCESSING_LATENCY: {
                "excellent": 20.0,
                "good": 40.0,
                "poor": 100.0,
            },
        }

        for metric, benchmark in benchmarks.items():
            metric_samples = [s.value for s in samples if s.metric == metric]

            if not metric_samples:
                continue

            avg_value = statistics.mean(metric_samples)

            if avg_value <= benchmark["excellent"]:
                rating = "excellent"
            elif avg_value <= benchmark["good"]:
                rating = "good"
            elif avg_value <= benchmark["poor"]:
                rating = "poor"
            else:
                rating = "critical"

            comparative[metric.value] = {
                "current_average": avg_value,
                "benchmark_rating": rating,
                "benchmarks": benchmark,
            }

        return comparative

    def _calculate_trend_slope(self, values: List[float]) -> float:
        """Calculate linear trend slope"""
        if len(values) < 2:
            return 0.0

        n = len(values)
        x = list(range(n))
        y = values

        # Calculate slope using linear regression
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi * xi for xi in x)

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        return slope

    async def _generate_optimization_recommendations(
        self, analysis: PerformanceAnalysis
    ) -> List[str]:
        """Generate optimization recommendations based on analysis"""
        recommendations = []

        # Based on bottlenecks
        if "bottlenecks" in analysis.detailed_results:
            for bottleneck in analysis.detailed_results["bottlenecks"]:
                metric = bottleneck["metric"]

                if metric == "cpu_usage":
                    recommendations.append(
                        "Optimize CPU-intensive operations or consider horizontal scaling"
                    )
                elif metric == "memory_usage":
                    recommendations.append(
                        "Implement memory pooling and optimize data structures"
                    )
                elif metric == "eeg_processing_latency":
                    recommendations.append(
                        "Optimize EEG signal processing algorithms and data pipelines"
                    )
                elif metric == "api_response_time":
                    recommendations.append(
                        "Implement API response caching and optimize database queries"
                    )

        # Based on trends
        if "historical" in analysis.detailed_results:
            for metric_name, trend_data in analysis.detailed_results[
                "historical"
            ].items():
                if trend_data["trend_direction"] == "degrading":
                    recommendations.append(
                        f"Address degrading trend in {metric_name} performance"
                    )

        # General recommendations
        if analysis.performance_score < 70:
            recommendations.append(
                "Overall performance needs attention - consider comprehensive optimization"
            )
        elif analysis.performance_score < 85:
            recommendations.append("Performance is acceptable but could be improved")

        if not recommendations:
            recommendations.append(
                "Performance is within acceptable ranges - continue monitoring"
            )

        return recommendations

    def _calculate_performance_score(self, samples: List[PerformanceSample]) -> float:
        """Calculate overall performance score"""
        if not samples:
            return 50.0  # Neutral score for no data

        scores = []

        # Group by metric
        metric_samples = {}
        for sample in samples:
            if sample.metric not in metric_samples:
                metric_samples[sample.metric] = []
            metric_samples[sample.metric].append(sample.value)

        # Score each metric
        for metric, values in metric_samples.items():
            if not values:
                continue

            threshold = self.threshold_configs.get(metric)
            if not threshold:
                continue

            avg_value = statistics.mean(values)
            level = self._evaluate_threshold(avg_value, threshold)

            # Convert level to score
            if level == PerformanceThreshold.EXCELLENT:
                scores.append(100)
            elif level == PerformanceThreshold.GOOD:
                scores.append(80)
            elif level == PerformanceThreshold.WARNING:
                scores.append(60)
            elif level == PerformanceThreshold.CRITICAL:
                scores.append(20)

        return statistics.mean(scores) if scores else 50.0

    def _generate_analysis_summary(
        self, analysis: PerformanceAnalysis
    ) -> Dict[str, Any]:
        """Generate analysis summary"""
        summary = {
            "analysis_type": analysis.analysis_type.value,
            "performance_score": analysis.performance_score,
            "metrics_analyzed": analysis.metrics_analyzed,
            "bottlenecks_identified": analysis.bottlenecks_identified,
            "recommendations_count": len(analysis.recommendations),
            "duration_seconds": analysis.duration_seconds,
        }

        # Add performance rating
        if analysis.performance_score >= 90:
            summary["rating"] = "excellent"
        elif analysis.performance_score >= 75:
            summary["rating"] = "good"
        elif analysis.performance_score >= 60:
            summary["rating"] = "fair"
        else:
            summary["rating"] = "poor"

        return summary

    def get_performance_samples(
        self, metric: Optional[PerformanceMetric] = None, time_window_hours: int = 24
    ) -> List[PerformanceSample]:
        """Get performance samples with optional filtering"""
        cutoff_time = datetime.now() - timedelta(hours=time_window_hours)

        samples = [
            sample
            for sample in self.performance_samples
            if sample.timestamp >= cutoff_time
        ]

        if metric:
            samples = [s for s in samples if s.metric == metric]

        return samples

    def export_performance_report(
        self, filepath: str, analysis: Optional[PerformanceAnalysis] = None
    ) -> bool:
        """Export performance analysis report"""
        if analysis is None:
            analysis = self.analysis_history[-1] if self.analysis_history else None

        if not analysis:
            logger.warning("No performance analysis available to export")
            return False

        try:
            export_data = {
                "analysis_id": analysis.analysis_id,
                "analysis_type": analysis.analysis_type.value,
                "timestamp": analysis.timestamp.isoformat(),
                "duration_seconds": analysis.duration_seconds,
                "performance_score": analysis.performance_score,
                "summary": analysis.summary,
                "recommendations": analysis.recommendations,
                "detailed_results": analysis.detailed_results,
            }

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Performance report exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to export performance report: {e}")
            return False


# Factory function for easy instantiation
def create_performance_analyzer(
    workspace_path: Optional[str] = None, sampling_interval: float = 1.0
) -> PerformanceAnalyzer:
    """
    Factory function to create performance analyzer

    Args:
        workspace_path: Path to workspace directory
        sampling_interval: Sampling interval in seconds

    Returns:
        Configured PerformanceAnalyzer instance
    """
    return PerformanceAnalyzer(
        workspace_path=workspace_path, sampling_interval=sampling_interval
    )


# Command-line interface
def main():
    """Main CLI function for performance analysis"""
    import argparse

    parser = argparse.ArgumentParser(
        description="L.I.F.E. Platform Performance Analyzer"
    )
    parser.add_argument(
        "--workspace", "-w", default=None, help="Workspace directory path"
    )
    parser.add_argument(
        "--monitor",
        "-m",
        action="store_true",
        help="Start real-time performance monitoring",
    )
    parser.add_argument(
        "--analyze",
        "-a",
        choices=["bottleneck", "historical", "comparative"],
        help="Perform performance analysis",
    )
    parser.add_argument(
        "--status", "-s", action="store_true", help="Show current performance status"
    )
    parser.add_argument(
        "--export", "-e", help="Export analysis report to specified file"
    )
    parser.add_argument(
        "--interval",
        "-i",
        type=float,
        default=1.0,
        help="Monitoring sampling interval in seconds",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create performance analyzer
    analyzer = create_performance_analyzer(
        workspace_path=args.workspace, sampling_interval=args.interval
    )

    print("L.I.F.E. Platform - Performance Analyzer")
    print("=" * 45)

    try:
        if args.monitor:
            # Start monitoring
            print("Starting real-time performance monitoring...")
            analyzer.start_real_time_monitoring()

            try:
                while True:
                    time.sleep(5)
                    status = analyzer.get_current_performance_status()
                    print(
                        f"[{status['timestamp'].strftime('%H:%M:%S')}] "
                        f"Health: {status['overall_health']} "
                        f"({len(status['alerts'])} alerts)"
                    )

                    if status["alerts"]:
                        for alert in status["alerts"][:2]:  # Show first 2 alerts
                            print(f"  ⚠️  {alert}")

            except KeyboardInterrupt:
                print("\nStopping monitoring...")
                analyzer.stop_monitoring()

        elif args.analyze:
            # Perform analysis
            analysis_type_map = {
                "bottleneck": AnalysisType.BOTTLENECK,
                "historical": AnalysisType.HISTORICAL,
                "comparative": AnalysisType.COMPARATIVE,
            }

            analysis_type = analysis_type_map.get(args.analyze, AnalysisType.BOTTLENECK)

            print(f"Performing {args.analyze} analysis...")

            # Run analysis
            analysis = asyncio.run(
                analyzer.perform_comprehensive_analysis(analysis_type)
            )

            print("\nAnalysis Results:")
            print(f"  Analysis ID: {analysis.analysis_id}")
            print(f"  Type: {analysis.analysis_type.value}")
            print(f"  Performance Score: {analysis.performance_score:.1f}/100")
            print(f"  Metrics Analyzed: {analysis.metrics_analyzed}")
            print(f"  Bottlenecks Found: {analysis.bottlenecks_identified}")
            print(f"  Duration: {analysis.duration_seconds:.2f}s")

            if analysis.recommendations:
                print("\nRecommendations:")
                for rec in analysis.recommendations[:5]:  # Show first 5
                    print(f"  • {rec}")

            if args.export:
                if analyzer.export_performance_report(args.export, analysis):
                    print(f"\nAnalysis report exported to {args.export}")
                else:
                    print("\nFailed to export analysis report")
                    return 1

        elif args.status:
            # Show current status
            status = analyzer.get_current_performance_status()

            print("Current Performance Status:")
            print(f"  Timestamp: {status['timestamp']}")
            print(f"  Overall Health: {status['overall_health']}")

            if status["metrics"]:
                print("\nMetrics:")
                for metric_name, metric_data in list(status["metrics"].items())[
                    :10
                ]:  # Show first 10
                    print(
                        f"  {metric_name}: {metric_data['value']:.2f}{metric_data.get('unit', '')} "
                        f"({metric_data['level']})"
                    )

            if status["alerts"]:
                print("\nAlerts:")
                for alert in status["alerts"]:
                    print(f"  ⚠️  {alert}")

            if status["recommendations"]:
                print("\nQuick Recommendations:")
                for rec in status["recommendations"][:3]:  # Show first 3
                    print(f"  • {rec}")

        else:
            # Default: show help
            parser.print_help()

    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
        analyzer.stop_monitoring()
    except Exception as e:
        print(f"\nPerformance analysis failed: {e}")
        analyzer.stop_monitoring()
        return 1

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
