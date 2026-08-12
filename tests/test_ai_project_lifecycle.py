import unittest

from px00.ai_project_lifecycle import (
    CrispMlqPhaseRecord,
    QuantitativeRiskInput,
    evaluate_delivery_gate,
    simulate_quantitative_risk,
)


class AiProjectLifecycleTests(unittest.TestCase):
    def test_crisp_phase_requires_quality_structure(self):
        record = CrispMlqPhaseRecord(
            phase="MODEL_ENGINEERING",
            requirements_constraints=("reproducible training",),
            tasks=("train baseline",),
            risks=("overfitting",),
            qa_methods=("cross validation",),
        )
        record.validate()

        broken = CrispMlqPhaseRecord(
            phase="MODEL_ENGINEERING",
            requirements_constraints=("reproducible training",),
            tasks=("train baseline",),
            risks=("overfitting",),
            qa_methods=(),
        )
        with self.assertRaisesRegex(ValueError, "CRISP_QA_METHODS_REQUIRED"):
            broken.validate()

    def test_demo_requires_alignment_not_model_metrics(self):
        result = evaluate_delivery_gate(
            "DEMO",
            {"technical_metric", "baseline", "data_feasibility"},
        )
        self.assertFalse(result.passed)
        self.assertIn("stakeholder_alignment", result.missing_evidence)
        self.assertIn("scenario_prototype", result.missing_evidence)

    def test_poc_can_pass_without_real_users(self):
        result = evaluate_delivery_gate(
            "POC",
            {
                "data_feasibility",
                "baseline",
                "technical_metric",
                "known_data_gaps",
                "go_no_go_evidence",
            },
        )
        self.assertTrue(result.passed)
        self.assertNotIn("real_users", result.provided_evidence)

    def test_mvp_requires_real_users_and_business_metric(self):
        result = evaluate_delivery_gate(
            "MVP",
            {
                "real_data",
                "product_metric",
                "technical_slo",
                "basic_observability",
                "rollback_path",
            },
        )
        self.assertFalse(result.passed)
        self.assertIn("real_users", result.missing_evidence)
        self.assertIn("business_metric", result.missing_evidence)

    def test_production_requires_operations_not_only_model_quality(self):
        result = evaluate_delivery_gate(
            "PRODUCTION",
            {
                "economic_effect",
                "security_controls",
                "sla_slo",
            },
        )
        self.assertFalse(result.passed)
        self.assertIn("ci_cd_release_governance", result.missing_evidence)
        self.assertIn("monitoring_alerting", result.missing_evidence)
        self.assertIn("recovery_dr", result.missing_evidence)

    def test_blocking_risk_prevents_stage_promotion_even_with_evidence(self):
        evidence = {
            "problem_scope",
            "stakeholder_alignment",
            "scenario_prototype",
        }
        result = evaluate_delivery_gate("DEMO", evidence, blocking_risk_refs=("RISK-X",))
        self.assertFalse(result.passed)
        self.assertEqual(result.blocking_risk_refs, ("RISK-X",))

    def test_quantitative_risk_is_reproducible(self):
        spec = QuantitativeRiskInput(
            probability=0.7,
            impact_minimum=60,
            impact_mode=80,
            impact_maximum=150,
            tolerance_limit=30,
            percentile_level=0.95,
            trials=5000,
            seed=42,
        )
        first = simulate_quantitative_risk(spec)
        second = simulate_quantitative_risk(spec)
        self.assertEqual(first, second)
        self.assertGreater(first.expected_loss, 0)
        self.assertGreater(first.percentile_loss, first.expected_loss)
        self.assertGreater(first.probability_exceeding_tolerance, 0.5)

    def test_quantitative_risk_mean_is_close_to_analytic_expectation(self):
        spec = QuantitativeRiskInput(
            probability=0.5,
            impact_minimum=10,
            impact_mode=40,
            impact_maximum=70,
            tolerance_limit=50,
            trials=20000,
            seed=9,
        )
        result = simulate_quantitative_risk(spec)
        analytic = 0.5 * ((10 + 40 + 70) / 3)
        self.assertAlmostEqual(result.expected_loss, analytic, delta=1.0)

    def test_invalid_triangular_distribution_is_rejected(self):
        spec = QuantitativeRiskInput(
            probability=0.5,
            impact_minimum=80,
            impact_mode=40,
            impact_maximum=70,
            tolerance_limit=50,
        )
        with self.assertRaisesRegex(ValueError, "RISK_MINIMUM_GREATER_THAN_MODE"):
            simulate_quantitative_risk(spec)


if __name__ == "__main__":
    unittest.main()
