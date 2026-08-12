import unittest

from px00.executors import ExecutorDefinition, GovernedExecutorBoundary, ScriptedExecutorAdapter
from px00.factory_executor_case import _advance_to_implementation, run_replaceable_executor_case
from px00.factory_mvp import AgentRdFactoryMvp
from px00.factory_mvp_case import PRODUCER, VERIFIER
from px00.factory_mvp_suite import run_security_block_case


class GovernedExecutorBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.mvp = AgentRdFactoryMvp()
        self.run_id = "EXEC-TEST-RUN"
        self.mvp.create_run(self.run_id, "P", PRODUCER, VERIFIER)
        _advance_to_implementation(self.mvp, self.run_id)
        self.boundary = GovernedExecutorBoundary()
        self.definition = ExecutorDefinition(
            executor_id="EXEC-TEST-1",
            executor_type="TEST_DOUBLE",
            version_ref="1.0",
            provider_ref="LOCAL_TEST",
            model_ref="test-model",
            allowed_stage_refs=("IMPLEMENT_BOUNDED_PROTOTYPE",),
        )
        self.boundary.register(self.definition)

    def invoke(self, output=None, assignment_ref=PRODUCER):
        return self.boundary.invoke_to_artifact(
            self.mvp,
            run_id=self.run_id,
            invocation_id="INV-1",
            executor_id=self.definition.executor_id,
            assignment_ref=assignment_ref,
            bounded_input={"x": 1},
            artifact_id="EXEC-ART-1",
            adapter=ScriptedExecutorAdapter(outputs=[output or {"candidate": 2}]),
            created_at="2026-08-12T19:40:00Z",
        )

    def test_invocation_pins_executor_assignment_and_hashes(self):
        record = self.invoke()
        self.assertEqual(record.executor_ref, "EXEC-TEST-1")
        self.assertEqual(record.executor_version_ref, "1.0")
        self.assertEqual(record.assignment_ref, PRODUCER)
        self.assertEqual(record.input_artifact_ref, "EX-ART-005")
        self.assertEqual(len(record.bounded_input_hash), 64)
        self.assertEqual(len(record.output_candidate_hash), 64)
        payload = self.mvp.artifact_payload("EXEC-ART-1")
        provenance = payload["executor_provenance"]
        self.assertEqual(provenance["invocation_ref"], "INV-1")
        self.assertEqual(provenance["executor_ref"], "EXEC-TEST-1")
        self.assertEqual(provenance["executor_version_ref"], "1.0")

    def test_wrong_assignment_is_rejected_before_adapter_call(self):
        adapter = ScriptedExecutorAdapter(outputs=[{"candidate": 2}])
        with self.assertRaisesRegex(ValueError, "EXECUTOR_ASSIGNMENT_MISMATCH"):
            self.boundary.invoke_to_artifact(
                self.mvp,
                run_id=self.run_id,
                invocation_id="INV-X",
                executor_id=self.definition.executor_id,
                assignment_ref=VERIFIER,
                bounded_input={"x": 1},
                artifact_id="EXEC-ART-X",
                adapter=adapter,
                created_at="2026-08-12T19:40:00Z",
            )
        self.assertEqual(adapter.call_count, 0)

    def test_executor_cannot_inject_structured_authority(self):
        with self.assertRaisesRegex(ValueError, "EXECUTOR_OUTPUT_AUTHORITY_INJECTION"):
            self.invoke({"tool_call": {"name": "shell"}})
        self.assertNotIn("INV-1", self.boundary.invocations)
        self.assertNotIn("EXEC-ART-1", self.mvp.artifacts)

    def test_external_effect_executor_is_forbidden_in_m1(self):
        boundary = GovernedExecutorBoundary()
        boundary.register(ExecutorDefinition(
            executor_id="EXEC-EFFECT",
            executor_type="TEST_DOUBLE",
            version_ref="1.0",
            provider_ref="LOCAL_TEST",
            model_ref=None,
            allowed_stage_refs=("IMPLEMENT_BOUNDED_PROTOTYPE",),
            external_effects_allowed=True,
        ))
        adapter = ScriptedExecutorAdapter(outputs=[{"candidate": 2}])
        with self.assertRaisesRegex(ValueError, "EXTERNAL_EFFECTS_FORBIDDEN_IN_M1"):
            boundary.invoke_to_artifact(
                self.mvp,
                run_id=self.run_id,
                invocation_id="INV-E",
                executor_id="EXEC-EFFECT",
                assignment_ref=PRODUCER,
                bounded_input={"x": 1},
                artifact_id="EXEC-ART-E",
                adapter=adapter,
                created_at="2026-08-12T19:40:00Z",
            )
        self.assertEqual(adapter.call_count, 0)

    def test_security_block_occurs_before_executor_invocation(self):
        blocked_mvp, blocked_run_id, _ = run_security_block_case()
        boundary = GovernedExecutorBoundary()
        boundary.register(self.definition)
        adapter = ScriptedExecutorAdapter(outputs=[{"candidate": "should-not-run"}])
        with self.assertRaisesRegex(ValueError, "EXECUTOR_STAGE_NOT_ALLOWED"):
            boundary.invoke_to_artifact(
                blocked_mvp,
                run_id=blocked_run_id,
                invocation_id="INV-BLOCKED",
                executor_id=self.definition.executor_id,
                assignment_ref=PRODUCER,
                bounded_input={"shell": "echo unsafe"},
                artifact_id="EXEC-ART-BLOCKED",
                adapter=adapter,
                created_at="2026-08-12T19:40:00Z",
            )
        self.assertEqual(adapter.call_count, 0)

    def test_replaceable_executor_case_preserves_bad_and_good_worker_history(self):
        mvp, boundary, run_id = run_replaceable_executor_case()
        run = mvp.runs[run_id]
        self.assertTrue(run.delivered)
        self.assertEqual(run.rework_count, 1)
        first = boundary.invocations["EXEC-INV-0001"]
        second = boundary.invocations["EXEC-INV-0002"]
        self.assertEqual(first.executor_ref, "EXEC-TAG-NORM-0001")
        self.assertEqual(first.executor_version_ref, "0.1")
        self.assertEqual(second.executor_ref, "EXEC-TAG-NORM-0002")
        self.assertEqual(second.executor_version_ref, "0.2")
        self.assertEqual(mvp.artifacts["EX-ART-008"].input_artifact_refs, ("EX-ART-007",))
        self.assertIn("VERIFY_AND_VALIDATE:FAIL", run.trace)
        self.assertIn(
            "REWORK:VERIFY_AND_VALIDATE->IMPLEMENT_BOUNDED_PROTOTYPE:EXEC-FINDING-0001",
            run.trace,
        )
        delivery = mvp.artifact_payload("EX-ART-012")
        self.assertFalse(delivery["live_provider_claim"])


if __name__ == "__main__":
    unittest.main()
