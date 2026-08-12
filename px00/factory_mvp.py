from __future__ import annotations
from dataclasses import dataclass, field, replace


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
    trace: tuple[str, ...] = ()

    @property
    def stage(self) -> str:
        return STAGES[self.stage_index]


@dataclass
class AgentRdFactoryMvp:
    runs: dict[str, MvpRun] = field(default_factory=dict)

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

    def advance(self, run_id: str, stage: str, *, outcome: str = "PASS") -> MvpRun:
        run = self._get(run_id)
        if run.delivered:
            raise ValueError("RUN_TERMINAL")
        expected = run.stage
        if stage != expected:
            raise ValueError(f"STAGE_ORDER_VIOLATION:{expected}")
        if outcome not in {"PASS", "FAIL"}:
            raise ValueError("INVALID_OUTCOME")

        if stage == "IMPLEMENT_BOUNDED_PROTOTYPE":
            if run.untrusted_input_present and not run.trust_gate_passed:
                raise ValueError("UNTRUSTED_INPUT_BLOCKED")
            if not run.security_precheck_passed:
                raise ValueError("SECURITY_PRECHECK_REQUIRED")

        if stage == "VERIFY_AND_VALIDATE" and run.producer_assignment_ref == run.verifier_assignment_ref:
            raise ValueError("INDEPENDENCE_VIOLATION")

        if stage == "GOVERNED_DELIVERY":
            if not run.verification_passed:
                raise ValueError("VERIFICATION_REQUIRED")
            if not run.socrates_passed:
                raise ValueError("SOCRATES_REQUIRED")

        updates: dict[str, object] = {"trace": run.trace + (f"{stage}:{outcome}",)}
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

    def _get(self, run_id: str) -> MvpRun:
        try:
            return self.runs[run_id]
        except KeyError as exc:
            raise ValueError("UNKNOWN_RUN") from exc
