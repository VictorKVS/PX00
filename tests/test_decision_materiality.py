import unittest

from px00.decision_materiality import DecisionMaterialityAssessment, DecisionMaterialityGate


class DecisionMaterialityGateTests(unittest.TestCase):
    def setUp(self):
        self.gate = DecisionMaterialityGate()

    def item(self, **overrides):
        base = dict(
            decision_ref="DEC-TEST-1",
            declared_class="D0_LOCAL_CONVENTIONAL",
            consequence="LOW",
            reversibility="EASY",
            uncertainty="LOW",
            blast_radius="LOCAL",
            risk_severity="S0",
            evidence_categories_present=frozenset({"CONVENTION_OR_PROJECT_RULE"}),
        )
        base.update(overrides)
        return DecisionMaterialityAssessment(**base)

    def test_d0_local_convention_passes_without_bureaucratic_review(self):
        result = self.gate.evaluate(self.item())
        self.assertEqual(result.status, "PASS")
        self.assertFalse(result.independent_review_required)

    def test_s3_cannot_be_declared_as_d1(self):
        result = self.gate.evaluate(
            self.item(
                declared_class="D1_IMPLEMENTATION",
                risk_severity="S3",
                evidence_categories_present=frozenset({"TECHNICAL_REFERENCE", "VERIFICATION"}),
            )
        )
        self.assertEqual(result.status, "MATERIALITY_UNDERCLASSIFIED")
        self.assertEqual(result.required_floor, "D2_ARCHITECTURE_PRODUCT")

    def test_architecture_boundary_promotes_to_d2(self):
        result = self.gate.evaluate(self.item(architecture_or_product_boundary=True))
        self.assertEqual(result.status, "MATERIALITY_UNDERCLASSIFIED")
        self.assertEqual(result.required_floor, "D2_ARCHITECTURE_PRODUCT")

    def test_d2_requires_complete_evidence_categories(self):
        result = self.gate.evaluate(
            self.item(
                declared_class="D2_ARCHITECTURE_PRODUCT",
                consequence="HIGH",
                evidence_categories_present=frozenset({"REQUIREMENTS", "CONSTRAINTS"}),
                independent_review_present=True,
            )
        )
        self.assertEqual(result.status, "INSUFFICIENT_EVIDENCE")
        self.assertIn("ALTERNATIVES", result.missing_evidence)
        self.assertIn("VERIFICATION_PLAN", result.missing_evidence)

    def test_d2_requires_independent_review_after_evidence_is_complete(self):
        evidence = frozenset(
            {
                "REQUIREMENTS",
                "CONSTRAINTS",
                "ALTERNATIVES",
                "DECISION_CRITERIA",
                "COST_OR_RESOURCE_VIEW",
                "RISK_VIEW",
                "TECHNICAL_REFERENCE",
                "VERIFICATION_PLAN",
            }
        )
        result = self.gate.evaluate(
            self.item(
                declared_class="D2_ARCHITECTURE_PRODUCT",
                consequence="HIGH",
                evidence_categories_present=evidence,
            )
        )
        self.assertEqual(result.status, "REVIEW_REQUIRED")

    def test_s4_forces_d3_and_cannot_be_averaged_down(self):
        result = self.gate.evaluate(
            self.item(
                declared_class="D2_ARCHITECTURE_PRODUCT",
                risk_severity="S4",
                consequence="LOW",
                reversibility="EASY",
                uncertainty="LOW",
                blast_radius="LOCAL",
            )
        )
        self.assertEqual(result.status, "MATERIALITY_UNDERCLASSIFIED")
        self.assertEqual(result.required_floor, "D3_REGULATED_SAFETY_CRITICAL")

    def test_d3_requires_qualified_review_and_approval(self):
        evidence = frozenset(
            {
                "REQUIREMENTS",
                "CONSTRAINTS",
                "ALTERNATIVES",
                "DECISION_CRITERIA",
                "COST_OR_RESOURCE_VIEW",
                "RISK_VIEW",
                "PRIMARY_OR_NORMATIVE_SOURCE",
                "APPLICABILITY",
                "RESIDUAL_RISK",
                "VERIFICATION_PLAN",
                "QUALIFIED_INDEPENDENT_REVIEW",
            }
        )
        without_review = self.gate.evaluate(
            self.item(
                declared_class="D3_REGULATED_SAFETY_CRITICAL",
                regulated_or_legally_mandatory=True,
                evidence_categories_present=evidence,
            )
        )
        self.assertEqual(without_review.status, "REVIEW_REQUIRED")

        without_approval = self.gate.evaluate(
            self.item(
                declared_class="D3_REGULATED_SAFETY_CRITICAL",
                regulated_or_legally_mandatory=True,
                evidence_categories_present=evidence,
                independent_review_present=True,
            )
        )
        self.assertEqual(without_approval.status, "APPROVAL_REQUIRED")

        passed = self.gate.evaluate(
            self.item(
                declared_class="D3_REGULATED_SAFETY_CRITICAL",
                regulated_or_legally_mandatory=True,
                evidence_categories_present=evidence,
                independent_review_present=True,
                approval_present=True,
            )
        )
        self.assertEqual(passed.status, "PASS")


if __name__ == "__main__":
    unittest.main()
