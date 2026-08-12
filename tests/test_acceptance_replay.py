from __future__ import annotations

import unittest

from px00.acceptance import ReplayGatedAcceptance
from px00.replay import ReplayReport


def report(status: str, reason: str = "R") -> ReplayReport:
    return ReplayReport(status=status, run_id="RUN-1", trace_id="TRACE-1", verified_event_count=2, reason_code=reason)


class ReplayGatedAcceptanceTests(unittest.TestCase):
    def setUp(self): self.gate=ReplayGatedAcceptance()

    def test_verified_replay_and_blocking_criteria_pass(self):
        result=self.gate.evaluate(replay_report=report("VERIFIED_RECORD"),blocking_criteria_passed=True)
        self.assertEqual(result.state,"PASS")

    def test_verified_replay_with_actions(self):
        result=self.gate.evaluate(replay_report=report("VERIFIED_RECORD"),blocking_criteria_passed=True,remaining_actions=("A1",))
        self.assertEqual(result.state,"PASS_WITH_ACTIONS")

    def test_verified_replay_does_not_override_failed_criteria(self):
        result=self.gate.evaluate(replay_report=report("VERIFIED_RECORD"),blocking_criteria_passed=False)
        self.assertEqual(result.state,"FAIL")

    def test_non_verified_replay_blocks_acceptance(self):
        for status in ("BROKEN_LINEAGE","TAMPER_DETECTED","POLICY_MISMATCH","INSUFFICIENT_EVIDENCE"):
            with self.subTest(status=status):
                result=self.gate.evaluate(replay_report=report(status),blocking_criteria_passed=True)
                self.assertEqual(result.state,"BLOCKED")

if __name__=="__main__": unittest.main()
