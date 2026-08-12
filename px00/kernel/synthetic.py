from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Iterable
from uuid import uuid4

from px00.policy import PolicyEngine, PolicyProfile, synthetic_policy_profiles
from px00.profile_registry import PolicyProfileRegistry, PolicySnapshot
from px00.tools.deterministic import BoundaryViolation, DeterministicMathTool


@dataclass(frozen=True)
class ActionRequest:
    action_request_id: str
    task_id: str
    run_id: str
    trace_id: str
    requester_role_id: str
    protocol_id: str
    protocol_version: str
    step_id: str
    capability: str
    action_class: str
    target_ref: str
    purpose_code: str
    requested_autonomy: str
    classification: str
    side_effect_class: str
    payload: dict[str, Any]
    requested_adapter_hint: str | None = None


@dataclass(frozen=True)
class AuthorityDecision:
    decision_id: str
    action_request_id: str
    run_id: str
    result: str
    effective_autonomy: str
    reason_code: str
    policy_snapshot_ref: str
    policy_snapshot_hash: str
    policy_hash_algorithm: str = "sha256"
    policy_refs: tuple[str, ...] = ()
    constraining_profile: str | None = None


@dataclass(frozen=True)
class CapabilityGrant:
    grant_id: str
    action_request_id: str
    authority_decision_id: str
    capability: str
    target_scope: str
    side_effect_ceiling: str
    data_classification_ceiling: str
    operation_count_limit: int
    one_time: bool = True
    status: str = "ACTIVE"


@dataclass(frozen=True)
class MaterialEvent:
    event_id: str
    trace_id: str
    action_request_id: str
    event_type: str
    status: str
    detail: str


@dataclass(frozen=True)
class GovernedResult:
    run_state: str
    action_request: ActionRequest
    policy_snapshot: PolicySnapshot
    authority_decision: AuthorityDecision
    capability_grant: CapabilityGrant | None
    output: Any | None
    events: tuple[MaterialEvent, ...]
    blocking_reason: str | None = None


