# DJ-0052 — Live Provider Readiness Boundary

Date: 2026-08-12
Project: PX00 / PROJECT-FFB-0001
Generation: TF-0064
ADR: ADR-0057

## Decision
Prepare the first live AI-provider integration without coupling FATHER to a provider and without committing or persisting credential values.

## Implemented
- `LIVE_PROVIDER_PROFILE` and `LIVE_PROVIDER_CALL_RECORD` contracts;
- provider-neutral `LiveHttpsExecutorAdapter`;
- HTTPS + exact host allowlist;
- explicit live opt-in;
- runtime credential loading by reference;
- data-classification egress control;
- timeout/response-size limits;
- HTTP/JSON/shape fail-closed handling;
- canonical request/response hashes;
- provider request/model identity capture;
- tests proving the adapter passes through the existing governed executor boundary without gaining authority or acceptance.

## CI/security observation
Initial CI failed the repository secret-hygiene test on an implementation variable. The control was preserved; code was changed instead. The corrected boundary passed unit/integration tests, secret scan and repository contract validation.

## Risk
`RISK-0011` is now `MITIGATING`, not resolved. Local transport/auth/egress containment is proven; real provider behavior is still unproven.

## Current summit
`SUMMIT-FFB-02 — FIRST GOVERNED LIVE EXECUTOR`: OPEN.

Next evidence must be an actual authorized provider call with bounded PUBLIC/INTERNAL input, no tools, no material external effect, preserved provider evidence, independent verification and Socrates.
