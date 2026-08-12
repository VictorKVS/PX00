# TF-0050 — Maturity-Gated Risk Management

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0045

## Generation
Introduced the first operational risk-management matrix for PX00 with maturity gates, scope-aware blocking, immediate containment and final remediation.

## Added
- `governance/RISK_MANAGEMENT_MATRIX.md`
- `schemas/RISK_TREATMENT_PLAN.yaml`
- `px00/risk_gates.py`
- `tests/test_risk_gates.py`
- `risk_treatments/TREATMENT-0001_ARGUS_AUDIT_0001.md`

## Immediate S4 work
RISK-0001 remediation was implemented in Context Package v0.2: exact knowledge object version and SHA-256 content digest are now pinned into package hashing and covered by tests.

RISK-0002 received a first fail-closed containment layer through `CONTEXT_TRUST_ASSESSMENT` and `ContextTrustGate`: context cannot manufacture authority, and untrusted/tainted context cannot directly drive material sensitive action without independent verification.

## Management rule
Critical risk treatment outranks feature velocity. Unrelated bounded prototype work may continue while risks are contained within their maturity envelope.

## Next
1. Verify RISK-0001 on full CI and close/reassess it.
2. Integrate ContextTrustGate into the real ActionRequest/Authority/Tool path and re-audit RISK-0002 residual severity.
3. Implement global canonical-ID uniqueness CI for RISK-0008.
4. Define transaction/idempotency semantics before durable persistence.
