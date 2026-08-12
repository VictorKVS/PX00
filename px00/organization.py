from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class KnowledgeBinding:
    binding_id: str
    role_ref: str
    knowledge_repository: str
    domain_path: str
    access_mode: str
    purpose: str
    protocol_refs: tuple[str, ...]
    object_type_allowlist: tuple[str, ...] = ()
    classification_ceiling: str | None = None
    version_or_ref: str | None = None


@dataclass(frozen=True)
class Department:
    department_id: str
    organization_ref: str
    name: str
    mandate: str
    role_refs: tuple[str, ...]
    inbound_protocol_refs: tuple[str, ...]
    outbound_protocol_refs: tuple[str, ...]


@dataclass
class CorporateOrganization:
    organization_id: str
    name: str
    governance_profile_ref: str
    departments: dict[str, Department] = field(default_factory=dict)
    knowledge_bindings: dict[str, KnowledgeBinding] = field(default_factory=dict)

    def add_department(self, department: Department) -> None:
        if department.department_id in self.departments:
            raise ValueError("DEPARTMENT_ID_REUSE")
        if department.organization_ref != self.organization_id:
            raise ValueError("DEPARTMENT_ORGANIZATION_MISMATCH")
        if not department.mandate.strip():
            raise ValueError("DEPARTMENT_MANDATE_REQUIRED")
        self.departments[department.department_id] = department

    def add_knowledge_binding(self, binding: KnowledgeBinding) -> None:
        if binding.binding_id in self.knowledge_bindings:
            raise ValueError("KNOWLEDGE_BINDING_ID_REUSE")
        if binding.access_mode not in {"READ", "QUERY", "PROPOSE"}:
            raise ValueError("UNKNOWN_KNOWLEDGE_ACCESS_MODE")
        if binding.knowledge_repository != "VictorKVS/KNOWLEDGE_CORE":
            raise ValueError("UNDECLARED_KNOWLEDGE_REPOSITORY")
        if not binding.domain_path.strip():
            raise ValueError("KNOWLEDGE_DOMAIN_REQUIRED")
        if not binding.protocol_refs:
            raise ValueError("KNOWLEDGE_BINDING_PROTOCOL_REQUIRED")
        self.knowledge_bindings[binding.binding_id] = binding

    def bindings_for_role(self, role_ref: str) -> tuple[KnowledgeBinding, ...]:
        return tuple(sorted((b for b in self.knowledge_bindings.values() if b.role_ref == role_ref), key=lambda b: b.binding_id))

    def validate_handoff(self, from_department: str, to_department: str, protocol_ref: str) -> bool:
        try:
            source = self.departments[from_department]
            target = self.departments[to_department]
        except KeyError as exc:
            raise ValueError("UNKNOWN_DEPARTMENT_REF") from exc
        if protocol_ref not in source.outbound_protocol_refs:
            raise ValueError("SOURCE_HANDOFF_PROTOCOL_NOT_DECLARED")
        if protocol_ref not in target.inbound_protocol_refs:
            raise ValueError("TARGET_HANDOFF_PROTOCOL_NOT_DECLARED")
        return True
