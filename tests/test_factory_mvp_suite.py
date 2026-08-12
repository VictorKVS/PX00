import unittest

from px00.factory_mvp_suite import (
    normalize_tags_v1,
    run_functional_scenario_suite,
    run_security_block_case,
    run_verification_rework_case,
)


class FactoryMvpScenarioSuiteTests(unittest.TestCase):
    def test_suite_covers_delivery_rework_and_security_block(self):
        outcomes, patterns = run_functional_scenario_suite()
        status_by_id = {item.scenario_id: item.status for item in outcomes}
        self.assertEqual(status_by_id["SCENARIO-IDEMPOTENCY"], "DELIVERED")
        self.assertEqual(status_by_id["SCENARIO-VERIFICATION-REWORK"], "DELIVERED_AFTER_REWORK")
        self.assertEqual(status_by_id["SCENARIO-SECURITY-BLOCK"], "BLOCKED_BY_SECURITY")
        self.assertEqual({item.pattern_id for item in patterns}, {"FFB-FP-0001", "FFB-FP-0002"})

    def test_verification_failure_reworks_and_preserves_failed_evidence(self):
        mvp, run_id, pattern = run_verification_rework_case()
        run = mvp.runs[run_id]
        self.assertTrue(run.delivered)
        self.assertEqual(run.rework_count, 1)
        self.assertEqual(len(run.artifact_refs), 12)
        self.assertEqual(pattern.evidence_ref, "RW-ART-007")
        self.assertIn("RW-ART-007", run.consumed_artifact_refs)
        self.assertIn(
            "REWORK:VERIFY_AND_VALIDATE->IMPLEMENT_BOUNDED_PROTOTYPE:FFB-FP-0001",
            run.trace,
        )
        self.assertEqual(mvp.artifacts["RW-ART-008"].input_artifact_refs, ("RW-ART-007",))
        for ref in run.artifact_refs:
            self.assertTrue(mvp.artifacts[ref].verify_digest())

    def test_corrected_normalizer_is_canonical(self):
        self.assertEqual(
            normalize_tags_v1([" Security ", "AI", "security", " ai "]),
            ("ai", "security"),
        )

    def test_security_block_never_reaches_prototype(self):
        mvp, run_id, pattern = run_security_block_case()
        run = mvp.runs[run_id]
        self.assertFalse(run.delivered)
        self.assertEqual(run.stage, "SECURITY_PRECHECK")
        self.assertEqual(run.last_outcome, "FAIL")
        self.assertEqual(pattern.pattern_type, "SECURITY_SCOPE_BLOCK")
        artifact_types = {mvp.artifacts[ref].artifact_type for ref in run.artifact_refs}
        self.assertNotIn("PROTOTYPE_ARTIFACT", artifact_types)


if __name__ == "__main__":
    unittest.main()
