from __future__ import annotations

from px00.executors import ExecutorDefinition, GovernedExecutorBoundary, ScriptedExecutorAdapter
from px00.factory_mvp import AgentRdFactoryMvp
from px00.factory_mvp_case import PRODUCER, SOCRATES, VERIFIER


def _advance_to_implementation(mvp: AgentRdFactoryMvp, run_id: str) -> None:
    mvp.complete_stage(run_id, "EX-ART-001", {
        "problem": "A replaceable worker must canonicalize capability tags without receiving runtime authority.",
        "objective": "Prove a governed executor can produce candidate content and be replaced after verifier-detected failure.",
        "constraints": ["no external effects", "candidate output is not truth", "independent verification required"],
    }, PRODUCER)
    mvp.complete_stage(run_id, "EX-ART-002", {
        "evidence": ["worker implementations can be wrong", "historical worker identity must remain pinned after replacement"]
    }, PRODUCER)
    mvp.complete_stage(run_id, "EX-ART-003", {
        "claims": [
            {"claim": "executor output requires downstream verification", "status": "SUPPORTED_FOR_CASE"},
            {"claim": "replacement must not rewrite the earlier invocation", "status": "SUPPORTED_FOR_CASE"},
        ]
    }, PRODUCER)
    mvp.complete_stage(run_id, "EX-ART-004", {
        "alternatives": [
            {"id": "A", "design": "executor writes accepted result directly", "disposition": "REJECT"},
            {"id": "B", "design": "executor returns candidate artifact then independent verifier gates it", "disposition": "SELECT"},
        ]
    }, PRODUCER)
    mvp.complete_stage(run_id, "EX-ART-005", {
        "verdict": "PASS",
        "scope": "local test-double executor only",
        "checks": ["external effects disabled", "no tool grants", "independent verifier remains separate"],
    }, PRODUCER)


def run_replaceable_executor_case() -> tuple[AgentRdFactoryMvp, GovernedExecutorBoundary, str]:
    mvp = AgentRdFactoryMvp()
    boundary = GovernedExecutorBoundary()
    run_id = "MVP-EXEC-RUN-0001"
    mvp.create_run(run_id, "PROBLEM-GOVERNED-EXECUTOR-0001", PRODUCER, VERIFIER)
    _advance_to_implementation(mvp, run_id)

    bad_definition = ExecutorDefinition(
        executor_id="EXEC-TAG-NORM-0001",
        executor_type="TEST_DOUBLE",
        version_ref="0.1",
        provider_ref="LOCAL_TEST",
        model_ref="scripted-bad-v1",
        allowed_stage_refs=("IMPLEMENT_BOUNDED_PROTOTYPE",),
    )
    good_definition = ExecutorDefinition(
        executor_id="EXEC-TAG-NORM-0002",
        executor_type="TEST_DOUBLE",
        version_ref="0.2",
        provider_ref="LOCAL_TEST",
        model_ref="scripted-good-v2",
        allowed_stage_refs=("IMPLEMENT_BOUNDED_PROTOTYPE",),
    )
    boundary.register(bad_definition)
    boundary.register(good_definition)

    bounded_input = {"tags": [" Security ", "AI", "security", " ai "]}
    bad_adapter = ScriptedExecutorAdapter(outputs=[{
        "prototype": "executor_tag_normalizer_v0_1",
        "normalized_tags": ["security", "ai", "security", "ai"],
        "candidate_only": True,
    }])
    boundary.invoke_to_artifact(
        mvp,
        run_id=run_id,
        invocation_id="EXEC-INV-0001",
        executor_id=bad_definition.executor_id,
        assignment_ref=PRODUCER,
        bounded_input=bounded_input,
        artifact_id="EX-ART-006",
        adapter=bad_adapter,
        created_at="2026-08-12T19:35:00Z",
    )
    mvp.advance(run_id, "IMPLEMENT_BOUNDED_PROTOTYPE")

    mvp.complete_stage(run_id, "EX-ART-007", {
        "verdict": "FAIL",
        "checks": {
            "duplicates_removed": False,
            "stable_sorted_order": False,
        },
        "finding": "executor v0.1 emitted duplicate, input-order-dependent candidate content",
    }, VERIFIER, outcome="FAIL")

    mvp.request_rework(run_id, "IMPLEMENT_BOUNDED_PROTOTYPE", "EXEC-FINDING-0001")
    good_adapter = ScriptedExecutorAdapter(outputs=[{
        "prototype": "executor_tag_normalizer_v0_2",
        "normalized_tags": ["ai", "security"],
        "candidate_only": True,
    }])
    boundary.invoke_to_artifact(
        mvp,
        run_id=run_id,
        invocation_id="EXEC-INV-0002",
        executor_id=good_definition.executor_id,
        assignment_ref=PRODUCER,
        bounded_input=bounded_input,
        artifact_id="EX-ART-008",
        adapter=good_adapter,
        created_at="2026-08-12T19:36:00Z",
    )
    mvp.advance(run_id, "IMPLEMENT_BOUNDED_PROTOTYPE")

    mvp.complete_stage(run_id, "EX-ART-009", {
        "verdict": "PASS",
        "checks": {
            "duplicates_removed": True,
            "stable_sorted_order": True,
            "expected_output": True,
        },
        "verified_candidate_ref": "EX-ART-008",
    }, VERIFIER)
    mvp.complete_stage(run_id, "EX-ART-010", {
        "verdict": "PASS_WITH_FINDING",
        "finding": "Executor replacement corrected candidate behavior; this proves boundary mechanics, not live-provider reliability.",
        "limitation": "both workers are local test doubles, not a live AI provider",
    }, SOCRATES)
    mvp.complete_stage(run_id, "EX-ART-011", {
        "admit": True,
        "lesson": "replaceable executor versions remain historical facts; verifier failure can trigger replacement without rewriting the original invocation",
        "knowledge_target": "KB-FACTORY-LESSONS",
    }, PRODUCER)
    mvp.complete_stage(run_id, "EX-ART-012", {
        "delivery": "governed replaceable executor boundary reference evidence",
        "accepted_candidate_ref": "EX-ART-008",
        "superseded_candidate_ref": "EX-ART-006",
        "executor_invocations": ["EXEC-INV-0001", "EXEC-INV-0002"],
        "live_provider_claim": False,
    }, PRODUCER)

    return mvp, boundary, run_id
