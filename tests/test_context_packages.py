import unittest

from px00.context_packages import (
    ContextPackageBuilder,
    KnowledgeBindingRef,
    KnowledgeObjectRef,
    KnowledgeRequest,
)


class ContextPackageBuilderTests(unittest.TestCase):
    def setUp(self):
        self.builder = ContextPackageBuilder()
        self.binding = KnowledgeBindingRef(
            binding_id="KBind-1",
            role_ref="ROLE-SECURITY",
            knowledge_space_id="KB-SECURITY",
            domain_id="controls",
            access_mode="QUERY",
            protocol_refs=("PROTO-SEC-1",),
            object_type_allowlist=("SRC", "EVD", "CLM"),
            classification_ceiling="CONFIDENTIAL",
        )
        self.request = KnowledgeRequest(
            knowledge_request_id="KREQ-1",
            task_ref="TASK-1",
            run_ref="RUN-1",
            role_ref="ROLE-SECURITY",
            protocol_ref="PROTO-SEC-1",
            binding_refs=("KBind-1",),
            query="find controls",
            requested_object_types=("SRC", "EVD"),
            max_objects=2,
            classification_ceiling="INTERNAL",
            purpose="security analysis",
        )

    def test_builds_bounded_immutable_context(self):
        candidates = (
            KnowledgeObjectRef("SRC-2", "SRC", "KB-SECURITY", "controls", "PUBLIC", "KROUTE-SNAP-1"),
            KnowledgeObjectRef("EVD-1", "EVD", "KB-SECURITY", "controls", "INTERNAL", "KROUTE-SNAP-1"),
            KnowledgeObjectRef("CLM-1", "CLM", "KB-SECURITY", "controls", "PUBLIC", "KROUTE-SNAP-1"),
        )
        package = self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(self.binding,), candidates=candidates, context_package_id="CTX-1")
        self.assertEqual(package.knowledge_object_refs, ("EVD-1", "SRC-2"))
        self.assertEqual(package.route_snapshot_refs, ("KROUTE-SNAP-1",))
        self.assertEqual(len(package.package_hash), 64)

    def test_role_mismatch_fails_closed(self):
        bad = KnowledgeBindingRef(**{**self.binding.__dict__, "role_ref": "ROLE-OTHER"})
        with self.assertRaisesRegex(ValueError, "BINDING_ROLE_MISMATCH"):
            self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(bad,), candidates=(), context_package_id="CTX-1")

    def test_protocol_mismatch_fails_closed(self):
        bad = KnowledgeBindingRef(**{**self.binding.__dict__, "protocol_refs": ("PROTO-OTHER",)})
        with self.assertRaisesRegex(ValueError, "PROTOCOL_NOT_ALLOWED_FOR_BINDING"):
            self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(bad,), candidates=(), context_package_id="CTX-1")

    def test_classification_overflow_is_rejected(self):
        req = KnowledgeRequest(**{**self.request.__dict__, "classification_ceiling": "SECRET"})
        with self.assertRaisesRegex(ValueError, "REQUEST_CLASSIFICATION_EXCEEDS_BINDING"):
            self.builder.build(req, assignment_ref="ASGN-1", bindings=(self.binding,), candidates=(), context_package_id="CTX-1")

    def test_physical_location_cannot_be_knowledge_id(self):
        candidate = KnowledgeObjectRef("https://github.com/VictorKVS/SECURITY_KB/file", "SRC", "KB-SECURITY", "controls", "PUBLIC", "KROUTE-SNAP-1")
        with self.assertRaisesRegex(ValueError, "PHYSICAL_LOCATION_USED_AS_KNOWLEDGE_ID"):
            self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(self.binding,), candidates=(candidate,), context_package_id="CTX-1")

    def test_physical_route_migration_does_not_change_logical_selection(self):
        candidate_a = KnowledgeObjectRef("SRC-1", "SRC", "KB-SECURITY", "controls", "PUBLIC", "KROUTE-SNAP-OLD")
        candidate_b = KnowledgeObjectRef("SRC-1", "SRC", "KB-SECURITY", "controls", "PUBLIC", "KROUTE-SNAP-NEW")
        first = self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(self.binding,), candidates=(candidate_a,), context_package_id="CTX-1")
        second = self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(self.binding,), candidates=(candidate_b,), context_package_id="CTX-2")
        self.assertEqual(first.knowledge_object_refs, second.knowledge_object_refs)
        self.assertNotEqual(first.package_hash, second.package_hash)


if __name__ == "__main__":
    unittest.main()
