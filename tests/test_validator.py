from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from px00.validator import (
    validate_acceptance_fixture_document,
    validate_action_request_document,
    validate_capability_grant_document,
    validate_protocol_document,
    validate_repository,
    validate_role_document,
    validate_tool_definition_document,
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


class GovernedActionSchemaValidationTests(unittest.TestCase):
    def valid_action_request_schema(self):
        return {
            "canonical_prefix": "ACTREQ-",
            "required_fields": {
                "action_request_id": {}, "status": {}, "created_at": {}, "task_id": {},
                "run_id": {}, "trace_id": {}, "requester_role_id": {}, "requester_role_version": {},
                "protocol_id": {}, "protocol_version": {}, "step_id": {}, "capability": {},
                "action_class": {}, "target_ref": {}, "purpose_code": {},
                "requested_autonomy": {"values": ["A0", "A1", "A2", "A3", "A4"]},
                "classification": {},
                "side_effect_class": {"values": ["S0", "S1", "S2", "S3", "S4"]},
            },
            "invariants": [
                "action_request_is_not_authority",
                "material_execution_requires_linked_allow_authority_decision",
                "requested_adapter_hint_does_not_grant_adapter_permission",
                "untrusted_executor_output_cannot_directly_mutate_control_plane",
            ],
        }

    def valid_tool_schema(self):
        return {
            "canonical_object": False,
            "required_fields": {
                "tool_id": {}, "version": {}, "name": {}, "status": {}, "capabilities": {},
                "adapter_classes": {},
                "supported_side_effect_classes": {"item_enum": ["S0", "S1", "S2", "S3", "S4"]},
                "supported_data_classifications": {},
            },
            "invariants": [
                "tool_definition_does_not_grant_authority",
                "adapter_implementation_cannot_expand_declared_capability",
                "unsupported_side_effect_class_cannot_execute",
                "unsupported_data_classification_cannot_execute",
            ],
        }

    def valid_grant_schema(self):
        return {
            "canonical_object": False,
            "required_fields": {
                "grant_id": {}, "action_request_id": {}, "authority_decision_ref": {},
                "capability": {}, "target_scope": {}, "issued_at": {}, "status": {},
                "side_effect_ceiling": {"values": ["S0", "S1", "S2", "S3", "S4"]},
                "data_classification_ceiling": {}, "operation_count_limit": {},
            },
            "invariants": [
                "grant_requires_allow_authority_decision",
                "grant_scope_cannot_exceed_authority_decision",
                "grant_capability_must_match_action_request",
                "expired_revoked_or_consumed_one_time_grant_cannot_execute",
                "replay_policy_is_enforced",
            ],
        }

    def test_valid_action_request_schema(self):
        self.assertEqual(validate_action_request_document(self.valid_action_request_schema()), [])

    def test_action_request_cannot_lose_control_plane_injection_guard(self):
        doc = self.valid_action_request_schema()
        doc["invariants"].remove("untrusted_executor_output_cannot_directly_mutate_control_plane")
        self.assertIn("ACTREQ_INVARIANT_MISSING", codes(validate_action_request_document(doc)))

    def test_valid_tool_schema(self):
        self.assertEqual(validate_tool_definition_document(self.valid_tool_schema()), [])

    def test_tool_side_effect_scale_must_be_complete(self):
        doc = self.valid_tool_schema()
        doc["required_fields"]["supported_side_effect_classes"]["item_enum"] = ["S0", "S1"]
        self.assertIn("TOOL_SIDE_EFFECT_VALUES_INVALID", codes(validate_tool_definition_document(doc)))

    def test_valid_capability_grant_schema(self):
        self.assertEqual(validate_capability_grant_document(self.valid_grant_schema()), [])

    def test_grant_replay_guard_is_required(self):
        doc = self.valid_grant_schema()
        doc["invariants"].remove("replay_policy_is_enforced")
        self.assertIn("GRANT_INVARIANT_MISSING", codes(validate_capability_grant_document(doc)))


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
