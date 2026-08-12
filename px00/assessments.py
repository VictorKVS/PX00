from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from uuid import uuid4

from px00.epistemics import ClaimAssessment, ClaimEvidenceEvaluator, EvidenceItem
from px00.knowledge_graph import ClaimEvidenceGraph
from px00.quality import EvidenceQualityAssessment, SourceQualityAssessment


@dataclass(frozen=True)
class ImmutableClaimAssessment:
    assessment_id: str
    claim_id: str
    evaluated_at: str
    evaluator_ref: str
    evaluator_version: str
    status: str
    evidence_refs: tuple[str, ...]
    source_assessment_refs: tuple[str, ...]
    evidence_assessment_refs: tuple[str, ...]
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
    caused_by_review_ref: str | None = None


class ClaimAssessmentStore:
    EVALUATOR_REF = "px00.ClaimEvidenceEvaluator"
    EVALUATOR_VERSION = "0.3"

    def __init__(self) -> None:
        self._items: dict[str, ImmutableClaimAssessment] = {}
        self._latest_by_claim: dict[str, str] = {}
        self._evaluator = ClaimEvidenceEvaluator()

    @staticmethod
    def _canonical_json(value: object) -> bytes:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

    @classmethod
    def _evidence_digest(cls, items: tuple[EvidenceItem, ...], source_refs: tuple[str, ...], evidence_refs: tuple[str, ...]) -> str:
        material = {
            "evidence": [asdict(item) for item in sorted(items, key=lambda item: item.evidence_id)],
            "source_assessments": sorted(source_refs),
            "evidence_assessments": sorted(evidence_refs),
        }
        return sha256(cls._canonical_json(material)).hexdigest()

    @staticmethod
    def _to_evaluator_items(graph: ClaimEvidenceGraph, claim_id: str, source_quality: dict[str, SourceQualityAssessment], evidence_quality: dict[str, EvidenceQualityAssessment]) -> tuple[tuple[EvidenceItem, ...], tuple[str, ...], tuple[str, ...]]:
        items=[]; source_refs=[]; evidence_refs=[]
        for node in graph.evidence_for_claim(claim_id):
            source_assessment=source_quality.get(node.source_ref); evidence_assessment=evidence_quality.get(node.evidence_id)
            if source_assessment is None: raise ValueError("SOURCE_QUALITY_ASSESSMENT_REQUIRED")
            if evidence_assessment is None: raise ValueError("EVIDENCE_QUALITY_ASSESSMENT_REQUIRED")
            if evidence_assessment.source_assessment_ref!=source_assessment.source_assessment_id: raise ValueError("EVIDENCE_SOURCE_ASSESSMENT_MISMATCH")
            items.append(EvidenceItem(node.evidence_id,node.source_ref,node.independence_group,node.stance,source_assessment.reliability,evidence_assessment.quality,source_assessment.recency,evidence_assessment.directness))
            source_refs.append(source_assessment.source_assessment_id); evidence_refs.append(evidence_assessment.evidence_assessment_id)
        return tuple(sorted(items,key=lambda x:x.evidence_id)),tuple(sorted(source_refs)),tuple(sorted(evidence_refs))

    def assess(self, graph: ClaimEvidenceGraph, claim_id: str, *, source_quality: dict[str, SourceQualityAssessment], evidence_quality: dict[str, EvidenceQualityAssessment], evaluated_at: str | None=None, caused_by_review_ref: str | None=None) -> ImmutableClaimAssessment:
        if claim_id not in graph.claims: raise ValueError("UNKNOWN_CLAIM_REF")
        evidence,source_refs,evidence_refs=self._to_evaluator_items(graph,claim_id,source_quality,evidence_quality)
        calculated: ClaimAssessment=self._evaluator.evaluate(claim_id,evidence); previous=self._latest_by_claim.get(claim_id)
        item=ImmutableClaimAssessment(
            assessment_id=f"CLMA-{uuid4().hex[:12]}",claim_id=claim_id,evaluated_at=evaluated_at or datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),
            evaluator_ref=self.EVALUATOR_REF,evaluator_version=self.EVALUATOR_VERSION,status=calculated.status,evidence_refs=tuple(x.evidence_id for x in evidence),
            source_assessment_refs=source_refs,evidence_assessment_refs=evidence_refs,evidence_set_hash=self._evidence_digest(evidence,source_refs,evidence_refs),hash_algorithm="sha256",
            support_score=calculated.support_score,contradiction_score=calculated.contradiction_score,source_reliability=calculated.source_reliability,evidence_quality=calculated.evidence_quality,
            independence=calculated.independence,recency=calculated.recency,directness=calculated.directness,corroboration=calculated.corroboration,
            previous_assessment_ref=previous,caused_by_review_ref=caused_by_review_ref)
        self._items[item.assessment_id]=item; self._latest_by_claim[claim_id]=item.assessment_id; return item

    def get(self, assessment_id: str) -> ImmutableClaimAssessment:
        try: return self._items[assessment_id]
        except KeyError as exc: raise ValueError("UNKNOWN_ASSESSMENT_REF") from exc

    def history(self, claim_id: str) -> tuple[ImmutableClaimAssessment,...]:
        return tuple(sorted((x for x in self._items.values() if x.claim_id==claim_id),key=lambda x:x.evaluated_at))
