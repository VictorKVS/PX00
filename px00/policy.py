from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

AUTONOMY_ORDER = {f"A{i}": i for i in range(5)}
SIDE_EFFECT_ORDER = {f"S{i}": i for i in range(5)}
REQUIRED_PROFILE_TYPES = frozenset(
    {"ROLE", "PROTOCOL", "PROJECT", "ORGANIZATION", "JURISDICTION", "TOOL", "DATA", "APPROVAL"}
)


@dataclass(frozen=True)
class PolicyProfile:
    profile_id: str
    profile_type: str
    version: str
    allowed_capabilities: frozenset[str]
    autonomy_ceiling: str
    side_effect_ceiling: str
    allowed_data_classifications: frozenset[str]
    operation_count_limit: int
    allowed_target_prefixes: tuple[str, ...] = ()
    approval_required_capabilities: frozenset[str] = frozenset()
    approval_present: bool = False
    capability_denies: frozenset[str] = frozenset()
    status: str = "ACTIVE"


@dataclass(frozen=True)
class PolicyDecision:
    result: str
    reason_code: str
    effective_autonomy: str
    effective_side_effect_ceiling: str
    effective_operation_count_limit: int
    profile_refs: tuple[str, ...]
    constraining_profile: str | None = None


class PolicyEngine:
    """Deterministic fail-closed restrictive profile intersection."""

    def evaluate(
        self,
        profiles: Iterable[PolicyProfile],
        *,
        capability: str,
        requested_autonomy: str,
        side_effect_class: str,
        classification: str,
        target_ref: str,
    ) -> PolicyDecision:
        items = tuple(profiles)
        refs = tuple(sorted(f"{p.profile_id}@{p.version}" for p in items))

        by_type = {p.profile_type for p in items if p.status == "ACTIVE"}
        missing = sorted(REQUIRED_PROFILE_TYPES - by_type)
        if missing:
            return self._deny(
                "MISSING_POLICY_PROFILE",
                items,
                refs,
                constraining_profile=",".join(missing),
            )

        inactive = sorted(p.profile_id for p in items if p.status != "ACTIVE")
        if inactive:
            return self._deny(
                "INACTIVE_POLICY_PROFILE",
                items,
                refs,
                constraining_profile=inactive[0],
            )

        for profile in items:
            if capability in profile.capability_denies:
                return self._deny("CAPABILITY_EXPLICITLY_DENIED", items, refs, profile.profile_id)
            if capability not in profile.allowed_capabilities:
                return self._deny("CAPABILITY_NOT_ALLOWED", items, refs, profile.profile_id)
            if classification not in profile.allowed_data_classifications:
                return self._deny("DATA_CLASSIFICATION_NOT_ALLOWED", items, refs, profile.profile_id)
            if profile.allowed_target_prefixes and not any(
                target_ref.startswith(prefix) for prefix in profile.allowed_target_prefixes
            ):
                return self._deny("TARGET_SCOPE_NOT_ALLOWED", items, refs, profile.profile_id)

        autonomy_profile = min(items, key=lambda p: AUTONOMY_ORDER[p.autonomy_ceiling])
        side_effect_profile = min(items, key=lambda p: SIDE_EFFECT_ORDER[p.side_effect_ceiling])
        operation_profile = min(items, key=lambda p: p.operation_count_limit)

        effective_autonomy = autonomy_profile.autonomy_ceiling
        effective_side_effect = side_effect_profile.side_effect_ceiling
        effective_operations = operation_profile.operation_count_limit

        if AUTONOMY_ORDER[requested_autonomy] > AUTONOMY_ORDER[effective_autonomy]:
            return PolicyDecision(
                result="DENY",
                reason_code="AUTONOMY_CEILING_EXCEEDED",
                effective_autonomy=effective_autonomy,
                effective_side_effect_ceiling=effective_side_effect,
                effective_operation_count_limit=effective_operations,
                profile_refs=refs,
                constraining_profile=autonomy_profile.profile_id,
            )

        if SIDE_EFFECT_ORDER[side_effect_class] > SIDE_EFFECT_ORDER[effective_side_effect]:
            return PolicyDecision(
                result="DENY",
                reason_code="SIDE_EFFECT_CEILING_EXCEEDED",
                effective_autonomy=effective_autonomy,
                effective_side_effect_ceiling=effective_side_effect,
                effective_operation_count_limit=effective_operations,
                profile_refs=refs,
                constraining_profile=side_effect_profile.profile_id,
            )

        approval_profiles = tuple(
            p for p in items if capability in p.approval_required_capabilities
        )
        missing_approval = tuple(p for p in approval_profiles if not p.approval_present)
        if missing_approval:
            return PolicyDecision(
                result="ESCALATE",
                reason_code="APPROVAL_REQUIRED",
                effective_autonomy=effective_autonomy,
                effective_side_effect_ceiling=effective_side_effect,
                effective_operation_count_limit=effective_operations,
                profile_refs=refs,
                constraining_profile=sorted(p.profile_id for p in missing_approval)[0],
            )

        return PolicyDecision(
            result="ALLOW",
            reason_code="EFFECTIVE_POLICY_ALLOWED",
            effective_autonomy=effective_autonomy,
            effective_side_effect_ceiling=effective_side_effect,
            effective_operation_count_limit=effective_operations,
            profile_refs=refs,
        )

    @staticmethod
    def _deny(
        reason: str,
        profiles: tuple[PolicyProfile, ...],
        refs: tuple[str, ...],
        constraining_profile: str | None = None,
    ) -> PolicyDecision:
        active = tuple(p for p in profiles if p.status == "ACTIVE") or profiles
        autonomy = min((p.autonomy_ceiling for p in active), key=lambda x: AUTONOMY_ORDER[x], default="A0")
        side_effect = min((p.side_effect_ceiling for p in active), key=lambda x: SIDE_EFFECT_ORDER[x], default="S0")
        operations = min((p.operation_count_limit for p in active), default=1)
        return PolicyDecision(
            result="DENY",
            reason_code=reason,
            effective_autonomy=autonomy,
            effective_side_effect_ceiling=side_effect,
            effective_operation_count_limit=operations,
            profile_refs=refs,
            constraining_profile=constraining_profile,
        )


def synthetic_policy_profiles(*, approval_present: bool = True) -> tuple[PolicyProfile, ...]:
    """Reference profiles for the public-safe math.multiply proof."""

    capability = frozenset({"math.multiply"})
    classifications = frozenset({"PUBLIC"})
    profiles = []
    for profile_type in sorted(REQUIRED_PROFILE_TYPES):
        profiles.append(
            PolicyProfile(
                profile_id=f"POLICY-{profile_type}-SYNTHETIC",
                profile_type=profile_type,
                version="0.1.0",
                allowed_capabilities=capability,
                autonomy_ceiling="A1",
                side_effect_ceiling="S0",
                allowed_data_classifications=classifications,
                operation_count_limit=1,
                allowed_target_prefixes=("synthetic://",),
                approval_required_capabilities=frozenset({"math.multiply"}) if profile_type == "APPROVAL" else frozenset(),
                approval_present=approval_present if profile_type == "APPROVAL" else False,
            )
        )
    return tuple(profiles)
