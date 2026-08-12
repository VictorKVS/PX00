from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Iterable


@dataclass(frozen=True)
class KnowledgeBindingRef:
    binding_id: str
    role_ref: str
    knowledge_space_id: str
    domain_id: str
    access_mode: str
    protocol_refs: tuple[str, ...]
    object_type_allowlist: tuple[str, ...] = ()
    classification_ceiling: str = "PUBLIC"


@dataclass(frozen=True)
class KnowledgeObjectRef:
    object_id: str
    version_id: str
    content_digest: str
    object_type: str
    knowledge_space_id: str
    domain_id: str
    classification: str
    route_snapshot_ref: str

    def version_ref(self) -> str:
        return f"{self.object_id}@{self.version_id}#{self.content_digest}"


@dataclass(frozen=True)
class KnowledgeRequest:
    knowledge_request_id: str
    task_ref: str
    run_ref: str
    role_ref: str
    protocol_ref: str
    binding_refs: tuple[str, ...]
    query: str
    requested_object_types: tuple[str, ...]
    max_objects: int
    classification_ceiling: str
    purpose: str


@dataclass(frozen=True)
class ContextPackage:
    context_package_id: str
    knowledge_request_ref: str
    run_ref: str
    role_ref: str
    assignment_ref: str
    binding_refs: tuple[str, ...]
    knowledge_object_refs: tuple[str, ...]
    knowledge_object_version_refs: tuple[str, ...]
    route_snapshot_refs: tuple[str, ...]
    package_hash: str
    hash_algorithm: str = "sha256"


class ContextPackageBuilder:
    CLASSIFICATION_ORDER = {"PUBLIC": 0, "INTERNAL": 1, "CONFIDENTIAL": 2, "SECRET": 3}

    @classmethod
    def _canonical(cls, value: object) -> bytes:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

    @classmethod
    def _classification_allowed(cls, value: str, ceiling: str) -> bool:
        try:
            return cls.CLASSIFICATION_ORDER[value] <= cls.CLASSIFICATION_ORDER[ceiling]
        except KeyError as exc:
            raise ValueError("UNKNOWN_CLASSIFICATION") from exc

    @staticmethod
    def _valid_sha256(value: str) -> bool:
        if len(value) != 64:
            return False
        try:
            int(value, 16)
        except ValueError:
            return False
        return True

    def build(
        self,
        request: KnowledgeRequest,
        *,
        assignment_ref: str,
        bindings: Iterable[KnowledgeBindingRef],
        candidates: Iterable[KnowledgeObjectRef],
        context_package_id: str,
    ) -> ContextPackage:
        bindings_by_id = {b.binding_id: b for b in bindings}
        selected_bindings: list[KnowledgeBindingRef] = []
        for binding_id in request.binding_refs:
            binding = bindings_by_id.get(binding_id)
            if binding is None:
                raise ValueError("UNKNOWN_KNOWLEDGE_BINDING")
            if binding.role_ref != request.role_ref:
                raise ValueError("BINDING_ROLE_MISMATCH")
            if request.protocol_ref not in binding.protocol_refs:
                raise ValueError("PROTOCOL_NOT_ALLOWED_FOR_BINDING")
            if not self._classification_allowed(request.classification_ceiling, binding.classification_ceiling):
                raise ValueError("REQUEST_CLASSIFICATION_EXCEEDS_BINDING")
            selected_bindings.append(binding)

        if request.max_objects <= 0:
            raise ValueError("INVALID_MAX_OBJECTS")

        allowed_types = set(request.requested_object_types)
        results: list[KnowledgeObjectRef] = []
        for candidate in candidates:
            if candidate.object_id.startswith("http://") or candidate.object_id.startswith("https://"):
                raise ValueError("PHYSICAL_LOCATION_USED_AS_KNOWLEDGE_ID")
            if not candidate.version_id.strip():
                raise ValueError("KNOWLEDGE_VERSION_REQUIRED")
            if not self._valid_sha256(candidate.content_digest):
                raise ValueError("INVALID_KNOWLEDGE_CONTENT_DIGEST")
            for binding in selected_bindings:
                if candidate.knowledge_space_id != binding.knowledge_space_id or candidate.domain_id != binding.domain_id:
                    continue
                if allowed_types and candidate.object_type not in allowed_types:
                    continue
                if binding.object_type_allowlist and candidate.object_type not in binding.object_type_allowlist:
                    continue
                if not self._classification_allowed(candidate.classification, request.classification_ceiling):
                    continue
                results.append(candidate)
                break

        results = sorted(results, key=lambda item: (item.object_id, item.version_id))[: request.max_objects]
        refs = tuple(item.object_id for item in results)
        version_refs = tuple(item.version_ref() for item in results)
        routes = tuple(sorted({item.route_snapshot_ref for item in results}))
        material = {
            "knowledge_request_ref": request.knowledge_request_id,
            "run_ref": request.run_ref,
            "role_ref": request.role_ref,
            "assignment_ref": assignment_ref,
            "binding_refs": tuple(sorted(request.binding_refs)),
            "knowledge_object_refs": refs,
            "knowledge_object_version_refs": version_refs,
            "route_snapshot_refs": routes,
        }
        digest = sha256(self._canonical(material)).hexdigest()
        return ContextPackage(
            context_package_id=context_package_id,
            knowledge_request_ref=request.knowledge_request_id,
            run_ref=request.run_ref,
            role_ref=request.role_ref,
            assignment_ref=assignment_ref,
            binding_refs=tuple(sorted(request.binding_refs)),
            knowledge_object_refs=refs,
            knowledge_object_version_refs=version_refs,
            route_snapshot_refs=routes,
            package_hash=digest,
        )
