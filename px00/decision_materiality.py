from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet


_ORDER = {
    "D0_LOCAL_CONVENTIONAL": 0,
    "D1_IMPLEMENTATION": 1,
    "D2_ARCHITECTURE_PRODUCT": 2,
    "D3_REGULATED_SAFETY_CRITICAL": 3,
}

_REQUIRED_EVIDENCE = {
    "D0_LOCAL_CONVENTIONAL": frozenset({"CONVENTION_OR_PROJECT_RULE"}),
    "D1_IMPLEMENTATION": frozenset({"TECHNICAL_REFERENCE", "VERIFICATION"}),
    "D2_ARCHITECTURE_PRODUCT": frozenset(
        {
            "REQUIREMENTS",
            "CONSTRAINTS",
            "ALTERNATIVES",
            "DECISION_CRITERIA",
            "COST_OR_RESOURCE_VIEW",
            "RISK_VIEW",
            "TECHNICAL_REFERENCE",
            "VERIFICATION_PLAN",
        }
    ),
    "D3_REGULATED_SAFETY_CRITICAL": frozenset(
        {
            "REQUIREMENTS",
            "CONSTRAINTS",
            "ALTERNATIVES",
            "DECISION_CRITERIA",
            "COST_OR_RESOURCE_VIEW",
            "RISK_VIEW",
            "PRIMARY_OR_NORMATIVE_SOURCE",
            "APPLICABILITY",
            "RESIDUAL_RISK",
            "VERIFICATION_PLAN",
            "QUALIFIED_INDEPENDENT_REVIEW",
        }
    ),
}

_RISK_FLOOR = {
    "S0": "D0_LOCAL_CONVENTIONAL",
    "S1": "D0_LOCAL_CONVENTIONAL",
    "S2": "D1_IMPLEMENTATION",
    "S3": "D2_ARCHITECTURE_PRODUCT",
    "S4": "D3_REGULATED_SAFETY_CRITICAL",
}


@dataclass(frozen=True)
class DecisionMaterialityAssessment:
    decision_ref: str
    declared_class: str
    consequence: str
    reversibility: str
    uncertainty: str
    blast_radius: str
    risk_severity: str
    evidence_categories_present: FrozenSet[str]
    independent_review_present: bool = False
    approval_present: bool = False
    regulated_or_legally_mandatory: bool = False
    safety_critical: bool = False
    irreversible_material_external_effect: bool = False
    architecture_or_product_boundary: bool = False
    material_vendor_or_lock_in: bool = False


@dataclass(frozen=True)
class MaterialityGateResult:
    status: str
    declared_class: str
    required_floor: str
    missing_evidence: tuple[str, ...]
    independent_review_required: bool
    approval_required: bool
    reason_code: str


class DecisionMaterialityGate:
    """Fail-closed reference gate for PX00-NORM-DM-0001."""

    @staticmethod
    def _max_class(*classes: str) -> str:
        return max(classes, key=lambda item: _ORDER[item])

    def required_floor(self, item: DecisionMaterialityAssessment) -> str:
        floor = _RISK_FLOOR[item.risk_severity]

        if (
            item.consequence == "CRITICAL"
            or item.regulated_or_legally_mandatory
            or item.safety_critical
            or item.irreversible_material_external_effect
            or item.risk_severity == "S4"
        ):
            return "D3_REGULATED_SAFETY_CRITICAL"

        d2_trigger = (
            item.consequence == "HIGH"
            or item.reversibility == "HARD"
            or item.uncertainty in {"HIGH", "VERY_HIGH"}
            or item.blast_radius in {"ORGANIZATION", "CUSTOMER_OR_PUBLIC", "PHYSICAL_WORLD"}
            or item.architecture_or_product_boundary
            or item.material_vendor_or_lock_in
            or item.risk_severity == "S3"
        )
        if d2_trigger:
            floor = self._max_class(floor, "D2_ARCHITECTURE_PRODUCT")

        return floor

    def evaluate(self, item: DecisionMaterialityAssessment) -> MaterialityGateResult:
        if item.declared_class not in _ORDER:
            raise ValueError("UNKNOWN_MATERIALITY_CLASS")
        if item.risk_severity not in _RISK_FLOOR:
            raise ValueError("UNKNOWN_RISK_SEVERITY")

        floor = self.required_floor(item)
        if _ORDER[item.declared_class] < _ORDER[floor]:
            return MaterialityGateResult(
                status="MATERIALITY_UNDERCLASSIFIED",
                declared_class=item.declared_class,
                required_floor=floor,
                missing_evidence=(),
                independent_review_required=_ORDER[floor] >= _ORDER["D2_ARCHITECTURE_PRODUCT"],
                approval_required=floor == "D3_REGULATED_SAFETY_CRITICAL",
                reason_code="DECLARED_CLASS_BELOW_MATERIALITY_FLOOR",
            )

        required = _REQUIRED_EVIDENCE[item.declared_class]
        missing = tuple(sorted(required - item.evidence_categories_present))
        if missing:
            return MaterialityGateResult(
                status="INSUFFICIENT_EVIDENCE",
                declared_class=item.declared_class,
                required_floor=floor,
                missing_evidence=missing,
                independent_review_required=_ORDER[item.declared_class] >= _ORDER["D2_ARCHITECTURE_PRODUCT"],
                approval_required=item.declared_class == "D3_REGULATED_SAFETY_CRITICAL",
                reason_code="MINIMUM_EVIDENCE_NOT_SATISFIED",
            )

        review_required = _ORDER[item.declared_class] >= _ORDER["D2_ARCHITECTURE_PRODUCT"]
        if review_required and not item.independent_review_present:
            return MaterialityGateResult(
                status="REVIEW_REQUIRED",
                declared_class=item.declared_class,
                required_floor=floor,
                missing_evidence=(),
                independent_review_required=True,
                approval_required=item.declared_class == "D3_REGULATED_SAFETY_CRITICAL",
                reason_code="INDEPENDENT_REVIEW_REQUIRED_BY_MATERIALITY",
            )

        approval_required = item.declared_class == "D3_REGULATED_SAFETY_CRITICAL"
        if approval_required and not item.approval_present:
            return MaterialityGateResult(
                status="APPROVAL_REQUIRED",
                declared_class=item.declared_class,
                required_floor=floor,
                missing_evidence=(),
                independent_review_required=True,
                approval_required=True,
                reason_code="ACCOUNTABLE_APPROVAL_REQUIRED_BY_D3_REFERENCE_GATE",
            )

        return MaterialityGateResult(
            status="PASS",
            declared_class=item.declared_class,
            required_floor=floor,
            missing_evidence=(),
            independent_review_required=review_required,
            approval_required=approval_required,
            reason_code="MATERIALITY_EVIDENCE_FLOOR_SATISFIED",
        )
