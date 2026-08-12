import unittest

from px00.challenges import AssessmentChallengeStore
from px00.quality import QualityAssessmentFactory


class AssessmentChallengeStoreTests(unittest.TestCase):
    def setUp(self):
        self.factory = QualityAssessmentFactory()
        self.store = AssessmentChallengeStore()
        self.src1 = self.factory.source(
            source_assessment_id="SRCA-1", source_ref="SRC-1", evaluator_ref="ROLE-0201",
            evaluator_version="0.1", basis_refs=("EVD-B1",), reliability=0.85, authority=0.8,
            recency=0.9, conflict_of_interest=0.2, evaluated_at="2026-08-12T10:00:00Z")
        self.store.register_source_assessment(self.src1)

    def test_challenge_does_not_mutate_target(self):
        challenge = self.store.challenge(
            target_assessment_ref="SRCA-1", challenger_ref="ROLE-0202", challenger_version="0.1",
            reason_code="SOURCE_AUTHORITY_OVERRATED", rationale_summary="authority evidence is weaker than scored",
            evidence_refs=("EVD-C1",), proposed_revision={"reliability": 0.55}, challenge_id="CHAL-1")
        self.assertEqual(challenge.target_assessment_ref, "SRCA-1")
        self.assertEqual(self.store.source_assessments["SRCA-1"].reliability, 0.85)

    def test_rejected_challenge_preserves_target_as_current_history(self):
        self.store.challenge(target_assessment_ref="SRCA-1", challenger_ref="ROLE-0202", challenger_version="0.1",
            reason_code="WEAK_BASIS", rationale_summary="challenge", evidence_refs=("EVD-C1",), challenge_id="CHAL-1")
        review = self.store.review(challenge_ref="CHAL-1", reviewer_ref="ROLE-0300", reviewer_version="0.1",
            decision="REJECT_CHALLENGE", reason_code="BASIS_SUFFICIENT", rationale_summary="original basis stands",
            basis_refs=("EVD-R1",), review_id="REVIEW-1")
        self.assertIsNone(review.replacement_assessment_ref)
        self.assertEqual(self.store.lineage("SRCA-1"), ("SRCA-1",))

    def test_accepted_challenge_requires_replacement(self):
        self.store.challenge(target_assessment_ref="SRCA-1", challenger_ref="ROLE-0202", challenger_version="0.1",
            reason_code="WEAK_BASIS", rationale_summary="challenge", evidence_refs=("EVD-C1",), challenge_id="CHAL-1")
        with self.assertRaisesRegex(ValueError, "REPLACEMENT_ASSESSMENT_REQUIRED"):
            self.store.review(challenge_ref="CHAL-1", reviewer_ref="ROLE-0300", reviewer_version="0.1",
                decision="ACCEPT_CHALLENGE", reason_code="AGREED", rationale_summary="accepted", basis_refs=("EVD-R1",))

    def test_accepted_challenge_creates_supersession_lineage(self):
        self.store.challenge(target_assessment_ref="SRCA-1", challenger_ref="ROLE-0202", challenger_version="0.1",
            reason_code="SOURCE_AUTHORITY_OVERRATED", rationale_summary="challenge", evidence_refs=("EVD-C1",),
            proposed_revision={"reliability": 0.55}, challenge_id="CHAL-1")
        replacement = self.factory.source(
            source_assessment_id="SRCA-2", source_ref="SRC-1", evaluator_ref="ROLE-0300", evaluator_version="0.1",
            basis_refs=("EVD-C1", "EVD-R1"), reliability=0.55, authority=0.7, recency=0.9,
            conflict_of_interest=0.2, evaluated_at="2026-08-12T11:00:00Z")
        review = self.store.review(challenge_ref="CHAL-1", reviewer_ref="ROLE-0300", reviewer_version="0.1",
            decision="ACCEPT_WITH_MODIFICATION", reason_code="REVISION_SUPPORTED", rationale_summary="re-score source",
            basis_refs=("EVD-R1",), replacement_assessment=replacement, review_id="REVIEW-1")
        self.assertEqual(review.replacement_assessment_ref, "SRCA-2")
        self.assertEqual(self.store.lineage("SRCA-2"), ("SRCA-2", "SRCA-1"))
        self.assertEqual(self.store.source_assessments["SRCA-1"].reliability, 0.85)

    def test_wrong_replacement_subject_is_rejected(self):
        self.store.challenge(target_assessment_ref="SRCA-1", challenger_ref="ROLE-0202", challenger_version="0.1",
            reason_code="WEAK_BASIS", rationale_summary="challenge", evidence_refs=("EVD-C1",), challenge_id="CHAL-1")
        replacement = self.factory.source(
            source_assessment_id="SRCA-2", source_ref="SRC-OTHER", evaluator_ref="ROLE-0300", evaluator_version="0.1",
            basis_refs=("EVD-R1",), reliability=0.5, authority=0.5, recency=0.5, conflict_of_interest=0.5)
        with self.assertRaisesRegex(ValueError, "REPLACEMENT_SUBJECT_MISMATCH"):
            self.store.review(challenge_ref="CHAL-1", reviewer_ref="ROLE-0300", reviewer_version="0.1",
                decision="ACCEPT_CHALLENGE", reason_code="AGREED", rationale_summary="accepted", basis_refs=("EVD-R1",),
                replacement_assessment=replacement)

    def test_invalid_proposed_revision_dimension_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "INVALID_PROPOSED_REVISION_DIMENSION"):
            self.store.challenge(target_assessment_ref="SRCA-1", challenger_ref="ROLE-0202", challenger_version="0.1",
                reason_code="WEAK_BASIS", rationale_summary="challenge", evidence_refs=("EVD-C1",),
                proposed_revision={"truth": 1.0})

if __name__ == "__main__":
    unittest.main()
