import unittest

from px00.epistemics import ClaimEvidenceEvaluator, EvidenceItem


class ClaimEvidenceEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.evaluator = ClaimEvidenceEvaluator()

    def ev(self, eid, source, group, stance="SUPPORT", strength=0.9):
        return EvidenceItem(eid, source, group, stance, strength, strength, strength, strength)

    def test_no_evidence_is_unsupported(self):
        result = self.evaluator.evaluate("CLM-1", ())
        self.assertEqual(result.status, "UNSUPPORTED")

    def test_one_independence_group_is_single_source_even_with_duplicates(self):
        result = self.evaluator.evaluate("CLM-1", (self.ev("E1", "S1", "G1"), self.ev("E2", "S2", "G1")))
        self.assertEqual(result.status, "SINGLE_SOURCE")
        self.assertLess(result.independence, 1.0)

    def test_two_independent_support_groups_are_corroborated(self):
        result = self.evaluator.evaluate("CLM-1", (self.ev("E1", "S1", "G1"), self.ev("E2", "S2", "G2")))
        self.assertEqual(result.status, "CORROBORATED")
        self.assertEqual(result.corroboration, 1.0)

    def test_strong_support_and_counterevidence_are_disputed(self):
        result = self.evaluator.evaluate("CLM-1", (self.ev("E1", "S1", "G1"), self.ev("E2", "S2", "G2", "CONTRADICT")))
        self.assertEqual(result.status, "DISPUTED")
        self.assertGreater(result.support_score, 0)
        self.assertGreater(result.contradiction_score, 0)

    def test_strong_counterevidence_without_support_is_refuted(self):
        result = self.evaluator.evaluate("CLM-1", (self.ev("E1", "S1", "G1", "CONTRADICT", 0.9),))
        self.assertEqual(result.status, "REFUTED")

    def test_unknown_stance_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "UNKNOWN_EVIDENCE_STANCE"):
            self.evaluator.evaluate("CLM-1", (self.ev("E1", "S1", "G1", "MAYBE"),))


if __name__ == "__main__":
    unittest.main()
