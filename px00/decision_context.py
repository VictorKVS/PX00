from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Tuple

from px00.decision_materiality import DecisionMaterialityAssessment, DecisionMaterialityGate
from px00.recorder import TraceDecisionContext


class DecisionContextError(ValueError):
    pass


@dataclass(frozen=True)
class GovernedProfessionalDecision:
    decision_id: str
    run_id: str
    role_ref: str
    assignment_ref: str
    materiality_class: str
    decision_question: str
    requirement_refs: Tuple[str, ...]
    constraint_refs: Tuple[str, ...]
    option_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    chosen_disposition: str
    chosen_option_refs: Tuple[str, ...] = ()
    rationale_summary: str = ""
    review_refs: Tuple[str, ...] = ()
    approval_refs: Tuple[str, ...] = ()
    verification_plan_ref: str = ""
    knowledge_snapshot_refs: Tuple[str, ...] = ()

    def canonical_digest(self) -> str:
        payload = asdict(self)
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        return sha256(raw).hexdigest()


class DecisionContextBinder:
    """Binds a material professional decision to a RUN only after PX00-NORM-DM-0001 passes."""

    _DISPOSITIONS = {
        "SELECT_OPTION",
        "MULTIPLE_VALID_OPTIONS",
        "REQUEST_MORE_EVIDENCE",
        "ESCALATE",
        "NO_GO",
    }

    @staticmethod
    def _require(value: str, code: str) -> None:
        if not value.strip():
            raise DecisionContextError(code)

    @staticmethod
    def _require_refs(values: Tuple[str, ...], code: str) -> None:
        if not values or any(not item.strip() for item in values):
            raise DecisionContextError(code)
        if len(set(values)) != len(values):
            raise DecisionContextError(f"DUPLICATE_{code}")

    def bind(
        self,
        *,
        decision: GovernedProfessionalDecision,
        assessment: DecisionMaterialityAssessment,
    ) -> TraceDecisionContext:
        self._require(decision.decision_id, "DECISION_ID_REQUIRED")
        self._require(decision.run_id, "RUN_ID_REQUIRED")
        self._require(decision.role_ref, "ROLE_REF_REQUIRED")
        self._require(decision.assignment_ref, "ASSIGNMENT_REF_REQUIRED")
        self._require(decision.decision_question, "DECISION_QUESTION_REQUIRED")
        self._require(decision.rationale_summary, "RATIONALE_REQUIRED")

        if decision.chosen_disposition not in self._DISPOSITIONS:
            raise DecisionContextError("UNKNOWN_DECISION_DISPOSITION")
        if assessment.decision_ref != decision.decision_id:
            raise DecisionContextError("DECISION_ASSESSMENT_REF_MISMATCH")
        if assessment.declared_class != decision.materiality_class:
            raise DecisionContextError("DECISION_MATERIALITY_MISMATCH")

        gate = DecisionMaterialityGate().evaluate(assessment)
        if gate.status != "PASS":
            raise DecisionContextError(f"MATERIALITY_GATE_{gate.status}")

        level = decision.materiality_class
        if level in {"D1_IMPLEMENTATION", "D2_ARCHITECTURE_PRODUCT", "D3_REGULATED_SAFETY_CRITICAL"}:
            self._require_refs(decision.evidence_refs, "EVIDENCE_REFS_REQUIRED")
            self._require(decision.verification_plan_ref, "VERIFICATION_PLAN_REF_REQUIRED")

        if level in {"D2_ARCHITECTURE_PRODUCT", "D3_REGULATED_SAFETY_CRITICAL"}:
            self._require_refs(decision.requirement_refs, "REQUIREMENT_REFS_REQUIRED")
            self._require_refs(decision.constraint_refs, "CONSTRAINT_REFS_REQUIRED")
            self._require_refs(decision.option_refs, "OPTION_REFS_REQUIRED")
            self._require_refs(decision.review_refs, "REVIEW_REFS_REQUIRED")

        if level == "D3_REGULATED_SAFETY_CRITICAL":
            self._require_refs(decision.approval_refs, "APPROVAL_REFS_REQUIRED")

        if decision.chosen_disposition == "SELECT_OPTION":
            self._require_refs(decision.chosen_option_refs, "CHOSEN_OPTION_REFS_REQUIRED")
            if any(ref not in decision.option_refs for ref in decision.chosen_option_refs):
                raise DecisionContextError("CHOSEN_OPTION_NOT_DECLARED")

        return TraceDecisionContext(
            decision_refs=(decision.decision_id,),
            decision_digests=(decision.canonical_digest(),),
            materiality_classes=(decision.materiality_class,),
        )
