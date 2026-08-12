# FFBJ-0020 — Gemini Provider Driver Readiness

Date: 2026-08-13
Tree_F: `TF-0073`
ADR: `ADR-0065`
Summit: `SUMMIT-FFB-02` remains OPEN

## Trigger

After Security Knowledge correctly blocked the first D3 professional run at its proof floor, Factory Builder continued the independent live-executor stream.

The first concrete provider selection exposed a real interface assumption: the M1 transport boundary was credential-safe but hardcoded to Bearer authentication.

## Action

Added a profile-controlled header authentication strategy and the first concrete provider driver:
- Gemini Interactions REST mapping;
- stable `v1` endpoint profile;
- pinned `gemini-3.6-flash` model reference;
- PUBLIC-only egress;
- text-only candidate;
- no tools/grounding/agent/files/background execution;
- fail-closed function/non-text response handling.

## Proven

Local provider-specific mapping passes the full PX00 contract pipeline while preserving old Bearer-provider behavior.

Credential material remains runtime-only and does not enter call records or candidate provenance.

## Not proven

No real authorized external inference has yet occurred. The summit cannot close on a fake transport/response.

`RISK-0011` remains MITIGATING.

## Next

Exactly one authorized PUBLIC Gemini inference, followed by independent verification, Socrates and ARGUS. Do not add another provider before this path is exercised unless a real blocker makes replacement necessary.
