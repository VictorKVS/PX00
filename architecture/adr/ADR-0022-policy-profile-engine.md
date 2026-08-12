# ADR-0022 — Policy/Profile Engine

**Status:** ACCEPTED FOR MINIMAL IMPLEMENTATION  
**Date:** 2026-08-12  
**Decision:** KEEP / IMPLEMENT DETERMINISTIC PROFILE INTERSECTION

## Context

ADR-0020 established the governed execution kernel and ADR-0021 established the Action Request / Tool Boundary. The first synthetic runtime still contains hardcoded policy facts such as the only allowed capability, permitted side-effect class and effective autonomy.

PX00 already declares `global by architecture, regional by policy` and defines effective authority as the intersection of role, protocol, project, organization, jurisdiction, tool, data-classification and approval constraints. Those constraints need one deterministic evaluation boundary before any real external adapter is permitted.

## Decision

PX00 SHALL introduce a **Policy/Profile Engine** that computes effective execution policy from explicit versioned profile inputs.

The engine is a control-plane component. It does not execute tools and does not provide professional reasoning.

The minimum evaluation chain is:

```text
role profile
∩ protocol profile
∩ project profile
∩ organization profile
∩ jurisdiction profile
∩ tool profile
∩ data-classification profile
∩ approval profile
        ↓
effective policy
        ↓
ALLOW | DENY | ESCALATE
```

## Fail-closed rule

Missing required policy input, an unknown capability, incompatible scope or malformed bound SHALL NOT silently widen authority.

The engine returns one of:

- `ALLOW` — every required layer permits the requested capability/action within the effective bounds;
- `DENY` — at least one applicable layer explicitly prohibits or caps the action below the request;
- `ESCALATE` — the policy requires governed approval or human decision not present in the current context.

## Restrictive intersection

The effective profile is always at least as restrictive as every applicable input profile.

For ordered ceilings:

- autonomy uses the lowest applicable `A0..A4` ceiling;
- side effects use the lowest applicable `S0..S4` ceiling;
- operation count uses the minimum positive limit;
- capabilities use set intersection;
- data classifications use the explicitly permitted intersection;
- target scopes must all accept the requested target;
- approval requirements accumulate rather than cancel each other.

No profile may expand a stricter profile.

## Profile types

The first implementation supports a common machine-readable profile contract with a `profile_type` field. Required types are:

```text
ROLE
PROTOCOL
PROJECT
ORGANIZATION
JURISDICTION
TOOL
DATA
APPROVAL
```

A later implementation may use separate specialized schemas when real requirements justify them, but the intersection semantics remain stable.

## Explainability

Every policy evaluation SHALL produce explicit reason codes and the profile IDs/versions that contributed to the decision. Hidden chain-of-thought is neither required nor stored.

A material authority decision can therefore state, for example:

```text
DENY
reason: SIDE_EFFECT_CEILING_EXCEEDED
constraining_profile: POLICY-JURISDICTION-...
```

## Version pinning

Profiles are versioned. A material run SHALL evaluate against pinned profile versions. Updating a profile does not silently change the authority basis of an already-started run.

## Separation from role identity

Role packages may declare policy references and capability ceilings, but the Policy Engine SHALL NOT contain hardcoded branches such as `if role == analyst`. It evaluates normalized profile data.

## First executable proof

The first proof remains synthetic and S0-only. It SHALL demonstrate that `math.multiply` succeeds only when all required policy layers allow it.

Negative tests SHALL cover at least:

- one restrictive layer denies a capability allowed elsewhere;
- lower autonomy ceiling wins;
- lower side-effect ceiling wins;
- target mismatch denies;
- classification mismatch denies;
- missing required profile fails closed;
- required approval without approval escalates;
- requested adapter hint cannot change policy;
- reordering profiles does not change the result;
- adding a stricter profile cannot produce a less restrictive result.

## Dependencies

No new third-party dependency is authorized. Standard-library Python data structures are sufficient for the deterministic reference implementation.

## Security rationale

Moving policy from executor/tool code into an explicit fail-closed intersection engine prevents privilege drift, provider-specific authorization, inconsistent regional behavior and accidental widening when a new role or adapter is added.

## Next gate

1. Add `schemas/POLICY_PROFILE.yaml`.
2. Add deterministic policy evaluation code and tests.
3. Integrate the synthetic kernel with the Policy Engine.
4. Require all CI/validator/security checks to remain green.
5. Keep real network, shell, mail, database and production mutation adapters blocked.

## Related decisions

- ADR-0001 — Global Core / Regional Profiles
- ADR-0010 — Authority-Gated Execution and Trace Contracts
- ADR-0020 — Minimal Governed Execution Kernel
- ADR-0021 — Governed Action Request and Universal Tool Boundary
- `governance/AUTHORITY_AUTONOMY_CONTRACT.md`
