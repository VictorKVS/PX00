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

    def submit_current(self, outcome="PASS"):
        run = self.mvp.runs["MVP-RUN-1"]
        self.seq += 1
        artifact_id = f"ART-{self.seq:02d}"
        self.mvp.submit_artifact(
            run.run_id,
            artifact_id,
            STAGE_ARTIFACT_TYPES[run.stage],
            {"stage": run.stage, "outcome": outcome},
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
                {},
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
                {},
                "ASSIGN-PRODUCER",
            )

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
