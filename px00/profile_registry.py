from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Iterable, Mapping

from px00.policy import PolicyProfile, REQUIRED_PROFILE_TYPES


class ProfileRegistryError(ValueError):
    pass


@dataclass(frozen=True)
class PolicySnapshot:
    snapshot_id: str
    run_id: str
    profile_refs: tuple[str, ...]
    profile_types: tuple[str, ...]
    normalization: str
    hash_algorithm: str
    snapshot_hash: str
    profiles: tuple[PolicyProfile, ...]


class PolicyProfileRegistry:
    """Deterministic registry for exact-version policy resolution."""

    def __init__(self, profiles: Iterable[PolicyProfile] = ()) -> None:
        self._profiles: dict[tuple[str, str], PolicyProfile] = {}
        for profile in profiles:
            self.register(profile)

    def register(self, profile: PolicyProfile) -> None:
        key = (profile.profile_id, profile.version)
        if key in self._profiles:
            raise ProfileRegistryError("DUPLICATE_PROFILE_VERSION")
        self._profiles[key] = profile

    def resolve_exact(self, requested: Mapping[str, tuple[str, str]]) -> tuple[PolicyProfile, ...]:
        missing_types = sorted(REQUIRED_PROFILE_TYPES - set(requested))
        extra_types = sorted(set(requested) - REQUIRED_PROFILE_TYPES)
        if missing_types:
            raise ProfileRegistryError(f"MISSING_PROFILE_TYPES:{','.join(missing_types)}")
        if extra_types:
            raise ProfileRegistryError(f"UNKNOWN_PROFILE_TYPES:{','.join(extra_types)}")

        resolved: list[PolicyProfile] = []
        for profile_type in sorted(REQUIRED_PROFILE_TYPES):
            profile_id, version = requested[profile_type]
            profile = self._profiles.get((profile_id, version))
            if profile is None:
                raise ProfileRegistryError(f"PROFILE_VERSION_NOT_FOUND:{profile_id}@{version}")
            if profile.profile_type != profile_type:
                raise ProfileRegistryError(f"PROFILE_TYPE_MISMATCH:{profile_id}@{version}")
            if profile.status != "ACTIVE":
                raise ProfileRegistryError(f"PROFILE_NOT_ACTIVE:{profile_id}@{version}")
            resolved.append(profile)
        return tuple(resolved)

    def snapshot(self, *, run_id: str, requested: Mapping[str, tuple[str, str]]) -> PolicySnapshot:
        profiles = self.resolve_exact(requested)
        digest = self.snapshot_hash(profiles)
        runtime_identity = sha256(f"{run_id}:{digest}".encode("utf-8")).hexdigest()
        return PolicySnapshot(
            snapshot_id=f"POLSNAP-{runtime_identity[:16]}",
            run_id=run_id,
            profile_refs=tuple(sorted(f"{p.profile_id}@{p.version}" for p in profiles)),
            profile_types=tuple(sorted(p.profile_type for p in profiles)),
            normalization="deterministic_json_v1",
            hash_algorithm="sha256",
            snapshot_hash=digest,
            profiles=profiles,
        )

    @staticmethod
    def snapshot_hash(profiles: Iterable[PolicyProfile]) -> str:
        normalized = []
        for profile in profiles:
            item = asdict(profile)
            for key, value in tuple(item.items()):
                if isinstance(value, frozenset):
                    item[key] = sorted(value)
                elif isinstance(value, tuple):
                    item[key] = list(value)
            normalized.append(item)
        normalized.sort(key=lambda x: (x["profile_type"], x["profile_id"], x["version"]))
        encoded = json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        return sha256(encoded).hexdigest()
