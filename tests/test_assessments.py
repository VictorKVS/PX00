import unittest

from px00.assessments import ClaimAssessmentStore
from px00.knowledge_graph import ClaimEvidenceGraph, ClaimNode, EvidenceNode, SourceNode
from px00.quality import QualityAssessmentFactory


class ClaimAssessmentStoreTests(unittest.TestCase):
    def setUp(self):
        self.graph = ClaimEvidenceGraph()
        for sid, locator, group in (("SRC-1","a","G1"),("SRC-2","b","G2"),("SRC-3","c","G3")):
            self.graph.add_source(SourceNode(sid, "DOCUMENT", locator, group))
        self.graph.add_claim(ClaimNode("CLM-1", "test claim"))
        self.store = ClaimAssessmentStore()
        self.factory = QualityAssessmentFactory()
        self.source_quality = {}
        self.evidence_quality = {}

    def _quality_for_source(self, source, strength=0.9):
        item = self.factory.source(
            source_assessment_id=f"SRCA-{source}", source_ref=source,
            evaluator_ref="ROLE-REVIEWER", evaluator_version="0.1", basis_refs=("POLICY-Q1",),
            reliability=strength, authority=strength, recency=strength, conflict_of_interest=0.1,
            evaluated_at="2026-08-12T09:00:00Z")
        self.source_quality[source] = item
        return item

    def _add(self, eid, source, group, stance="SUPPORT", strength=0.9):
        self.graph.add_evidence(EvidenceNode(eid, source, stance, group)); self.graph.link_evidence("CLM-1", eid)
        source_assessment = self.source_quality.get(source) or self._quality_for_source(source, strength)
        self.evidence_quality[eid] = self.factory.evidence(
            evidence_assessment_id=f"EVDA-{eid}", evidence_ref=eid, source_assessment_ref=source_assessment.source_assessment_id,
            evaluator_ref="ROLE-REVIEWER", evaluator_version="0.1", basis_refs=("PROTO-Q1",),
            quality=strength, directness=strength, completeness=strength, reproducibility=strength, relevance=strength,
            evaluated_at="2026-08-12T09:05:00Z")

    def _assess(self, when):
        return self.store.assess(self.graph, "CLM-1", source_quality=self.source_quality,
                                 evidence_quality=self.evidence_quality, evaluated_at=when)

    def test_first_assessment_with_no_evidence_is_unsupported(self):
        a=self._assess("2026-08-12T10:00:00Z")
        self.assertEqual(a.status,"UNSUPPORTED"); self.assertEqual(a.evidence_refs,()); self.assertIsNone(a.previous_assessment_ref)

    def test_two_independent_sources_create_corroborated_assessment(self):
        self._add("EVD-1","SRC-1","G1"); self._add("EVD-2","SRC-2","G2")
        a=self._assess("2026-08-12T10:00:00Z")
        self.assertEqual(a.status,"CORROBORATED"); self.assertEqual(a.evidence_refs,("EVD-1","EVD-2"))
        self.assertEqual(len(a.source_assessment_refs),2); self.assertEqual(len(a.evidence_assessment_refs),2)

    def test_new_evidence_creates_new_assessment_without_mutating_old(self):
        self._add("EVD-1","SRC-1","G1"); first=self._assess("2026-08-12T10:00:00Z")
        self._add("EVD-2","SRC-2","G2"); second=self._assess("2026-08-12T11:00:00Z")
        self.assertEqual(first.status,"SINGLE_SOURCE"); self.assertEqual(second.status,"CORROBORATED")
        self.assertEqual(second.previous_assessment_ref,first.assessment_id); self.assertNotEqual(first.evidence_set_hash,second.evidence_set_hash)

    def test_counterevidence_changes_later_assessment_not_history(self):
        self._add("EVD-1","SRC-1","G1"); self._add("EVD-2","SRC-2","G2"); first=self._assess("2026-08-12T10:00:00Z")
        self._add("EVD-3","SRC-3","G3","CONTRADICT"); second=self._assess("2026-08-12T11:00:00Z")
        self.assertEqual(first.status,"CORROBORATED"); self.assertEqual(second.status,"DISPUTED")
        self.assertEqual(self.store.get(first.assessment_id).status,"CORROBORATED")

    def test_same_material_evidence_and_quality_are_order_stable(self):
        self._add("EVD-2","SRC-2","G2"); self._add("EVD-1","SRC-1","G1")
        first=self._assess("2026-08-12T10:00:00Z"); second=self._assess("2026-08-12T11:00:00Z")
        self.assertEqual(first.evidence_set_hash,second.evidence_set_hash)

    def test_missing_source_quality_fails_closed(self):
        self._add("EVD-1","SRC-1","G1"); self.source_quality.clear()
        with self.assertRaisesRegex(ValueError,"SOURCE_QUALITY_ASSESSMENT_REQUIRED"): self._assess("2026-08-12T10:00:00Z")

    def test_missing_evidence_quality_fails_closed(self):
        self._add("EVD-1","SRC-1","G1"); self.evidence_quality.clear()
        with self.assertRaisesRegex(ValueError,"EVIDENCE_QUALITY_ASSESSMENT_REQUIRED"): self._assess("2026-08-12T10:00:00Z")

    def test_evidence_source_assessment_mismatch_fails_closed(self):
        self._add("EVD-1","SRC-1","G1"); wrong=self._quality_for_source("SRC-2")
        current=self.evidence_quality["EVD-1"]
        from dataclasses import replace
        self.evidence_quality["EVD-1"]=replace(current,source_assessment_ref=wrong.source_assessment_id)
        with self.assertRaisesRegex(ValueError,"EVIDENCE_SOURCE_ASSESSMENT_MISMATCH"): self._assess("2026-08-12T10:00:00Z")

if __name__=="__main__": unittest.main()
