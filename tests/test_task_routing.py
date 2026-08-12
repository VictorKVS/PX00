import unittest
from dataclasses import replace

from px00.context_packages import ContextPackage
from px00.staffing import AgentAssignment, RoleResponsibility
from px00.task_routing import TaskRouter, TaskRoutingRequest


class TaskRouterTests(unittest.TestCase):
    def setUp(self):
        self.router = TaskRouter()
        self.responsibility = RoleResponsibility(
            responsibility_id="RESP-ANALYZE-1", role_id="ROLE-ANALYST", department_id="DEPT-ANALYSIS",
            duty_code="ANALYZE_EVIDENCE", description="Analyze evidence", allowed_protocol_refs=("PROTO-ANALYSIS",),
            knowledge_binding_refs=("KBI-ANALYSIS",), required_outputs=("FIND",), escalation_conditions=("INSUFFICIENT_EVIDENCE",),
        )
        self.assignment = AgentAssignment(
            assignment_id="ASSIGN-ANALYST-1", agent_id="AGENT-17", role_id="ROLE-ANALYST", department_id="DEPT-ANALYSIS",
            executor_type="LLM", model_ref="MODEL-A@1", knowledge_binding_refs=("KBI-ANALYSIS",), status="ACTIVE",
        )
        self.context = ContextPackage(
            context_package_id="CTX-1", knowledge_request_ref="KREQ-1", run_ref="RUN-1", role_ref="ROLE-ANALYST",
            assignment_ref="ASSIGN-ANALYST-1", binding_refs=("KBI-ANALYSIS",), knowledge_object_refs=("EVD-1",),
            route_snapshot_refs=("KBROUTE-1@v1",), package_hash="a" * 64,
        )
        self.request = TaskRoutingRequest("TASK-1", "RUN-1", "ANALYZE_EVIDENCE", "PROTO-ANALYSIS")

    def test_routes_by_responsibility_and_pins_exact_executor(self):
        decision, pin = self.router.route(self.request, responsibilities=(self.responsibility,), assignments=(self.assignment,),
                                          context_packages=(self.context,), routing_decision_id="ROUTEDEC-1")
        self.assertEqual(decision.responsibility_ref, "RESP-ANALYZE-1")
        self.assertEqual(decision.assignment_ref, "ASSIGN-ANALYST-1")
        self.assertEqual(pin.model_ref, "MODEL-A@1")
        self.assertEqual(pin.context_package_hash, "a" * 64)
        self.router.verify_pin(pin, assignment=self.assignment, responsibility=self.responsibility, context=self.context)

    def test_suspended_assignment_is_not_selected(self):
        with self.assertRaisesRegex(ValueError, "NO_ELIGIBLE_ACTIVE_ASSIGNMENT_WITH_CONTEXT"):
            self.router.route(self.request, responsibilities=(self.responsibility,), assignments=(replace(self.assignment, status="SUSPENDED"),),
                              context_packages=(self.context,), routing_decision_id="ROUTEDEC-1")

    def test_wrong_duty_has_no_eligible_responsibility(self):
        with self.assertRaisesRegex(ValueError, "NO_ELIGIBLE_RESPONSIBILITY"):
            self.router.route(replace(self.request, required_duty_code="WRITE_REPORT"), responsibilities=(self.responsibility,),
                              assignments=(self.assignment,), context_packages=(self.context,), routing_decision_id="ROUTEDEC-1")

    def test_context_for_other_assignment_is_not_usable(self):
        bad = replace(self.context, assignment_ref="ASSIGN-OTHER")
        with self.assertRaisesRegex(ValueError, "NO_ELIGIBLE_ACTIVE_ASSIGNMENT_WITH_CONTEXT"):
            self.router.route(self.request, responsibilities=(self.responsibility,), assignments=(self.assignment,),
                              context_packages=(bad,), routing_decision_id="ROUTEDEC-1")

    def test_assignment_without_required_role_knowledge_is_not_eligible(self):
        bad = replace(self.assignment, knowledge_binding_refs=())
        with self.assertRaisesRegex(ValueError, "NO_ELIGIBLE_ACTIVE_ASSIGNMENT_WITH_CONTEXT"):
            self.router.route(self.request, responsibilities=(self.responsibility,), assignments=(bad,),
                              context_packages=(self.context,), routing_decision_id="ROUTEDEC-1")

    def test_later_model_change_breaks_historical_pin_verification(self):
        _, pin = self.router.route(self.request, responsibilities=(self.responsibility,), assignments=(self.assignment,),
                                   context_packages=(self.context,), routing_decision_id="ROUTEDEC-1")
        with self.assertRaisesRegex(ValueError, "PIN_EXECUTOR_MISMATCH"):
            self.router.verify_pin(pin, assignment=replace(self.assignment, model_ref="MODEL-B@2"),
                                   responsibility=self.responsibility, context=self.context)

    def test_context_hash_tampering_breaks_pin(self):
        _, pin = self.router.route(self.request, responsibilities=(self.responsibility,), assignments=(self.assignment,),
                                   context_packages=(self.context,), routing_decision_id="ROUTEDEC-1")
        with self.assertRaisesRegex(ValueError, "PIN_CONTEXT_MISMATCH"):
            self.router.verify_pin(pin, assignment=self.assignment, responsibility=self.responsibility,
                                   context=replace(self.context, package_hash="b" * 64))


if __name__ == "__main__":
    unittest.main()
