from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class ContextTrustAssessment:
    trust_assessment_id: str
    context_package_ref: str
    trust_label: str
    provenance_refs: tuple[str, ...]
    independent_verification_refs: tuple[str, ...] = ()
    taint_reason_refs: tuple[str, ...] = ()


class ContextTrustGate:
    VALID_LABELS = {"TRUSTED_INTERNAL", "VERIFIED_EXTERNAL", "UNTRUSTED_EXTERNAL", "TAINTED"}

    def allow_use(self, assessment: ContextTrustAssessment, *, use_type: str) -> bool:
        if assessment.trust_label not in self.VALID_LABELS:
            raise ValueError("UNKNOWN_CONTEXT_TRUST_LABEL")
        if use_type not in {"ANALYSIS_ONLY", "MATERIAL_REVERSIBLE", "MATERIAL_SENSITIVE"}:
            raise ValueError("UNKNOWN_CONTEXT_USE_TYPE")

        if use_type == "ANALYSIS_ONLY":
            return True

        if assessment.trust_label == "TAINTED":
            return False

        if assessment.trust_label == "UNTRUSTED_EXTERNAL":
            return bool(assessment.independent_verification_refs)

        if use_type == "MATERIAL_SENSITIVE" and assessment.trust_label == "VERIFIED_EXTERNAL":
            return bool(assessment.independent_verification_refs)

        return True

    @staticmethod
    def may_influence_authority(assessment: ContextTrustAssessment) -> bool:
        # Retrieved/model/tool content is never a source of authority.
        return False
