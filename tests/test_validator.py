from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from px00.validator import (
    validate_acceptance_fixture_document,
    validate_protocol_document,
    validate_repository,
    validate_role_document,
    validate_tree_f,
)


def codes(issues):
    return {issue.code for issue in issues}


class RoleValidationTests(unittest.TestCase):
    def valid_role(self):
        return {
            "identity": {
                "role_id": "ROLE-0201",
                "canonical_name": "analyst",
                "package_version": "0.1.0",
                "status": "pilot",
            },
            "mission": {"purpose": "Analyze evidence."},
            "authority": {
                "autonomy_level": "A1",
                "allowed_actions": ["read"],
                "prohibited_actions": ["execute_external_side_effects"],
                "human_approval_required_for": ["any_action_outside_A1"],
            },
            "knowledge": {"retrieval_is_evidence": False},
            "protocols": {},
            "schemas": {},
            "evaluation": {},
            "traceability": {
                "task_id_required": True,
                "run_id_required": True,
                "trace_id_required": True,
                "protocol_version_required": True,
                "material_input_ids_required": True,
                "material_output_ids_required": True,
            },
            "failure_policy": {},
            "security": {"secrets_in_role_package": "prohibited"},
        }

    def test_valid_low_autonomy_role(self):
        self.assertEqual(validate_role_document(self.valid_role()), [])

    def test_low_autonomy_role_must_block_external_side_effects(self):
        doc = self.valid_role()
        doc["authority"]["prohibited_actions"] = []
        self.assertIn("ROLE_LOW_AUTONOMY_SIDE_EFFECT_GUARD_MISSING", codes(validate_role_document(doc)))

    def test_retrieval_cannot_be_evidence(self):
        doc = self.valid_role()
        doc["knowledge"]["retrieval_is_evidence"] = True
        self.assertIn("ROLE_RETRIEVAL_EVIDENCE_POLICY", codes(validate_role_document(doc)))

    def test_secret_like_value_is_rejected(self):
        doc = self.valid_role()
        doc["provider_config"] = {"api_key": "real-looking-secret"}
        self.assertIn("POTENTIAL_SECRET", codes(validate_role_document(doc)))


class ProtocolValidationTests(unittest.TestCase):
    def valid_protocol(self):
        return {
            "protocol_id": "PROTO-0201",
            "version": "0.1.0",
            "status": "pilot",
            "purpose": "Bounded analysis.",
            "bounds": {
                "max_evidence_request_cycles": 3,
                "unbounded_loops": "prohibited",
            },
            "steps": [
                {
                    "step_id": "A01",
                    "purpose": "Validate.",
                    "action_class": "validate",
                    "success_condition": "valid",
                    "failure_transition": "FAIL",
                    "event_requirement": "material_gate_event",
                }
            ],
            "completion_criteria": ["output_persisted"],
            "terminal_states": [
                "COMPLETED",
                "FAILED",
                "DENIED",
                "ESCALATED",
                "CANCELLED",
                "BLOCKED",
            ],
        }

    def test_valid_protocol(self):
        self.assertEqual(validate_protocol_document(self.valid_protocol()), [])

    def test_unbounded_loop_policy_is_rejected(self):
        doc = self.valid_protocol()
        doc["bounds"]["unbounded_loops"] = "allowed"
        self.assertIn("PROTOCOL_UNBOUNDED_LOOP", codes(validate_protocol_document(doc)))

    def test_protocol_requires_enforceable_bound(self):
        doc = self.valid_protocol()
        doc["bounds"] = {"unbounded_loops": "prohibited"}
        self.assertIn("PROTOCOL_BOUND_NOT_ENFORCEABLE", codes(validate_protocol_document(doc)))

    def test_optional_step_requires_condition(self):
        doc = self.valid_protocol()
        doc["steps"][0]["optional"] = True
        self.assertIn("PROTOCOL_OPTIONAL_CONDITION_MISSING", codes(validate_protocol_document(doc)))


class AcceptanceValidationTests(unittest.TestCase):
    def test_pass_gate_requires_evidence_rule(self):
        doc = {
            "status": "NOT_TESTED",
            "blocking_criteria": [{"id": "A", "expected": "PASS"}],
            "acceptance_state_rule": {"pass_requires_all_blocking_criteria_with_evidence": False},
            "security": {"runtime_side_effects": "prohibited"},
        }
        self.assertIn("ACCEPTANCE_EVIDENCE_GATE_MISSING", codes(validate_acceptance_fixture_document(doc, "fixture")))

    def test_pilot_fixture_must_prohibit_side_effects(self):
        doc = {
            "status": "NOT_TESTED",
            "blocking_criteria": [{"id": "A", "expected": "PASS"}],
            "acceptance_state_rule": {"pass_requires_all_blocking_criteria_with_evidence": True},
            "security": {"runtime_side_effects": "allowed"},
        }
        self.assertIn("PILOT_RUNTIME_SIDE_EFFECT_POLICY", codes(validate_acceptance_fixture_document(doc, "fixture")))


class TreeFValidationTests(unittest.TestCase):
    def test_sequence_is_contiguous(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tree = root / "Tree_F"
            tree.mkdir()
            (tree / "TF-0001_A.md").write_text("# 1", encoding="utf-8")
            (tree / "TF-0002_B.md").write_text("# 2", encoding="utf-8")
            self.assertEqual(validate_tree_f(root), [])

    def test_gap_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tree = root / "Tree_F"
            tree.mkdir()
            (tree / "TF-0001_A.md").write_text("# 1", encoding="utf-8")
            (tree / "TF-0003_C.md").write_text("# 3", encoding="utf-8")
            self.assertIn("TREE_F_SEQUENCE_GAP", codes(validate_tree_f(root)))


class RepositoryIntegrationTests(unittest.TestCase):
    def test_current_repository_contracts(self):
        root = Path(__file__).resolve().parents[1]
        issues = validate_repository(root)
        details = "\n".join(f"{item.code} {item.path}: {item.message}" for item in issues)
        self.assertEqual(issues, [], details)


if __name__ == "__main__":
    unittest.main()
