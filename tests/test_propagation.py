import unittest

from px00.assessments import ClaimAssessmentStore
from px00.challenges import AssessmentChallengeStore
from px00.knowledge_graph import ClaimEvidenceGraph, ClaimNode, EvidenceNode, SourceNode
from px00.propagation import CausalReassessmentPropagator
from px00.quality import QualityAssessmentFactory


class CausalPropagationTests(unittest.TestCase):
    def setUp(self):
        self.graph=ClaimEvidenceGraph(); self.graph.add_source(SourceNode("SRC-1","DOCUMENT","a","G1")); self.graph.add_source(SourceNode("SRC-2","DOCUMENT","b","G2"))
        self.graph.add_evidence(EvidenceNode("EVD-1","SRC-1","SUPPORT","G1")); self.graph.add_evidence(EvidenceNode("EVD-2","SRC-2","SUPPORT","G2")); self.graph.add_claim(ClaimNode("CLM-1","x"))
        self.graph.link_evidence("CLM-1","EVD-1"); self.graph.link_evidence("CLM-1","EVD-2")
        f=QualityAssessmentFactory(); self.f=f
        self.s1=f.source(source_assessment_id="SRCA-1",source_ref="SRC-1",evaluator_ref="R",evaluator_version="1",basis_refs=("B1",),reliability=.9,authority=.9,recency=.9,conflict_of_interest=.1,evaluated_at="2026-08-12T10:00:00Z")
        self.s2=f.source(source_assessment_id="SRCA-2",source_ref="SRC-2",evaluator_ref="R",evaluator_version="1",basis_refs=("B2",),reliability=.9,authority=.9,recency=.9,conflict_of_interest=.1,evaluated_at="2026-08-12T10:00:00Z")
        self.e1=f.evidence(evidence_assessment_id="EVDA-1",evidence_ref="EVD-1",source_assessment_ref="SRCA-1",evaluator_ref="R",evaluator_version="1",basis_refs=("B3",),quality=.9,directness=.9,completeness=.9,reproducibility=.9,relevance=.9,evaluated_at="2026-08-12T10:00:00Z")
        self.e2=f.evidence(evidence_assessment_id="EVDA-2",evidence_ref="EVD-2",source_assessment_ref="SRCA-2",evaluator_ref="R",evaluator_version="1",basis_refs=("B4",),quality=.9,directness=.9,completeness=.9,reproducibility=.9,relevance=.9,evaluated_at="2026-08-12T10:00:00Z")
        self.source_quality={"SRC-1":self.s1,"SRC-2":self.s2}; self.evidence_quality={"EVD-1":self.e1,"EVD-2":self.e2}
        self.claims=ClaimAssessmentStore(); self.first=self.claims.assess(self.graph,"CLM-1",source_quality=self.source_quality,evidence_quality=self.evidence_quality,evaluated_at="2026-08-12T10:00:00Z")
        self.reviews=AssessmentChallengeStore(); self.reviews.register_source_assessment(self.s1)

    def _accepted_review(self):
        ch=self.reviews.challenge(target_assessment_ref="SRCA-1",challenger_ref="ROLE-0202",challenger_version="1",reason_code="OVERRATED",rationale_summary="basis changed",evidence_refs=("EVD-X",))
        replacement=self.f.source(source_assessment_id="SRCA-1B",source_ref="SRC-1",evaluator_ref="REV",evaluator_version="1",basis_refs=("B5",),reliability=.1,authority=.4,recency=.5,conflict_of_interest=.8,evaluated_at="2026-08-12T11:00:00Z")
        review=self.reviews.review(challenge_ref=ch.challenge_id,reviewer_ref="HUMAN",reviewer_version="1",decision="ACCEPT_WITH_MODIFICATION",reason_code="VALID",rationale_summary="accepted",basis_refs=("B6",),replacement_assessment=replacement)
        refreshed=self.f.evidence(evidence_assessment_id="EVDA-1B",evidence_ref="EVD-1",source_assessment_ref="SRCA-1B",evaluator_ref="REV",evaluator_version="1",basis_refs=("B7",),quality=.1,directness=.3,completeness=.5,reproducibility=.5,relevance=.8,evaluated_at="2026-08-12T11:00:00Z")
        return review, refreshed

    def test_accepted_source_review_creates_causal_claim_reassessment(self):
        review, refreshed=self._accepted_review(); result=CausalReassessmentPropagator(self.claims).propagate(graph=self.graph,review_store=self.reviews,review_ref=review.review_id,source_quality=self.source_quality,evidence_quality=self.evidence_quality,refreshed_evidence_quality={"EVD-1":refreshed},evaluated_at="2026-08-12T11:00:00Z")
        self.assertEqual(result.affected_claims,("CLM-1",)); latest=self.claims.history("CLM-1")[-1]
        self.assertEqual(latest.caused_by_review_ref,review.review_id); self.assertEqual(latest.previous_assessment_ref,self.first.assessment_id); self.assertNotEqual(latest.evidence_set_hash,self.first.evidence_set_hash)

    def test_source_review_requires_refreshed_evidence_assessment(self):
        review,_=self._accepted_review()
        with self.assertRaisesRegex(ValueError,"REFRESHED_EVIDENCE_ASSESSMENT_REQUIRED"):
            CausalReassessmentPropagator(self.claims).propagate(graph=self.graph,review_store=self.reviews,review_ref=review.review_id,source_quality=self.source_quality,evidence_quality=self.evidence_quality)

    def test_non_accepting_review_cannot_propagate(self):
        ch=self.reviews.challenge(target_assessment_ref="SRCA-1",challenger_ref="R",challenger_version="1",reason_code="X",rationale_summary="x",evidence_refs=("E",))
        review=self.reviews.review(challenge_ref=ch.challenge_id,reviewer_ref="H",reviewer_version="1",decision="REJECT_CHALLENGE",reason_code="NO",rationale_summary="no",basis_refs=("B",))
        with self.assertRaisesRegex(ValueError,"NON_ACCEPTING_REVIEW_CANNOT_PROPAGATE"):
            CausalReassessmentPropagator(self.claims).propagate(graph=self.graph,review_store=self.reviews,review_ref=review.review_id,source_quality=self.source_quality,evidence_quality=self.evidence_quality)

if __name__=="__main__": unittest.main()
