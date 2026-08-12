from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable


CRISP_MLQ_PHASES = (
    "BUSINESS_AND_DATA_UNDERSTANDING",
    "DATA_ENGINEERING",
    "MODEL_ENGINEERING",
    "QUALITY_ASSURANCE",
    "DEPLOYMENT",
    "MONITORING_AND_MAINTENANCE",
)

DELIVERY_STAGES = ("DEMO", "POC", "MVP", "PRODUCTION")

STAGE_REQUIRED_EVIDENCE: dict[str, frozenset[str]] = {
    "DEMO": frozenset(
        {
            "problem_scope",
            "stakeholder_alignment",
            "scenario_prototype",
        }
    ),
    "POC": frozenset(
        {
            "data_feasibility",
            "baseline",
            "technical_metric",
            "known_data_gaps",
            "go_no_go_evidence",
        }
    ),
    "MVP": frozenset(
        {
            "real_users",
            "real_data",
            "business_metric",
            "product_metric",
            "technical_slo",
            "basic_observability",
            "rollback_path",
        }
    ),
    "PRODUCTION": frozenset(
        {
            "sla_slo",
            "ci_cd_release_governance",
            "security_controls",
            "monitoring_alerting",
            "drift_detection",
            "recovery_dr",
            "support_incident_process",
            "model_governance",
            "economic_effect",
        }
    ),
}


@dataclass(frozen=True)
class CrispMlqPhaseRecord:
    phase: str
    requirements_constraints: tuple[str, ...]
    tasks: tuple[str, ...]
    risks: tuple[str, ...]
    qa_methods: tuple[str, ...]

    def validate(self) -> None:
        if self.phase not in CRISP_MLQ_PHASES:
            raise ValueError("UNKNOWN_CRISP_MLQ_PHASE")
        if not self.requirements_constraints:
            raise ValueError("CRISP_REQUIREMENTS_REQUIRED")
        if not self.tasks:
            raise ValueError("CRISP_TASKS_REQUIRED")
        if not self.risks:
            raise ValueError("CRISP_RISKS_REQUIRED")
        if not self.qa_methods:
            raise ValueError("CRISP_QA_METHODS_REQUIRED")


@dataclass(frozen=True)
class DeliveryGateEvaluation:
    stage: str
    decision: str
    provided_evidence: tuple[str, ...]
    missing_evidence: tuple[str, ...]
    blocking_risk_refs: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return self.decision == "GO"


def evaluate_delivery_gate(
    stage: str,
    evidence: Iterable[str],
    *,
    blocking_risk_refs: Iterable[str] = (),
) -> DeliveryGateEvaluation:
    if stage not in DELIVERY_STAGES:
        raise ValueError("UNKNOWN_DELIVERY_STAGE")
    provided = frozenset(evidence)
    required = STAGE_REQUIRED_EVIDENCE[stage]
    missing = tuple(sorted(required - provided))
    blockers = tuple(sorted(set(blocking_risk_refs)))
    decision = "GO" if not missing and not blockers else "HOLD"
    return DeliveryGateEvaluation(
        stage=stage,
        decision=decision,
        provided_evidence=tuple(sorted(provided)),
        missing_evidence=missing,
        blocking_risk_refs=blockers,
    )


@dataclass(frozen=True)
class QuantitativeRiskInput:
    probability: float
    impact_minimum: float
    impact_mode: float
    impact_maximum: float
    tolerance_limit: float
    percentile_level: float = 0.95
    trials: int = 10_000
    seed: int = 1

    def validate(self) -> None:
        if not 0.0 <= self.probability <= 1.0:
            raise ValueError("RISK_PROBABILITY_OUT_OF_RANGE")
        if self.trials < 100:
            raise ValueError("RISK_TRIALS_TOO_LOW")
        if not 0.0 < self.percentile_level < 1.0:
            raise ValueError("RISK_PERCENTILE_OUT_OF_RANGE")
        if self.impact_minimum > self.impact_mode:
            raise ValueError("RISK_MINIMUM_GREATER_THAN_MODE")
        if self.impact_mode > self.impact_maximum:
            raise ValueError("RISK_MODE_GREATER_THAN_MAXIMUM")
        if self.impact_minimum < 0.0:
            raise ValueError("RISK_NEGATIVE_IMPACT_UNSUPPORTED")


@dataclass(frozen=True)
class QuantitativeRiskResult:
    expected_loss: float
    percentile_loss: float
    probability_exceeding_tolerance: float
    trials: int
    seed: int


def _linear_percentile(sorted_values: list[float], level: float) -> float:
    if not sorted_values:
        raise ValueError("EMPTY_RISK_SAMPLE")
    position = (len(sorted_values) - 1) * level
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)
    fraction = position - lower
    return sorted_values[lower] + (sorted_values[upper] - sorted_values[lower]) * fraction


def simulate_quantitative_risk(spec: QuantitativeRiskInput) -> QuantitativeRiskResult:
    spec.validate()
    rng = random.Random(spec.seed)
    losses: list[float] = []
    exceedances = 0
    total = 0.0

    for _ in range(spec.trials):
        if rng.random() < spec.probability:
            loss = rng.triangular(
                spec.impact_minimum,
                spec.impact_maximum,
                spec.impact_mode,
            )
        else:
            loss = 0.0
        losses.append(loss)
        total += loss
        if loss > spec.tolerance_limit:
            exceedances += 1

    losses.sort()
    return QuantitativeRiskResult(
        expected_loss=total / spec.trials,
        percentile_loss=_linear_percentile(losses, spec.percentile_level),
        probability_exceeding_tolerance=exceedances / spec.trials,
        trials=spec.trials,
        seed=spec.seed,
    )
