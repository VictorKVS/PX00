import unittest

from px00.context_packages import (
    ContextPackageBuilder,
    KnowledgeBindingRef,
    KnowledgeObjectRef,
    KnowledgeRequest,
)


D1 = "1" * 64
D2 = "2" * 64


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

    def obj(
        self,
        oid,
        otype,
        digest=D1,
        version="v1",
        route="KROUTE-SNAP-1",
        classification="PUBLIC",
        snapshot=None,
    ):
        return KnowledgeObjectRef(
            oid,
            version,
            digest,
            otype,
            "KB-SECURITY",
            "controls",
            classification,
            route,
            snapshot,
        )

    def test_builds_bounded_immutable_context(self):
        candidates = (
            self.obj("SRC-2", "SRC"),
            self.obj("EVD-1", "EVD", classification="INTERNAL"),
            self.obj("CLM-1", "CLM"),
        )
        package = self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(self.binding,), candidates=candidates, context_package_id="CTX-1")
        self.assertEqual(package.knowledge_object_refs, ("EVD-1", "SRC-2"))
        self.assertEqual(package.knowledge_object_version_refs, (f"EVD-1@v1#{D1}", f"SRC-2@v1#{D1}"))
        self.assertEqual(package.route_snapshot_refs, ("KROUTE-SNAP-1",))
        self.assertEqual(package.knowledge_snapshot_refs, ())
        self.assertEqual(len(package.package_hash), 64)

    def test_external_snapshot_is_preserved_in_context(self):
        candidate = self.obj("SRC-1", "SRC", snapshot="KSNAP-SEC-0001")
        package = self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(self.binding,), candidates=(candidate,), context_package_id="CTX-1")
        self.assertEqual(package.knowledge_snapshot_refs, ("KSNAP-SEC-0001",))

    def test_external_snapshot_change_changes_package_hash(self):
        first = self.builder.build(
            self.request,
            assignment_ref="ASGN-1",
            bindings=(self.binding,),
            candidates=(self.obj("SRC-1", "SRC", snapshot="KSNAP-SEC-0001"),),
            context_package_id="CTX-1",
        )
        second = self.builder.build(
            self.request,
            assignment_ref="ASGN-1",
            bindings=(self.binding,),
            candidates=(self.obj("SRC-1", "SRC", snapshot="KSNAP-SEC-0002"),),
            context_package_id="CTX-2",
        )
        self.assertEqual(first.knowledge_object_version_refs, second.knowledge_object_version_refs)
        self.assertNotEqual(first.package_hash, second.package_hash)

    def test_content_change_under_same_object_id_changes_package_hash(self):
        first = self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(self.binding,), candidates=(self.obj("SRC-1","SRC",D1),), context_package_id="CTX-1")
        second = self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(self.binding,), candidates=(self.obj("SRC-1","SRC",D2),), context_package_id="CTX-2")
        self.assertEqual(first.knowledge_object_refs, second.knowledge_object_refs)
        self.assertNotEqual(first.knowledge_object_version_refs, second.knowledge_object_version_refs)
        self.assertNotEqual(first.package_hash, second.package_hash)

    def test_version_change_under_same_object_id_changes_package_hash(self):
        first = self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(self.binding,), candidates=(self.obj("SRC-1","SRC",D1,"v1"),), context_package_id="CTX-1")
        second = self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(self.binding,), candidates=(self.obj("SRC-1","SRC",D1,"v2"),), context_package_id="CTX-2")
        self.assertNotEqual(first.package_hash, second.package_hash)

    def test_invalid_digest_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "INVALID_KNOWLEDGE_CONTENT_DIGEST"):
            self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(self.binding,), candidates=(self.obj("SRC-1","SRC","bad"),), context_package_id="CTX-1")

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
        candidate = self.obj("https://github.com/VictorKVS/SECURITY_KB/file", "SRC")
        with self.assertRaisesRegex(ValueError, "PHYSICAL_LOCATION_USED_AS_KNOWLEDGE_ID"):
            self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(self.binding,), candidates=(candidate,), context_package_id="CTX-1")

    def test_physical_route_migration_preserves_logical_and_content_identity(self):
        candidate_a = self.obj("SRC-1", "SRC", D1, "v1", "KROUTE-SNAP-OLD")
        candidate_b = self.obj("SRC-1", "SRC", D1, "v1", "KROUTE-SNAP-NEW")
        first = self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(self.binding,), candidates=(candidate_a,), context_package_id="CTX-1")
        second = self.builder.build(self.request, assignment_ref="ASGN-1", bindings=(self.binding,), candidates=(candidate_b,), context_package_id="CTX-2")
        self.assertEqual(first.knowledge_object_refs, second.knowledge_object_refs)
        self.assertEqual(first.knowledge_object_version_refs, second.knowledge_object_version_refs)
        self.assertNotEqual(first.package_hash, second.package_hash)


if __name__ == "__main__":
    unittest.main()
