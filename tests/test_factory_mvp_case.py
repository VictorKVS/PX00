import unittest

from px00.factory_mvp import STAGES
from px00.factory_mvp_case import (
    PRODUCER,
    SOCRATES,
    VERIFIER,
    derive_idempotency_key,
    run_synthetic_idempotency_case,
)


class FactoryFunctionalMvpCaseTests(unittest.TestCase):
    def test_idempotency_key_is_deterministic_scoped_and_unambiguous(self):
        a = derive_idempotency_key("R1", "DELIVER", "T1")
        self.assertEqual(a, derive_idempotency_key("R1", "DELIVER", "T1"))
        self.assertNotEqual(a, derive_idempotency_key("R2", "DELIVER", "T1"))
        self.assertNotEqual(a, derive_idempotency_key("R1", "ARCHIVE", "T1"))
        self.assertNotEqual(a, derive_idempotency_key("R1", "DELIVER", "T2"))
        self.assertNotEqual(
            derive_idempotency_key("A|B", "C", "D"),
            derive_idempotency_key("A", "B|C", "D"),
        )
        self.assertEqual(len(a), 64)

    def test_full_functional_case_delivers_typed_artifact_chain(self):
        mvp, run_id = run_synthetic_idempotency_case()
        run = mvp.runs[run_id]
        self.assertTrue(run.delivered)
        self.assertEqual(len(run.artifact_refs), len(STAGES))
        self.assertEqual(len(run.consumed_artifact_refs), len(STAGES))
        self.assertEqual(mvp.artifacts[run.artifact_refs[6]].producer_assignment_ref, VERIFIER)
        self.assertEqual(mvp.artifacts[run.artifact_refs[7]].producer_assignment_ref, SOCRATES)
        self.assertEqual(mvp.artifacts[run.artifact_refs[0]].producer_assignment_ref, PRODUCER)
        for ref in run.artifact_refs:
            self.assertTrue(mvp.artifacts[ref].verify_digest())

    def test_socrates_preserves_exactly_once_limitation(self):
        mvp, run_id = run_synthetic_idempotency_case()
        run = mvp.runs[run_id]
        socrates = mvp.artifact_payload(run.artifact_refs[7])
        delivery = mvp.artifact_payload(run.artifact_refs[-1])
        self.assertEqual(socrates["verdict"], "PASS_WITH_FINDING")
        self.assertIn("does not itself guarantee exactly-once", socrates["finding"])
        self.assertIn("no exactly-once claim", delivery["limitations"])

    def test_delivery_cannot_hide_missing_transactional_control(self):
        mvp, run_id = run_synthetic_idempotency_case()
        delivery = mvp.artifact_payload(mvp.runs[run_id].artifact_refs[-1])
        self.assertEqual(
            delivery["next_if_needed"],
            "pair key identity with durable uniqueness and atomic execution state",
        )


if __name__ == "__main__":
    unittest.main()
