from __future__ import annotations
from dataclasses import dataclass

from px00.factory_mvp import AgentRdFactoryMvp
from px00.factory_mvp_case import PRODUCER, SOCRATES, VERIFIER, run_synthetic_idempotency_case


@dataclass(frozen=True)
class FailurePatternObservation:
    pattern_id: str
    pattern_type: str
    run_id: str
    stage: str
    evidence_ref: str
    summary: str


@dataclass(frozen=True)
class ScenarioOutcome:
    scenario_id: str
    run_id: str
    status: str
    rework_count: int
    artifact_count: int


def normalize_tags_v0(tags: list[str]) -> tuple[str, ...]:
    """Intentionally incomplete prototype: normalizes text but preserves duplicates/order."""
    return tuple(tag.strip().lower() for tag in tags if tag.strip())


def normalize_tags_v1(tags: list[str]) -> tuple[str, ...]:
    """Corrected deterministic canonical tag set."""
    return tuple(sorted({tag.strip().lower() for tag in tags if tag.strip()}))


def run_verification_rework_case() -> tuple[AgentRdFactoryMvp, str, FailurePatternObservation]:
    mvp = AgentRdFactoryMvp()
    run_id = "MVP-FUNC-RUN-0002"
    mvp.create_run(run_id, "PROBLEM-CANONICAL-TAGS-0001", PRODUCER, VERIFIER)

    mvp.complete_stage(run_id, "RW-ART-001", {
        "problem": "Equivalent capability tags arrive with case, whitespace and duplicate variation.",
        "objective": "Produce one deterministic canonical tag set.",
        "constraints": ["pure local transformation", "stable output", "no external action"],
    }, PRODUCER)
    mvp.complete_stage(run_id, "RW-ART-002", {
        "evidence": ["case and whitespace variation can create false distinct values", "duplicates inflate downstream counts"],
        "scope": "synthetic deterministic input",
    }, PRODUCER)
    mvp.complete_stage(run_id, "RW-ART-003", {
        "claims": [
            {"claim": "trim and lowercase are necessary", "status": "SUPPORTED_FOR_CASE"},
            {"claim": "deduplication and stable ordering are also required", "status": "SUPPORTED_FOR_CASE"},
        ]
    }, PRODUCER)
    mvp.complete_stage(run_id, "RW-ART-004", {
        "alternatives": [
            {"id": "A", "design": "trim+lower only", "disposition": "PROTOTYPE_FIRST"},
            {"id": "B", "design": "trim+lower+dedupe+sort", "disposition": "TARGET"},
        ]
    }, PRODUCER)
    mvp.complete_stage(run_id, "RW-ART-005", {
        "verdict": "PASS",
        "scope": "pure local string normalization",
        "checks": ["no secrets", "no network", "no external side effect"],
    }, PRODUCER)

    sample = [" Security ", "AI", "security", " ai "]
    first = normalize_tags_v0(sample)
    mvp.complete_stage(run_id, "RW-ART-006", {
        "prototype": "normalize_tags_v0",
        "sample_input": sample,
        "sample_output": list(first),
    }, PRODUCER)

    mvp.complete_stage(run_id, "RW-ART-007", {
        "verdict": "FAIL",
        "checks": {
            "trimmed": all(value == value.strip() for value in first),
            "lowercase": all(value == value.lower() for value in first),
            "duplicates_removed": len(first) == len(set(first)),
            "stable_sorted_order": tuple(sorted(first)) == first,
        },
        "finding": "Prototype normalizes text but still emits duplicates and input-dependent ordering.",
    }, VERIFIER, outcome="FAIL")

    pattern = FailurePatternObservation(
        pattern_id="FFB-FP-0001",
        pattern_type="VERIFICATION_REWORK_REQUIRED",
        run_id=run_id,
        stage="VERIFY_AND_VALIDATE",
        evidence_ref="RW-ART-007",
        summary="Independent verification found a functional defect that requires returning to implementation.",
    )

    mvp.request_rework(run_id, "IMPLEMENT_BOUNDED_PROTOTYPE", pattern.pattern_id)
    corrected = normalize_tags_v1(sample)
    mvp.complete_stage(run_id, "RW-ART-008", {
        "prototype": "normalize_tags_v1",
        "sample_input": sample,
        "sample_output": list(corrected),
        "rework_from": "RW-ART-007",
    }, PRODUCER)
    mvp.complete_stage(run_id, "RW-ART-009", {
        "verdict": "PASS",
        "checks": {
            "duplicates_removed": len(corrected) == len(set(corrected)),
            "stable_sorted_order": tuple(sorted(corrected)) == corrected,
            "expected_output": corrected == ("ai", "security"),
        },
    }, VERIFIER)
    mvp.complete_stage(run_id, "RW-ART-010", {
        "verdict": "PASS_WITH_FINDING",
        "finding": "Canonicalization rules are domain policy and must be versioned if semantics later change.",
    }, SOCRATES)
    mvp.complete_stage(run_id, "RW-ART-011", {
        "admit": True,
        "lesson": "Failed independent verification must be able to cause explicit implementation rework without deleting failed evidence.",
        "knowledge_target": "KB-FACTORY-LESSONS",
    }, PRODUCER)
    mvp.complete_stage(run_id, "RW-ART-012", {
        "delivery": "canonical tag normalizer with preserved failed-attempt lineage",
        "result": list(corrected),
        "rework_count": 1,
    }, PRODUCER)

    return mvp, run_id, pattern


