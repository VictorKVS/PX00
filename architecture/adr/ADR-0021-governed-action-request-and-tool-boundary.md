# ADR-0021 — Governed Action Request and Universal Tool Boundary

**Status:** ACCEPTED FOR CONTRACT DESIGN  
**Date:** 2026-08-12  
**Decision:** KEEP / CONTRACT BEFORE ADAPTERS

## Context

ADR-0020 establishes a Minimal Governed Execution Kernel and requires authority evaluation at each material action boundary. PX00 now needs one universal mechanism between a role/executor that wants an action and the mechanism that can make that action effective.

Without a common boundary, each role can accumulate direct integrations with GitHub, filesystems, shell, HTTP, databases, mail or other services. That would fragment authorization, make tool permissions role-specific, enable privilege drift and create bypass paths around protocol/event/trace controls.

## Decision

PX00 SHALL introduce a governed **Action Request / Tool Boundary**.

The primary invariant is:

> No governed role or untrusted executor directly invokes an externally effective tool. It requests an action; PX00 evaluates authority and executes only through the governed tool boundary.

The material path is:

```text
ROLE / EXECUTOR
→ ACTION REQUEST
→ AUTHORITY DECISION
→ scoped capability grant when ALLOW
→ TOOL BOUNDARY
→ adapter
→ tool/external effect
→ execution receipt/event
→ artifact/source/evidence processing
```

## Intent over mechanism

A role SHOULD request the capability and governed intent it needs, rather than selecting a privileged implementation mechanism.

Example:

```text
required capability: repository.file.read
```

not:

```text
run shell and read an arbitrary local credential path
```

Tool resolution may later select GitHub API, a governed connector, local Git, another adapter or `DENY` according to policy and context.

## Canonical object decision

This requirement justifies one new canonical orchestration object:

- `ACTREQ-*` — **Action Request**: one governed request for a material capability/action, with its own request/authorization/execution lifecycle and trace meaning.

To avoid object proliferation, this ADR does **not** create canonical `TOOL-*`, `GRANT-*` or `RCPT-*` object families in Baseline 0.1.

Instead:

- tool definitions are governed configuration/contracts referenced by stable IDs;
- a capability grant is a scoped execution authorization derived from an existing Authority Decision and may be represented inside authority/runtime schemas;
- an execution receipt is represented through `EVT-*` plus referenced `ART-*` output where material payload preservation is required.

## Authority separation

`ACTREQ-*` and Authority Decision are distinct. Only `ALLOW` may create an executable scoped capability grant. `DENY` produces no effective action. `ESCALATE` follows the protocol escalation path.

## Capability grant

An allowed material action SHOULD be translated into a narrow runtime capability grant containing only the scope required for the authorized action. A grant cannot exceed the Authority Decision from which it is derived.

## Tool boundary

The Tool Boundary SHALL accept structured governed inputs, not free-form claims of privilege. It SHALL verify the capability grant and adapter/tool scope before invocation and SHALL produce a material success/failure event.

## Adapter rule

Adapters implement capabilities. They do not grant authority. They SHALL NOT reinterpret missing authority as permission.

## Side-effect classification

Autonomy and action impact are different dimensions. PX00 SHALL use a side-effect classification:

```text
S0 — no externally effective mutation
S1 — local/reversible state
S2 — controlled governed mutation
S3 — external effect
S4 — high-impact or difficult-to-reverse effect
```

The classification does not itself grant authority.

## Tool result and evidence

Tool output does not automatically become evidence or admitted knowledge.

```text
tool result
→ SRC/ART
→ EVD when admitted for a claim/purpose
→ FIND
→ Knowledge Gate
→ KN
```

## Prompt/data injection boundary

Untrusted source content and executor output cannot directly alter control-plane authority, protocol versions, declared transitions or acceptance criteria.

## Initial capabilities

The first executable tool-boundary proof SHALL use a deterministic synthetic capability such as `math.multiply` with no network, customer data or external side effect.

Negative tests SHALL cover missing/denied authority, capability and target mismatch, expired/revoked/replayed grants, unauthorized adapters, side-effect overflow and untrusted output attempting to mutate control-plane state.

## Consequences

The design creates one auditable path to effects, keeps role implementations provider-independent, separates authorization from adapter mechanics and makes prompt/data injection non-authoritative by construction.

## Related decisions

- ADR-0010 — Authority-Gated Execution and Trace Contracts
- ADR-0020 — Minimal Governed Execution Kernel
- `architecture/CANONICAL_OBJECT_MODEL.md`
- `governance/AUTHORITY_AUTONOMY_CONTRACT.md`
- `protocols/PROTOCOL_EXECUTION_CONTRACT.md`
