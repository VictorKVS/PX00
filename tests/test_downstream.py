import unittest

from px00.downstream import DependencyNode, DownstreamDependencyGraph


class DownstreamDependencyGraphTests(unittest.TestCase):
    def setUp(self):
        self.graph = DownstreamDependencyGraph()
        self.graph.add_node(DependencyNode("CLMA-1", "CLAIM_ASSESSMENT"))
        self.graph.add_node(DependencyNode("KN-1", "KNOWLEDGE"))
        self.graph.add_node(DependencyNode("DEC-1", "DECISION"))
        self.graph.add_node(DependencyNode("PLAN-1", "PLAN"))
        self.graph.add_dependency("CLMA-1", "KN-1")
        self.graph.add_dependency("KN-1", "DEC-1")
        self.graph.add_dependency("DEC-1", "PLAN-1")

    def test_claim_change_marks_full_downstream_chain(self):
        impact = self.graph.propagate(trigger_ref="CLMA-1", caused_by_ref="REVIEW-9", created_at="2026-08-12T12:00:00Z")
        self.assertEqual(self.graph.nodes["KN-1"].status, "STALE")
        self.assertEqual(self.graph.nodes["DEC-1"].status, "REASSESSMENT_REQUIRED")
        self.assertEqual(self.graph.nodes["PLAN-1"].status, "REVIEW_REQUIRED")
        self.assertEqual(impact.affected_objects, ("KN-1", "DEC-1", "PLAN-1"))
        self.assertEqual(impact.propagation_depth, 3)
        self.assertEqual(impact.caused_by_ref, "REVIEW-9")

    def test_propagation_preserves_causal_paths(self):
        impact = self.graph.propagate(trigger_ref="CLMA-1", caused_by_ref="REVIEW-9")
        plan = next(change for change in impact.status_changes if change.object_ref == "PLAN-1")
        self.assertEqual(plan.path, ("CLMA-1", "KN-1", "DEC-1", "PLAN-1"))

    def test_duplicate_edge_does_not_duplicate_impact(self):
        self.graph.add_dependency("CLMA-1", "KN-1")
        impact = self.graph.propagate(trigger_ref="CLMA-1", caused_by_ref="REVIEW-9")
        self.assertEqual(impact.affected_objects.count("KN-1"), 1)

    def test_cycle_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "DEPENDENCY_CYCLE"):
            self.graph.add_dependency("PLAN-1", "CLMA-1")

    def test_unknown_node_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "UNKNOWN_DEPENDENCY_NODE_REF"):
            self.graph.add_dependency("KN-1", "DEC-404")

    def test_propagation_does_not_delete_or_cancel_objects(self):
        self.graph.propagate(trigger_ref="CLMA-1", caused_by_ref="REVIEW-9")
        self.assertIn("DEC-1", self.graph.nodes)
        self.assertIn("PLAN-1", self.graph.nodes)
        self.assertNotEqual(self.graph.nodes["DEC-1"].status, "CANCELLED")
        self.assertNotEqual(self.graph.nodes["PLAN-1"].status, "CANCELLED")


if __name__ == "__main__":
    unittest.main()
