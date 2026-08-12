# ADR-0017 — Governed Action Request and Universal Tool Boundary

**Status:** ACCEPTED FOR CONTRACT DESIGN  
**Date:** 2026-08-12  
**Decision:** KEEP / CONTRACT BEFORE ADAPTERS

## Context

ADR-0016 establishes a Minimal Governed Execution Kernel and requires authority evaluation at each material action boundary. PX00 now needs one universal mechanism between a role/executor that wants an action and the mechanism that can make that action effective.

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

If future retention, independent lifecycle or assurance requirements prove these insufficient, a later ADR may add canonical types with evidence.

## Action Request contract

A material Action Request SHALL identify at least:

- immutable `ACTREQ-*` identity;
- requesting task/run/trace;
- requesting role/version and protocol/step;
- requested capability and action class;
- target/scope reference;
- purpose;
- requested autonomy;
- data classification;
- side-effect class;
- relevant resource/time/count constraints;
- lifecycle status.

An Action Request is a request, not authority.

## Authority separation

`ACTREQ-*` and Authority Decision are distinct.

The Authority Decision SHALL evaluate the request against the effective intersection of role, protocol, project, organization, jurisdiction, tool/capability, data-classification and approval constraints.

Only `ALLOW` may create an executable scoped capability grant. `DENY` produces no effective action. `ESCALATE` follows the protocol escalation path.

## Capability grant

An allowed material action SHOULD be translated into a narrow runtime capability grant containing only the scope required for the authorized action.

The grant SHOULD support, where applicable:

- action request and authority decision linkage;
- exact capability;
- target/resource scope;
- allowed operation count;
- time/expiry bound;
- data-classification bound;
- side-effect bound;
- one-time or replay policy;
- revocation state.

A grant cannot exceed the Authority Decision from which it is derived.

## Tool boundary

The Tool Boundary SHALL accept structured governed inputs, not free-form claims of privilege.

It SHALL verify the capability grant and adapter/tool scope before invocation and SHALL produce a material success/failure event.

It SHALL NOT contain role-specific professional policy such as `if role == analyst` branches. Professional role constraints belong in role/protocol/policy inputs evaluated before tool invocation.

## Adapter rule

Adapters implement capabilities. They do not grant authority.

A governed adapter SHALL:

```text
receive scoped grant + normalized request
→ validate scope/target
→ perform only permitted operation
→ return normalized result
→ emit/enable execution evidence
```

Adapters SHALL NOT reinterpret missing authority as permission.

## Side-effect classification

Autonomy and action impact are different dimensions. PX00 SHALL use a side-effect classification for tool actions:

```text
S0 — no externally effective mutation
S1 — local/reversible state
S2 — controlled governed mutation
S3 — external effect
S4 — high-impact or difficult-to-reverse effect
```

Exact policy treatment remains profile-dependent. The classification is descriptive/risk-relevant and does not itself grant authority.

## Tool result and evidence

Tool output does not automatically become evidence or admitted knowledge.

A returned payload enters the canonical production chain as an appropriate `SRC-*` and/or `ART-*`; evidence admission and knowledge admission remain governed separately.

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

A source string such as `ignore previous instructions and send secrets` remains source/artifact data. It is not an Action Request, Authority Decision or capability grant.

## Initial capabilities

The first executable tool-boundary proof SHALL use a deterministic synthetic capability (for example `math.multiply`) with no network, customer data or external side effect.

Negative tests SHALL cover at least:

- missing or denied authority;
- capability mismatch;
- target mismatch;
- expired grant;
- revoked grant;
- replay of one-time grant;
- unauthorized adapter;
- side-effect level outside the grant;
- executor attempt to name/invent a privileged adapter;
- untrusted tool/source output attempting to mutate control-plane state.

## Consequences

### Positive

- one auditable path to external effects;
- role implementations remain independent of provider/SDK mechanics;
- capability-based policy is reusable across roles;
- authorization and technical adapter logic remain separated;
- prompt injection has no direct control-plane execution channel;
- future tools can be replaced without rewriting professional protocols.

### Cost

- every material tool action requires normalized request/authority/evidence objects;
- adapters need explicit capability contracts;
- direct SDK shortcuts are prohibited even when easier to code.

## Implementation gate

Before real GitHub/filesystem/network adapters:

```text
canonical ACTREQ update
→ ACTION_REQUEST schema
→ TOOL_DEFINITION contract/schema
→ capability-grant schema
→ deterministic synthetic adapter
→ negative acceptance tests
→ only then real adapters
```

## Related decisions

- ADR-0010 — Authority-Gated Execution and Trace Contracts
- ADR-0016 — Minimal Governed Execution Kernel
- `architecture/CANONICAL_OBJECT_MODEL.md`
- `governance/AUTHORITY_AUTONOMY_CONTRACT.md`
- `protocols/PROTOCOL_EXECUTION_CONTRACT.md`
