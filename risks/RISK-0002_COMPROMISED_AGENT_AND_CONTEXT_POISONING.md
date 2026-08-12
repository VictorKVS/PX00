# RISK-0002 — Compromised Agent and Context Poisoning Threat Model Gap

Status: OPEN
Severity: S4
Category: SECURITY
Source: ARGUS-SEC-002
Owner: ROLE-SECURITY-ARCHITECT

## Risk
PX00 constrains authority but does not yet model an assigned agent, model provider, retrieved knowledge object, prompt/context source or tool result as potentially malicious or compromised.

## Required mitigation
Define trust boundaries, taint/provenance labels, prompt/context injection controls, independent verification, emergency revocation and compromised-assignment response.

## Verification
Adversarial tests must show that malicious context cannot silently expand authority, bypass review, or become trusted knowledge without provenance and verification.
