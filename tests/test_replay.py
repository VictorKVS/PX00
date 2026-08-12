from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from px00.kernel import SyntheticGovernedKernel
from px00.recorder import AppendOnlyEventRecorder
from px00.replay import ReadOnlyReplayVerifier


class ReplayVerifierTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        self.kernel=SyntheticGovernedKernel(); self.recorder=AppendOnlyEventRecorder(self.root); self.verifier=ReadOnlyReplayVerifier(self.recorder)
        self.request=self.kernel.prepare_request(8,9); self.result=self.kernel.execute_request(self.request,allow=True)
        self.recorder.record_all(self.result.events); self.recorder.persist_manifest(self.request.trace_id)

    def tearDown(self): self.tmp.cleanup()

    def test_verified_record(self):
        report=self.verifier.verify(request=self.request,authority=self.result.authority_decision,snapshot=self.result.policy_snapshot,events=self.result.events)
        self.assertEqual(report.status,"VERIFIED_RECORD"); self.assertEqual(report.verified_event_count,len(self.result.events))
        self.assertEqual(report.reason_code,"GOVERNED_LINEAGE_VERIFIED")

    def test_no_events_is_insufficient_evidence(self):
        report=self.verifier.verify(request=self.request,authority=self.result.authority_decision,snapshot=self.result.policy_snapshot,events=())
        self.assertEqual(report.status,"INSUFFICIENT_EVIDENCE")

    def test_authority_policy_hash_mismatch_is_policy_mismatch(self):
        bad=replace(self.result.authority_decision,policy_snapshot_hash="0"*64)
        report=self.verifier.verify(request=self.request,authority=bad,snapshot=self.result.policy_snapshot,events=self.result.events)
        self.assertEqual(report.status,"POLICY_MISMATCH")

    def test_event_authority_mismatch_breaks_lineage(self):
        bad_events=list(self.result.events); bad_events[-1]=replace(bad_events[-1],authority_decision_ref="AUTH-other")
        report=self.verifier.verify(request=self.request,authority=self.result.authority_decision,snapshot=self.result.policy_snapshot,events=bad_events)
        self.assertEqual(report.status,"BROKEN_LINEAGE")

    def test_manifest_tampering_is_detected_without_execution(self):
        path=self.root/f"{self.request.trace_id}.manifest.json"; raw=json.loads(path.read_text(encoding="utf-8")); raw["manifest_hash"]="0"*64
        path.write_text(json.dumps(raw,sort_keys=True,separators=(",", ":"))+"\n",encoding="utf-8")
        report=self.verifier.verify(request=self.request,authority=self.result.authority_decision,snapshot=self.result.policy_snapshot,events=self.result.events)
        self.assertEqual(report.status,"TAMPER_DETECTED")

    def test_replay_has_no_tool_boundary_dependency(self):
        self.assertFalse(hasattr(self.verifier,"_tool"))

if __name__=="__main__": unittest.main()
