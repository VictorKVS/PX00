from __future__ import annotations
from dataclasses import dataclass


MATURITY_ORDER = {
    "M0_CONCEPT": 0,
    "M1_PROTOTYPE": 1,
    "M2_INTEGRATED_PROTOTYPE": 2,
    "M3_CONTROLLED_PILOT": 3,
    "M4_PRE_PRODUCTION": 4,
    "M5_PRODUCTION": 5,
}

MAX_UNRESOLVED_BY_SEVERITY = {
    "S4": "M0_CONCEPT",
    "S3": "M2_INTEGRATED_PROTOTYPE",
    "S2": "M3_CONTROLLED_PILOT",
    "S1": "M4_PRE_PRODUCTION",
    "S0": "M5_PRODUCTION",
}


@dataclass(frozen=True)
class RiskGateInput:
    risk_id: str
    severity: str
    status: str
    affected_scope_refs: tuple[str, ...]
    treatment_type: str
    containment_verified: bool


@dataclass(frozen=True)
class PromotionDecision:
    allowed: bool
    blockers: tuple[str, ...]
    rationale: tuple[str, ...]


class RiskMaturityGate:
    def evaluate(self, *, target_maturity: str, promoted_scope_refs: tuple[str, ...], risks: tuple[RiskGateInput, ...]) -> PromotionDecision:
        if target_maturity not in MATURITY_ORDER:
            raise ValueError("UNKNOWN_MATURITY")
        scope = set(promoted_scope_refs)
        blockers: list[str] = []
        rationale: list[str] = []

        for risk in risks:
            if risk.severity not in MAX_UNRESOLVED_BY_SEVERITY:
                raise ValueError("UNKNOWN_RISK_SEVERITY")
            if not scope.intersection(risk.affected_scope_refs):
                continue
            if risk.status in {"RESOLVED", "SUPERSEDED"}:
                continue
            if risk.severity == "S4" and risk.treatment_type in {"ACCEPT", "MONITOR"}:
                blockers.append(risk.risk_id)
                rationale.append(f"{risk.risk_id}: S4 cannot be accepted or merely monitored")
                continue
            if risk.severity in {"S4", "S3", "S2", "S1"} and not risk.containment_verified:
                blockers.append(risk.risk_id)
                rationale.append(f"{risk.risk_id}: containment is not verified")
                continue
            max_level = MATURITY_ORDER[MAX_UNRESOLVED_BY_SEVERITY[risk.severity]]
            if MATURITY_ORDER[target_maturity] > max_level:
                blockers.append(risk.risk_id)
                rationale.append(f"{risk.risk_id}: unresolved {risk.severity} exceeds maturity gate")

        return PromotionDecision(not blockers, tuple(sorted(set(blockers))), tuple(rationale))
