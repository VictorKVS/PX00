from __future__ import annotations
from dataclasses import dataclass, field
import hashlib
import json
from typing import Protocol

from px00.factory_mvp import AgentRdFactoryMvp, STAGE_ARTIFACT_TYPES


FORBIDDEN_OUTPUT_KEYS = {
    "acceptance_record",
    "authority_decision",
    "capability_grant",
    "tool_call",
    "tool_result",
}


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ExecutorDefinition:
    executor_id: str
    executor_type: str
    version_ref: str
    provider_ref: str
    allowed_stage_refs: tuple[str, ...]
    external_effects_allowed: bool = False
    status: str = "ACTIVE"
    model_ref: str | None = None


@dataclass(frozen=True)
class ExecutorInvocation:
    invocation_id: str
    run_ref: str
    stage_ref: str
    assignment_ref: str
    executor_ref: str
    executor_version_ref: str
    provider_ref: str
    model_ref: str | None
    input_artifact_ref: str
    bounded_input_hash: str
    output_candidate_hash: str
    output_artifact_ref: str
    status: str
    created_at: str


class ExecutorAdapter(Protocol):
    def execute(self, bounded_input: dict[str, object]) -> dict[str, object]: ...


@dataclass
class ScriptedExecutorAdapter:
    """Local replaceable worker used to prove the boundary without external provider access."""

    outputs: list[dict[str, object]]
    call_count: int = 0

    def execute(self, bounded_input: dict[str, object]) -> dict[str, object]:
        if self.call_count >= len(self.outputs):
            raise ValueError("EXECUTOR_SCRIPT_EXHAUSTED")
        output = self.outputs[self.call_count]
        self.call_count += 1
        return dict(output)


@dataclass
class GovernedExecutorBoundary:
    definitions: dict[str, ExecutorDefinition] = field(default_factory=dict)
    invocations: dict[str, ExecutorInvocation] = field(default_factory=dict)

    def register(self, definition: ExecutorDefinition) -> None:
        if definition.executor_id in self.definitions:
            raise ValueError("EXECUTOR_ID_REUSE")
        if definition.status not in {"ACTIVE", "SUSPENDED", "RETIRED"}:
            raise ValueError("INVALID_EXECUTOR_STATUS")
        self.definitions[definition.executor_id] = definition

    def invoke_to_artifact(
        self,
        mvp: AgentRdFactoryMvp,
        *,
        run_id: str,
        invocation_id: str,
        executor_id: str,
        assignment_ref: str,
        bounded_input: dict[str, object],
        artifact_id: str,
        adapter: ExecutorAdapter,
        created_at: str,
    ) -> ExecutorInvocation:
        if invocation_id in self.invocations:
            raise ValueError("INVOCATION_ID_REUSE")
        try:
            definition = self.definitions[executor_id]
        except KeyError as exc:
            raise ValueError("UNKNOWN_EXECUTOR") from exc
        if definition.status != "ACTIVE":
            raise ValueError("EXECUTOR_NOT_ACTIVE")
        if definition.external_effects_allowed:
            raise ValueError("EXTERNAL_EFFECTS_FORBIDDEN_IN_M1")

        run = mvp._get(run_id)
        stage = run.stage
        if stage not in definition.allowed_stage_refs:
            raise ValueError("EXECUTOR_STAGE_NOT_ALLOWED")
        if stage != "IMPLEMENT_BOUNDED_PROTOTYPE":
            raise ValueError("M1_EXECUTOR_STAGE_NOT_SUPPORTED")
        if assignment_ref != run.producer_assignment_ref:
            raise ValueError("EXECUTOR_ASSIGNMENT_MISMATCH")
        if not run.artifact_refs:
            raise ValueError("EXECUTOR_INPUT_ARTIFACT_REQUIRED")

        input_artifact_ref = run.artifact_refs[-1]
        input_artifact = mvp.artifacts[input_artifact_ref]
        if not input_artifact.verify_digest():
            raise ValueError("EXECUTOR_INPUT_DIGEST_MISMATCH")

        candidate = adapter.execute(dict(bounded_input))
        if not isinstance(candidate, dict):
            raise ValueError("EXECUTOR_OUTPUT_MUST_BE_OBJECT")
        forbidden = FORBIDDEN_OUTPUT_KEYS.intersection(candidate)
        if forbidden:
            raise ValueError("EXECUTOR_OUTPUT_AUTHORITY_INJECTION")

        bounded_input_hash = _sha256(bounded_input)
        output_candidate_hash = _sha256(candidate)
        candidate_with_provenance = dict(candidate)
        candidate_with_provenance["executor_provenance"] = {
            "invocation_ref": invocation_id,
            "executor_ref": definition.executor_id,
            "executor_version_ref": definition.version_ref,
            "provider_ref": definition.provider_ref,
            "model_ref": definition.model_ref,
            "assignment_ref": assignment_ref,
            "bounded_input_hash": bounded_input_hash,
            "output_candidate_hash": output_candidate_hash,
        }

        mvp.submit_artifact(
            run_id,
            artifact_id,
            STAGE_ARTIFACT_TYPES[stage],
            candidate_with_provenance,
            assignment_ref,
        )

        record = ExecutorInvocation(
            invocation_id=invocation_id,
            run_ref=run_id,
            stage_ref=stage,
            assignment_ref=assignment_ref,
            executor_ref=definition.executor_id,
            executor_version_ref=definition.version_ref,
            provider_ref=definition.provider_ref,
            model_ref=definition.model_ref,
            input_artifact_ref=input_artifact_ref,
            bounded_input_hash=bounded_input_hash,
            output_candidate_hash=output_candidate_hash,
            output_artifact_ref=artifact_id,
            status="COMPLETED",
            created_at=created_at,
        )
        self.invocations[invocation_id] = record
        return record
