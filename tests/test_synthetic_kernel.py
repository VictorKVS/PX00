from __future__ import annotations

import unittest
from dataclasses import replace

from px00.kernel import SyntheticGovernedKernel
from px00.tools import BoundaryViolation, DeterministicMathTool


class SyntheticGovernedKernelTests(unittest.TestCase):
    def setUp(self): self.kernel = SyntheticGovernedKernel()

    def test_valid_multiply_completes(self):
        request = self.kernel.prepare_request(10, 2); result = self.kernel.execute_request(request, allow=True)
        self.assertEqual(result.run_state, "COMPLETED"); self.assertEqual(result.output, 20)
        self.assertEqual(result.authority_decision.result, "ALLOW"); self.assertTrue(result.authority_decision.policy_refs)
        self.assertEqual(result.policy_snapshot.run_id, request.run_id)
        self.assertEqual(result.authority_decision.policy_snapshot_ref, result.policy_snapshot.snapshot_id)
        self.assertEqual(result.authority_decision.policy_snapshot_hash, result.policy_snapshot.snapshot_hash)
        self.assertIsNotNone(result.capability_grant); self.assertEqual(result.capability_grant.status, "CONSUMED")
        tool_event = next(e for e in result.events if e.event_type == "TOOL_BOUNDARY")
        self.assertEqual(tool_event.run_id, request.run_id); self.assertEqual(tool_event.task_id, request.task_id)
        self.assertEqual(tool_event.action_request_ref, request.action_request_id)
        self.assertEqual(tool_event.authority_decision_ref, result.authority_decision.decision_id)
        self.assertEqual(tool_event.policy_snapshot_ref, result.policy_snapshot.snapshot_id)
        self.assertEqual(tool_event.policy_snapshot_hash, result.policy_snapshot.snapshot_hash)
        self.assertIsNotNone(tool_event.capability_grant_ref)

    def test_missing_authority_denies_without_grant(self):
        request = self.kernel.prepare_request(10, 2); result = self.kernel.execute_request(request, allow=False)
        self.assertEqual(result.run_state, "DENIED"); self.assertIsNone(result.capability_grant); self.assertIsNone(result.output)
        self.assertEqual(result.blocking_reason, "AUTHORITY_ABSENT")
        self.assertEqual(result.events[0].authority_decision_ref, result.authority_decision.decision_id)

    def test_capability_mismatch_is_denied_before_grant(self):
        result = self.kernel.execute_request(replace(self.kernel.prepare_request(10, 2), capability="shell.execute"), allow=True)
        self.assertEqual(result.run_state, "DENIED"); self.assertEqual(result.blocking_reason, "CAPABILITY_NOT_ALLOWED")

    def test_side_effect_overflow_is_denied_before_grant(self):
        result = self.kernel.execute_request(replace(self.kernel.prepare_request(10, 2), side_effect_class="S3"), allow=True)
        self.assertEqual(result.run_state, "DENIED"); self.assertEqual(result.blocking_reason, "SIDE_EFFECT_CEILING_EXCEEDED")

    def test_privileged_adapter_hint_does_not_change_execution(self):
        result = self.kernel.execute_request(self.kernel.prepare_request(6, 7, requested_adapter_hint="shell-root"), allow=True)
        self.assertEqual(result.run_state, "COMPLETED"); self.assertEqual(result.output, 42)

    def test_executor_payload_cannot_invent_control_transition(self):
        request = replace(self.kernel.prepare_request(3, 4), payload={"left":3,"right":4,"next_step":"DELETE_DATABASE","authority":"ADMIN"})
        result = self.kernel.execute_request(request, allow=True)
        self.assertEqual(result.run_state, "COMPLETED"); self.assertEqual(result.output, 12)
        self.assertEqual(result.authority_decision.effective_autonomy, "A1")

    def test_snapshot_from_another_run_is_denied(self):
        a=self.kernel.prepare_request(2,3); b=self.kernel.prepare_request(4,5); sb=self.kernel.create_policy_snapshot(b)
        result=self.kernel.execute_request(a,allow=True,policy_snapshot=sb)
        self.assertEqual(result.run_state,"DENIED"); self.assertEqual(result.blocking_reason,"POLICY_SNAPSHOT_RUN_MISMATCH")
        self.assertIsNone(result.capability_grant)

    def test_grant_rejects_policy_snapshot_ref_mismatch(self):
        r=self.kernel.prepare_request(2,5); s=self.kernel.create_policy_snapshot(r); a=self.kernel.evaluate_authority(r,allow=True,policy_snapshot=s)
        self.assertIsNone(self.kernel.issue_grant(r,replace(a,policy_snapshot_ref="POLSNAP-tampered"),s))

    def test_grant_rejects_policy_snapshot_hash_mismatch(self):
        r=self.kernel.prepare_request(2,5); s=self.kernel.create_policy_snapshot(r); a=self.kernel.evaluate_authority(r,allow=True,policy_snapshot=s)
        self.assertIsNone(self.kernel.issue_grant(r,replace(a,policy_snapshot_hash="0"*64),s))


class DeterministicToolBoundaryTests(unittest.TestCase):
    def setUp(self): self.kernel=SyntheticGovernedKernel(); self.tool=DeterministicMathTool()
    def _active_pair(self):
        r=self.kernel.prepare_request(2,5); a=self.kernel.evaluate_authority(r,allow=True); g=self.kernel.issue_grant(r,a); self.assertIsNotNone(g); return r,g
    def test_target_mismatch_blocks(self):
        r,g=self._active_pair()
        with self.assertRaisesRegex(BoundaryViolation,"GRANT_TARGET_MISMATCH"): self.tool.execute(r,replace(g,target_scope="synthetic://other"))
    def test_consumed_grant_blocks_replay(self):
        r,g=self._active_pair()
        with self.assertRaisesRegex(BoundaryViolation,"GRANT_NOT_ACTIVE"): self.tool.execute(r,replace(g,status="CONSUMED"))
    def test_data_classification_overflow_blocks(self):
        r,g=self._active_pair()
        with self.assertRaisesRegex(BoundaryViolation,"DATA_CLASSIFICATION_CEILING_EXCEEDED"): self.tool.execute(replace(r,classification="SECRET"),g)
    def test_request_grant_identity_mismatch_blocks(self):
        r,g=self._active_pair()
        with self.assertRaisesRegex(BoundaryViolation,"GRANT_REQUEST_MISMATCH"): self.tool.execute(r,replace(g,action_request_id="ACTREQ-other"))

if __name__ == "__main__": unittest.main()
