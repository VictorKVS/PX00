from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable


@dataclass(frozen=True)
class KnowledgeRoute:
    knowledge_space_id: str
    logical_domain: str
    route_version: str
    endpoint_type: str
    endpoint_locator: str
    endpoint_ref: str
    status: str = "ACTIVE"
    resolver_priority: int = 100
    content_root: str | None = None
    migration_from_ref: str | None = None


@dataclass(frozen=True)
class KnowledgeBindingRef:
    binding_id: str
    role_ref: str
    knowledge_space_id: str
    logical_domain: str
    access_mode: str
    purpose: str
    protocol_refs: tuple[str, ...]


class KnowledgeRouteRegistry:
    """Resolves stable knowledge-space identities to mutable physical endpoints."""

    ALLOWED_STATUS = {"ACTIVE", "MIGRATING", "SUSPENDED", "RETIRED"}
    ALLOWED_ENDPOINT_TYPES = {"GITHUB_REPOSITORY", "GIT_REPOSITORY", "OBJECT_STORE", "DATABASE", "API"}

    def __init__(self, routes: Iterable[KnowledgeRoute] = ()) -> None:
        self._routes: Dict[tuple[str, str], KnowledgeRoute] = {}
        for route in routes:
            self.register(route)

    def register(self, route: KnowledgeRoute) -> None:
        if route.status not in self.ALLOWED_STATUS:
            raise ValueError("UNKNOWN_ROUTE_STATUS")
        if route.endpoint_type not in self.ALLOWED_ENDPOINT_TYPES:
            raise ValueError("UNKNOWN_ENDPOINT_TYPE")
        key = (route.knowledge_space_id, route.route_version)
        if key in self._routes:
            raise ValueError("KNOWLEDGE_ROUTE_VERSION_REUSE")
        self._routes[key] = route

    def resolve(self, knowledge_space_id: str, logical_domain: str) -> KnowledgeRoute:
        candidates = [
            route for route in self._routes.values()
            if route.knowledge_space_id == knowledge_space_id
            and route.logical_domain == logical_domain
            and route.status in {"ACTIVE", "MIGRATING"}
        ]
        if not candidates:
            raise ValueError("NO_ACTIVE_KNOWLEDGE_ROUTE")
        candidates.sort(key=lambda route: (route.resolver_priority, route.route_version), reverse=True)
        return candidates[0]

    def resolve_binding(self, binding: KnowledgeBindingRef) -> KnowledgeRoute:
        return self.resolve(binding.knowledge_space_id, binding.logical_domain)

    def history(self, knowledge_space_id: str, logical_domain: str) -> tuple[KnowledgeRoute, ...]:
        routes = [
            route for route in self._routes.values()
            if route.knowledge_space_id == knowledge_space_id and route.logical_domain == logical_domain
        ]
        return tuple(sorted(routes, key=lambda route: route.route_version))
