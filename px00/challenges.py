from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from px00.quality import EvidenceQualityAssessment, SourceQualityAssessment


@dataclass(frozen=True)
class AssessmentChallenge:
    challenge_id: str
    target_assessment_ref: str
    target_type: str
    challenger_ref: str
    challenger_version: str
    created_at: str
    reason_code: str
    rationale_summary: str
    evidence_refs: tuple[str, ...]
    proposed_revision: tuple[tuple[str, float], ...] = ()


@dataclass(frozen=True)
class AssessmentReview:
    review_id: str
    challenge_ref: str
    target_assessment_ref: str
    reviewer_ref: str
    reviewer_version: str
    reviewed_at: str
    decision: str
    reason_code: str
    rationale_summary: str
    basis_refs: tuple[str, ...]
    replacement_assessment_ref: str | None = None


class AssessmentChallengeStore:
    DECISIONS = {"REJECT_CHALLENGE", "ACCEPT_CHALLENGE", "ACCEPT_WITH_MODIFICATION", "ESCALATE"}

    def __init__(self) -> None:
        self.source_assessments: dict[str, SourceQualityAssessment] = {}
        self.evidence_assessments: dict[str, EvidenceQualityAssessment] = {}
        self.challenges: dict[str, AssessmentChallenge] = {}
        self.reviews: dict[str, AssessmentReview] = {}
        self.supersedes: dict[str, str] = {}

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def register_source_assessment(self, item: SourceQualityAssessment) -> None:
        if item.source_assessment_id in self.source_assessments or item.source_assessment_id in self.evidence_assessments:
            raise ValueError("ASSESSMENT_ID_REUSE")
        self.source_assessments[item.source_assessment_id] = item

    def register_evidence_assessment(self, item: EvidenceQualityAssessment) -> None:
        if item.evidence_assessment_id in self.source_assessments or item.evidence_assessment_id in self.evidence_assessments:
            raise ValueError("ASSESSMENT_ID_REUSE")
        self.evidence_assessments[item.evidence_assessment_id] = item

    def _target_type(self, assessment_ref: str) -> str:
        if assessment_ref in self.source_assessments:
            return "SOURCE_ASSESSMENT"
        if assessment_ref in self.evidence_assessments:
            return "EVIDENCE_ASSESSMENT"
        raise ValueError("UNKNOWN_ASSESSMENT_REF")

    def challenge(
        self,
        *,
        target_assessment_ref: str,
        challenger_ref: str,
        challenger_version: str,
        reason_code: str,
        rationale_summary: str,
        evidence_refs: tuple[str, ...],
        proposed_revision: dict[str, float] | None = None,
        challenge_id: str | None = None,
        created_at: str | None = None,
    ) -> AssessmentChallenge:
        target_type = self._target_type(target_assessment_ref)
        if not reason_code or not rationale_summary:
            raise ValueError("CHALLENGE_REASON_REQUIRED")
        allowed = {
            "SOURCE_ASSESSMENT": {"reliability", "authority", "recency", "conflict_of_interest"},
            "EVIDENCE_ASSESSMENT": {"quality", "directness", "completeness", "reproducibility", "relevance"},
        }[target_type]
        proposed_revision = proposed_revision or {}
        if not set(proposed_revision).issubset(allowed):
            raise ValueError("INVALID_PROPOSED_REVISION_DIMENSION")
        for value in proposed_revision.values():
            if not 0.0 <= float(value) <= 1.0:
                raise ValueError("QUALITY_DIMENSION_OUT_OF_RANGE")
        item = AssessmentChallenge(
            challenge_id=challenge_id or f"CHAL-{uuid4().hex[:12]}",
            target_assessment_ref=target_assessment_ref,
            target_type=target_type,
            challenger_ref=challenger_ref,
            challenger_version=challenger_version,
            created_at=created_at or self._now(),
            reason_code=reason_code,
            rationale_summary=rationale_summary,
            evidence_refs=tuple(sorted(evidence_refs)),
            proposed_revision=tuple(sorted((key, float(value)) for key, value in proposed_revision.items())),
        )
        if item.challenge_id in self.challenges:
            raise ValueError("CHALLENGE_ID_REUSE")
        self.challenges[item.challenge_id] = item
        return item

    def review(
        self,
        *,
        challenge_ref: str,
        reviewer_ref: str,
        reviewer_version: str,
        decision: str,
        reason_code: str,
        rationale_summary: str,
        basis_refs: tuple[str, ...],
        replacement_assessment: SourceQualityAssessment | EvidenceQualityAssessment | None = None,
        review_id: str | None = None,
        reviewed_at: str | None = None,
    ) -> AssessmentReview:
        if challenge_ref not in self.challenges:
            raise ValueError("UNKNOWN_CHALLENGE_REF")
        if decision not in self.DECISIONS:
            raise ValueError("UNKNOWN_REVIEW_DECISION")
        challenge = self.challenges[challenge_ref]
        accepts = decision in {"ACCEPT_CHALLENGE", "ACCEPT_WITH_MODIFICATION"}
        if accepts and replacement_assessment is None:
            raise ValueError("REPLACEMENT_ASSESSMENT_REQUIRED")
        if not accepts and replacement_assessment is not None:
            raise ValueError("REPLACEMENT_NOT_ALLOWED_FOR_NON_ACCEPTING_REVIEW")
        replacement_ref = None
        if replacement_assessment is not None:
            if challenge.target_type == "SOURCE_ASSESSMENT":
                if not isinstance(replacement_assessment, SourceQualityAssessment):
                    raise ValueError("REPLACEMENT_TYPE_MISMATCH")
                if replacement_assessment.source_ref != self.source_assessments[challenge.target_assessment_ref].source_ref:
                    raise ValueError("REPLACEMENT_SUBJECT_MISMATCH")
                self.register_source_assessment(replacement_assessment)
                replacement_ref = replacement_assessment.source_assessment_id
            else:
                if not isinstance(replacement_assessment, EvidenceQualityAssessment):
                    raise ValueError("REPLACEMENT_TYPE_MISMATCH")
                if replacement_assessment.evidence_ref != self.evidence_assessments[challenge.target_assessment_ref].evidence_ref:
                    raise ValueError("REPLACEMENT_SUBJECT_MISMATCH")
                self.register_evidence_assessment(replacement_assessment)
                replacement_ref = replacement_assessment.evidence_assessment_id
            self.supersedes[replacement_ref] = challenge.target_assessment_ref
        item = AssessmentReview(
            review_id=review_id or f"REVIEW-{uuid4().hex[:12]}",
            challenge_ref=challenge_ref,
            target_assessment_ref=challenge.target_assessment_ref,
            reviewer_ref=reviewer_ref,
            reviewer_version=reviewer_version,
            reviewed_at=reviewed_at or self._now(),
            decision=decision,
            reason_code=reason_code,
            rationale_summary=rationale_summary,
            basis_refs=tuple(sorted(basis_refs)),
            replacement_assessment_ref=replacement_ref,
        )
        if item.review_id in self.reviews:
            raise ValueError("REVIEW_ID_REUSE")
        self.reviews[item.review_id] = item
        return item

    def lineage(self, assessment_ref: str) -> tuple[str, ...]:
        self._target_type(assessment_ref)
        result = [assessment_ref]
        cursor = assessment_ref
        while cursor in self.supersedes:
            cursor = self.supersedes[cursor]
            result.append(cursor)
        return tuple(result)
