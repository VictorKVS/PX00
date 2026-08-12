from __future__ import annotations
from dataclasses import dataclass, field, replace
import hashlib
import json


STAGES = (
    "QUALIFY_PROBLEM",
    "RESEARCH_EVIDENCE",
    "ASSESS_CLAIMS",
    "DESIGN_ALTERNATIVES",
    "SECURITY_PRECHECK",
    "IMPLEMENT_BOUNDED_PROTOTYPE",
    "VERIFY_AND_VALIDATE",
    "SOCRATES_CHALLENGE",
    "KNOWLEDGE_ADMISSION",
    "GOVERNED_DELIVERY",
)

STAGE_ARTIFACT_TYPES = {
    "QUALIFY_PROBLEM": "PROBLEM_BRIEF",
    "RESEARCH_EVIDENCE": "RESEARCH_EVIDENCE",
    "ASSESS_CLAIMS": "CLAIM_ASSESSMENT",
    "DESIGN_ALTERNATIVES": "DESIGN_OPTIONS",
    "SECURITY_PRECHECK": "SECURITY_PRECHECK_REPORT",
    "IMPLEMENT_BOUNDED_PROTOTYPE": "PROTOTYPE_ARTIFACT",
    "VERIFY_AND_VALIDATE": "VERIFICATION_REPORT",
    "SOCRATES_CHALLENGE": "SOCRATES_REVIEW",
    "KNOWLEDGE_ADMISSION": "KNOWLEDGE_ADMISSION_RECORD",
    "GOVERNED_DELIVERY": "DELIVERY_PACKAGE",
}

GATED_VERDICT_STAGES = {
    "SECURITY_PRECHECK",
    "VERIFY_AND_VALIDATE",
    "SOCRATES_CHALLENGE",
}


