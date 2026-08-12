import unittest

from px00.organization import CorporateOrganization, Department, KnowledgeBinding


class CorporateOrganizationTests(unittest.TestCase):
    def setUp(self):
        self.org = CorporateOrganization("ORG-1", "PX00", "POLICY-ORG-1")
        self.org.add_department(Department("DEP-AN", "ORG-1", "Analysis", "Analyze governed material", ("ROLE-0201",), ("PROTO-HANDOFF",), ("PROTO-HANDOFF",)))
        self.org.add_department(Department("DEP-SEC", "ORG-1", "Security", "Provide security expertise", ("ROLE-SEC",), ("PROTO-HANDOFF",), ("PROTO-HANDOFF",)))

    def test_role_can_have_multiple_knowledge_bindings(self):
        self.org.add_knowledge_binding(KnowledgeBinding("KB-1", "ROLE-SEC", "VictorKVS/KNOWLEDGE_CORE", "security-core/regulations", "QUERY", "resolve regulatory requirements", ("PROTO-SEC",)))
        self.org.add_knowledge_binding(KnowledgeBinding("KB-2", "ROLE-SEC", "VictorKVS/KNOWLEDGE_CORE", "security-core/threats", "READ", "analyze threats", ("PROTO-SEC",)))
        bindings = self.org.bindings_for_role("ROLE-SEC")
        self.assertEqual(tuple(x.binding_id for x in bindings), ("KB-1", "KB-2"))

    def test_unknown_repository_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "UNDECLARED_KNOWLEDGE_REPOSITORY"):
            self.org.add_knowledge_binding(KnowledgeBinding("KB-1", "ROLE-SEC", "random/repo", "x", "READ", "x", ("P",)))

    def test_binding_requires_protocol_context(self):
        with self.assertRaisesRegex(ValueError, "KNOWLEDGE_BINDING_PROTOCOL_REQUIRED"):
            self.org.add_knowledge_binding(KnowledgeBinding("KB-1", "ROLE-SEC", "VictorKVS/KNOWLEDGE_CORE", "security-core", "READ", "x", ()))

    def test_cross_department_handoff_requires_declared_protocol_on_both_sides(self):
        self.assertTrue(self.org.validate_handoff("DEP-AN", "DEP-SEC", "PROTO-HANDOFF"))

    def test_missing_target_protocol_blocks_handoff(self):
        self.org.departments["DEP-SEC"] = Department("DEP-SEC", "ORG-1", "Security", "Provide security expertise", ("ROLE-SEC",), (), ("PROTO-HANDOFF",))
        with self.assertRaisesRegex(ValueError, "TARGET_HANDOFF_PROTOCOL_NOT_DECLARED"):
            self.org.validate_handoff("DEP-AN", "DEP-SEC", "PROTO-HANDOFF")


if __name__ == "__main__":
    unittest.main()
