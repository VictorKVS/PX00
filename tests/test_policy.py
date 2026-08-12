from __future__ import annotations

import unittest
from dataclasses import replace

from px00.policy import PolicyEngine, synthetic_policy_profiles


class PolicyEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = PolicyEngine()
        self.profiles = synthetic_policy_profiles()

    def evaluate(self, profiles=None, **overrides):
        args = {
            "capability": "math.multiply",
            "requested_autonomy": "A1",
            "side_effect_class": "S0",
            "classification": "PUBLIC",
            "target_ref": "synthetic://math.multiply",
        }
        args.update(overrides)
        return self.engine.evaluate(self.profiles if profiles is None else profiles, **args)

    def test_all_profiles_allow(self):
        result = self.evaluate()
        self.assertEqual(result.result, "ALLOW")
        self.assertEqual(result.reason_code, "EFFECTIVE_POLICY_ALLOWED")
        self.assertEqual(result.effective_autonomy, "A1")
        self.assertEqual(result.effective_side_effect_ceiling, "S0")

    def test_one_restrictive_profile_denies_capability(self):
        profiles = list(self.profiles)
        profiles[0] = replace(profiles[0], allowed_capabilities=frozenset())
        result = self.evaluate(tuple(profiles))
        self.assertEqual(result.result, "DENY")
        self.assertEqual(result.reason_code, "CAPABILITY_NOT_ALLOWED")

    def test_explicit_deny_overrides_allow(self):
        profiles = list(self.profiles)
        profiles[2] = replace(profiles[2], capability_denies=frozenset({"math.multiply"}))
        result = self.evaluate(tuple(profiles))
        self.assertEqual(result.result, "DENY")
        self.assertEqual(result.reason_code, "CAPABILITY_EXPLICITLY_DENIED")

    def test_lower_autonomy_ceiling_wins(self):
        profiles = list(self.profiles)
        profiles[1] = replace(profiles[1], autonomy_ceiling="A0")
        result = self.evaluate(tuple(profiles))
        self.assertEqual(result.result, "DENY")
        self.assertEqual(result.reason_code, "AUTONOMY_CEILING_EXCEEDED")
        self.assertEqual(result.effective_autonomy, "A0")

    def test_lower_side_effect_ceiling_wins(self):
        result = self.evaluate(side_effect_class="S1")
        self.assertEqual(result.result, "DENY")
        self.assertEqual(result.reason_code, "SIDE_EFFECT_CEILING_EXCEEDED")

    def test_target_mismatch_denies(self):
        result = self.evaluate(target_ref="external://resource")
        self.assertEqual(result.result, "DENY")
        self.assertEqual(result.reason_code, "TARGET_SCOPE_NOT_ALLOWED")

    def test_classification_mismatch_denies(self):
        result = self.evaluate(classification="SECRET")
        self.assertEqual(result.result, "DENY")
        self.assertEqual(result.reason_code, "DATA_CLASSIFICATION_NOT_ALLOWED")

    def test_missing_required_profile_fails_closed(self):
        profiles = tuple(p for p in self.profiles if p.profile_type != "JURISDICTION")
        result = self.evaluate(profiles)
        self.assertEqual(result.result, "DENY")
        self.assertEqual(result.reason_code, "MISSING_POLICY_PROFILE")

    def test_required_approval_without_approval_escalates(self):
        profiles = synthetic_policy_profiles(approval_present=False)
        result = self.evaluate(profiles)
        self.assertEqual(result.result, "ESCALATE")
        self.assertEqual(result.reason_code, "APPROVAL_REQUIRED")

    def test_profile_order_does_not_change_result(self):
        normal = self.evaluate(self.profiles)
        reversed_result = self.evaluate(tuple(reversed(self.profiles)))
        self.assertEqual(normal, reversed_result)

    def test_adding_stricter_profile_cannot_widen(self):
        baseline = self.evaluate(self.profiles)
        stricter = replace(
            self.profiles[0],
            profile_id="POLICY-EXTRA-STRICT",
            profile_type=self.profiles[0].profile_type,
            autonomy_ceiling="A0",
        )
        result = self.evaluate(self.profiles + (stricter,))
        self.assertEqual(baseline.result, "ALLOW")
        self.assertEqual(result.result, "DENY")
        self.assertEqual(result.effective_autonomy, "A0")

    def test_inactive_profile_cannot_authorize(self):
        profiles = list(self.profiles)
        profiles[0] = replace(profiles[0], status="SUSPENDED")
        result = self.evaluate(tuple(profiles))
        self.assertEqual(result.result, "DENY")
        self.assertEqual(result.reason_code, "MISSING_POLICY_PROFILE")


if __name__ == "__main__":
    unittest.main()
