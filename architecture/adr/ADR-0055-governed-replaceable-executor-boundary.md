# ADR-0055 — Governed Replaceable Executor Boundary

Date: 2026-08-12
Status: accepted for M1 boundary; live-provider evidence pending
Project: PROJECT-FFB-0001

## Context
TF-0061 proved deterministic functional delivery, governed rework and safe refusal. The next maturity step is to introduce a replaceable worker without allowing the worker implementation, model or provider to become an implicit source of organizational authority or acceptance.

Directly embedding one provider SDK into Factory Builder would couple role identity, provider, model and runtime authority, and would make historical replacement harder to audit.

## Decision
Introduce an executor boundary below `AGENT_ASSIGNMENT` and above provider-specific adapters.

A governed executor invocation pins:
- RUN and current stage;
- worker assignment;
- executor definition;
- executor version;
- provider/model references where applicable;
- input artifact;
- bounded input hash;
- candidate output hash;
- output artifact.

Executor output is **candidate content**. It becomes a typed stage artifact but does not become verified truth, accepted knowledge, an authority decision or a capability grant merely because invocation completed.

For the M1 boundary experiment:
- external effects are forbidden;
- only `IMPLEMENT_BOUNDED_PROTOTYPE` is executor-enabled;
- assignment must equal the governed producer assignment;
- current input artifact must verify;
- structured authority/tool fields are rejected at the boundary;
- verifier and Socrates remain downstream and independent.

## Replacement proof
`MVP-EXEC-RUN-0001` uses two pinned local test-double workers:

`EXEC-TAG-NORM-0001 v0.1 → candidate → VERIFY FAIL → REWORK → EXEC-TAG-NORM-0002 v0.2 → candidate → VERIFY PASS → SOCRATES → DELIVERY`

The first invocation, first candidate and verifier failure remain historical evidence after replacement.

## Invariants
- role identity is independent of executor/model/provider;
- executor definition never expands assignment authority;
- invocation success is not task success;
- executor output never bypasses independent verification or Socrates;
- replacement does not rewrite earlier invocation history;
- no executor output can manufacture a Tool Boundary grant;
- live provider maturity is not claimed from local test doubles.

## Risks
- `RISK-0011` remains OPEN until the same boundary is exercised against an authorized live AI/provider adapter.
- Existing `RISK-0002`, `RISK-0009` and `RISK-0010` continue to bound external input, durable provenance and durable rework maturity.

## Consequence
Provider-specific integration can now be added as an adapter rather than as a new control plane. The next generation should implement exactly one authorized live-provider adapter if credentials/connectivity are available; otherwise the summit must remain open rather than being simulated as complete.
