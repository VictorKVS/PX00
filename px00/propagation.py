from __future__ import annotations

from dataclasses import dataclass

from px00.assessments import ClaimAssessmentStore, ImmutableClaimAssessment
from px00.challenges import AssessmentChallengeStore, AssessmentReview
from px00.knowledge_graph import ClaimEvidenceGraph
from px00.quality import EvidenceQualityAssessment, SourceQualityAssessment


@dataclass(frozen=True)
class ReassessmentPropagationResult:
    review_ref: str
    affected_claims: tuple[str, ...]
    new_claim_assessment_refs: tuple[str, ...]
    status_changes: tuple[tuple[str, str | None, str], ...]


class CausalReassessmentPropagator:
    """Propagates accepted quality-review changes into new immutable claim assessments."""

    ACCEPTING = {"ACCEPT_CHALLENGE", "ACCEPT_WITH_MODIFICATION"}

    def __init__(self, claim_assessments: ClaimAssessmentStore) -> None:
        self._claim_assessments = claim_assessments

    @staticmethod
    def _affected_claims(graph: ClaimEvidenceGraph, target_type: str, subject_ref: str) -> tuple[str, ...]:
        if target_type == "SOURCE_ASSESSMENT":
            evidence_ids = {eid for eid, node in graph.evidence.items() if node.source_ref == subject_ref}
        else:
            evidence_ids = {subject_ref}
        claims = {
            claim_id
            for claim_id, evidence_id in graph.support_edges | graph.contradiction_edges
            if evidence_id in evidence_ids
        }
        return tuple(sorted(claims))

    def propagate(
        self,
        *,
        graph: ClaimEvidenceGraph,
        review_store: AssessmentChallengeStore,
        review_ref: str,
        source_quality: dict[str, SourceQualityAssessment],
        evidence_quality: dict[str, EvidenceQualityAssessment],
        refreshed_evidence_quality: dict[str, EvidenceQualityAssessment] | None = None,
        evaluated_at: str | None = None,
    ) -> ReassessmentPropagationResult:
        if review_ref not in review_store.reviews:
            raise ValueError("UNKNOWN_REVIEW_REF")
        review: AssessmentReview = review_store.reviews[review_ref]
        if review.decision not in self.ACCEPTING:
            raise ValueError("NON_ACCEPTING_REVIEW_CANNOT_PROPAGATE")
        if not review.replacement_assessment_ref:
            raise ValueError("REPLACEMENT_ASSESSMENT_REQUIRED")

        challenge = review_store.challenges[review.challenge_ref]
        old_status_by_claim: dict[str, str | None] = {}
        for claim_id in graph.claims:
            history = self._claim_assessments.history(claim_id)
            old_status_by_claim[claim_id] = history[-1].status if history else None

        if challenge.target_type == "SOURCE_ASSESSMENT":
            replacement = review_store.source_assessments[review.replacement_assessment_ref]
            subject_ref = replacement.source_ref
            source_quality[subject_ref] = replacement
            refreshed_evidence_quality = refreshed_evidence_quality or {}
            for evidence_id, node in graph.evidence.items():
                if node.source_ref != subject_ref:
                    continue
                refreshed = refreshed_evidence_quality.get(evidence_id)
                if refreshed is None:
                    raise ValueError("REFRESHED_EVIDENCE_ASSESSMENT_REQUIRED")
                if refreshed.evidence_ref != evidence_id or refreshed.source_assessment_ref != replacement.source_assessment_id:
                    raise ValueError("REFRESHED_EVIDENCE_ASSESSMENT_MISMATCH")
                evidence_quality[evidence_id] = refreshed
        else:
            replacement = review_store.evidence_assessments[review.replacement_assessment_ref]
            subject_ref = replacement.evidence_ref
            evidence_quality[subject_ref] = replacement
            source_ref = graph.evidence[subject_ref].source_ref
            active_source = source_quality.get(source_ref)
            if active_source is None or replacement.source_assessment_ref != active_source.source_assessment_id:
                raise ValueError("REPLACEMENT_EVIDENCE_SOURCE_ASSESSMENT_MISMATCH")

        affected = self._affected_claims(graph, challenge.target_type, subject_ref)
        created: list[ImmutableClaimAssessment] = []
        changes: list[tuple[str, str | None, str]] = []
        for claim_id in affected:
            new_assessment = self._claim_assessments.assess(
                graph,
                claim_id,
                source_quality=source_quality,
                evidence_quality=evidence_quality,
                evaluated_at=evaluated_at,
                caused_by_review_ref=review_ref,
            )
            created.append(new_assessment)
            changes.append((claim_id, old_status_by_claim.get(claim_id), new_assessment.status))

        return ReassessmentPropagationResult(
            review_ref=review_ref,
            affected_claims=affected,
            new_claim_assessment_refs=tuple(item.assessment_id for item in created),
            status_changes=tuple(changes),
        )