def _canonical_payload(payload: dict[str, object]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _declared_verdict_matches(stage: str, payload: dict[str, object], outcome: str) -> bool:
    if stage not in GATED_VERDICT_STAGES:
        return True
    verdict = payload.get("verdict")
    if not isinstance(verdict, str):
        raise ValueError("ARTIFACT_VERDICT_REQUIRED")
    if stage == "SOCRATES_CHALLENGE":
        pass_verdicts = {"PASS", "PASS_WITH_FINDING", "PASS_WITH_ACTIONS"}
        fail_verdicts = {"FAIL", "REWORK", "BLOCK"}
        return verdict in (pass_verdicts if outcome == "PASS" else fail_verdicts)
    return verdict == outcome


@dataclass(frozen=True)
class MvpArtifact:
    artifact_id: str
    run_id: str
    stage: str
    artifact_type: str
    producer_assignment_ref: str
    input_artifact_refs: tuple[str, ...]
    payload_json: str
    content_digest: str

    def verify_digest(self) -> bool:
        return hashlib.sha256(self.payload_json.encode("utf-8")).hexdigest() == self.content_digest


@dataclass(frozen=True)
class MvpRun:
    run_id: str
    problem_ref: str
    producer_assignment_ref: str
    verifier_assignment_ref: str
    stage_index: int = 0
    untrusted_input_present: bool = False
    trust_gate_passed: bool = False
    security_precheck_passed: bool = False
    verification_passed: bool = False
    socrates_passed: bool = False
    delivered: bool = False
    artifact_refs: tuple[str, ...] = ()
    consumed_artifact_refs: tuple[str, ...] = ()
    trace: tuple[str, ...] = ()

    @property
    def stage(self) -> str:
        return STAGES[self.stage_index]


@dataclass
class AgentRdFactoryMvp:
    runs: dict[str, MvpRun] = field(default_factory=dict)
    artifacts: dict[str, MvpArtifact] = field(default_factory=dict)

    def create_run(
        self,
        run_id: str,
        problem_ref: str,
        producer_assignment_ref: str,
        verifier_assignment_ref: str,
        *,
        untrusted_input_present: bool = False,
    ) -> MvpRun:
        if run_id in self.runs:
            raise ValueError("RUN_ID_REUSE")
        if producer_assignment_ref == verifier_assignment_ref:
            raise ValueError("INDEPENDENCE_VIOLATION")
        run = MvpRun(
            run_id=run_id,
            problem_ref=problem_ref,
            producer_assignment_ref=producer_assignment_ref,
            verifier_assignment_ref=verifier_assignment_ref,
            untrusted_input_present=untrusted_input_present,
            trace=("RUN_CREATED",),
        )
        self.runs[run_id] = run
        return run

    def pass_trust_gate(self, run_id: str) -> MvpRun:
        run = self._get(run_id)
        if run.delivered:
            raise ValueError("RUN_TERMINAL")
        run = replace(run, trust_gate_passed=True, trace=run.trace + ("TRUST_GATE_PASS",))
        self.runs[run_id] = run
        return run

    def submit_artifact(
        self,
        run_id: str,
        artifact_id: str,
        artifact_type: str,
        payload: dict[str, object],
        producer_assignment_ref: str,
        *,
        input_artifact_refs: tuple[str, ...] | None = None,
    ) -> MvpArtifact:
        run = self._get(run_id)
        if run.delivered:
            raise ValueError("RUN_TERMINAL")
        if artifact_id in self.artifacts:
            raise ValueError("ARTIFACT_ID_REUSE")

        expected_type = STAGE_ARTIFACT_TYPES[run.stage]
        if artifact_type != expected_type:
            raise ValueError(f"ARTIFACT_TYPE_MISMATCH:{expected_type}")

        if run.stage == "VERIFY_AND_VALIDATE" and producer_assignment_ref != run.verifier_assignment_ref:
            raise ValueError("VERIFIER_ASSIGNMENT_REQUIRED")
        if run.stage == "SOCRATES_CHALLENGE" and producer_assignment_ref in {
            run.producer_assignment_ref,
            run.verifier_assignment_ref,
        }:
            raise ValueError("SOCRATES_INDEPENDENCE_VIOLATION")

        expected_inputs: tuple[str, ...] = ()
        if run.artifact_refs:
            expected_inputs = (run.artifact_refs[-1],)
        actual_inputs = expected_inputs if input_artifact_refs is None else tuple(input_artifact_refs)
        if actual_inputs != expected_inputs:
            raise ValueError("ARTIFACT_LINEAGE_MISMATCH")

        payload_json = _canonical_payload(payload)
        digest = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
        artifact = MvpArtifact(
            artifact_id=artifact_id,
            run_id=run_id,
            stage=run.stage,
            artifact_type=artifact_type,
            producer_assignment_ref=producer_assignment_ref,
            input_artifact_refs=actual_inputs,
            payload_json=payload_json,
            content_digest=digest,
        )
        self.artifacts[artifact_id] = artifact
        run = replace(
            run,
            artifact_refs=run.artifact_refs + (artifact_id,),
            trace=run.trace + (f"ARTIFACT:{artifact_id}:{digest}",),
        )
        self.runs[run_id] = run
        return artifact

    def advance(self, run_id: str, stage: str, *, outcome: str = "PASS") -> MvpRun:
        run = self._get(run_id)
        if run.delivered:
            raise ValueError("RUN_TERMINAL")
        expected = run.stage
        if stage != expected:
            raise ValueError(f"STAGE_ORDER_VIOLATION:{expected}")
        if outcome not in {"PASS", "FAIL"}:
            raise ValueError("INVALID_OUTCOME")
        if not run.artifact_refs:
            raise ValueError("ARTIFACT_REQUIRED")

        artifact_ref = run.artifact_refs[-1]
        artifact = self.artifacts[artifact_ref]
        if artifact.stage != stage or artifact_ref in run.consumed_artifact_refs:
            raise ValueError("FRESH_STAGE_ARTIFACT_REQUIRED")
        if not artifact.verify_digest():
            raise ValueError("ARTIFACT_DIGEST_MISMATCH")
        payload = json.loads(artifact.payload_json)
        if not _declared_verdict_matches(stage, payload, outcome):
            raise ValueError("ARTIFACT_OUTCOME_MISMATCH")

        if stage == "IMPLEMENT_BOUNDED_PROTOTYPE":
            if run.untrusted_input_present and not run.trust_gate_passed:
                raise ValueError("UNTRUSTED_INPUT_BLOCKED")
            if not run.security_precheck_passed:
                raise ValueError("SECURITY_PRECHECK_REQUIRED")

        if stage == "VERIFY_AND_VALIDATE" and artifact.producer_assignment_ref != run.verifier_assignment_ref:
            raise ValueError("INDEPENDENCE_VIOLATION")

        if stage == "GOVERNED_DELIVERY":
            if not run.verification_passed:
                raise ValueError("VERIFICATION_REQUIRED")
            if not run.socrates_passed:
                raise ValueError("SOCRATES_REQUIRED")

        updates: dict[str, object] = {
            "trace": run.trace + (f"{stage}:{outcome}",),
            "consumed_artifact_refs": run.consumed_artifact_refs + (artifact_ref,),
        }
        if stage == "SECURITY_PRECHECK":
            updates["security_precheck_passed"] = outcome == "PASS"
        elif stage == "VERIFY_AND_VALIDATE":
            updates["verification_passed"] = outcome == "PASS"
        elif stage == "SOCRATES_CHALLENGE":
            updates["socrates_passed"] = outcome == "PASS"
        elif stage == "GOVERNED_DELIVERY":
            updates["delivered"] = outcome == "PASS"

        if outcome == "FAIL":
            run = replace(run, **updates)
            self.runs[run_id] = run
            return run

        next_index = min(run.stage_index + 1, len(STAGES) - 1)
        if stage == STAGES[-1]:
            next_index = run.stage_index
        updates["stage_index"] = next_index
        run = replace(run, **updates)
        self.runs[run_id] = run
        return run

    def complete_stage(
        self,
        run_id: str,
        artifact_id: str,
        payload: dict[str, object],
        producer_assignment_ref: str,
        *,
        outcome: str = "PASS",
    ) -> MvpRun:
        run = self._get(run_id)
        self.submit_artifact(
            run_id,
            artifact_id,
            STAGE_ARTIFACT_TYPES[run.stage],
            payload,
            producer_assignment_ref,
        )
        return self.advance(run_id, run.stage, outcome=outcome)

    def artifact_payload(self, artifact_id: str) -> dict[str, object]:
        try:
            artifact = self.artifacts[artifact_id]
        except KeyError as exc:
            raise ValueError("UNKNOWN_ARTIFACT") from exc
        if not artifact.verify_digest():
            raise ValueError("ARTIFACT_DIGEST_MISMATCH")
        return json.loads(artifact.payload_json)

    def _get(self, run_id: str) -> MvpRun:
        try:
            return self.runs[run_id]
        except KeyError as exc:
            raise ValueError("UNKNOWN_RUN") from exc
