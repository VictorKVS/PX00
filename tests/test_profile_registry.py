from __future__ import annotations

import unittest
from dataclasses import replace

from px00.policy import REQUIRED_PROFILE_TYPES, synthetic_policy_profiles
from px00.profile_registry import PolicyProfileRegistry, ProfileRegistryError


def exact_request(profiles):
    return {p.profile_type: (p.profile_id, p.version) for p in profiles}


class PolicyProfileRegistryTests(unittest.TestCase):
    def setUp(self):
        self.profiles = synthetic_policy_profiles()
        self.registry = PolicyProfileRegistry(self.profiles)
        self.requested = exact_request(self.profiles)

    def test_exact_resolution_covers_all_required_types(self):
        resolved = self.registry.resolve_exact(self.requested)
        self.assertEqual({p.profile_type for p in resolved}, set(REQUIRED_PROFILE_TYPES))

    def test_missing_required_type_fails_closed(self):
        requested = dict(self.requested)
        requested.pop("JURISDICTION")
        with self.assertRaisesRegex(ProfileRegistryError, "MISSING_PROFILE_TYPES"):
            self.registry.resolve_exact(requested)

    def test_unknown_exact_version_fails_closed(self):
        requested = dict(self.requested)
        profile_id, _ = requested["PROJECT"]
        requested["PROJECT"] = (profile_id, "9.9.9")
        with self.assertRaisesRegex(ProfileRegistryError, "PROFILE_VERSION_NOT_FOUND"):
            self.registry.resolve_exact(requested)

    def test_inactive_profile_cannot_enter_new_snapshot(self):
        project = next(p for p in self.profiles if p.profile_type == "PROJECT")
        inactive = replace(project, version="0.2.0", status="SUSPENDED")
        self.registry.register(inactive)
        requested = dict(self.requested)
        requested["PROJECT"] = (inactive.profile_id, inactive.version)
        with self.assertRaisesRegex(ProfileRegistryError, "PROFILE_NOT_ACTIVE"):
            self.registry.snapshot(run_id="RUN-2", requested=requested)

    def test_duplicate_exact_profile_version_is_rejected(self):
        with self.assertRaisesRegex(ProfileRegistryError, "DUPLICATE_PROFILE_VERSION"):
            self.registry.register(self.profiles[0])

    def test_profile_order_does_not_change_hash(self):
        forward = self.registry.snapshot_hash(self.profiles)
        reverse = self.registry.snapshot_hash(tuple(reversed(self.profiles)))
        self.assertEqual(forward, reverse)

    def test_material_policy_change_changes_hash(self):
        changed = list(self.profiles)
        changed[0] = replace(changed[0], operation_count_limit=2)
        self.assertNotEqual(
            self.registry.snapshot_hash(self.profiles),
            self.registry.snapshot_hash(changed),
        )

    def test_same_policy_content_has_same_hash_but_distinct_run_snapshot_identity(self):
        first = self.registry.snapshot(run_id="RUN-A", requested=self.requested)
        second = self.registry.snapshot(run_id="RUN-B", requested=self.requested)
        self.assertEqual(first.snapshot_hash, second.snapshot_hash)
        self.assertNotEqual(first.snapshot_id, second.snapshot_id)
        self.assertNotEqual(first.run_id, second.run_id)

    def test_existing_snapshot_does_not_migrate_after_registry_update(self):
        snapshot = self.registry.snapshot(run_id="RUN-OLD", requested=self.requested)
        project = next(p for p in self.profiles if p.profile_type == "PROJECT")
        newer = replace(project, version="0.2.0", autonomy_ceiling="A0")
        self.registry.register(newer)
        self.assertEqual(snapshot.profile_refs, tuple(sorted(f"{p.profile_id}@{p.version}" for p in self.profiles)))
        self.assertTrue(all("@0.2.0" not in ref for ref in snapshot.profile_refs))
        self.assertEqual(snapshot.snapshot_hash, self.registry.snapshot_hash(snapshot.profiles))

    def test_new_run_can_explicitly_pin_new_version(self):
        project = next(p for p in self.profiles if p.profile_type == "PROJECT")
        newer = replace(project, version="0.2.0", autonomy_ceiling="A0")
        self.registry.register(newer)
        requested = dict(self.requested)
        requested["PROJECT"] = (newer.profile_id, newer.version)
        snapshot = self.registry.snapshot(run_id="RUN-NEW", requested=requested)
        self.assertIn(f"{newer.profile_id}@0.2.0", snapshot.profile_refs)
        self.assertEqual(next(p for p in snapshot.profiles if p.profile_type == "PROJECT").autonomy_ceiling, "A0")


if __name__ == "__main__":
    unittest.main()
