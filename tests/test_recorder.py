from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from px00.kernel import SyntheticGovernedKernel
from px00.recorder import AppendOnlyEventRecorder, RecorderIntegrityError


class AppendOnlyRecorderTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name); self.recorder=AppendOnlyEventRecorder(self.root); self.kernel=SyntheticGovernedKernel()
    def tearDown(self): self.tmp.cleanup()
    def _events(self):
        request=self.kernel.prepare_request(3,7); return self.kernel.execute_request(request,allow=True).events

    def test_record_all_builds_verified_chain(self):
        events=self._events(); manifest=self.recorder.record_all(events)
        self.assertEqual(manifest.event_count,len(events)); self.assertEqual(manifest.event_refs,tuple(e.event_id for e in events))
        self.assertEqual(manifest.chain_head_hash,manifest.event_hashes[-1]); self.assertEqual(manifest.integrity_algorithm,"sha256_chain_v1")

    def test_persisted_manifest_verifies_against_live_chain(self):
        events=self._events(); self.recorder.record_all(events); persisted=self.recorder.persist_manifest(events[0].trace_id)
        verified=self.recorder.verify_persisted_manifest(events[0].trace_id)
        self.assertEqual(verified.manifest_hash,persisted.manifest_hash); self.assertEqual(verified.manifest.event_count,len(events))

    def test_manifest_tampering_is_detected(self):
        events=self._events(); self.recorder.record_all(events); self.recorder.persist_manifest(events[0].trace_id)
        path=self.root/f"{events[0].trace_id}.manifest.json"; raw=json.loads(path.read_text(encoding="utf-8")); raw["manifest"]["event_count"]+=1
        path.write_text(json.dumps(raw,sort_keys=True,separators=(",", ":"))+"\n",encoding="utf-8")
        with self.assertRaisesRegex(RecorderIntegrityError,"TRACE_MANIFEST_HASH_MISMATCH"): self.recorder.verify_persisted_manifest(events[0].trace_id)

    def test_chain_change_after_manifest_is_detected(self):
        events=self._events(); self.recorder.record_all(events); self.recorder.persist_manifest(events[0].trace_id)
        path=self.root/f"{events[0].trace_id}.jsonl"; rows=path.read_text(encoding="utf-8").splitlines(); path.write_text(rows[0]+"\n",encoding="utf-8")
        with self.assertRaises(RecorderIntegrityError): self.recorder.verify_persisted_manifest(events[0].trace_id)

    def test_event_id_reuse_is_rejected(self):
        event=self._events()[0]; self.recorder.append(event)
        with self.assertRaisesRegex(RecorderIntegrityError,"EVENT_ID_REUSE"): self.recorder.append(event)

    def test_trace_context_mismatch_is_rejected(self):
        events=self._events(); self.recorder.append(events[0]); bad=replace(events[1],run_id="RUN-other")
        with self.assertRaisesRegex(RecorderIntegrityError,"TRACE_CONTEXT_MISMATCH"): self.recorder.append(bad)

    def test_payload_tampering_is_detected(self):
        events=self._events(); self.recorder.record_all(events); path=self.root/f"{events[0].trace_id}.jsonl"
        rows=[json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()]; rows[0]["payload"]["detail"]="tampered"
        path.write_text("\n".join(json.dumps(x,sort_keys=True,separators=(",", ":")) for x in rows)+"\n",encoding="utf-8")
        with self.assertRaisesRegex(RecorderIntegrityError,"EVENT_HASH_MISMATCH"): self.recorder.verify(events[0].trace_id)

    def test_event_deletion_is_detected_by_previous_hash(self):
        events=self._events(); self.recorder.record_all(events); path=self.root/f"{events[0].trace_id}.jsonl"; rows=path.read_text(encoding="utf-8").splitlines()
        path.write_text(rows[-1]+"\n",encoding="utf-8")
        with self.assertRaisesRegex(RecorderIntegrityError,"PREVIOUS_HASH_MISMATCH"): self.recorder.verify(events[0].trace_id)

    def test_event_reordering_is_detected(self):
        events=self._events(); self.recorder.record_all(events); path=self.root/f"{events[0].trace_id}.jsonl"; rows=path.read_text(encoding="utf-8").splitlines()
        path.write_text("\n".join(reversed(rows))+"\n",encoding="utf-8")
        with self.assertRaisesRegex(RecorderIntegrityError,"PREVIOUS_HASH_MISMATCH"): self.recorder.verify(events[0].trace_id)

if __name__=="__main__": unittest.main()
