from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


STATUS_BY_TYPE = {
    "CLAIM_ASSESSMENT": ("CURRENT", "SUPERSEDED"),
    "KNOWLEDGE": ("CURRENT", "STALE"),
    "DECISION": ("CURRENT", "REASSESSMENT_REQUIRED"),
    "PLAN": ("CURRENT", "REVIEW_REQUIRED"),
}


@dataclass(frozen=True)
class DependencyNode:
    object_ref: str
    object_type: str
    status: str = "CURRENT"


@dataclass(frozen=True)
class StatusChange:
    object_ref: str
    object_type: str
    previous_status: str
    new_status: str
    path: tuple[str, ...]


@dataclass(frozen=True)
class DownstreamImpact:
    impact_id: str
    trigger_ref: str
    trigger_type: str
    caused_by_ref: str
    created_at: str
    affected_objects: tuple[str, ...]
    status_changes: tuple[StatusChange, ...]
    propagation_depth: int


@dataclass
class DownstreamDependencyGraph:
    nodes: dict[str, DependencyNode] = field(default_factory=dict)
    edges: set[tuple[str, str]] = field(default_factory=set)
    impacts: dict[str, DownstreamImpact] = field(default_factory=dict)

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def add_node(self, node: DependencyNode) -> None:
        if node.object_ref in self.nodes:
            raise ValueError("DEPENDENCY_NODE_ID_REUSE")
        if node.object_type not in STATUS_BY_TYPE:
            raise ValueError("UNKNOWN_DEPENDENCY_OBJECT_TYPE")
        if node.status not in STATUS_BY_TYPE[node.object_type]:
            raise ValueError("INVALID_DEPENDENCY_STATUS")
        self.nodes[node.object_ref] = node

    def add_dependency(self, upstream_ref: str, downstream_ref: str) -> None:
        if upstream_ref not in self.nodes or downstream_ref not in self.nodes:
            raise ValueError("UNKNOWN_DEPENDENCY_NODE_REF")
        if upstream_ref == downstream_ref:
            raise ValueError("DEPENDENCY_CYCLE")
        self.edges.add((upstream_ref, downstream_ref))
        if self._reachable(downstream_ref, upstream_ref):
            self.edges.remove((upstream_ref, downstream_ref))
            raise ValueError("DEPENDENCY_CYCLE")

    def _reachable(self, start: str, target: str) -> bool:
        seen = set()
        stack = [start]
        while stack:
            current = stack.pop()
            if current == target:
                return True
            if current in seen:
                continue
            seen.add(current)
            stack.extend(dst for src, dst in self.edges if src == current)
        return False

    @staticmethod
    def _stale_status(object_type: str) -> str:
        return STATUS_BY_TYPE[object_type][1]

    def propagate(self, *, trigger_ref: str, caused_by_ref: str, impact_id: str | None = None, created_at: str | None = None) -> DownstreamImpact:
        if trigger_ref not in self.nodes:
            raise ValueError("UNKNOWN_TRIGGER_REF")
        trigger = self.nodes[trigger_ref]
        queue = [(trigger_ref, (trigger_ref,))]
        visited = {trigger_ref}
        changes: list[StatusChange] = []
        max_depth = 0

        while queue:
            current, path = queue.pop(0)
            for src, dst in sorted(self.edges):
                if src != current or dst in visited:
                    continue
                visited.add(dst)
                node = self.nodes[dst]
                new_status = self._stale_status(node.object_type)
                if node.status != new_status:
                    changes.append(StatusChange(dst, node.object_type, node.status, new_status, path + (dst,)))
                    self.nodes[dst] = DependencyNode(dst, node.object_type, new_status)
                queue.append((dst, path + (dst,)))
                max_depth = max(max_depth, len(path))

        impact = DownstreamImpact(
            impact_id=impact_id or f"IMPACT-{uuid4().hex[:12]}",
            trigger_ref=trigger_ref,
            trigger_type=trigger.object_type,
            caused_by_ref=caused_by_ref,
            created_at=created_at or self._now(),
            affected_objects=tuple(change.object_ref for change in changes),
            status_changes=tuple(changes),
            propagation_depth=max_depth,
        )
        if impact.impact_id in self.impacts:
            raise ValueError("IMPACT_ID_REUSE")
        self.impacts[impact.impact_id] = impact
        return impact
