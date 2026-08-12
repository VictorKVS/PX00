# DJ-0056 — First Real Security Knowledge Snapshot Bridge

Date: 2026-08-12
Generation: TF-0068
ADR: ADR-0061

## What changed
The cross-repository Security Knowledge boundary moved from synthetic references to the first real canonical object.

Real object:
`FSB-117-2025` from `VictorKVS/KNOWLEDGE_CORE`.

The producer snapshot pins the exact historical Git commit, source-card SHA-256, source locator, knowledge state, freshness and classification. PX00 independently verifies the manifest digest and turns it into a runtime knowledge snapshot and ContextPackage.

## Critical maturity restraint
The canonical record verifies official source metadata only. Full text and atomization remain pending.

Therefore the imported state is exactly:
`SOURCE_VERIFIED`.

Not:
`VERIFIED ATOMIC REQUIREMENT`.

## Defect caught before acceptance
The first manifest-envelope version omitted classification and freshness from its digest.

The gate was hardened before acceptance. Both fields are now integrity-bound because they can alter consumer admission/usage behavior.

## Reproducibility proof
KNOWLEDGE_CORE CI uses full Git history and validates snapshot content using `git show` against the pinned commit. Current `main` is newer than the snapshot commit, yet the old object remains verifiable.

PX00 regression tests pin exact producer manifest, runtime snapshot and ContextPackage hashes.

## Risk
`RISK-0012` remains `MITIGATING`, now narrowed to the missing actual RUN/trace/replay portion.

## Next
Carry `SEC-SNAPSHOT-0001` / `CTX-SEC-REAL-0001` through a bounded FATHER RUN and replay path. Do not claim expert Security reasoning until a true atomic VERIFIED requirement slice later passes the same route.
