import unittest

from px00.context_packages import ContextPackageBuilder, KnowledgeBindingRef, KnowledgeRequest
from px00.knowledge_manifest_bridge import KnowledgeManifestBridge


MANIFEST = {
    "schema_version": 1,
    "manifest_id": "SEC-SNAPSHOT-0001",
    "knowledge_space_id": "KB-SECURITY",
    "canonical_repository": "VictorKVS/KNOWLEDGE_CORE",
    "repository_commit_sha": "8f7e1cb7a5abec39e0432ce7a811591a5dcadc8d",
    "content_root": "security-knowledge/",
    "selection_request_ref": "INTEGRATION-REQ-SEC-0001",
    "hash_algorithm": "sha256",
    "selected_objects": [
        {
            "object_id": "FSB-117-2025",
            "version_id": "record-rev-8f7e1cb7a5ab",
            "object_type": "SOURCE_METADATA",
            "repository_relative_path": "security-knowledge/legislation/RU/regulators/FSB/117-2025/document.yaml",
            "content_digest_sha256": "5bdfd92728c6be35cdbffba5c57bb843bf1f3e48813c47fab2a755a5a3351710",
            "knowledge_state": "SOURCE_VERIFIED",
            "source_locator_ref": "publication.pravo.gov.ru:0001202503260008",
            "freshness_state": "CURRENT_METADATA_AT_PINNED_COMMIT",
            "classification": "PUBLIC",
            "selection_reason": (
                "First cross-repository integration slice. Official metadata is verified while the "
                "full source text and atomization remain explicitly pending, so this object proves "
                "provenance/snapshot transport but must not be treated as a VERIFIED atomic requirement."
            ),
        }
    ],
    "manifest_digest": "8830d3aa51dab48586bdc96945f2e38182ced261eacef05fb10ef42ac9ce81d2",
}
EXPECTED_RUNTIME_SNAPSHOT_DIGEST = "04d5ec28431e8c13863dab9896533435dac735ceb36b6bf59e4f05eea1f7eac3"
EXPECTED_CONTEXT_PACKAGE_HASH = "9c09e6a4075f25ce2e341d1b0bd2fa4f59dedadf364019492be337893c220a2a"


class KnowledgeManifestBridgeTests(unittest.TestCase):
    def setUp(self):
        self.bridge = KnowledgeManifestBridge()

    def import_slice(self, manifest=MANIFEST):
        return self.bridge.import_manifest(
            manifest,
            expected_repository="VictorKVS/KNOWLEDGE_CORE",
            expected_knowledge_space_id="KB-SECURITY",
            expected_content_root="security-knowledge/",
            route_snapshot_ref="KROUTE-SECURITY-v1",
            domain_id="SECURITY",
            product_ref="SEC-PROD-0001",
            domain_ref="SECURITY",
        )

    def tampered_manifest(self, field, value):
        tampered = dict(MANIFEST)
        tampered["selected_objects"] = [dict(MANIFEST["selected_objects"][0])]
        tampered["selected_objects"][0][field] = value
        return tampered

    def test_real_manifest_digest_matches_consumer_algorithm(self):
        self.assertEqual(
            self.bridge.producer_manifest_digest(MANIFEST),
            MANIFEST["manifest_digest"],
        )

    def test_import_preserves_source_verified_without_promotion(self):
        imported = self.import_slice()
        self.assertEqual(imported.producer_manifest_id, "SEC-SNAPSHOT-0001")
        self.assertEqual(imported.snapshot.repository_commit_sha, MANIFEST["repository_commit_sha"])
        self.assertEqual(imported.snapshot.knowledge_space_id, "KB-SECURITY")
        self.assertEqual(imported.snapshot.snapshot_digest, EXPECTED_RUNTIME_SNAPSHOT_DIGEST)
        self.assertEqual(imported.objects[0].knowledge_state, "SOURCE_VERIFIED")
        self.assertNotEqual(imported.objects[0].knowledge_state, "VERIFIED")
        self.assertEqual(
            imported.objects[0].source_locator_ref,
            "publication.pravo.gov.ru:0001202503260008",
        )
        self.assertEqual(imported.objects[0].freshness_state, "CURRENT_METADATA_AT_PINNED_COMMIT")
        self.assertEqual(imported.objects[0].context_object.classification, "PUBLIC")

    def test_imported_real_slice_builds_snapshot_bound_context_package(self):
        imported = self.import_slice()
        binding = KnowledgeBindingRef(
            binding_id="KBIND-SECURITY-1",
            role_ref="ROLE-SECURITY",
            knowledge_space_id="KB-SECURITY",
            domain_id="SECURITY",
            access_mode="QUERY",
            protocol_refs=("PROTO-SECURITY-SNAPSHOT-1",),
            object_type_allowlist=("SOURCE_METADATA",),
            classification_ceiling="PUBLIC",
        )
        request = KnowledgeRequest(
            knowledge_request_id="KREQ-SEC-REAL-0001",
            task_ref="TASK-SEC-REAL-0001",
            run_ref="RUN-SEC-REAL-0001",
            role_ref="ROLE-SECURITY",
            protocol_ref="PROTO-SECURITY-SNAPSHOT-1",
            binding_refs=("KBIND-SECURITY-1",),
            query="Provide pinned official metadata for FSB Order 117/2025",
            requested_object_types=("SOURCE_METADATA",),
            max_objects=1,
            classification_ceiling="PUBLIC",
            purpose="cross-repository provenance integration proof",
        )
        package = ContextPackageBuilder().build(
            request,
            assignment_ref="ASGN-SECURITY-REAL-0001",
            bindings=(binding,),
            candidates=tuple(item.context_object for item in imported.objects),
            context_package_id="CTX-SEC-REAL-0001",
        )
        self.assertEqual(package.knowledge_object_refs, ("FSB-117-2025",))
        self.assertEqual(package.knowledge_snapshot_refs, ("SEC-SNAPSHOT-0001",))
        self.assertEqual(package.route_snapshot_refs, ("KROUTE-SECURITY-v1",))
        self.assertEqual(package.package_hash, EXPECTED_CONTEXT_PACKAGE_HASH)

    def test_tampered_selection_state_fails_manifest_integrity(self):
        with self.assertRaisesRegex(ValueError, "PRODUCER_MANIFEST_DIGEST_MISMATCH"):
            self.import_slice(self.tampered_manifest("knowledge_state", "VERIFIED"))

    def test_tampered_source_locator_fails_manifest_integrity(self):
        with self.assertRaisesRegex(ValueError, "PRODUCER_MANIFEST_DIGEST_MISMATCH"):
            self.import_slice(self.tampered_manifest("source_locator_ref", "invented-locator"))

    def test_tampered_classification_fails_manifest_integrity(self):
        with self.assertRaisesRegex(ValueError, "PRODUCER_MANIFEST_DIGEST_MISMATCH"):
            self.import_slice(self.tampered_manifest("classification", "INTERNAL"))

    def test_tampered_freshness_fails_manifest_integrity(self):
        with self.assertRaisesRegex(ValueError, "PRODUCER_MANIFEST_DIGEST_MISMATCH"):
            self.import_slice(self.tampered_manifest("freshness_state", "STALE"))

    def test_wrong_repository_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "PRODUCER_REPOSITORY_MISMATCH"):
            self.bridge.import_manifest(
                MANIFEST,
                expected_repository="VictorKVS/OTHER",
                expected_knowledge_space_id="KB-SECURITY",
                expected_content_root="security-knowledge/",
                route_snapshot_ref="KROUTE-SECURITY-v1",
                domain_id="SECURITY",
            )


if __name__ == "__main__":
    unittest.main()
