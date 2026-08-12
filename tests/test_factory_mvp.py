import unittest
from px00.factory_mvp import AgentRdFactoryMvp, STAGES, STAGE_ARTIFACT_TYPES


class FactoryMvpTests(unittest.TestCase):
    def setUp(self):
        self.mvp = AgentRdFactoryMvp()
        self.seq = 0

    def create(self, **kw):
        return self.mvp.create_run(
            "MVP-RUN-1",
            "PROBLEM-1",
            "ASSIGN-PRODUCER",
            "ASSIGN-VERIFIER",
            **kw,
        )

    def producer_for_stage(self, stage):
        if stage == "VERIFY_AND_VALIDATE":
            return "ASSIGN-VERIFIER"
        if stage == "SOCRATES_CHALLENGE":
            return "ASSIGN-SOCRATES"
        return "ASSIGN-PRODUCER"

    def payload_for_stage(self, stage, outcome="PASS"):
        payload = {"stage": stage, "outcome": outcome}
        if stage in {"SECURITY_PRECHECK", "VERIFY_AND_VALIDATE"}:
            payload["verdict"] = outcome
        elif stage == "SOCRATES_CHALLENGE":
            payload["verdict"] = "PASS" if outcome == "PASS" else "FAIL"
        return payload

    def submit_current(self, outcome="PASS"):
        run = self.mvp.runs["MVP-RUN-1"]
        self.seq += 1
        artifact_id = f"ART-{self.seq:02d}"
        self.mvp.submit_artifact(
            run.run_id,
            artifact_id,
            STAGE_ARTIFACT_TYPES[run.stage],
            self.payload_for_stage(run.stage, outcome),
            self.producer_for_stage(run.stage),
        )
        return artifact_id

    def pass_current(self):
        run = self.mvp.runs["MVP-RUN-1"]
        self.submit_current()
        return self.mvp.advance(run.run_id, run.stage)

    def advance_until(self, target):
        while self.mvp.runs["MVP-RUN-1"].stage != target:
            self.pass_current()

    def complete(self):
        for _ in STAGES:
            self.pass_current()

    def test_independent_verifier_required_at_creation(self):
        with self.assertRaisesRegex(ValueError, "INDEPENDENCE_VIOLATION"):
            self.mvp.create_run("R", "P", "A", "A")

    def test_stage_order_is_strict(self):
        self.create()
        with self.assertRaisesRegex(ValueError, "STAGE_ORDER_VIOLATION"):
            self.mvp.advance("MVP-RUN-1", "RESEARCH_EVIDENCE")

    def test_stage_cannot_pass_without_artifact(self):
        self.create()
        with self.assertRaisesRegex(ValueError, "ARTIFACT_REQUIRED"):
            self.mvp.advance("MVP-RUN-1", "QUALIFY_PROBLEM")

    def test_wrong_artifact_type_is_rejected(self):
        self.create()
        with self.assertRaisesRegex(ValueError, "ARTIFACT_TYPE_MISMATCH"):
            self.mvp.submit_artifact(
                "MVP-RUN-1", "ART-X", "DELIVERY_PACKAGE", {}, "ASSIGN-PRODUCER"
            )

    def test_artifact_lineage_is_strict(self):
        self.create()
        self.pass_current()
        with self.assertRaisesRegex(ValueError, "ARTIFACT_LINEAGE_MISMATCH"):
            self.mvp.submit_artifact(
                "MVP-RUN-1",
                "ART-X",
                STAGE_ARTIFACT_TYPES["RESEARCH_EVIDENCE"],
                {},
                "ASSIGN-PRODUCER",
                input_artifact_refs=("WRONG-PARENT",),
            )

    def test_artifact_ids_are_append_only(self):
        self.create()
        self.mvp.submit_artifact(
            "MVP-RUN-1", "ART-X", "PROBLEM_BRIEF", {}, "ASSIGN-PRODUCER"
        )
        with self.assertRaisesRegex(ValueError, "ARTIFACT_ID_REUSE"):
            self.mvp.submit_artifact(
                "MVP-RUN-1", "ART-X", "PROBLEM_BRIEF", {}, "ASSIGN-PRODUCER"
            )

    def test_verification_artifact_requires_pinned_verifier(self):
        self.create()
        self.advance_until("VERIFY_AND_VALIDATE")
        with self.assertRaisesRegex(ValueError, "VERIFIER_ASSIGNMENT_REQUIRED"):
            self.mvp.submit_artifact(
                "MVP-RUN-1",
                "ART-X",
                "VERIFICATION_REPORT",
                {"verdict": "PASS"},
                "ASSIGN-PRODUCER",
            )

    def test_socrates_artifact_requires_independence(self):
        self.create()
        self.advance_until("SOCRATES_CHALLENGE")
        with self.assertRaisesRegex(ValueError, "SOCRATES_INDEPENDENCE_VIOLATION"):
            self.mvp.submit_artifact(
                "MVP-RUN-1",
                "ART-X",
                "SOCRATES_REVIEW",
                {"verdict": "PASS"},
                "ASSIGN-PRODUCER",
            )

    def test_gated_artifact_verdict_must_match_runtime_outcome(self):
        self.create()
        self.advance_until("SECURITY_PRECHECK")
        self.mvp.submit_artifact(
            "MVP-RUN-1",
            "ART-X",
            "SECURITY_PRECHECK_REPORT",
            {"verdict": "FAIL"},
            "ASSIGN-PRODUCER",
        )
        with self.assertRaisesRegex(ValueError, "ARTIFACT_OUTCOME_MISMATCH"):
            self.mvp.advance("MVP-RUN-1", "SECURITY_PRECHECK", outcome="PASS")

    def test_untrusted_input_blocks_prototype_until_trust_gate(self):
        self.create(untrusted_input_present=True)
        self.advance_until("IMPLEMENT_BOUNDED_PROTOTYPE")
        self.submit_current()
        with self.assertRaisesRegex(ValueError, "UNTRUSTED_INPUT_BLOCKED"):
            self.mvp.advance("MVP-RUN-1", "IMPLEMENT_BOUNDED_PROTOTYPE")
        self.mvp.pass_trust_gate("MVP-RUN-1")
        self.mvp.advance("MVP-RUN-1", "IMPLEMENT_BOUNDED_PROTOTYPE")

    def test_security_precheck_blocks_prototype_on_failure(self):
        self.create()
        self.advance_until("SECURITY_PRECHECK")
        self.submit_current(outcome="FAIL")
        self.mvp.advance("MVP-RUN-1", "SECURITY_PRECHECK", outcome="FAIL")
        self.assertEqual(self.mvp.runs["MVP-RUN-1"].stage, "SECURITY_PRECHECK")
        with self.assertRaisesRegex(ValueError, "FRESH_STAGE_ARTIFACT_REQUIRED"):
            self.mvp.advance("MVP-RUN-1", "SECURITY_PRECHECK")

    def test_rework_requires_failed_stage(self):
        self.create()
        with self.assertRaisesRegex(ValueError, "REWORK_REQUIRES_FAILED_STAGE"):
            self.mvp.request_rework("MVP-RUN-1", "QUALIFY_PROBLEM", "FINDING-1")

    def test_failed_verification_can_rework_to_implementation_with_append_only_lineage(self):
        self.create()
        self.advance_until("VERIFY_AND_VALIDATE")
        failed_ref = self.submit_current(outcome="FAIL")
        self.mvp.advance("MVP-RUN-1", "VERIFY_AND_VALIDATE", outcome="FAIL")

        failed_run = self.mvp.runs["MVP-RUN-1"]
        self.assertEqual(failed_run.last_outcome, "FAIL")
        self.assertFalse(failed_run.verification_passed)
        self.assertTrue(failed_run.security_precheck_passed)

        self.mvp.request_rework(
            "MVP-RUN-1", "IMPLEMENT_BOUNDED_PROTOTYPE", "VERIFY-FINDING-1"
        )
        rework_run = self.mvp.runs["MVP-RUN-1"]
        self.assertEqual(rework_run.stage, "IMPLEMENT_BOUNDED_PROTOTYPE")
        self.assertEqual(rework_run.rework_count, 1)
        self.assertTrue(rework_run.security_precheck_passed)
        self.assertFalse(rework_run.verification_passed)
        self.assertIn(
            "REWORK:VERIFY_AND_VALIDATE->IMPLEMENT_BOUNDED_PROTOTYPE:VERIFY-FINDING-1",
            rework_run.trace,
        )

        rework_ref = self.submit_current()
        self.assertEqual(self.mvp.artifacts[rework_ref].input_artifact_refs, (failed_ref,))
        self.mvp.advance("MVP-RUN-1", "IMPLEMENT_BOUNDED_PROTOTYPE")
        self.pass_current()
        self.assertTrue(self.mvp.runs["MVP-RUN-1"].verification_passed)

    def test_rework_target_must_be_earlier_and_reasoned(self):
        self.create()
        self.advance_until("VERIFY_AND_VALIDATE")
        self.submit_current(outcome="FAIL")
        self.mvp.advance("MVP-RUN-1", "VERIFY_AND_VALIDATE", outcome="FAIL")
        with self.assertRaisesRegex(ValueError, "REWORK_TARGET_MUST_BE_EARLIER"):
            self.mvp.request_rework("MVP-RUN-1", "SOCRATES_CHALLENGE", "FINDING-1")
        with self.assertRaisesRegex(ValueError, "REWORK_REASON_REQUIRED"):
            self.mvp.request_rework("MVP-RUN-1", "IMPLEMENT_BOUNDED_PROTOTYPE", "")

    def test_happy_path_reaches_governed_delivery_with_artifact_chain(self):
        self.create(untrusted_input_present=True)
        self.mvp.pass_trust_gate("MVP-RUN-1")
        self.complete()
        run = self.mvp.runs["MVP-RUN-1"]
        self.assertTrue(run.verification_passed)
        self.assertTrue(run.socrates_passed)
        self.assertTrue(run.delivered)
        self.assertEqual(len(run.artifact_refs), len(STAGES))
        for ref in run.artifact_refs:
            self.assertTrue(self.mvp.artifacts[ref].verify_digest())
        self.assertIn("GOVERNED_DELIVERY:PASS", run.trace)

    def test_successful_delivery_is_terminal(self):
        self.create()
        self.complete()
        with self.assertRaisesRegex(ValueError, "RUN_TERMINAL"):
            self.mvp.advance("MVP-RUN-1", "GOVERNED_DELIVERY")
        with self.assertRaisesRegex(ValueError, "RUN_TERMINAL"):
            self.mvp.pass_trust_gate("MVP-RUN-1")

    def test_run_ids_are_append_only(self):
        self.create()
        with self.assertRaisesRegex(ValueError, "RUN_ID_REUSE"):
            self.create()


if __name__ == "__main__":
    unittest.main()
