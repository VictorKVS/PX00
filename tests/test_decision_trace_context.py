from __future__ import annotations

from dataclasses import replace
import tempfile
import unittest
from pathlib import Path

from px00.decision_context import DecisionContextBinder, DecisionContextError, GovernedProfessionalDecision
from px00.decision_materiality import DecisionMaterialityAssessment
from px00.kernel import SyntheticGovernedKernel
from px00.recorder import AppendOnlyEventRecorder, TraceDecisionContext
from px00.replay import ReadOnlyReplayVerifier


D2_EVIDENCE = frozenset(
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


class DecisionTraceContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.kernel = SyntheticGovernedKernel()
        self.recorder = AppendOnlyEventRecorder(self.root)
        self.replay = ReadOnlyReplayVerifier(self.recorder)
        self.request = self.kernel.prepare_request(5, 7)
        self.result = self.kernel.execute_request(self.request, allow=True)
        self.role_ref = "ROLE-ARCH-TEST"
        self.assignment_ref = "ASSIGN-ARCH-TEST"

    def tearDown(self):
        self.tmp.cleanup()

    def assessment(self, **overrides):
        base = dict(
            decision_ref="DEC-ARCH-0001",
            declared_class="D2_ARCHITECTURE_PRODUCT",
            consequence="HIGH",
            reversibility="MANAGED",
            uncertainty="MODERATE",
            blast_radius="SYSTEM",
            risk_severity="S3",
            evidence_categories_present=D2_EVIDENCE,
            independent_review_present=True,
            architecture_or_product_boundary=True,
        )
        base.update(overrides)
        return DecisionMaterialityAssessment(**base)

    def decision(self, **overrides):
        base = dict(
            decision_id="DEC-ARCH-0001",
            run_id=self.request.run_id,
            role_ref=self.role_ref,
            assignment_ref=self.assignment_ref,
            materiality_class="D2_ARCHITECTURE_PRODUCT",
            decision_question="Select storage design for a bounded governed component",
            requirement_refs=("REQ-1", "REQ-2"),
            constraint_refs=("CONSTRAINT-BUDGET", "CONSTRAINT-RECOVERY"),
            option_refs=("OPT-A", "OPT-B", "OPT-C"),
            evidence_refs=("EVIDENCE-BENCHMARK", "EVIDENCE-VENDOR-DOC", "EVIDENCE-COST"),
            chosen_disposition="SELECT_OPTION",
            chosen_option_refs=("OPT-B",),
            rationale_summary="OPT-B satisfies hard recovery constraints within budget with lower operational burden than OPT-C.",
            review_refs=("REVIEW-INDEPENDENT-1",),
            verification_plan_ref="VERIFY-PLAN-1",
        )
        base.update(overrides)
        return GovernedProfessionalDecision(**base)

    def bind(self, *, decision=None, assessment=None):
        return DecisionContextBinder().bind(
            decision=decision or self.decision(),
            assessment=assessment or self.assessment(),
            expected_run_id=self.request.run_id,
            expected_role_ref=self.role_ref,
            expected_assignment_ref=self.assignment_ref,
        )

    def test_material_decision_cannot_bind_when_gate_is_not_passed(self):
        incomplete = self.assessment(
            evidence_categories_present=frozenset({"REQUIREMENTS", "CONSTRAINTS"})
        )
        with self.assertRaisesRegex(DecisionContextError, "MATERIALITY_GATE_INSUFFICIENT_EVIDENCE"):
            self.bind(assessment=incomplete)

    def test_decision_cannot_bind_to_wrong_run(self):
        with self.assertRaisesRegex(DecisionContextError, "DECISION_RUN_MISMATCH"):
            self.bind(decision=self.decision(run_id="RUN-OTHER"))

    def test_selected_option_must_be_declared(self):
        with self.assertRaisesRegex(DecisionContextError, "CHOSEN_OPTION_NOT_DECLARED"):
            self.bind(decision=self.decision(chosen_option_refs=("OPT-Z",)))

    def test_d2_decision_is_digest_pinned_into_trace_and_replay(self):
        context = self.bind()
        self.recorder.record_all(self.result.events)
        persisted = self.recorder.persist_manifest(self.request.trace_id, decision_context=context)

        self.assertEqual(persisted.manifest.decision_refs, ("DEC-ARCH-0001",))
        self.assertEqual(persisted.manifest.decision_materiality_classes, ("D2_ARCHITECTURE_PRODUCT",))

        report = self.replay.verify(
            request=self.request,
            authority=self.result.authority_decision,
            snapshot=self.result.policy_snapshot,
            events=self.result.events,
            decision_context=context,
        )
        self.assertEqual(report.status, "VERIFIED_RECORD")
        self.assertTrue(report.decision_context_verified)
        self.assertEqual(report.reason_code, "GOVERNED_LINEAGE_AND_DECISION_CONTEXT_VERIFIED")

    def test_replay_cannot_silently_omit_persisted_decision_context(self):
        context = self.bind()
        self.recorder.record_all(self.result.events)
        self.recorder.persist_manifest(self.request.trace_id, decision_context=context)

        report = self.replay.verify(
            request=self.request,
            authority=self.result.authority_decision,
            snapshot=self.result.policy_snapshot,
            events=self.result.events,
        )
        self.assertEqual(report.status, "TAMPER_DETECTED")
        self.assertEqual(report.reason_code, "TRACE_DECISION_CONTEXT_EXPECTATION_REQUIRED")

    def test_replay_detects_decision_digest_substitution(self):
        context = self.bind()
        self.recorder.record_all(self.result.events)
        self.recorder.persist_manifest(self.request.trace_id, decision_context=context)
        changed = replace(context, decision_digests=("0" * 64,))

        report = self.replay.verify(
            request=self.request,
            authority=self.result.authority_decision,
            snapshot=self.result.policy_snapshot,
            events=self.result.events,
            decision_context=changed,
        )
        self.assertEqual(report.status, "TAMPER_DETECTED")
        self.assertEqual(report.reason_code, "TRACE_MANIFEST_EVENT_OR_DECISION_CONTEXT_MISMATCH")


if __name__ == "__main__":
    unittest.main()
