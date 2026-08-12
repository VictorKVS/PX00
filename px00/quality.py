from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json


@dataclass(frozen=True)
class SourceQualityAssessment:
    source_assessment_id: str
    source_ref: str
    evaluator_ref: str
    evaluator_version: str
    evaluated_at: str
    basis_refs: tuple[str, ...]
    reliability: float
    authority: float
    recency: float
    conflict_of_interest: float
    assessment_hash: str


@dataclass(frozen=True)
class EvidenceQualityAssessment:
    evidence_assessment_id: str
    evidence_ref: str
    source_assessment_ref: str
    evaluator_ref: str
    evaluator_version: str
    evaluated_at: str
    basis_refs: tuple[str, ...]
    quality: float
    directness: float
    completeness: float
    reproducibility: float
    relevance: float
    assessment_hash: str


class QualityAssessmentFactory:
    @staticmethod
    def _bounded(value: float) -> float:
        value = float(value)
        if not 0.0 <= value <= 1.0:
            raise ValueError("QUALITY_DIMENSION_OUT_OF_RANGE")
        return value

    @staticmethod
    def _hash(payload: dict) -> str:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        return sha256(encoded).hexdigest()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def source(
        self,
        *,
        source_assessment_id: str,
        source_ref: str,
        evaluator_ref: str,
        evaluator_version: str,
        basis_refs: tuple[str, ...],
        reliability: float,
        authority: float,
        recency: float,
        conflict_of_interest: float,
        evaluated_at: str | None = None,
    ) -> SourceQualityAssessment:
        if not basis_refs:
            raise ValueError("SOURCE_ASSESSMENT_BASIS_REQUIRED")
        payload = {
            "source_assessment_id": source_assessment_id,
            "source_ref": source_ref,
            "evaluator_ref": evaluator_ref,
            "evaluator_version": evaluator_version,
            "evaluated_at": evaluated_at or self._now(),
            "basis_refs": tuple(sorted(basis_refs)),
            "reliability": self._bounded(reliability),
            "authority": self._bounded(authority),
            "recency": self._bounded(recency),
            "conflict_of_interest": self._bounded(conflict_of_interest),
        }
        return SourceQualityAssessment(**payload, assessment_hash=self._hash(payload))

    def evidence(
        self,
        *,
        evidence_assessment_id: str,
        evidence_ref: str,
        source_assessment_ref: str,
        evaluator_ref: str,
        evaluator_version: str,
        basis_refs: tuple[str, ...],
        quality: float,
        directness: float,
        completeness: float,
        reproducibility: float,
        relevance: float,
        evaluated_at: str | None = None,
    ) -> EvidenceQualityAssessment:
        if not basis_refs:
            raise ValueError("EVIDENCE_ASSESSMENT_BASIS_REQUIRED")
        payload = {
            "evidence_assessment_id": evidence_assessment_id,
            "evidence_ref": evidence_ref,
            "source_assessment_ref": source_assessment_ref,
            "evaluator_ref": evaluator_ref,
            "evaluator_version": evaluator_version,
            "evaluated_at": evaluated_at or self._now(),
            "basis_refs": tuple(sorted(basis_refs)),
            "quality": self._bounded(quality),
            "directness": self._bounded(directness),
            "completeness": self._bounded(completeness),
            "reproducibility": self._bounded(reproducibility),
            "relevance": self._bounded(relevance),
        }
        return EvidenceQualityAssessment(**payload, assessment_hash=self._hash(payload))
