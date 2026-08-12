import unittest
from px00.factory_mvp import AgentRdFactoryMvp, STAGES


class FactoryMvpTests(unittest.TestCase):
    def setUp(self):
        self.mvp = AgentRdFactoryMvp()

    def create(self, **kw):
        return self.mvp.create_run(
            "MVP-RUN-1",
            "PROBLEM-1",
            "ASSIGN-PRODUCER",
            "ASSIGN-VERIFIER",
            **kw,
        )

    def advance_until(self, target):
        while self.mvp.runs["MVP-RUN-1"].stage != target:
            stage = self.mvp.runs["MVP-RUN-1"].stage
            self.mvp.advance("MVP-RUN-1", stage)

    def complete(self):
        for stage in STAGES:
            self.mvp.advance("MVP-RUN-1", stage)

    def test_independent_verifier_required_at_creation(self):
        with self.assertRaisesRegex(ValueError, "INDEPENDENCE_VIOLATION"):
            self.mvp.create_run("R", "P", "A", "A")

    def test_stage_order_is_strict(self):
        self.create()
        with self.assertRaisesRegex(ValueError, "STAGE_ORDER_VIOLATION"):
            self.mvp.advance("MVP-RUN-1", "RESEARCH_EVIDENCE")

    def test_untrusted_input_blocks_prototype_until_trust_gate(self):
        self.create(untrusted_input_present=True)
        self.advance_until("IMPLEMENT_BOUNDED_PROTOTYPE")
        with self.assertRaisesRegex(ValueError, "UNTRUSTED_INPUT_BLOCKED"):
            self.mvp.advance("MVP-RUN-1", "IMPLEMENT_BOUNDED_PROTOTYPE")
        self.mvp.pass_trust_gate("MVP-RUN-1")
        self.mvp.advance("MVP-RUN-1", "IMPLEMENT_BOUNDED_PROTOTYPE")

    def test_security_precheck_blocks_prototype_on_failure(self):
        self.create()
        for stage in STAGES[:4]:
            self.mvp.advance("MVP-RUN-1", stage)
        self.mvp.advance("MVP-RUN-1", "SECURITY_PRECHECK", outcome="FAIL")
        self.assertEqual(self.mvp.runs["MVP-RUN-1"].stage, "SECURITY_PRECHECK")

    def test_happy_path_reaches_governed_delivery(self):
        self.create(untrusted_input_present=True)
        self.mvp.pass_trust_gate("MVP-RUN-1")
        self.complete()
        run = self.mvp.runs["MVP-RUN-1"]
        self.assertTrue(run.verification_passed)
        self.assertTrue(run.socrates_passed)
        self.assertTrue(run.delivered)
        self.assertIn("GOVERNED_DELIVERY:PASS", run.trace)

    def test_successful_delivery_is_terminal(self):
        self.create()
        self.complete()
        with self.assertRaisesRegex(ValueError, "RUN_TERMINAL"):
            self.mvp.advance("MVP-RUN-1", "GOVERNED_DELIVERY")
        with self.assertRaisesRegex(ValueError, "RUN_TERMINAL"):
            self.mvp.pass_trust_gate("MVP-RUN-1")

    def test_failed_socrates_cannot_be_delivered(self):
        self.create()
        self.advance_until("SOCRATES_CHALLENGE")
        self.mvp.advance("MVP-RUN-1", "SOCRATES_CHALLENGE", outcome="FAIL")
        self.assertFalse(self.mvp.runs["MVP-RUN-1"].socrates_passed)
        self.assertEqual(self.mvp.runs["MVP-RUN-1"].stage, "SOCRATES_CHALLENGE")

    def test_run_ids_are_append_only(self):
        self.create()
        with self.assertRaisesRegex(ValueError, "RUN_ID_REUSE"):
            self.create()


if __name__ == "__main__":
    unittest.main()
