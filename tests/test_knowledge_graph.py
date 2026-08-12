import unittest

from px00.knowledge_graph import ClaimEvidenceGraph, ClaimNode, EvidenceNode, SourceNode


class ClaimEvidenceGraphTests(unittest.TestCase):
    def setUp(self):
        self.g = ClaimEvidenceGraph()
        self.g.add_source(SourceNode("SRC-1", "WEB", "https://a.example", "G1"))
        self.g.add_source(SourceNode("SRC-2", "DOCUMENT", "doc://b", "G2"))

    def test_support_and_contradiction_edges_are_separate(self):
        self.g.add_evidence(EvidenceNode("EVD-1", "SRC-1", "SUPPORT", "G1"))
        self.g.add_evidence(EvidenceNode("EVD-2", "SRC-2", "CONTRADICT", "G2"))
        self.g.add_claim(ClaimNode("CLM-1", "statement"))
        self.g.link_evidence("CLM-1", "EVD-1"); self.g.link_evidence("CLM-1", "EVD-2")
        self.assertIn(("CLM-1", "EVD-1"), self.g.support_edges)
        self.assertIn(("CLM-1", "EVD-2"), self.g.contradiction_edges)

    def test_unknown_source_ref_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "UNKNOWN_SOURCE_REF"):
            self.g.add_evidence(EvidenceNode("EVD-X", "SRC-X", "SUPPORT", "GX"))

    def test_independence_group_must_match_source(self):
        with self.assertRaisesRegex(ValueError, "INDEPENDENCE_GROUP_MISMATCH"):
            self.g.add_evidence(EvidenceNode("EVD-1", "SRC-1", "SUPPORT", "G9"))

    def test_claim_revision_preserves_lineage(self):
        self.g.add_claim(ClaimNode("CLM-1", "old statement"))
        self.g.add_claim(ClaimNode("CLM-2", "revised statement", supersedes="CLM-1"))
        self.assertEqual(self.g.claim_lineage("CLM-2"), ("CLM-2", "CLM-1"))
        self.assertIn("CLM-1", self.g.claims)

    def test_unknown_superseded_claim_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "UNKNOWN_SUPERSEDED_CLAIM"):
            self.g.add_claim(ClaimNode("CLM-2", "statement", supersedes="CLM-X"))

    def test_derived_source_requires_known_parent(self):
        with self.assertRaisesRegex(ValueError, "UNKNOWN_PARENT_SOURCE"):
            self.g.add_source(SourceNode("SRC-3", "WEB", "https://c.example", "G1", parent_source_refs=("SRC-X",)))


if __name__ == "__main__":
    unittest.main()
