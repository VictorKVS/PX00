import unittest

from px00.quality import QualityAssessmentFactory


class QualityAssessmentFactoryTests(unittest.TestCase):
    def setUp(self): self.factory=QualityAssessmentFactory()

    def test_source_assessment_requires_basis(self):
        with self.assertRaisesRegex(ValueError,"SOURCE_ASSESSMENT_BASIS_REQUIRED"):
            self.factory.source(source_assessment_id="SRCA-1",source_ref="SRC-1",evaluator_ref="ROLE-1",evaluator_version="0.1",basis_refs=(),reliability=.8,authority=.7,recency=.9,conflict_of_interest=.2)

    def test_evidence_assessment_requires_basis(self):
        with self.assertRaisesRegex(ValueError,"EVIDENCE_ASSESSMENT_BASIS_REQUIRED"):
            self.factory.evidence(evidence_assessment_id="EVDA-1",evidence_ref="EVD-1",source_assessment_ref="SRCA-1",evaluator_ref="ROLE-1",evaluator_version="0.1",basis_refs=(),quality=.8,directness=.7,completeness=.9,reproducibility=.6,relevance=.9)

    def test_dimension_out_of_range_is_rejected(self):
        with self.assertRaisesRegex(ValueError,"QUALITY_DIMENSION_OUT_OF_RANGE"):
            self.factory.source(source_assessment_id="SRCA-1",source_ref="SRC-1",evaluator_ref="ROLE-1",evaluator_version="0.1",basis_refs=("B1",),reliability=1.1,authority=.7,recency=.9,conflict_of_interest=.2)

    def test_same_material_assessment_is_hash_stable(self):
        kwargs=dict(source_assessment_id="SRCA-1",source_ref="SRC-1",evaluator_ref="ROLE-1",evaluator_version="0.1",basis_refs=("B2","B1"),reliability=.8,authority=.7,recency=.9,conflict_of_interest=.2,evaluated_at="2026-08-12T09:00:00Z")
        a=self.factory.source(**kwargs); b=self.factory.source(**kwargs)
        self.assertEqual(a.assessment_hash,b.assessment_hash)

    def test_material_change_changes_hash(self):
        base=dict(source_assessment_id="SRCA-1",source_ref="SRC-1",evaluator_ref="ROLE-1",evaluator_version="0.1",basis_refs=("B1",),authority=.7,recency=.9,conflict_of_interest=.2,evaluated_at="2026-08-12T09:00:00Z")
        a=self.factory.source(reliability=.8,**base); b=self.factory.source(reliability=.6,**base)
        self.assertNotEqual(a.assessment_hash,b.assessment_hash)

if __name__=="__main__": unittest.main()
