# DJ-0039 — Maturity-Gated Risk Management

Date: 2026-08-12
Tree_F: TF-0050
ADR: ADR-0045
Source audit: ARGUS_AUDIT_0001

## Decision
PX00 now treats risk as a maturity constraint, not as a passive backlog. Reliability outranks speed at critical boundaries.

## Operating model
Every material risk has:
- immediate containment;
- final remediation;
- owner;
- verification criteria;
- latest maturity where it may remain unresolved;
- residual/reopened history.

S4 cannot be accepted or merely monitored. It must be eliminated or isolated/disabled immediately. Lower severities may coexist with prototype work only inside explicit maturity gates.

## Concrete progress
RISK-0001 moved to VERIFYING after Context Package v0.2 began pinning exact knowledge object version + SHA-256 content digest.

RISK-0002 moved to MITIGATING after a first ContextTrustGate was added. This is containment only; the S4 remains until the gate is integrated into the material-action path and adversarial tests prove the isolation.

## Project implication
Feature development can continue in unrelated bounded scopes. Promotion to higher maturity is blocked per risk scope and severity rather than by an indiscriminate project-wide freeze.

## Next risk order
RISK-0001 verification -> RISK-0002 action-path integration -> RISK-0008 ID uniqueness CI -> RISK-0004 concurrency/idempotency -> RISK-0003 durable persistence -> RISK-0005 executor snapshot -> RISK-0006 reviewer independence -> RISK-0007 culture/anti-Goodhart charter.
