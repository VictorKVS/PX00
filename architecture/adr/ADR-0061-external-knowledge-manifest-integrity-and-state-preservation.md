# ADR-0061 — External Knowledge Manifest Integrity and State Preservation

Status: Accepted
Date: 2026-08-12
Related: ADR-0060, TF-0068, RISK-0012

## Context
ADR-0060 established immutable cross-repository `KNOWLEDGE_SNAPSHOT` pinning. The next integration problem is semantic rather than only structural: a canonical knowledge producer can export an object whose state is weaker than final `VERIFIED` knowledge, and the runtime must preserve that state exactly.

The first real slice is `FSB-117-2025` from `VictorKVS/KNOWLEDGE_CORE`. Its source card contains officially verified publication metadata but explicitly leaves full-text ingestion and atomization pending.

Therefore:

`SOURCE_VERIFIED metadata ≠ VERIFIED atomic requirement`.

A transport bridge that silently upgrades this distinction would corrupt the Security Knowledge epistemic model even if all SHA-256 values were technically correct.

## Decision
External knowledge is imported through a producer manifest whose material envelope is integrity-bound and independently recomputed by the consumer.

The manifest digest covers at least:
- schema version;
- canonical repository and exact commit;
- knowledge space/content root/request reference;
- selected object ID/version/type/path;
- exact content SHA-256;
- producer knowledge state;
- source locator when present;
- freshness state;
- classification;
- selection reason.

PX00 `KnowledgeManifestBridge` validates the producer envelope and then constructs a runtime `KNOWLEDGE_SNAPSHOT` and ContextPackage candidate objects without upgrading producer knowledge state.

## Why classification and freshness are integrity fields
Classification controls whether an object may enter a context under a binding ceiling. Freshness controls whether a consumer should treat an object as current, stale or reassessment-required.

If either can be changed without altering the producer manifest digest, an attacker or integration defect could modify effective runtime behavior while the manifest still appears valid.

Therefore both participate in manifest integrity.

## Producer versus consumer verification
### KNOWLEDGE_CORE producer
Responsible for proving that the selected object exists at the pinned historical commit and that its declared content digest matches the exact historical bytes.

Current CI uses full Git history and verifies via:
`git show <commit>:<path>`.

### PX00 consumer
Responsible for independently recomputing the producer manifest digest, enforcing expected repository/knowledge-space/content-root boundaries, preserving producer state/classification/freshness, and creating the runtime snapshot/context hash.

PX00 does not independently reinterpret the source into a stronger knowledge state during transport.

## First real proof
`SEC-SNAPSHOT-0001` exports the canonical source metadata record `FSB-117-2025` from historical KNOWLEDGE_CORE commit `8f7e1cb7a5abec39e0432ce7a811591a5dcadc8d`.

The proof intentionally stops at `SOURCE_VERIFIED` because the canonical record declares:
- metadata: verified official;
- full text: pending ingestion;
- atomization: pending.

This slice proves cross-repository provenance transport, not legal applicability or atomic regulatory reasoning.

## Security invariants
- `MANIFEST VALID ≠ KNOWLEDGE TRUE`.
- `SOURCE_VERIFIED ≠ VERIFIED REQUIREMENT`.
- `SNAPSHOT PINNED ≠ APPLICABLE TO ORGANIZATION`.
- `KNOWLEDGE CONTEXT ≠ ACTION AUTHORITY`.
- Consumer may reject producer material but may not silently upgrade its verification state.
- A mutable branch name is never historical knowledge identity.

## Consequences
Positive:
- epistemic state survives repository boundaries;
- classification/freshness tampering becomes detectable;
- source-metadata slices can be integrated before full corpus atomization without false maturity claims;
- future domain knowledge repositories can reuse the producer/consumer pattern.

Costs:
- producer and consumer canonicalization algorithms must remain contract-compatible;
- manifest schema changes require versioned compatibility/migration handling;
- current proof still lacks an actual RUN/replay.

## Remaining work
`RISK-0012` remains MITIGATING until the real snapshot-bound ContextPackage participates in an actual FATHER RUN and replay after further KNOWLEDGE_CORE changes.

A later proof must also use a true atomic `VERIFIED` requirement slice before Security-domain expert reasoning is considered end-to-end demonstrated.
