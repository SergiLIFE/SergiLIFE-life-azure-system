"""
Clinical Validation Framework for L.I.F.E Platform

ASCII-safe logging and minimal external deps. This module provides a thin
framework to design clinical trials and validate a set of equations against
patient EEG data. It is designed to accept an `equations` mapping compatible
with the L.I.F.E algorithm core (e.g., life_algo.equations).

Usage example:

    clinical_validator = ClinicalValidationFramework(life_algo.equations)
    trial_config = clinical_validator.design_clinical_trial(
        primary_endpoint="attention_improvement",
        secondary_endpoints=["academic_performance", "self_regulation"],
        effect_size=0.5,
        power=0.8,
    )

    results = await clinical_validator.validate_all_equations(
        test_data=patient_eeg_data,
        clinical_threshold=0.95,
    )

Copyright 2025 - Sergio Paya Borrull
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


@dataclass
class TrialConfig:
    primary_endpoint: str
    secondary_endpoints: List[str]
    effect_size: float
    power: float
    alpha: float = 0.05
    sample_size_estimate: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class EquationValidationResult:
    equation_name: str
    score: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ClinicalValidationSummary:
    threshold: float
    results: List[EquationValidationResult]
    pass_rate: float
    passed_all: bool
    evaluated_at: datetime = field(default_factory=datetime.utcnow)


class ClinicalValidationFramework:
    """Validates equations on EEG test data against clinical thresholds."""

    def __init__(self, equations: Dict[str, Callable[..., float]]):
        # Expect a mapping like: {"eq2_neuroplasticity": callable, ...}
        self.equations = equations

    def design_clinical_trial(
        self,
        primary_endpoint: str,
        secondary_endpoints: List[str],
        effect_size: float,
        power: float,
        alpha: float = 0.05,
    ) -> TrialConfig:
        # Simple Cohen's d based sample size ballpark (very rough):
        # n per group ~ 16 / d^2 for 80% power at alpha=0.05 (rule of thumb)
        # Scale for arbitrary power linearly (approx) for this stub.
        base = 16.0 / max(1e-6, effect_size**2)
        power_scale = max(0.1, power / 0.8)
        n_per_group = int(round(base * power_scale))
        sample_size_estimate = max(20, n_per_group * 2)

        return TrialConfig(
            primary_endpoint=primary_endpoint,
            secondary_endpoints=secondary_endpoints,
            effect_size=effect_size,
            power=power,
            alpha=alpha,
            sample_size_estimate=sample_size_estimate,
        )

    async def validate_all_equations(
        self,
        test_data: List[float],
        clinical_threshold: float = 0.95,
        context: Optional[Dict[str, Any]] = None,
    ) -> ClinicalValidationSummary:
        """
        Executes each equation function and derives a normalized score in [0,1].
        This is a pragmatic stub: in a real setting, pass domain inputs per eq.
        """
        if not isinstance(test_data, list) or len(test_data) == 0:
            raise ValueError("test_data must be a non-empty list of floats")

        # Primitive normalization anchors for stub scoring
        mean_signal = statistics.fmean(test_data)
        std_signal = statistics.pstdev(test_data) if len(test_data) > 1 else 0.0

        results: List[EquationValidationResult] = []
        # Run equations concurrently if they are IO-bound; here just sequential for clarity
        for name, fn in self.equations.items():
            try:
                # Provide simple arguments by convention; override via context
                kwargs = {"mean_signal": mean_signal, "std_signal": std_signal}
                if context:
                    kwargs.update(context)

                raw_value = fn(**{k: v for k, v in kwargs.items() if k in fn.__code__.co_varnames})  # type: ignore[attr-defined]

                # Normalize to 0..1 using a simple logistic-like squash
                score = self._normalize_score(raw_value)
                passed = score >= clinical_threshold
                results.append(
                    EquationValidationResult(
                        equation_name=name,
                        score=score,
                        passed=passed,
                        details={"raw": raw_value},
                    )
                )
            except Exception as ex:  # pragma: no cover (best-effort safety)
                results.append(
                    EquationValidationResult(
                        equation_name=name,
                        score=0.0,
                        passed=False,
                        details={"error": str(ex)},
                    )
                )

        pass_rate = sum(1 for r in results if r.passed) / max(1, len(results))
        return ClinicalValidationSummary(
            threshold=clinical_threshold,
            results=results,
            pass_rate=pass_rate,
            passed_all=all(r.passed for r in results),
        )

    def _normalize_score(self, x: float) -> float:
        # Squash to ~0..1 without external deps
        # score = 1 / (1 + exp(-x)) approximated by rational function for safety
        try:
            # Clip extreme values
            if x > 10:
                return 0.999
            if x < -10:
                return 0.001
            # Center around 0.5 for x=0; slope modest
            return 0.5 + (x / 20.0)
        except Exception:
            return 0.0
