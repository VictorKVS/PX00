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
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.recorder = AppendOnlyEventRecorder(self.root)
        self.kernel = SyntheticGovernedKernel()

    def tearDown(self):
        self.tmp.cleanup()

    def _events(self):
        request = self.kernel.prepare_request(3, 7)
        result = self.kernel.execute_request(request, allow=True)
        return result.events

    def test_record_all_builds_verified_chain(self):
        events = self._events()
        manifest = self.recorder.record_all(events)
        self.assertEqual(manifest.event_count, len(events))
        self.assertEqual(manifest.event_refs, tuple(e.event_id for e in events))
        self.assertEqual(len(manifest.event_hashes), len(events))
        self.assertEqual(manifest.chain_head_hash, manifest.event_hashes[-1])
        self.assertEqual(manifest.integrity_algorithm, "sha256_chain_v1")

    def test_event_id_reuse_is_rejected(self):
        event = self._events()[0]
        self.recorder.append(event)
        with self.assertRaisesRegex(RecorderIntegrityError, "EVENT_ID_REUSE"):
            self.recorder.append(event)

    def test_trace_context_mismatch_is_rejected(self):
        events = self._events()
        self.recorder.append(events[0])
        bad = replace(events[1], run_id="RUN-other")
        with self.assertRaisesRegex(RecorderIntegrityError, "TRACE_CONTEXT_MISMATCH"):
            self.recorder.append(bad)

    def test_payload_tampering_is_detected(self):
        events = self._events(); self.recorder.record_all(events)
        path = self.root / f"{events[0].trace_id}.jsonl"
        rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()]
        rows[0]["payload"]["detail"] = "tampered"
        path.write_text("\n".join(json.dumps(x, sort_keys=True, separators=(",", ":")) for x in rows) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(RecorderIntegrityError, "EVENT_HASH_MISMATCH"):
            self.recorder.verify(events[0].trace_id)

    def test_event_deletion_is_detected_by_previous_hash(self):
        events = self._events(); self.recorder.record_all(events)
        path = self.root / f"{events[0].trace_id}.jsonl"
        rows = path.read_text(encoding="utf-8").splitlines()
        if len(rows) < 2:
            self.skipTest("need at least two events")
        path.write_text(rows[-1] + "\n", encoding="utf-8")
        with self.assertRaisesRegex(RecorderIntegrityError, "PREVIOUS_HASH_MISMATCH"):
            self.recorder.verify(events[0].trace_id)

    def test_event_reordering_is_detected(self):
        events = self._events(); self.recorder.record_all(events)
        path = self.root / f"{events[0].trace_id}.jsonl"
        rows = path.read_text(encoding="utf-8").splitlines()
        if len(rows) < 2:
            self.skipTest("need at least two events")
        path.write_text("\n".join(reversed(rows)) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(RecorderIntegrityError, "PREVIOUS_HASH_MISMATCH"):
            self.recorder.verify(events[0].trace_id)


if __name__ == "__main__":
    unittest.main()
