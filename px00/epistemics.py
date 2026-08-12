from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Iterable


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    source_id: str
    independence_group: str
    stance: str  # SUPPORT | CONTRADICT
    source_reliability: float
    evidence_quality: float
    recency: float
    directness: float


@dataclass(frozen=True)
class ClaimAssessment:
    claim_id: str
    status: str
    evidence_refs: tuple[str, ...]
    support_score: float
    contradiction_score: float
    source_reliability: float
    evidence_quality: float
    independence: float
    recency: float
    directness: float
    corroboration: float


class ClaimEvidenceEvaluator:
    """Deterministic support-state evaluator. It does not declare truth."""

    @staticmethod
    def _bounded(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    def evaluate(self, claim_id: str, evidence: Iterable[EvidenceItem]) -> ClaimAssessment:
        items = tuple(evidence)
        if not items:
            return ClaimAssessment(claim_id, "UNSUPPORTED", (), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        support = tuple(x for x in items if x.stance == "SUPPORT")
        contradict = tuple(x for x in items if x.stance == "CONTRADICT")
        if len(support) + len(contradict) != len(items):
            raise ValueError("UNKNOWN_EVIDENCE_STANCE")

        def item_strength(x: EvidenceItem) -> float:
            return mean(self._bounded(v) for v in (x.source_reliability, x.evidence_quality, x.recency, x.directness))

        support_score = mean(item_strength(x) for x in support) if support else 0.0
        contradiction_score = mean(item_strength(x) for x in contradict) if contradict else 0.0
        groups = {x.independence_group for x in support}
        independence = min(1.0, len(groups) / 2.0) if support else 0.0
        corroboration = min(1.0, len(groups) / 2.0) if support else 0.0

        if support and contradict:
            status = "DISPUTED" if support_score >= 0.5 and contradiction_score >= 0.5 else "CONTRADICTED"
        elif contradict:
            status = "REFUTED" if contradiction_score >= 0.75 else "CONTRADICTED"
        elif len(groups) >= 2:
            status = "CORROBORATED"
        else:
            status = "SINGLE_SOURCE"

        return ClaimAssessment(
            claim_id=claim_id,
            status=status,
            evidence_refs=tuple(x.evidence_id for x in items),
            support_score=round(support_score, 4),
            contradiction_score=round(contradiction_score, 4),
            source_reliability=round(mean(self._bounded(x.source_reliability) for x in items), 4),
            evidence_quality=round(mean(self._bounded(x.evidence_quality) for x in items), 4),
            independence=round(independence, 4),
            recency=round(mean(self._bounded(x.recency) for x in items), 4),
            directness=round(mean(self._bounded(x.directness) for x in items), 4),
            corroboration=round(corroboration, 4),
        )
