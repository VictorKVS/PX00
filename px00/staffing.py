from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RoleResponsibility:
    responsibility_id: str
    role_id: str
    department_id: str
    duty_code: str
    description: str
    allowed_protocol_refs: tuple[str, ...]
    knowledge_binding_refs: tuple[str, ...]
    required_outputs: tuple[str, ...] = ()
    escalation_conditions: tuple[str, ...] = ()


@dataclass(frozen=True)
class AgentAssignment:
    assignment_id: str
    agent_id: str
    role_id: str
    department_id: str
    executor_type: str
    model_ref: str
    knowledge_binding_refs: tuple[str, ...]
    capability_refs: tuple[str, ...] = ()
    tool_profile_refs: tuple[str, ...] = ()
    status: str = "ACTIVE"


@dataclass(frozen=True)
class HandoffPackage:
    handoff_id: str
    task_id: str
    from_role_id: str
    to_role_id: str
    protocol_ref: str
    responsibility_ref: str
    input_refs: tuple[str, ...]
    output_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    assumptions: tuple[str, ...]
    unresolved_questions: tuple[str, ...]
    blocking_findings: tuple[str, ...]
    acceptance_state: str
    previous_handoff_ref: str | None = None


@dataclass
class StaffingRegistry:
    responsibilities: dict[str, RoleResponsibility] = field(default_factory=dict)
    assignments: dict[str, AgentAssignment] = field(default_factory=dict)
    handoffs: dict[str, HandoffPackage] = field(default_factory=dict)
    role_knowledge_bindings: dict[str, set[str]] = field(default_factory=dict)
    allowed_role_protocols: dict[str, set[str]] = field(default_factory=dict)

    def declare_role(self, role_id: str, *, knowledge_bindings: tuple[str, ...], protocols: tuple[str, ...]) -> None:
        self.role_knowledge_bindings[role_id] = set(knowledge_bindings)
        self.allowed_role_protocols[role_id] = set(protocols)

    def add_responsibility(self, item: RoleResponsibility) -> None:
        if item.responsibility_id in self.responsibilities:
            raise ValueError("RESPONSIBILITY_ID_REUSE")
        if item.role_id not in self.role_knowledge_bindings:
            raise ValueError("UNKNOWN_ROLE_REF")
        if not set(item.knowledge_binding_refs).issubset(self.role_knowledge_bindings[item.role_id]):
            raise ValueError("RESPONSIBILITY_KNOWLEDGE_BINDING_OVERFLOW")
        if not set(item.allowed_protocol_refs).issubset(self.allowed_role_protocols[item.role_id]):
            raise ValueError("RESPONSIBILITY_PROTOCOL_OVERFLOW")
        self.responsibilities[item.responsibility_id] = item

    def assign_agent(self, item: AgentAssignment) -> None:
        if item.assignment_id in self.assignments:
            raise ValueError("ASSIGNMENT_ID_REUSE")
        if item.role_id not in self.role_knowledge_bindings:
            raise ValueError("UNKNOWN_ROLE_REF")
        if item.status not in {"ACTIVE", "SUSPENDED", "RETIRED"}:
            raise ValueError("UNKNOWN_ASSIGNMENT_STATUS")
        if not set(item.knowledge_binding_refs).issubset(self.role_knowledge_bindings[item.role_id]):
            raise ValueError("ASSIGNMENT_KNOWLEDGE_BINDING_OVERFLOW")
        self.assignments[item.assignment_id] = item

    def can_start_run(self, assignment_id: str) -> bool:
        try:
            assignment = self.assignments[assignment_id]
        except KeyError as exc:
            raise ValueError("UNKNOWN_ASSIGNMENT_REF") from exc
        return assignment.status == "ACTIVE"

    def create_handoff(self, item: HandoffPackage) -> None:
        if item.handoff_id in self.handoffs:
            raise ValueError("HANDOFF_ID_REUSE")
        if item.from_role_id not in self.allowed_role_protocols or item.to_role_id not in self.allowed_role_protocols:
            raise ValueError("UNKNOWN_ROLE_REF")
        if item.protocol_ref not in self.allowed_role_protocols[item.from_role_id]:
            raise ValueError("SENDER_PROTOCOL_NOT_ALLOWED")
        if item.protocol_ref not in self.allowed_role_protocols[item.to_role_id]:
            raise ValueError("RECEIVER_PROTOCOL_NOT_ALLOWED")
        responsibility = self.responsibilities.get(item.responsibility_ref)
        if responsibility is None:
            raise ValueError("UNKNOWN_RESPONSIBILITY_REF")
        if responsibility.role_id != item.from_role_id:
            raise ValueError("HANDOFF_RESPONSIBILITY_ROLE_MISMATCH")
        if item.blocking_findings and item.acceptance_state == "READY":
            raise ValueError("READY_WITH_BLOCKING_FINDINGS")
        if item.acceptance_state not in {"READY", "NEEDS_REWORK", "BLOCKED", "ESCALATED"}:
            raise ValueError("UNKNOWN_HANDOFF_STATE")
        self.handoffs[item.handoff_id] = item