def run_security_block_case() -> tuple[AgentRdFactoryMvp, str, FailurePatternObservation]:
    mvp = AgentRdFactoryMvp()
    run_id = "MVP-FUNC-RUN-0003"
    mvp.create_run(run_id, "PROBLEM-UNBOUNDED-SHELL-0001", PRODUCER, VERIFIER)

    mvp.complete_stage(run_id, "BLK-ART-001", {
        "problem": "A requested prototype would execute arbitrary shell material supplied by the task.",
        "objective": "Determine whether this behavior belongs inside the bounded M1 factory MVP.",
        "constraints": ["M1 permits no material external action"],
    }, PRODUCER)
    mvp.complete_stage(run_id, "BLK-ART-002", {
        "evidence": ["arbitrary shell execution can create material external effects", "current MVP has no grant for such effects"]
    }, PRODUCER)
    mvp.complete_stage(run_id, "BLK-ART-003", {
        "claims": [{"claim": "the requested behavior exceeds the current bounded execution scope", "status": "SUPPORTED_FOR_CASE"}]
    }, PRODUCER)
    mvp.complete_stage(run_id, "BLK-ART-004", {
        "alternatives": [
            {"id": "A", "design": "execute shell directly", "disposition": "REJECT"},
            {"id": "B", "design": "stop at security gate and require a future governed tool boundary", "disposition": "SELECT"},
        ]
    }, PRODUCER)
    mvp.complete_stage(run_id, "BLK-ART-005", {
        "verdict": "FAIL",
        "reason": "material external action is outside the accepted M1 bounded scope",
        "required_future_control": "ActionRequest + AuthorityDecision + CapabilityGrant + Tool Boundary",
    }, PRODUCER, outcome="FAIL")

    pattern = FailurePatternObservation(
        pattern_id="FFB-FP-0002",
        pattern_type="SECURITY_SCOPE_BLOCK",
        run_id=run_id,
        stage="SECURITY_PRECHECK",
        evidence_ref="BLK-ART-005",
        summary="Security gate correctly stopped a request that exceeded the bounded MVP authority envelope.",
    )
    return mvp, run_id, pattern


def run_functional_scenario_suite() -> tuple[tuple[ScenarioOutcome, ...], tuple[FailurePatternObservation, ...]]:
    idempotency_mvp, idempotency_run_id = run_synthetic_idempotency_case()
    rework_mvp, rework_run_id, rework_pattern = run_verification_rework_case()
    blocked_mvp, blocked_run_id, blocked_pattern = run_security_block_case()

    outcomes = (
        ScenarioOutcome(
            "SCENARIO-IDEMPOTENCY",
            idempotency_run_id,
            "DELIVERED",
            idempotency_mvp.runs[idempotency_run_id].rework_count,
            len(idempotency_mvp.runs[idempotency_run_id].artifact_refs),
        ),
        ScenarioOutcome(
            "SCENARIO-VERIFICATION-REWORK",
            rework_run_id,
            "DELIVERED_AFTER_REWORK",
            rework_mvp.runs[rework_run_id].rework_count,
            len(rework_mvp.runs[rework_run_id].artifact_refs),
        ),
        ScenarioOutcome(
            "SCENARIO-SECURITY-BLOCK",
            blocked_run_id,
            "BLOCKED_BY_SECURITY",
            blocked_mvp.runs[blocked_run_id].rework_count,
            len(blocked_mvp.runs[blocked_run_id].artifact_refs),
        ),
    )
    return outcomes, (rework_pattern, blocked_pattern)
