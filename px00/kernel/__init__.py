"""Minimal governed execution kernel primitives for PX00.

The package is intentionally narrow. Production runtime, external side effects,
and model/tool autonomy remain outside the current gate.
"""

from .synthetic import (
    ActionRequest,
    AuthorityDecision,
    CapabilityGrant,
    GovernedResult,
    MaterialEvent,
    SyntheticGovernedKernel,
)

__all__ = [
    "ActionRequest",
    "AuthorityDecision",
    "CapabilityGrant",
    "GovernedResult",
    "MaterialEvent",
    "SyntheticGovernedKernel",
]
