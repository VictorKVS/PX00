import unittest

from px00.assessments import ClaimAssessmentStore
from px00.knowledge_graph import ClaimEvidenceGraph, ClaimNode, EvidenceNode, SourceNode


class ClaimAssessmentStoreTests(unittest.TestCase):
    def setUp(self):
        self.graph = ClaimEvidenceGraph()
        self.graph.add_source(SourceNode("SRC-1", "DOCUMENT", "a", "G1"))
        self.graph.add_source(SourceNode("SRC-2", "DOCUMENT", "b", "G2"))
        self.graph.add_source(SourceNode("SRC-3", "DOCUMENT", "c", "G3"))
        self.graph.add_claim(ClaimNode("CLM-1", "test claim"))
        self.store = ClaimAssessmentStore()

    def _add(self, eid, source, group, stance="SUPPORT"):
        self.graph.add_evidence(EvidenceNode(eid, source, stance, group))
        self.graph.link_evidence("CLM-1", eid)

    def test_first_assessment_with_no_evidence_is_unsupported(self):
        a = self.store.assess(self.graph, "CLM-1", evaluated_at="2026-08-12T10:00:00Z")
        self.assertEqual(a.status, "UNSUPPORTED")
        self.assertEqual(a.evidence_refs, ())
        self.assertIsNone(a.previous_assessment_ref)

    def test_two_independent_sources_create_corroborated_assessment(self):
        self._add("EVD-1", "SRC-1", "G1")
        self._add("EVD-2", "SRC-2", "G2")
        a = self.store.assess(self.graph, "CLM-1", evaluated_at="2026-08-12T10:00:00Z")
        self.assertEqual(a.status, "CORROBORATED")
        self.assertEqual(a.evidence_refs, ("EVD-1", "EVD-2"))

    def test_new_evidence_creates_new_assessment_without_mutating_old(self):
        self._add("EVD-1", "SRC-1", "G1")
        first = self.store.assess(self.graph, "CLM-1", evaluated_at="2026-08-12T10:00:00Z")
        self._add("EVD-2", "SRC-2", "G2")
        second = self.store.assess(self.graph, "CLM-1", evaluated_at="2026-08-12T11:00:00Z")
        self.assertEqual(first.status, "SINGLE_SOURCE")
        self.assertEqual(first.evidence_refs, ("EVD-1",))
        self.assertEqual(second.status, "CORROBORATED")
        self.assertEqual(second.previous_assessment_ref, first.assessment_id)
        self.assertNotEqual(first.evidence_set_hash, second.evidence_set_hash)

    def test_counterevidence_changes_later_assessment_not_history(self):
        self._add("EVD-1", "SRC-1", "G1")
        self._add("EVD-2", "SRC-2", "G2")
        first = self.store.assess(self.graph, "CLM-1", evaluated_at="2026-08-12T10:00:00Z")
        self._add("EVD-3", "SRC-3", "G3", "CONTRADICT")
        second = self.store.assess(self.graph, "CLM-1", evaluated_at="2026-08-12T11:00:00Z")
        self.assertEqual(first.status, "CORROBORATED")
        self.assertEqual(second.status, "DISPUTED")
        self.assertEqual(self.store.get(first.assessment_id).status, "CORROBORATED")

    def test_same_material_evidence_is_order_stable(self):
        self._add("EVD-2", "SRC-2", "G2")
        self._add("EVD-1", "SRC-1", "G1")
        first = self.store.assess(self.graph, "CLM-1", evaluated_at="2026-08-12T10:00:00Z")
        second = self.store.assess(self.graph, "CLM-1", evaluated_at="2026-08-12T11:00:00Z")
        self.assertEqual(first.evidence_set_hash, second.evidence_set_hash)

if __name__ == "__main__":
    unittest.main()
