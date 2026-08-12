from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any
from uuid import uuid4

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
    result: str
    effective_autonomy: str
    reason_code: str


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
    authority_decision: AuthorityDecision
    capability_grant: CapabilityGrant | None
    output: Any | None
    events: tuple[MaterialEvent, ...]
    blocking_reason: str | None = None


class SyntheticGovernedKernel:
    """First executable PX00 governed action proof.

    It intentionally supports one synthetic S0 capability only: ``math.multiply``.
    No network, filesystem mutation, subprocess, model, connector, or external
    side effect is available from this kernel.
    """

    CAPABILITY = "math.multiply"
    TARGET = "synthetic://math.multiply"
    ROLE_ID = "ROLE-TEST-0001"
    PROTOCOL_ID = "PROTO-TEST-0001"
    PROTOCOL_VERSION = "0.1.0"
    STEP_ID = "S02"

    def __init__(self) -> None:
        self._tool = DeterministicMathTool()

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

    def evaluate_authority(self, request: ActionRequest, *, allow: bool) -> AuthorityDecision:
        if request.capability != self.CAPABILITY:
            return AuthorityDecision(
                decision_id=f"AUTH-{uuid4().hex[:12]}",
                action_request_id=request.action_request_id,
                result="DENY",
                effective_autonomy="A1",
                reason_code="CAPABILITY_NOT_ALLOWED",
            )
        if request.side_effect_class != "S0":
            return AuthorityDecision(
                decision_id=f"AUTH-{uuid4().hex[:12]}",
                action_request_id=request.action_request_id,
                result="DENY",
                effective_autonomy="A1",
                reason_code="SIDE_EFFECT_CLASS_NOT_ALLOWED",
            )
        return AuthorityDecision(
            decision_id=f"AUTH-{uuid4().hex[:12]}",
            action_request_id=request.action_request_id,
            result="ALLOW" if allow else "DENY",
            effective_autonomy="A1",
            reason_code="SYNTHETIC_SCOPE_ALLOWED" if allow else "AUTHORITY_ABSENT",
        )

    def issue_grant(
        self,
        request: ActionRequest,
        authority: AuthorityDecision,
    ) -> CapabilityGrant | None:
        if authority.result != "ALLOW":
            return None
        if authority.action_request_id != request.action_request_id:
            return None
        return CapabilityGrant(
            grant_id=f"GRANT-{uuid4().hex[:12]}",
            action_request_id=request.action_request_id,
            authority_decision_id=authority.decision_id,
            capability=request.capability,
            target_scope=request.target_ref,
            side_effect_ceiling="S0",
            data_classification_ceiling="PUBLIC",
            operation_count_limit=1,
            one_time=True,
        )

    def execute_request(
        self,
        request: ActionRequest,
        *,
        allow: bool,
    ) -> GovernedResult:
        authority = self.evaluate_authority(request, allow=allow)
        events: list[MaterialEvent] = [
            self._event(request, "AUTHORITY_DECISION", authority.result, authority.reason_code)
        ]
        if authority.result != "ALLOW":
            return GovernedResult(
                run_state="DENIED",
                action_request=request,
                authority_decision=authority,
                capability_grant=None,
                output=None,
                events=tuple(events),
                blocking_reason=authority.reason_code,
            )

        grant = self.issue_grant(request, authority)
        if grant is None:
            events.append(self._event(request, "GRANT", "BLOCKED", "GRANT_NOT_ISSUED"))
            return GovernedResult(
                run_state="BLOCKED",
                action_request=request,
                authority_decision=authority,
                capability_grant=None,
                output=None,
                events=tuple(events),
                blocking_reason="GRANT_NOT_ISSUED",
            )

        try:
            output = self._tool.execute(request, grant)
        except BoundaryViolation as exc:
            events.append(self._event(request, "TOOL_BOUNDARY", "BLOCKED", exc.code))
            return GovernedResult(
                run_state="BLOCKED",
                action_request=request,
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
            authority_decision=authority,
            capability_grant=consumed_grant,
            output=output,
            events=tuple(events),
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
