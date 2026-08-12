from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from px00.context_packages import ContextPackage
from px00.staffing import AgentAssignment, RoleResponsibility


@dataclass(frozen=True)
class TaskRoutingRequest:
    task_id: str
    run_id: str
    required_duty_code: str
    protocol_ref: str
    department_ref: str | None = None


@dataclass(frozen=True)
class TaskRoutingDecision:
    routing_decision_id: str
    task_ref: str
    run_ref: str
    responsibility_ref: str
    role_ref: str
    department_ref: str
    assignment_ref: str
    agent_ref: str
    executor_type: str
    model_ref: str
    protocol_ref: str
    context_package_ref: str
    context_package_hash: str
    reason_codes: tuple[str, ...]


@dataclass(frozen=True)
class RunStaffingPin:
    run_id: str
    task_id: str
    responsibility_ref: str
    role_id: str
    department_id: str
    assignment_ref: str
    agent_id: str
    executor_type: str
    model_ref: str
    context_package_ref: str
    context_package_hash: str


class TaskRouter:
    def route(
        self,
        request: TaskRoutingRequest,
        *,
        responsibilities: Iterable[RoleResponsibility],
        assignments: Iterable[AgentAssignment],
        context_packages: Iterable[ContextPackage],
        routing_decision_id: str,
    ) -> tuple[TaskRoutingDecision, RunStaffingPin]:
        eligible_responsibilities = [
            item for item in responsibilities
            if item.duty_code == request.required_duty_code
            and request.protocol_ref in item.allowed_protocol_refs
            and (request.department_ref is None or item.department_id == request.department_ref)
        ]
        if not eligible_responsibilities:
            raise ValueError("NO_ELIGIBLE_RESPONSIBILITY")

        eligible_responsibilities.sort(key=lambda item: (item.department_id, item.role_id, item.responsibility_id))

        assignment_by_role: dict[tuple[str, str], list[AgentAssignment]] = {}
        for item in assignments:
            if item.status != "ACTIVE":
                continue
            assignment_by_role.setdefault((item.role_id, item.department_id), []).append(item)
        for items in assignment_by_role.values():
            items.sort(key=lambda item: item.assignment_id)

        contexts = tuple(context_packages)
        for responsibility in eligible_responsibilities:
            candidates = assignment_by_role.get((responsibility.role_id, responsibility.department_id), [])
            for assignment in candidates:
                if not set(responsibility.knowledge_binding_refs).issubset(set(assignment.knowledge_binding_refs)):
                    continue
                matching_contexts = [
                    ctx for ctx in contexts
                    if ctx.run_ref == request.run_id
                    and ctx.role_ref == responsibility.role_id
                    and ctx.assignment_ref == assignment.assignment_id
                ]
                if not matching_contexts:
                    continue
                matching_contexts.sort(key=lambda item: item.context_package_id)
                context = matching_contexts[0]
                decision = TaskRoutingDecision(
                    routing_decision_id=routing_decision_id,
                    task_ref=request.task_id,
                    run_ref=request.run_id,
                    responsibility_ref=responsibility.responsibility_id,
                    role_ref=responsibility.role_id,
                    department_ref=responsibility.department_id,
                    assignment_ref=assignment.assignment_id,
                    agent_ref=assignment.agent_id,
                    executor_type=assignment.executor_type,
                    model_ref=assignment.model_ref,
                    protocol_ref=request.protocol_ref,
                    context_package_ref=context.context_package_id,
                    context_package_hash=context.package_hash,
                    reason_codes=("RESPONSIBILITY_MATCH", "ACTIVE_ASSIGNMENT", "CONTEXT_MATCH"),
                )
                pin = RunStaffingPin(
                    run_id=request.run_id,
                    task_id=request.task_id,
                    responsibility_ref=responsibility.responsibility_id,
                    role_id=responsibility.role_id,
                    department_id=responsibility.department_id,
                    assignment_ref=assignment.assignment_id,
                    agent_id=assignment.agent_id,
                    executor_type=assignment.executor_type,
                    model_ref=assignment.model_ref,
                    context_package_ref=context.context_package_id,
                    context_package_hash=context.package_hash,
                )
                return decision, pin

        raise ValueError("NO_ELIGIBLE_ACTIVE_ASSIGNMENT_WITH_CONTEXT")

    @staticmethod
    def verify_pin(pin: RunStaffingPin, *, assignment: AgentAssignment, responsibility: RoleResponsibility, context: ContextPackage) -> None:
        if assignment.status != "ACTIVE":
            raise ValueError("PINNED_ASSIGNMENT_NOT_ACTIVE_AT_START")
        if responsibility.responsibility_id != pin.responsibility_ref or responsibility.role_id != pin.role_id:
            raise ValueError("PIN_RESPONSIBILITY_MISMATCH")
        if assignment.assignment_id != pin.assignment_ref or assignment.role_id != pin.role_id or assignment.department_id != pin.department_id:
            raise ValueError("PIN_ASSIGNMENT_MISMATCH")
        if assignment.agent_id != pin.agent_id or assignment.model_ref != pin.model_ref or assignment.executor_type != pin.executor_type:
            raise ValueError("PIN_EXECUTOR_MISMATCH")
        if context.context_package_id != pin.context_package_ref or context.package_hash != pin.context_package_hash:
            raise ValueError("PIN_CONTEXT_MISMATCH")
        if context.run_ref != pin.run_id or context.role_ref != pin.role_id or context.assignment_ref != pin.assignment_ref:
            raise ValueError("PIN_CONTEXT_LINEAGE_MISMATCH")
