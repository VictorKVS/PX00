# TF-0024 — Governed Action Request and Universal Tool Boundary

**Date:** 2026-08-12  
**Status:** ACCEPTED FOR CONTRACT DESIGN  
**Lifecycle decision:** KEEP / CONTRACT BEFORE ADAPTERS  
**Primary ADR:** `architecture/adr/ADR-0017-governed-action-request-and-tool-boundary.md`

## Trigger

TF-0023 defined a minimal governed execution kernel. The kernel still requires a universal material-action boundary so roles and executors cannot acquire direct tool access or bypass authority, protocol, event and trace controls.

## Material structural change

This generation introduces the `ACTREQ-*` canonical orchestration object and a universal Action Request / Tool Boundary design.

The intended path is:

```text
ROLE / EXECUTOR
→ ACTREQ
→ AUTHORITY DECISION
→ scoped capability grant
→ TOOL BOUNDARY
→ adapter
→ material event / artifact
→ evidence processing
```

## Canonical vocabulary decision

Only one new canonical object family is justified now:

```text
ACTREQ-* = Action Request
```

`TOOL`, capability-grant and execution-receipt concepts remain governed runtime/configuration structures rather than new canonical object families in this generation. Material execution receipts are represented through `EVT-*` and, where payload preservation is required, `ART-*`.

This keeps the object model minimal while preserving distinct action-request lifecycle and trace semantics.

## Core invariants

1. Roles and untrusted executors do not directly call externally effective tools.
2. An Action Request is never equivalent to authority.
3. Only an `ALLOW` Authority Decision may produce executable scoped capability.
4. Capability scope cannot exceed the Authority Decision.
5. Tool adapters implement capability; they do not make governance decisions.
6. Professional role policy does not live inside adapters.
7. Executor/source/tool output cannot directly mutate control-plane state.
8. Tool output does not automatically become `EVD-*` or `KN-*`.
9. Autonomy level and side-effect impact are separate dimensions.
10. First executable proof is deterministic and has no real external side effect.

## Intent over mechanism

The role requests the governed capability it needs, for example:

```text
repository.file.read
```

rather than dictating a privileged mechanism such as arbitrary shell execution. A future tool resolver chooses a permitted implementation or denies the request according to policy.

## Side-effect classification

The architecture introduces a policy-relevant impact scale:

```text
S0 — no externally effective mutation
S1 — local/reversible state
S2 — controlled governed mutation
S3 — external effect
S4 — high-impact or difficult-to-reverse effect
```

The scale does not grant authority and is not a replacement for A0..A4 autonomy.

## Planned contract artifacts

```text
schemas/ACTION_REQUEST.yaml
schemas/TOOL_DEFINITION.yaml
schemas/CAPABILITY_GRANT.yaml
```

A future deterministic tool-boundary implementation may use:

```text
px00/tools/
├── boundary.py
├── resolver.py
├── grants.py
├── contracts.py
└── adapters/
    └── deterministic.py
```

Code remains gated by schemas, fixtures and tests.

## Initial acceptance design

The first tool-boundary fixture will use a synthetic capability such as `math.multiply` and prove:

- valid request/authority/grant executes;
- denied authority cannot execute;
- capability mismatch blocks;
- target mismatch blocks;
- expired/revoked grant blocks;
- one-time grant cannot be replayed;
- unauthorized adapter cannot execute;
- side-effect level outside scope blocks;
- executor cannot force a privileged adapter;
- untrusted result cannot create control-plane authority or transitions.

## Algorithms / libraries

**Runtime design:** normalized capability request + fail-closed authority + scoped capability grant + adapter dispatch + event/artifact result preservation.

**New third-party libraries:** NONE.

## DevOps conclusion

No real external adapter is authorized by this record. GitHub/filesystem/HTTP/mail/database/shell integration must wait for deterministic boundary tests. This avoids creating an external side-effect path before the authorization boundary itself has executable evidence.

## Security conclusion

`PASS_WITH_ACTIONS` for contract design.

The design substantially reduces direct-tool privilege drift and establishes a control-plane boundary against prompt/data injection. Runtime enforcement remains unproven until acceptance tests exist.

## Evaluation

- authority separation: 5/5;
- provider/tool replaceability: 5/5;
- traceability: 5/5;
- object-model discipline: 5/5 because only `ACTREQ-*` is added and other concepts reuse existing canonical evidence/decision/event families;
- implementation maturity: 2/5 pending schemas and deterministic tests.

Scores are coarse engineering decision aids, not statistical measurements.

## Next gate

Update the Canonical Object Model with `ACTREQ-*`, add machine-readable Action Request / Tool Definition / Capability Grant schemas, validate them, then define deterministic acceptance fixtures before implementing tool adapters.

## Supersession / rollback

This record is append-only. Later generations may alter capability taxonomy or adapter implementation but must preserve the no-direct-tool and fail-closed authority invariants unless a separately evaluated decision supersedes them.
