from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load(rel: str):
    with (ROOT / rel).open("r", encoding="utf-8") as stream:
        return yaml.safe_load(stream)


class PolicyLineageContractTests(unittest.TestCase):
    def test_run_record_requires_policy_snapshot_lineage(self):
        doc = load("schemas/RUN_RECORD.yaml")
        policy = doc.get("policy") or {}
        self.assertIn("policy_snapshot_ref", policy)
        self.assertIn("policy_snapshot_hash", policy)
        self.assertEqual(policy.get("hash_algorithm"), "sha256")
        invariants = set(doc.get("invariants") or [])
        self.assertIn("policy_snapshot_is_fixed_for_run_unless_explicit_migration_occurs", invariants)
        self.assertIn("material_authority_decisions_must_match_run_policy_snapshot_ref_and_hash", invariants)

    def test_authority_decision_requires_same_snapshot_identity_and_hash(self):
        doc = load("schemas/AUTHORITY_DECISION.yaml")
        required = doc.get("required_fields") or {}
        for field in (
            "run_id",
            "action_request_id",
            "policy_snapshot_ref",
            "policy_snapshot_hash",
            "policy_hash_algorithm",
        ):
            self.assertIn(field, required)
        self.assertEqual(required["policy_hash_algorithm"].get("values"), ["sha256"])
        invariants = set(doc.get("invariants") or [])
        self.assertIn("authority_decision_policy_snapshot_must_match_bound_run_snapshot", invariants)
        self.assertIn("policy_snapshot_hash_mismatch_is_blocking", invariants)
        self.assertIn("policy_snapshot_lineage_cannot_be_changed_by_executor_output", invariants)

    def test_policy_snapshot_separates_runtime_identity_from_content_hash(self):
        doc = load("schemas/POLICY_SNAPSHOT.yaml")
        invariants = set(doc.get("invariants") or [])
        self.assertIn("snapshot_runtime_identity_is_distinct_per_run", invariants)
        self.assertIn(
            "equal_policy_content_may_have_equal_hash_across_runs_without_equal_snapshot_identity",
            invariants,
        )
        required = doc.get("required_fields") or {}
        self.assertEqual(required["hash_algorithm"].get("values"), ["sha256"])


if __name__ == "__main__":
    unittest.main()
