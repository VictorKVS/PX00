from __future__ import annotations

import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from px00.context_packages import ContextPackageBuilder, KnowledgeBindingRef, KnowledgeRequest
from px00.kernel import SyntheticGovernedKernel
from px00.knowledge_manifest_bridge import KnowledgeManifestBridge
from px00.recorder import AppendOnlyEventRecorder
from px00.replay import ReadOnlyReplayVerifier
from px00.run_knowledge import RunKnowledgeBinder


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


class SecurityKnowledgeRunReplayTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.kernel = SyntheticGovernedKernel()
        base_request = self.kernel.prepare_request(4, 5)
        self.request = replace(base_request, requester_role_id="ROLE-SECURITY")
        self.result = self.kernel.execute_request(self.request, allow=True)

        self.imported = KnowledgeManifestBridge().import_manifest(
            MANIFEST,
            expected_repository="VictorKVS/KNOWLEDGE_CORE",
            expected_knowledge_space_id="KB-SECURITY",
            expected_content_root="security-knowledge/",
            route_snapshot_ref="KROUTE-SECURITY-v1",
            domain_id="SECURITY",
            product_ref="SEC-PROD-0001",
            domain_ref="SECURITY",
        )
        self.assignment_ref = "ASGN-SECURITY-REPLAY-0001"
        self.binding = KnowledgeBindingRef(
            binding_id="KBIND-SECURITY-REPLAY-1",
            role_ref="ROLE-SECURITY",
            knowledge_space_id="KB-SECURITY",
            domain_id="SECURITY",
            access_mode="QUERY",
            protocol_refs=(self.request.protocol_id,),
            object_type_allowlist=("SOURCE_METADATA",),
            classification_ceiling="PUBLIC",
        )
        knowledge_request = KnowledgeRequest(
            knowledge_request_id="KREQ-SECURITY-REPLAY-0001",
            task_ref=self.request.task_id,
            run_ref=self.request.run_id,
            role_ref="ROLE-SECURITY",
            protocol_ref=self.request.protocol_id,
            binding_refs=(self.binding.binding_id,),
            query="Pin official source metadata for replay provenance proof",
            requested_object_types=("SOURCE_METADATA",),
            max_objects=1,
            classification_ceiling="PUBLIC",
            purpose="prove real external knowledge context survives governed RUN replay",
        )
        self.context = ContextPackageBuilder().build(
            knowledge_request,
            assignment_ref=self.assignment_ref,
            bindings=(self.binding,),
            candidates=tuple(item.context_object for item in self.imported.objects),
            context_package_id="CTX-SECURITY-REPLAY-0001",
        )
        self.pin = RunKnowledgeBinder().bind(
            run_id=self.request.run_id,
            role_ref="ROLE-SECURITY",
            assignment_ref=self.assignment_ref,
            context_package=self.context,
            imported_slices=(self.imported,),
        )
        self.trace_context = self.pin.to_trace_context()
        self.recorder = AppendOnlyEventRecorder(self.root)
        self.recorder.record_all(self.result.events)
        self.persisted = self.recorder.persist_manifest(self.request.trace_id, self.trace_context)
        self.verifier = ReadOnlyReplayVerifier(self.recorder)

    def tearDown(self):
        self.tmp.cleanup()

    def test_real_security_snapshot_is_bound_to_trace_manifest(self):
        manifest = self.persisted.manifest
        self.assertEqual(manifest.context_package_ref, self.context.context_package_id)
        self.assertEqual(manifest.context_package_hash, self.context.package_hash)
        self.assertEqual(manifest.knowledge_snapshot_refs, ("SEC-SNAPSHOT-0001",))
        self.assertEqual(manifest.knowledge_snapshot_digests, (self.imported.snapshot.snapshot_digest,))
        self.assertEqual(manifest.producer_manifest_refs, ("SEC-SNAPSHOT-0001",))
        self.assertEqual(manifest.producer_manifest_digests, (MANIFEST["manifest_digest"],))

    def test_read_only_replay_verifies_events_policy_and_real_knowledge_context(self):
        report = self.verifier.verify(
            request=self.request,
            authority=self.result.authority_decision,
            snapshot=self.result.policy_snapshot,
            events=self.result.events,
            knowledge_context=self.trace_context,
        )
        self.assertEqual(report.status, "VERIFIED_RECORD")
        self.assertEqual(report.reason_code, "GOVERNED_LINEAGE_AND_KNOWLEDGE_CONTEXT_VERIFIED")
        self.assertTrue(report.knowledge_context_verified)
        self.assertEqual(report.context_package_ref, self.context.context_package_id)
        self.assertEqual(report.context_package_hash, self.context.package_hash)
        self.assertEqual(report.knowledge_snapshot_refs, ("SEC-SNAPSHOT-0001",))

    def test_replay_cannot_ignore_knowledge_context_on_knowledge_bound_trace(self):
        report = self.verifier.verify(
            request=self.request,
            authority=self.result.authority_decision,
            snapshot=self.result.policy_snapshot,
            events=self.result.events,
        )
        self.assertEqual(report.status, "TAMPER_DETECTED")
        self.assertEqual(report.reason_code, "TRACE_KNOWLEDGE_CONTEXT_EXPECTATION_REQUIRED")

    def test_changed_context_package_hash_breaks_replay(self):
        wrong = replace(self.trace_context, context_package_hash="0" * 64)
        report = self.verifier.verify(
            request=self.request,
            authority=self.result.authority_decision,
            snapshot=self.result.policy_snapshot,
            events=self.result.events,
            knowledge_context=wrong,
        )
        self.assertEqual(report.status, "TAMPER_DETECTED")
        self.assertEqual(report.reason_code, "TRACE_MANIFEST_EVENT_OR_KNOWLEDGE_CONTEXT_MISMATCH")

    def test_changed_snapshot_digest_breaks_replay(self):
        wrong = replace(self.trace_context, knowledge_snapshot_digests=("0" * 64,))
        report = self.verifier.verify(
            request=self.request,
            authority=self.result.authority_decision,
            snapshot=self.result.policy_snapshot,
            events=self.result.events,
            knowledge_context=wrong,
        )
        self.assertEqual(report.status, "TAMPER_DETECTED")

    def test_run_binder_rejects_context_from_another_run(self):
        wrong_context = replace(self.context, run_ref="RUN-OTHER")
        with self.assertRaisesRegex(ValueError, "RUN_CONTEXT_PACKAGE_MISMATCH"):
            RunKnowledgeBinder().bind(
                run_id=self.request.run_id,
                role_ref="ROLE-SECURITY",
                assignment_ref=self.assignment_ref,
                context_package=wrong_context,
                imported_slices=(self.imported,),
            )

    def test_this_is_transport_replay_not_verified_requirement_reasoning(self):
        self.assertEqual(self.imported.objects[0].knowledge_state, "SOURCE_VERIFIED")
        self.assertNotEqual(self.imported.objects[0].knowledge_state, "VERIFIED")
        self.assertEqual(self.result.output, 20)


if __name__ == "__main__":
    unittest.main()