class SyntheticGovernedKernel:
    """First executable PX00 governed action proof with pinned policy lineage."""

    CAPABILITY = "math.multiply"
    TARGET = "synthetic://math.multiply"
    ROLE_ID = "ROLE-TEST-0001"
    PROTOCOL_ID = "PROTO-TEST-0001"
    PROTOCOL_VERSION = "0.1.0"
    STEP_ID = "S02"

    def __init__(self, profiles: Iterable[PolicyProfile] | None = None) -> None:
        self._tool = DeterministicMathTool()
        self._policy = PolicyEngine()
        self._profiles = tuple(profiles) if profiles is not None else synthetic_policy_profiles()
        self._registry = PolicyProfileRegistry(self._profiles)
        self._requested_profiles = {
            profile.profile_type: (profile.profile_id, profile.version) for profile in self._profiles
        }

    def prepare_request(
        self,
        left: int | float,
        right: int | float,
        *,
        requested_adapter_hint: str | None = None,
    ) -> ActionRequest:
        trace_suffix = uuid4().hex
        return ActionRequest(
            action_request_id=f"ACTREQ-{trace_suffix[:12]}",
            task_id=f"TASK-{trace_suffix[12:20]}",
            run_id=f"RUN-{trace_suffix[20:28]}",
            trace_id=f"TRACE-{trace_suffix[4:16]}",
            requester_role_id=self.ROLE_ID,
            protocol_id=self.PROTOCOL_ID,
            protocol_version=self.PROTOCOL_VERSION,
            step_id=self.STEP_ID,
            capability=self.CAPABILITY,
            action_class="transform",
            target_ref=self.TARGET,
            purpose_code="synthetic_acceptance_proof",
            requested_autonomy="A1",
            classification="PUBLIC",
            side_effect_class="S0",
            payload={"left": left, "right": right},
            requested_adapter_hint=requested_adapter_hint,
        )

    def create_policy_snapshot(self, request: ActionRequest) -> PolicySnapshot:
        return self._registry.snapshot(run_id=request.run_id, requested=self._requested_profiles)

    def evaluate_authority(
        self,
        request: ActionRequest,
        *,
        allow: bool,
        policy_snapshot: PolicySnapshot | None = None,
    ) -> AuthorityDecision:
        snapshot = policy_snapshot or self.create_policy_snapshot(request)
        if snapshot.run_id != request.run_id:
            return self._lineage_denial(request, snapshot, "POLICY_SNAPSHOT_RUN_MISMATCH")

        if not allow:
            return AuthorityDecision(
                decision_id=f"AUTH-{uuid4().hex[:12]}",
                action_request_id=request.action_request_id,
                run_id=request.run_id,
                result="DENY",
                effective_autonomy="A0",
                reason_code="AUTHORITY_ABSENT",
                policy_snapshot_ref=snapshot.snapshot_id,
                policy_snapshot_hash=snapshot.snapshot_hash,
                policy_refs=snapshot.profile_refs,
            )

        policy = self._policy.evaluate(
            snapshot.profiles,
            capability=request.capability,
            requested_autonomy=request.requested_autonomy,
            side_effect_class=request.side_effect_class,
            classification=request.classification,
            target_ref=request.target_ref,
        )
        return AuthorityDecision(
            decision_id=f"AUTH-{uuid4().hex[:12]}",
            action_request_id=request.action_request_id,
            run_id=request.run_id,
            result=policy.result,
            effective_autonomy=policy.effective_autonomy,
            reason_code=policy.reason_code,
            policy_snapshot_ref=snapshot.snapshot_id,
            policy_snapshot_hash=snapshot.snapshot_hash,
            policy_refs=policy.profile_refs,
            constraining_profile=policy.constraining_profile,
        )

    def issue_grant(
        self,
        request: ActionRequest,
        authority: AuthorityDecision,
        policy_snapshot: PolicySnapshot | None = None,
    ) -> CapabilityGrant | None:
        snapshot = policy_snapshot or self.create_policy_snapshot(request)
        if authority.result != "ALLOW":
            return None
        if authority.action_request_id != request.action_request_id or authority.run_id != request.run_id:
            return None
        if authority.policy_snapshot_ref != snapshot.snapshot_id:
            return None
        if authority.policy_snapshot_hash != snapshot.snapshot_hash:
            return None
        return CapabilityGrant(
            grant_id=f"GRANT-{uuid4().hex[:12]}",
            action_request_id=request.action_request_id,
            authority_decision_id=authority.decision_id,
            capability=request.capability,
            target_scope=request.target_ref,
            side_effect_ceiling=request.side_effect_class,
            data_classification_ceiling=request.classification,
            operation_count_limit=1,
            one_time=True,
        )

    def execute_request(
        self,
        request: ActionRequest,
        *,
        allow: bool,
        policy_snapshot: PolicySnapshot | None = None,
    ) -> GovernedResult:
        snapshot = policy_snapshot or self.create_policy_snapshot(request)
        authority = self.evaluate_authority(request, allow=allow, policy_snapshot=snapshot)
        events: list[MaterialEvent] = [
            self._event(request, "AUTHORITY_DECISION", authority.result, authority.reason_code)
        ]
        if authority.result != "ALLOW":
            run_state = "ESCALATED" if authority.result == "ESCALATE" else "DENIED"
            return GovernedResult(
                run_state=run_state,
                action_request=request,
                policy_snapshot=snapshot,
                authority_decision=authority,
                capability_grant=None,
                output=None,
                events=tuple(events),
                blocking_reason=authority.reason_code,
            )

        grant = self.issue_grant(request, authority, snapshot)
        if grant is None:
            events.append(self._event(request, "GRANT", "BLOCKED", "POLICY_LINEAGE_MISMATCH"))
            return GovernedResult(
                run_state="BLOCKED",
                action_request=request,
                policy_snapshot=snapshot,
                authority_decision=authority,
                capability_grant=None,
                output=None,
                events=tuple(events),
                blocking_reason="POLICY_LINEAGE_MISMATCH",
            )

        try:
            output = self._tool.execute(request, grant)
        except BoundaryViolation as exc:
            events.append(self._event(request, "TOOL_BOUNDARY", "BLOCKED", exc.code))
            return GovernedResult(
                run_state="BLOCKED",
                action_request=request,
                policy_snapshot=snapshot,
                authority_decision=authority,
                capability_grant=grant,
                output=None,
                events=tuple(events),
                blocking_reason=exc.code,
            )

        consumed_grant = replace(grant, status="CONSUMED")
        events.append(self._event(request, "TOOL_BOUNDARY", "SUCCEEDED", "SYNTHETIC_EXECUTION_OK"))
        return GovernedResult(
            run_state="COMPLETED",
            action_request=request,
            policy_snapshot=snapshot,
            authority_decision=authority,
            capability_grant=consumed_grant,
            output=output,
            events=tuple(events),
        )

    def _lineage_denial(
        self,
        request: ActionRequest,
        snapshot: PolicySnapshot,
        reason: str,
    ) -> AuthorityDecision:
        return AuthorityDecision(
            decision_id=f"AUTH-{uuid4().hex[:12]}",
            action_request_id=request.action_request_id,
            run_id=request.run_id,
            result="DENY",
            effective_autonomy="A0",
            reason_code=reason,
            policy_snapshot_ref=snapshot.snapshot_id,
            policy_snapshot_hash=snapshot.snapshot_hash,
            policy_refs=snapshot.profile_refs,
        )

    @staticmethod
    def _event(request: ActionRequest, event_type: str, status: str, detail: str) -> MaterialEvent:
        return MaterialEvent(
            event_id=f"EVT-{uuid4().hex[:12]}",
            trace_id=request.trace_id,
            action_request_id=request.action_request_id,
            event_type=event_type,
            status=status,
            detail=detail,
        )
