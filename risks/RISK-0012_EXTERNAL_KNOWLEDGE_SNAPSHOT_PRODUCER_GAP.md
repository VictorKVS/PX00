# RISK-0012 — External Knowledge Snapshot Producer Gap

Status: RESOLVED
Severity: S3
Resolution scope: M1 bounded cross-repository provenance/replay
Category: KNOWLEDGE / CROSS-REPOSITORY / REPRODUCIBILITY / INTEGRITY
Source: TF-0067 design pass; narrowed by TF-0068; resolved by TF-0069
Owner: FFB-ROLE-0004 Knowledge Architect + FFB-ROLE-0006 Principal Software Engineer
Independent review: ARGUS_AUDIT_0002 — PASS_WITH_RESTRICTIONS

## Original risk
PX00/FATHER needed to consume actively changing canonical knowledge from `VictorKVS/KNOWLEDGE_CORE` while preserving the exact historical knowledge state used by a RUN. Without a producer manifest, immutable repository/object pinning and replay binding, historical runs could silently follow a newer `main` or lose the provenance needed to reproduce a decision.

## Resolution evidence
### Producer-side canonical evidence
`VictorKVS/KNOWLEDGE_CORE` now provides:
- `security-knowledge/corpus/snapshot-export-schema.yaml`;
- real producer manifest `SEC-SNAPSHOT-0001`;
- historical Git validation using full checkout history and `git show <pinned_commit>:<path>`;
- CI verification of exact object SHA-256 and manifest digest.

The first real object is `FSB-117-2025` at pinned commit:
`8f7e1cb7a5abec39e0432ce7a811591a5dcadc8d`.

Pinned source-card digest:
`5bdfd92728c6be35cdbffba5c57bb843bf1f3e48813c47fab2a755a5a3351710`.

Producer manifest digest:
`8830d3aa51dab48586bdc96945f2e38182ced261eacef05fb10ef42ac9ce81d2`.

The repository head advanced after the pinned commit, while historical validation continued to pass.

### Consumer-side evidence
PX00 now provides:
- `KNOWLEDGE_SNAPSHOT`;
- `KnowledgeManifestBridge` with independent producer-digest recomputation;
- state/classification/freshness preservation;
- `RunKnowledgeBinder` matching RUN/role/assignment to ContextPackage and snapshot set;
- knowledge-bound persisted trace manifests;
- read-only replay that fails closed if a recorded knowledge context is omitted or changed.

Pinned runtime snapshot digest:
`04d5ec28431e8c13863dab9896533435dac735ceb36b6bf59e4f05eea1f7eac3`.

The first fixed integration ContextPackage proof uses hash:
`9c09e6a4075f25ce2e341d1b0bd2fa4f59dedadf364019492be337893c220a2a`.

TF-0069 additionally creates a bounded governed RUN whose trace manifest stores:
- ContextPackage ref/hash;
- knowledge snapshot ref/digest;
- producer manifest ref/digest.

Read-only replay verifies event/policy lineage and the expected knowledge context. Negative tests prove replay fails when:
- knowledge context is omitted;
- context package hash changes;
- snapshot digest changes;
- producer state/locator/classification/freshness is tampered;
- context belongs to another RUN.

### Epistemic restraint preserved
The first real slice is intentionally only `SOURCE_VERIFIED` because the canonical FSB record states full text and atomization are still pending.

Resolution of this risk therefore proves **historical knowledge provenance/replay**, not expert Security reasoning.

`SOURCE_VERIFIED ≠ VERIFIED REQUIREMENT` remains mandatory.

## Independent review
`ARGUS_AUDIT_0002_KNOWLEDGE_BOUND_REPLAY.md` returns `PASS_WITH_RESTRICTIONS` and permits resolution only for the bounded M1 provenance/replay claim.

The audit explicitly rejects broader claims of:
- full-text regulatory verification;
- applicability;
- compliance;
- expert Security reasoning;
- production durability;
- live AI correctness;
- complete FATHER corporate loop.

## Reopen conditions
Reopen RISK-0012 if any of the following occurs:
- historical replay resolves mutable `main/latest` instead of pinned state;
- a material RUN omits ContextPackage/snapshot/manifest provenance;
- producer manifest schema changes without compatible consumer evidence;
- consumer code silently upgrades producer knowledge state;
- classification/freshness or another use-affecting field can change outside integrity protection;
- repository/storage migration makes pinned historical objects unavailable or unverifiable;
- a new knowledge backend cannot provide equivalent immutable version/content provenance.

## Related remaining risks
Resolution does not replace:
- durable store/recovery risks such as RISK-0003;
- production concurrency/transaction concerns;
- external/untrusted input risks;
- artifact-envelope integrity concerns;
- live-provider risk RISK-0011.

## Next maturity proof
Repeat the same path with a truly atomic `VERIFIED` Security requirement slice and use it in a bounded professional reasoning task with independent expert/Socrates review.

That future proof is a different maturity claim and cannot inherit this resolution automatically.
