import unittest

from px00.staffing import AgentAssignment, HandoffPackage, RoleResponsibility, StaffingRegistry


class StaffingRegistryTests(unittest.TestCase):
    def setUp(self):
        self.registry = StaffingRegistry()
        self.registry.declare_role("ROLE-ANALYST", knowledge_bindings=("KB-ANALYSIS", "KB-CORP"), protocols=("PROTO-HANDOFF", "PROTO-ANALYZE"))
        self.registry.declare_role("ROLE-SECURITY", knowledge_bindings=("KB-SECURITY", "KB-CORP"), protocols=("PROTO-HANDOFF", "PROTO-REVIEW"))
        self.responsibility = RoleResponsibility(
            "RESP-1", "ROLE-ANALYST", "DEPT-ANALYSIS", "ANALYZE_CASE", "Analyze case and produce evidence-backed finding",
            ("PROTO-HANDOFF",), ("KB-ANALYSIS", "KB-CORP"), ("FIND",), ("INSUFFICIENT_EVIDENCE",),
        )
        self.registry.add_responsibility(self.responsibility)

    def test_assignment_may_use_subset_of_role_knowledge(self):
        assignment = AgentAssignment("ASG-1", "AGENT-1", "ROLE-ANALYST", "DEPT-ANALYSIS", "LLM", "model-x", ("KB-ANALYSIS",))
        self.registry.assign_agent(assignment)
        self.assertTrue(self.registry.can_start_run("ASG-1"))

    def test_assignment_cannot_expand_role_knowledge(self):
        assignment = AgentAssignment("ASG-1", "AGENT-1", "ROLE-ANALYST", "DEPT-ANALYSIS", "LLM", "model-x", ("KB-SECURITY",))
        with self.assertRaisesRegex(ValueError, "ASSIGNMENT_KNOWLEDGE_BINDING_OVERFLOW"):
            self.registry.assign_agent(assignment)

    def test_suspended_assignment_cannot_start_run(self):
        assignment = AgentAssignment("ASG-1", "AGENT-1", "ROLE-ANALYST", "DEPT-ANALYSIS", "LLM", "model-x", ("KB-ANALYSIS",), status="SUSPENDED")
        self.registry.assign_agent(assignment)
        self.assertFalse(self.registry.can_start_run("ASG-1"))

    def test_handoff_requires_protocol_on_both_roles(self):
        handoff = HandoffPackage("HO-1", "TASK-1", "ROLE-ANALYST", "ROLE-SECURITY", "PROTO-HANDOFF", "RESP-1", (), ("FIND-1",), ("EVD-1",), (), (), (), "READY")
        self.registry.create_handoff(handoff)
        self.assertIn("HO-1", self.registry.handoffs)

    def test_ready_handoff_with_blocking_finding_fails(self):
        handoff = HandoffPackage("HO-1", "TASK-1", "ROLE-ANALYST", "ROLE-SECURITY", "PROTO-HANDOFF", "RESP-1", (), ("FIND-1",), ("EVD-1",), (), (), ("BLOCK-1",), "READY")
        with self.assertRaisesRegex(ValueError, "READY_WITH_BLOCKING_FINDINGS"):
            self.registry.create_handoff(handoff)

    def test_handoff_does_not_transfer_authority(self):
        handoff = HandoffPackage("HO-1", "TASK-1", "ROLE-ANALYST", "ROLE-SECURITY", "PROTO-HANDOFF", "RESP-1", (), ("FIND-1",), ("EVD-1",), (), ("QUESTION-1",), (), "READY")
        self.registry.create_handoff(handoff)
        self.assertFalse(hasattr(self.registry.handoffs["HO-1"], "authority"))


if __name__ == "__main__":
    unittest.main()
