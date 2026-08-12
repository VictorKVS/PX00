# ADR-0023 — Policy Profile Registry and Run Pinning

**Status:** ACCEPTED FOR IMPLEMENTATION  
**Date:** 2026-08-12  
**Decision:** KEEP

## Context

ADR-0022 introduced restrictive policy-profile intersection. Reproducible governed execution now requires exact profile versions to be resolved before a RUN and preserved for the lifetime of that RUN. A mutable lookup by profile name is insufficient because policy may change while execution is active.

## Decision

PX00 SHALL introduce a deterministic Policy Profile Registry / Resolver and immutable Run Policy Snapshot.

The resolver SHALL:

1. resolve one exact ACTIVE profile version for every required profile type;
2. reject missing, ambiguous, inactive or unknown requested versions fail-closed;
3. never silently substitute a newer profile version after RUN creation;
4. normalize resolved profile content into a deterministic representation;
5. calculate a SHA-256 snapshot hash over the normalized representation;
6. bind profile references and snapshot hash to the RUN/authority evidence chain;
7. permit later registry updates without mutating an existing snapshot.

## Resolution model

```text
requested context
→ registry lookup
→ exact profile versions
→ canonical normalization
→ SHA-256 snapshot hash
→ RUN policy snapshot
→ Policy Engine
→ Authority Decision
```

## Version rule

A profile identity is `(profile_id, version)`. `profile_id` alone is not sufficient for a running execution.

New versions are additive. Updating a policy produces a new version rather than rewriting the semantic content of an already pinned version.

## Snapshot rule

A policy snapshot contains the complete resolved set required to reproduce the policy decision. The hash is evidence of exact normalized policy input, not a digital signature and not proof against a malicious repository administrator.

The first implementation uses SHA-256 from the Python standard library and deterministic JSON serialization with sorted keys and stable list ordering.

## Drift behavior

If a registry is updated after a RUN is created:

- new RUNs may resolve the new ACTIVE version according to explicit resolution rules;
- the existing RUN continues with its pinned snapshot;
- a material policy revocation may separately terminate/block the RUN through a governed revocation mechanism, but silent live migration is prohibited.

## Security invariants

- missing required layer fails closed;
- duplicate `(profile_id, version)` is rejected;
- ambiguous default resolution is rejected;
- inactive profiles cannot authorize a new RUN;
- snapshot hash changes when material normalized policy content changes;
- profile ordering does not change the snapshot hash;
- executor/tool output cannot choose or rewrite the snapshot;
- RUN policy pinning is immutable after creation.

## Dependencies

No new third-party dependency. Python standard library `hashlib` and `json` are sufficient.

## Initial acceptance

Tests SHALL prove exact-version resolution, complete required-type coverage, duplicate rejection, inactive rejection, deterministic hash, order independence, material-change hash drift and old-snapshot stability after registry update.

## Related decisions

- ADR-0020 — Minimal Governed Execution Kernel
- ADR-0021 — Governed Action Request and Universal Tool Boundary
- ADR-0022 — Policy / Profile Engine
