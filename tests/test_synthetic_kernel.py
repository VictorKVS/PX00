from __future__ import annotations

import unittest
from dataclasses import replace

from px00.kernel import SyntheticGovernedKernel
from px00.tools import BoundaryViolation, DeterministicMathTool


class SyntheticGovernedKernelTests(unittest.TestCase):
    def setUp(self):
        self.kernel = SyntheticGovernedKernel()

    def test_valid_multiply_completes(self):
        request = self.kernel.prepare_request(10, 2)
        result = self.kernel.execute_request(request, allow=True)
        self.assertEqual(result.run_state, "COMPLETED")
        self.assertEqual(result.output, 20)
        self.assertEqual(result.authority_decision.result, "ALLOW")
        self.assertTrue(result.authority_decision.policy_refs)
        self.assertEqual(result.policy_snapshot.run_id, request.run_id)
        self.assertEqual(result.authority_decision.policy_snapshot_ref, result.policy_snapshot.snapshot_id)
        self.assertEqual(result.authority_decision.policy_snapshot_hash, result.policy_snapshot.snapshot_hash)
        self.assertIsNotNone(result.capability_grant)
        self.assertEqual(result.capability_grant.status, "CONSUMED")
        self.assertTrue(any(event.event_type == "TOOL_BOUNDARY" for event in result.events))

    def test_missing_authority_denies_without_grant(self):
        request = self.kernel.prepare_request(10, 2)
        result = self.kernel.execute_request(request, allow=False)
        self.assertEqual(result.run_state, "DENIED")
        self.assertIsNone(result.capability_grant)
        self.assertIsNone(result.output)
        self.assertEqual(result.blocking_reason, "AUTHORITY_ABSENT")

    def test_capability_mismatch_is_denied_before_grant(self):
        request = replace(self.kernel.prepare_request(10, 2), capability="shell.execute")
        result = self.kernel.execute_request(request, allow=True)
        self.assertEqual(result.run_state, "DENIED")
        self.assertEqual(result.blocking_reason, "CAPABILITY_NOT_ALLOWED")

    def test_side_effect_overflow_is_denied_before_grant(self):
        request = replace(self.kernel.prepare_request(10, 2), side_effect_class="S3")
        result = self.kernel.execute_request(request, allow=True)
        self.assertEqual(result.run_state, "DENIED")
        self.assertEqual(result.blocking_reason, "SIDE_EFFECT_CEILING_EXCEEDED")

    def test_privileged_adapter_hint_does_not_change_execution(self):
        request = self.kernel.prepare_request(6, 7, requested_adapter_hint="shell-root")
        result = self.kernel.execute_request(request, allow=True)
        self.assertEqual(result.run_state, "COMPLETED")
        self.assertEqual(result.output, 42)

    def test_executor_payload_cannot_invent_control_transition(self):
        request = replace(
            self.kernel.prepare_request(3, 4),
            payload={"left": 3, "right": 4, "next_step": "DELETE_DATABASE", "authority": "ADMIN"},
        )
        result = self.kernel.execute_request(request, allow=True)
        self.assertEqual(result.run_state, "COMPLETED")
        self.assertEqual(result.output, 12)
        self.assertEqual(result.authority_decision.effective_autonomy, "A1")

    def test_snapshot_from_another_run_is_denied(self):
        request_a = self.kernel.prepare_request(2, 3)
        request_b = self.kernel.prepare_request(4, 5)
        snapshot_b = self.kernel.create_policy_snapshot(request_b)
        result = self.kernel.execute_request(request_a, allow=True, policy_snapshot=snapshot_b)
        self.assertEqual(result.run_state, "DENIED")
        self.assertEqual(result.blocking_reason, "POLICY_SNAPSHOT_RUN_MISMATCH")
        self.assertIsNone(result.capability_grant)

    def test_grant_rejects_policy_snapshot_ref_mismatch(self):
        request = self.kernel.prepare_request(2, 5)
        snapshot = self.kernel.create_policy_snapshot(request)
        authority = self.kernel.evaluate_authority(request, allow=True, policy_snapshot=snapshot)
        tampered = replace(authority, policy_snapshot_ref="POLSNAP-tampered")
        self.assertIsNone(self.kernel.issue_grant(request, tampered, snapshot))

    def test_grant_rejects_policy_snapshot_hash_mismatch(self):
        request = self.kernel.prepare_request(2, 5)
        snapshot = self.kernel.create_policy_snapshot(request)
        authority = self.kernel.evaluate_authority(request, allow=True, policy_snapshot=snapshot)
        tampered = replace(authority, policy_snapshot_hash="0" * 64)
        self.assertIsNone(self.kernel.issue_grant(request, tampered, snapshot))


class DeterministicToolBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.kernel = SyntheticGovernedKernel()
        self.tool = DeterministicMathTool()

    def _active_pair(self):
        request = self.kernel.prepare_request(2, 5)
        authority = self.kernel.evaluate_authority(request, allow=True)
        grant = self.kernel.issue_grant(request, authority)
        self.assertIsNotNone(grant)
        return request, grant

    def test_target_mismatch_blocks(self):
        request, grant = self._active_pair()
        bad = replace(grant, target_scope="synthetic://other")
        with self.assertRaisesRegex(BoundaryViolation, "GRANT_TARGET_MISMATCH"):
            self.tool.execute(request, bad)

    def test_consumed_grant_blocks_replay(self):
        request, grant = self._active_pair()
        consumed = replace(grant, status="CONSUMED")
        with self.assertRaisesRegex(BoundaryViolation, "GRANT_NOT_ACTIVE"):
            self.tool.execute(request, consumed)

    def test_data_classification_overflow_blocks(self):
        request, grant = self._active_pair()
        secret_request = replace(request, classification="SECRET")
        with self.assertRaisesRegex(BoundaryViolation, "DATA_CLASSIFICATION_CEILING_EXCEEDED"):
            self.tool.execute(secret_request, grant)

    def test_request_grant_identity_mismatch_blocks(self):
        request, grant = self._active_pair()
        bad = replace(grant, action_request_id="ACTREQ-other")
        with self.assertRaisesRegex(BoundaryViolation, "GRANT_REQUEST_MISMATCH"):
            self.tool.execute(request, bad)


if __name__ == "__main__":
    unittest.main()
