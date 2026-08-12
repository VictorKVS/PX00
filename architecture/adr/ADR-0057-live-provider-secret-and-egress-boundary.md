# ADR-0057 — Live Provider Secret and Data-Egress Boundary

Date: 2026-08-12
Status: Accepted
Project: PROJECT-FFB-0001

## Context
SUMMIT-FFB-02 requires one real non-deterministic AI provider. The provider-neutral executor boundary from ADR-0055 proves assignment/stage pinning, candidate artifacts, independent verification and rework, but a live provider introduces a new external trust boundary: credentials, HTTPS transport, endpoint identity, data egress, response size/shape, provider request identity and model alias behavior.

A live integration must not force provider-specific assumptions into FATHER or weaken repository secret hygiene merely to make the first API call work.

## Decision
Introduce a provider-neutral live HTTPS boundary below the governed executor boundary and above provider-specific request/response drivers.

The boundary SHALL:
- require HTTPS and exact host allowlisting;
- reject endpoint userinfo;
- load credential values only at runtime through a referenced environment/secret source;
- require an explicit opt-in flag before any live network call;
- enforce allowed data classifications before transport;
- bound timeout and response size;
- fail closed on transport/HTTP/JSON/shape failures;
- preserve canonical request/response hashes;
- preserve provider request ID and returned model identity when exposed;
- never persist authentication credentials in provider profiles or call records;
- return provider content only as a candidate to the existing governed executor path;
- preserve independent verification, Socrates and rework semantics;
- keep CI regression tests independent from real credentials and real provider availability.

Provider-specific drivers SHALL be replaceable. A driver may map our bounded payload to a provider API and parse its response, but it cannot alter role identity, organizational authority, tool grants or acceptance semantics.

## Separation of claims
`LIVE_PROVIDER_BOUNDARY_READY ≠ LIVE_PROVIDER_PROVEN ≠ AGENT_FACTORY_SUMMIT_ACCEPTED`.

Mocked/fake transport proves our local boundary logic only. SUMMIT-FFB-02 remains open until a real authorized provider call supplies live evidence.

## Data policy
The first live pilot is restricted to PUBLIC/INTERNAL bounded inputs. RESTRICTED data is denied unless a later provider/data-processing profile explicitly proves that such egress is authorized and safe.

## Consequences
Positive:
- live-provider integration becomes a small replaceable driver/configuration problem;
- credentials stay out of Git and durable evidence;
- provider/data egress is explicit and auditable;
- provider output remains subordinate to verification/acceptance;
- future providers can be added without changing FATHER's management model.

Trade-offs:
- first live call requires explicit provider configuration and credential provisioning;
- provider-specific auth/token-refresh behavior still needs its own driver where applicable;
- external provider behavior remains unproven until actual execution.

## Evidence
- `schemas/LIVE_PROVIDER_PROFILE.yaml`;
- `schemas/LIVE_PROVIDER_CALL_RECORD.yaml`;
- `px00/live_provider.py`;
- `tests/test_live_provider.py`;
- `LIVE_PROVIDER_PILOT_READINESS.yaml`;
- RISK-0011 updated to MITIGATING.

## Follow-up
Select one authorized provider, implement exactly one provider driver, configure only non-sensitive pilot input and execute the first live PoC call through this boundary.
