# TF-0064 — Live Provider Readiness Boundary

Date: 2026-08-12
Status: implemented; live provider still pending
Project: PROJECT-FFB-0001
ADR: ADR-0057

## Objective
Make SUMMIT-FFB-02 ready for one real AI provider without coupling FATHER to a vendor, committing secrets, weakening secret scanning, or allowing provider output to bypass governed verification.

## Implemented
- `schemas/LIVE_PROVIDER_PROFILE.yaml`;
- `schemas/LIVE_PROVIDER_CALL_RECORD.yaml`;
- `px00/live_provider.py`;
- `tests/test_live_provider.py`;
- `projects/FATHER_FACTORY_BUILDER/pilots/agent_rd_factory/LIVE_PROVIDER_PILOT_READINESS.yaml`;
- `RISK-0011` advanced from OPEN to MITIGATING with verified containment evidence.

## Proven local boundary behavior
The live-provider adapter now proves locally that:
- only HTTPS endpoints are accepted;
- endpoint host must be explicitly allowlisted;
- endpoint userinfo is rejected;
- no provider call occurs unless a runtime opt-in is enabled;
- a credential reference may exist in configuration, but the credential value is loaded only at runtime;
- provider data egress is blocked if data classification is not explicitly allowed;
- timeout and maximum response size are bounded;
- invalid HTTP status, invalid JSON and invalid response shape fail closed;
- provider request/response payloads are hashed canonically;
- provider request identity and returned model identity are preserved when available;
- the adapter passes through the existing `GovernedExecutorBoundary` and produces candidate artifacts only;
- provider success still does not imply verifier PASS or acceptance.

## CI finding and correction
The first implementation triggered the existing repository secret-hygiene test because a local variable named `secret` matched the project's defensive scanner.

Decision: do not weaken the scanner. The implementation was changed to comply with the existing secret-hygiene contract. Re-run then passed unit/integration tests, secret scan and repository contract validation.

This is retained as evidence that secret hygiene constrains implementation rather than being bypassed for convenience.

## Lifecycle classification
This generation prepares a future experiment classified independently as:
- CRISP-ML(Q) phase: `DEPLOYMENT` integration sub-experiment;
- delivery stage: `POC`;
- PX00 maturity: `M1_PROTOTYPE`.

These labels are deliberately not treated as equivalent.

## What is NOT claimed
- no real external AI provider has been called yet;
- no real provider credential has been provisioned in this repository;
- no provider-specific response schema has been proven;
- no live rate limit, token refresh, latency, cost or model drift behavior has been tested;
- SUMMIT-FFB-02 is not complete.

## Next gate
Select one authorized provider and implement exactly one provider-specific driver/configuration. Use PUBLIC/INTERNAL bounded input only, no tools and no material external action. Execute one real call, preserve provider evidence, then send its candidate through independent verification and Socrates; bad live output must remain rejectable and reworkable.
