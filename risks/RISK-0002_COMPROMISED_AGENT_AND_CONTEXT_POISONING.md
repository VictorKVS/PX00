# RISK-0002 — Compromised Agent and Context Poisoning Threat Model Gap

Status: MITIGATING
Severity: S4
Category: SECURITY
Source: ARGUS-SEC-002
Owner: ROLE-SECURITY-ARCHITECT

## Risk
PX00 must assume an assigned agent, model provider, retrieved knowledge object, prompt/context source or tool result may be malicious, compromised or adversarially crafted.

## Immediate containment implemented
A `CONTEXT_TRUST_ASSESSMENT` and fail-closed `ContextTrustGate` now establish the first hard boundary:
- context can never manufacture authority or capability;
- `TAINTED` context may be analyzed but cannot directly drive material action;
- `UNTRUSTED_EXTERNAL` context requires independent verification before material use;
- even `VERIFIED_EXTERNAL` context requires independent verification for sensitive material action;
- unknown trust labels fail closed.

This is containment, not final closure.

## Final remediation still required
- complete trust-boundary/threat model for agent, provider, tools, KB and external inputs;
- taint propagation across derived context/results;
- prompt/context injection detection and policy handling;
- independent reviewer eligibility and separation of duties;
- capability emergency revocation / kill switch;
- compromised-assignment quarantine and replacement protocol;
- adversarial integration tests proving no authority expansion, review bypass or silent knowledge promotion.

## Verification
The risk remains S4 until the containment is integrated into the actual material-action path and verified end-to-end. After verified isolation, ARGUS may reassess the residual risk to S3 while full adversarial hardening continues.
