import unittest

from px00.knowledge_routing import KnowledgeBindingRef, KnowledgeRoute, KnowledgeRouteRegistry


class KnowledgeRouteRegistryTests(unittest.TestCase):
    def setUp(self):
        self.binding = KnowledgeBindingRef(
            binding_id="KBD-SEC-ANALYST",
            role_ref="ROLE-SECURITY",
            knowledge_space_id="KB-SECURITY",
            logical_domain="security-core",
            access_mode="QUERY",
            purpose="security_analysis",
            protocol_refs=("PROTO-SEC-ANALYZE",),
        )

    def test_binding_resolves_to_initial_monorepo_location(self):
        registry = KnowledgeRouteRegistry((
            KnowledgeRoute("KB-SECURITY", "security-core", "1", "GITHUB_REPOSITORY", "VictorKVS/KNOWLEDGE_CORE", "main", content_root="security-core", resolver_priority=10),
        ))
        route = registry.resolve_binding(self.binding)
        self.assertEqual(route.endpoint_locator, "VictorKVS/KNOWLEDGE_CORE")
        self.assertEqual(route.content_root, "security-core")

    def test_migration_changes_physical_location_not_binding_identity(self):
        old = KnowledgeRoute("KB-SECURITY", "security-core", "1", "GITHUB_REPOSITORY", "VictorKVS/KNOWLEDGE_CORE", "main", status="MIGRATING", content_root="security-core", resolver_priority=10)
        new = KnowledgeRoute("KB-SECURITY", "security-core", "2", "GITHUB_REPOSITORY", "VictorKVS/SECURITY_KB", "main", content_root="/", migration_from_ref="KB-SECURITY@1", resolver_priority=20)
        registry = KnowledgeRouteRegistry((old, new))
        route = registry.resolve_binding(self.binding)
        self.assertEqual(route.endpoint_locator, "VictorKVS/SECURITY_KB")
        self.assertEqual(self.binding.knowledge_space_id, "KB-SECURITY")
        self.assertEqual(self.binding.logical_domain, "security-core")

    def test_suspended_route_is_not_selected(self):
        registry = KnowledgeRouteRegistry((
            KnowledgeRoute("KB-SECURITY", "security-core", "1", "GITHUB_REPOSITORY", "VictorKVS/SECURITY_KB", "main", status="SUSPENDED"),
        ))
        with self.assertRaisesRegex(ValueError, "NO_ACTIVE_KNOWLEDGE_ROUTE"):
            registry.resolve_binding(self.binding)

    def test_route_version_is_immutable(self):
        registry = KnowledgeRouteRegistry()
        route = KnowledgeRoute("KB-SECURITY", "security-core", "1", "GITHUB_REPOSITORY", "VictorKVS/KNOWLEDGE_CORE", "main")
        registry.register(route)
        with self.assertRaisesRegex(ValueError, "KNOWLEDGE_ROUTE_VERSION_REUSE"):
            registry.register(route)

    def test_unknown_endpoint_type_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "UNKNOWN_ENDPOINT_TYPE"):
            KnowledgeRouteRegistry((KnowledgeRoute("KB-X", "x", "1", "MAGIC", "somewhere", "main"),))


if __name__ == "__main__":
    unittest.main()
