from __future__ import annotations
import hashlib

from px00.factory_mvp import AgentRdFactoryMvp


PRODUCER = "ASSIGN-RD-PRODUCER-0001"
VERIFIER = "ASSIGN-RD-VERIFIER-0001"
SOCRATES = "ASSIGN-RD-SOCRATES-0001"


def derive_idempotency_key(run_id: str, operation: str, target: str) -> str:
    material = f"{run_id}|{operation}|{target}".encode("utf-8")
    return hashlib.sha256(material).hexdigest()


def run_synthetic_idempotency_case() -> tuple[AgentRdFactoryMvp, str]:
    """Execute one deterministic, bounded, no-side-effect functional MVP case."""
    mvp = AgentRdFactoryMvp()
    run_id = "MVP-FUNC-RUN-0001"
    mvp.create_run(
        run_id,
        "PROBLEM-IDEMPOTENCY-0001",
        PRODUCER,
        VERIFIER,
    )

    mvp.complete_stage(
        run_id,
        "FUNC-ART-001",
        {
            "problem": "A retried synthetic delivery may be submitted more than once.",
            "objective": "Design a deterministic deduplication identity for one logical delivery.",
            "constraints": ["no external action", "no secret input", "deterministic output"],
        },
        PRODUCER,
    )
    mvp.complete_stage(
        run_id,
        "FUNC-ART-002",
        {
            "evidence": [
                "Retries can repeat the same logical request.",
                "A deduplication key must remain stable for the same logical request.",
                "Different logical requests should not share the same intended identity.",
            ],
            "evidence_scope": "synthetic engineering facts for MVP only",
        },
        PRODUCER,
    )
    mvp.complete_stage(
        run_id,
        "FUNC-ART-003",
        {
            "claims": [
                {"claim": "random request IDs are unsuitable as deterministic retry identity", "status": "SUPPORTED_FOR_CASE"},
                {"claim": "canonical request material can be hashed into a stable identity", "status": "SUPPORTED_FOR_CASE"},
                {"claim": "an idempotency key alone does not create exactly-once execution", "status": "SUPPORTED_FOR_CASE"},
            ]
        },
        PRODUCER,
    )
    mvp.complete_stage(
        run_id,
        "FUNC-ART-004",
        {
            "alternatives": [
                {"id": "A", "design": "random UUID per attempt", "disposition": "REJECT"},
                {"id": "B", "design": "SHA-256(run_id|operation|target)", "disposition": "SELECT"},
            ],
            "selected": "B",
            "reason": "stable under retry and deterministic for the bounded synthetic case",
        },
        PRODUCER,
    )
    mvp.complete_stage(
        run_id,
        "FUNC-ART-005",
        {
            "verdict": "PASS",
            "scope": "pure local hashing only",
            "checks": [
                "no external tool or network call",
                "no credential or regulated data",
                "hash output is identity evidence, not authorization",
            ],
        },
        PRODUCER,
    )

    same_a = derive_idempotency_key(run_id, "DELIVER", "TARGET-A")
    same_b = derive_idempotency_key(run_id, "DELIVER", "TARGET-A")
    other_target = derive_idempotency_key(run_id, "DELIVER", "TARGET-B")
    other_operation = derive_idempotency_key(run_id, "ARCHIVE", "TARGET-A")

    mvp.complete_stage(
        run_id,
        "FUNC-ART-006",
        {
            "prototype": "derive_idempotency_key",
            "algorithm": "sha256(run_id|operation|target)",
            "sample_key": same_a,
            "bounded_execution": True,
        },
        PRODUCER,
    )
    mvp.complete_stage(
        run_id,
        "FUNC-ART-007",
        {
            "verdict": "PASS",
            "checks": {
                "same_request_same_key": same_a == same_b,
                "different_target_different_key": same_a != other_target,
                "different_operation_different_key": same_a != other_operation,
                "sha256_hex_length": len(same_a) == 64,
            },
        },
        VERIFIER,
    )
    mvp.complete_stage(
        run_id,
        "FUNC-ART-008",
        {
            "verdict": "PASS_WITH_FINDING",
            "finding_id": "SOC-MVP-001",
            "finding": "Deterministic identity prevents accidental key drift but does not itself guarantee exactly-once execution.",
            "required_future_control": "durable uniqueness plus atomic state transition before material side effects",
        },
        SOCRATES,
    )
    mvp.complete_stage(
        run_id,
        "FUNC-ART-009",
        {
            "admit": True,
            "lesson": "Idempotency identity and transactional exactly-once semantics are separate controls.",
            "knowledge_target": "KB-FACTORY-LESSONS",
            "scope": "candidate lesson pending normal governed knowledge admission outside this synthetic harness",
        },
        PRODUCER,
    )
    mvp.complete_stage(
        run_id,
        "FUNC-ART-010",
        {
            "delivery": "deterministic idempotency-key prototype and verification evidence",
            "selected_design": "SHA-256(run_id|operation|target)",
            "sample_key": same_a,
            "limitations": [
                "no durable deduplication store",
                "no transaction boundary",
                "no exactly-once claim",
                "no material external action",
            ],
            "next_if_needed": "pair key identity with durable uniqueness and atomic execution state",
        },
        PRODUCER,
    )

    if not mvp.runs[run_id].delivered:
        raise AssertionError("FUNCTIONAL_CASE_NOT_DELIVERED")
    return mvp, run_id
