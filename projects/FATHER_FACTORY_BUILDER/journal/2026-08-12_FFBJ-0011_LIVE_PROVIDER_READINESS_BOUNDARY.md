# FFBJ-0011 — Live Provider Readiness Boundary

Date: 2026-08-12
Project: PROJECT-FFB-0001
Generation: TF-0064
ADR: ADR-0057

## Where we are
SUMMIT-FFB-02 remains OPEN, but the provider-neutral executor boundary now has a secret-safe and data-egress-aware HTTPS layer ready for one real provider driver/configuration.

## What was implemented
- live provider profile contract;
- append-only live provider call metadata contract;
- HTTPS host allowlisting;
- explicit runtime live-enable gate;
- runtime credential reference/value separation;
- data-classification egress gate;
- timeout and response-size bounds;
- HTTP/JSON/shape fail-closed behavior;
- request/response hashes;
- provider request/model identity capture when available;
- integration through existing GovernedExecutorBoundary;
- first live-provider pilot readiness record.

## Failure found during development
The first CI run failed secret hygiene because the implementation used a local variable named `secret`. The defensive scanner treated it as a potential secret assignment.

The scanner was not weakened. The implementation was changed to comply with the existing security control, after which unit/integration, secret hygiene and repository contract validation passed.

Lesson: security controls are allowed to constrain implementation ergonomics; implementation is not allowed to disable the control merely to become green.

## Risk impact
`RISK-0011` moved from OPEN to MITIGATING.

Locally proven containment now covers endpoint identity, opt-in, credential non-persistence, egress classification, bounded transport and provider evidence metadata. The risk remains unresolved because no actual provider authentication, latency, rate limit, response schema, model drift or non-deterministic output has yet been observed.

## Lifecycle classification
The first live inference will be:
- CRISP-ML(Q): DEPLOYMENT integration experiment;
- delivery stage: POC;
- PX00 maturity: M1_PROTOTYPE.

These are independent labels.

## Next summit action
Configure one authorized provider and one provider-specific driver, send only PUBLIC/INTERNAL bounded data, execute one real inference without tools, and pass the candidate through independent verification and Socrates. A bad live result must be rejectable and reworkable.

## Maturity statement
`LIVE_PROVIDER_BOUNDARY_READY = YES`.
`LIVE_PROVIDER_PROVEN = NO`.
`SUMMIT-FFB-02 = OPEN`.
