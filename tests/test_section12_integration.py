
import asyncio

from life_algorithm_section12_integration import (  # type: ignore[import]
    EducationPilotTelemetry,
    LIFEAlgorithmSection12,
)


def test_education_cycle_runs_without_optional_dependencies():
    orchestrator = LIFEAlgorithmSection12()
    eeg_signal = [0.5 for _ in range(256)]
    report = asyncio.run(
        orchestrator.run_education_cycle(
            eeg_signal,
            tenant_id="tenant-test",
            course_id="course-42",
        )
    )
    assert isinstance(report, EducationPilotTelemetry)
    assert 0.0 <= report.cognitive_load <= 1.0
    assert report.guardrail_state in {"continue", "rollback", "revert", "unknown"}
    assert report.venturi_cognitive >= 0.0
    assert report.venturi_render >= 0.0
    assert report.venturi_offload >= 0.0


def test_federated_daily_sync_aggregates_reports():
    orchestrator = LIFEAlgorithmSection12()
    eeg_signal = [0.5 + (idx % 5) * 0.01 for idx in range(128)]
    education = asyncio.run(
        orchestrator.run_education_cycle(
            eeg_signal,
            tenant_id="tenant-sync",
            course_id="course-sync",
        )
    )
    aggregation = asyncio.run(orchestrator.run_federated_daily_sync([education]))
    assert aggregation.participating_nodes == 1
    assert "avg_latency_ms" in aggregation.metrics_summary
    assert aggregation.guardrail_flags
    assert "avg_venturi_cognitive" in aggregation.metrics_summary
    assert aggregation.metrics_summary["avg_venturi_cognitive"] >= 0.0
