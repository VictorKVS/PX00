from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from uuid import uuid4

from px00.epistemics import ClaimAssessment, ClaimEvidenceEvaluator, EvidenceItem
from px00.knowledge_graph import ClaimEvidenceGraph


@dataclass(frozen=True)
class ImmutableClaimAssessment:
    assessment_id: str
    claim_id: str
    evaluated_at: str
    evaluator_ref: str
    evaluator_version: str
    status: str
    evidence_refs: tuple[str, ...]
    evidence_set_hash: str
    hash_algorithm: str
    support_score: float
    contradiction_score: float
    source_reliability: float
    evidence_quality: float
    independence: float
    recency: float
    directness: float
    corroboration: float
    previous_assessment_ref: str | None = None


class ClaimAssessmentStore:
    EVALUATOR_REF = "px00.ClaimEvidenceEvaluator"
    EVALUATOR_VERSION = "0.1"

    def __init__(self) -> None:
        self._items: dict[str, ImmutableClaimAssessment] = {}
        self._latest_by_claim: dict[str, str] = {}
        self._evaluator = ClaimEvidenceEvaluator()

    @staticmethod
    def _canonical_json(value: object) -> bytes:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

    @classmethod
    def _evidence_digest(cls, items: tuple[EvidenceItem, ...]) -> str:
        material = [asdict(item) for item in sorted(items, key=lambda item: item.evidence_id)]
        return sha256(cls._canonical_json(material)).hexdigest()

    @staticmethod
    def _to_evaluator_items(graph: ClaimEvidenceGraph, claim_id: str) -> tuple[EvidenceItem, ...]:
        items = []
        for node in graph.evidence_for_claim(claim_id):
            source = graph.sources[node.source_ref]
            # Reference defaults until richer source/evidence quality metadata is added.
            items.append(EvidenceItem(
                evidence_id=node.evidence_id,
                source_id=node.source_ref,
                independence_group=node.independence_group,
                stance=node.stance,
                source_reliability=1.0,
                evidence_quality=1.0,
                recency=1.0,
                directness=1.0,
            ))
        return tuple(sorted(items, key=lambda item: item.evidence_id))

    def assess(self, graph: ClaimEvidenceGraph, claim_id: str, *, evaluated_at: str | None = None) -> ImmutableClaimAssessment:
        if claim_id not in graph.claims:
            raise ValueError("UNKNOWN_CLAIM_REF")
        evidence = self._to_evaluator_items(graph, claim_id)
        calculated: ClaimAssessment = self._evaluator.evaluate(claim_id, evidence)
        previous = self._latest_by_claim.get(claim_id)
        item = ImmutableClaimAssessment(
            assessment_id=f"CLMA-{uuid4().hex[:12]}",
            claim_id=claim_id,
            evaluated_at=evaluated_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            evaluator_ref=self.EVALUATOR_REF,
            evaluator_version=self.EVALUATOR_VERSION,
            status=calculated.status,
            evidence_refs=tuple(x.evidence_id for x in evidence),
            evidence_set_hash=self._evidence_digest(evidence),
            hash_algorithm="sha256",
            support_score=calculated.support_score,
            contradiction_score=calculated.contradiction_score,
            source_reliability=calculated.source_reliability,
            evidence_quality=calculated.evidence_quality,
            independence=calculated.independence,
            recency=calculated.recency,
            directness=calculated.directness,
            corroboration=calculated.corroboration,
            previous_assessment_ref=previous,
        )
        self._items[item.assessment_id] = item
        self._latest_by_claim[claim_id] = item.assessment_id
        return item

    def get(self, assessment_id: str) -> ImmutableClaimAssessment:
        try:
            return self._items[assessment_id]
        except KeyError as exc:
            raise ValueError("UNKNOWN_ASSESSMENT_REF") from exc

    def history(self, claim_id: str) -> tuple[ImmutableClaimAssessment, ...]:
        result = [item for item in self._items.values() if item.claim_id == claim_id]
        return tuple(sorted(result, key=lambda item: item.evaluated_at))
