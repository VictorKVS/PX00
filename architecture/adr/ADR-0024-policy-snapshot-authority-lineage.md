# ADR-0024 — Policy Snapshot Lineage in RUN and Authority Decisions

**Status:** ACCEPTED FOR IMPLEMENTATION  
**Date:** 2026-08-12  
**Decision:** KEEP

## Context

PX00 can now resolve exact policy-profile versions and create a deterministic SHA-256 policy snapshot bound to a RUN. However, the existing `RUN_RECORD` and `AUTHORITY_DECISION` contracts do not yet require that snapshot identity/hash to be carried through authority evaluation. Without that linkage, a later reviewer could know which policy snapshot existed for a run but not prove that a specific ALLOW/DENY/ESCALATE decision was evaluated against exactly that snapshot.

## Decision

Every governed RUN that uses policy evaluation SHALL pin one policy snapshot identity and hash before material authority decisions are issued.

Every material Authority Decision SHALL carry the same policy snapshot reference and hash. A mismatch between RUN-pinned policy snapshot and decision policy snapshot is a blocking integrity failure.

The lineage becomes:

```text
exact PolicyProfile versions
→ POLICY SNAPSHOT
→ RUN_RECORD.policy_snapshot_ref/hash
→ AUTHORITY_DECISION.policy_snapshot_ref/hash
→ ACTREQ
→ CapabilityGrant
→ Tool Boundary
→ EVT/ART
```

## Invariants

1. A RUN cannot claim governed policy execution without a pinned policy snapshot reference and hash.
2. A material Authority Decision for that RUN must reference the same snapshot identity and hash.
3. Policy snapshot hash mismatch blocks execution; it cannot be downgraded to a warning.
4. Newer policy-profile versions do not mutate an already pinned RUN.
5. AuthorityDecision rationale may summarize policy outcome but does not replace the snapshot evidence.
6. Capability grants may only derive from an ALLOW decision whose policy lineage matches the active RUN.
7. Executor/model/tool output cannot alter policy snapshot refs or hashes.

## Security rationale

The snapshot hash becomes the reproducibility anchor for authority. This prevents ambiguous reconstruction, silent policy drift, and a class of confused-deputy/TOCTOU errors where a request is evaluated under one policy state but executed as if another policy state applied.

## Technology

No new dependency. Existing SHA-256 deterministic normalization from `px00/profile_registry.py` remains the reference implementation.

## Verification

Tests must prove:

- valid matching RUN/AuthorityDecision snapshot linkage allows the synthetic path;
- snapshot reference mismatch blocks;
- snapshot hash mismatch blocks;
- a newer registered profile version does not alter the pinned hash;
- grant issuance rejects an AuthorityDecision whose policy lineage differs from the active snapshot.

## Related

- ADR-0020 — Minimal Governed Execution Kernel
- ADR-0021 — Governed Action Request and Universal Tool Boundary
- ADR-0022 — Policy/Profile Engine
- ADR-0023 — Policy Profile Registry and Run Pinning
