from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


CELL_ORDER = {
    "UNSCOPED": 0,
    "EMPTY": 1,
    "SEEDED": 2,
    "EVIDENCE_BACKED": 3,
    "INDEPENDENTLY_REVIEWED": 4,
    "EXPERT_READY": 5,
}


@dataclass(frozen=True)
class CoverageCell:
    cell_id: str
    domain: str
    criticality: str
    status: str
    provenance_complete: bool
    quality_assessed: bool
    temporal_scope_pinned: bool
    conflicts_visible: bool
    freshness_current: bool

    def validate(self) -> None:
        if self.criticality not in {"FOUNDATIONAL", "IMPORTANT", "SUPPORTING"}:
            raise ValueError("INVALID_SECURITY_KNOWLEDGE_CELL_CRITICALITY")
        if self.status == "STALE_OR_REASSESSMENT_REQUIRED":
            return
        if self.status not in CELL_ORDER:
            raise ValueError("INVALID_SECURITY_KNOWLEDGE_CELL_STATUS")


@dataclass(frozen=True)
class ExpertReadinessEvidence:
    benchmark_version_ref: str | None
    benchmark_reproducible: bool
    benchmark_requires_evidence_refs: bool
    benchmark_has_unknown_refusal_cases: bool
    benchmark_has_conflict_cases: bool
    socrates_passed: bool
    argus_passed: bool
    unresolved_s4_on_integrity_path: bool


@dataclass(frozen=True)
class ExpertReadinessDecision:
    decision: str
    blocking_reasons: tuple[str, ...]


class SecurityKnowledgeReadinessGate:
    """Fail-closed expert-readiness gate for the declared Security Knowledge scope."""

    def evaluate(
        self,
        cells: Iterable[CoverageCell],
        evidence: ExpertReadinessEvidence,
    ) -> ExpertReadinessDecision:
        items = tuple(cells)
        if not items:
            return ExpertReadinessDecision("HOLD", ("NO_DECLARED_COVERAGE_CELLS",))

        blockers: list[str] = []
        seen_ids: set[str] = set()
        foundational_count = 0

        for cell in items:
            cell.validate()
            if cell.cell_id in seen_ids:
                blockers.append(f"DUPLICATE_CELL_ID:{cell.cell_id}")
                continue
            seen_ids.add(cell.cell_id)

            if cell.criticality == "FOUNDATIONAL":
                foundational_count += 1
                if cell.status == "STALE_OR_REASSESSMENT_REQUIRED":
                    blockers.append(f"FOUNDATIONAL_CELL_STALE:{cell.cell_id}")
                    continue
                if CELL_ORDER[cell.status] < CELL_ORDER["INDEPENDENTLY_REVIEWED"]:
                    blockers.append(f"FOUNDATIONAL_CELL_NOT_REVIEWED:{cell.cell_id}")
                if not cell.provenance_complete:
                    blockers.append(f"PROVENANCE_INCOMPLETE:{cell.cell_id}")
                if not cell.quality_assessed:
                    blockers.append(f"QUALITY_NOT_ASSESSED:{cell.cell_id}")
                if not cell.temporal_scope_pinned:
                    blockers.append(f"TEMPORAL_SCOPE_NOT_PINNED:{cell.cell_id}")
                if not cell.conflicts_visible:
                    blockers.append(f"CONFLICT_VISIBILITY_MISSING:{cell.cell_id}")
                if not cell.freshness_current:
                    blockers.append(f"FRESHNESS_NOT_CURRENT:{cell.cell_id}")

        if foundational_count == 0:
            blockers.append("NO_FOUNDATIONAL_CELLS_DECLARED")

        if not evidence.benchmark_version_ref:
            blockers.append("BENCHMARK_VERSION_MISSING")
        if not evidence.benchmark_reproducible:
            blockers.append("BENCHMARK_NOT_REPRODUCIBLE")
        if not evidence.benchmark_requires_evidence_refs:
            blockers.append("BENCHMARK_DOES_NOT_REQUIRE_EVIDENCE")
        if not evidence.benchmark_has_unknown_refusal_cases:
            blockers.append("BENCHMARK_MISSING_UNKNOWN_REFUSAL_CASES")
        if not evidence.benchmark_has_conflict_cases:
            blockers.append("BENCHMARK_MISSING_CONFLICT_CASES")
        if not evidence.socrates_passed:
            blockers.append("SOCRATES_NOT_PASSED")
        if not evidence.argus_passed:
            blockers.append("ARGUS_NOT_PASSED")
        if evidence.unresolved_s4_on_integrity_path:
            blockers.append("UNRESOLVED_S4_ON_KNOWLEDGE_INTEGRITY_PATH")

        if blockers:
            return ExpertReadinessDecision("HOLD", tuple(blockers))
        return ExpertReadinessDecision("PASS", ())
