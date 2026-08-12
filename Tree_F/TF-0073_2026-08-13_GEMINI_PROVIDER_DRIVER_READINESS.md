# TF-0073 — Gemini Provider Driver Readiness

Date: 2026-08-13
Status: COMPLETE — PROVIDER-SPECIFIC LOCAL READINESS
ADR: `ADR-0065`
Summit: `SUMMIT-FFB-02 — First Governed Live Executor` remains OPEN
Risk: `RISK-0011` remains MITIGATING

## Why this generation exists

The provider-neutral live boundary was ready, but no concrete external AI provider had yet been mapped. Selecting Google Gemini exposed a real portability defect before any live call: the reference adapter hardcoded `Authorization: Bearer`, while Gemini's Interactions REST API authenticates with a provider-specific API-key header.

TF-0073 fixes the boundary without creating a Gemini-specific transport fork and adds the first concrete provider driver.

## Implemented

### Header-auth portability
`LiveProviderProfile` now controls:
- authentication header name;
- authentication prefix;
- runtime credential environment reference.

Defaults preserve existing Bearer behavior.

Validation rejects unsafe header names and CR/LF in configured prefixes.

### Gemini Interactions driver
Added `px00/gemini_provider.py`.

Bounded pilot request:
- endpoint family: Gemini Interactions API;
- API version: stable `v1`;
- model reference: `gemini-3.6-flash`;
- text input only;
- `store=false`;
- no tools;
- no provider agent;
- no grounding;
- no files;
- no multimodal input;
- no background execution.

Bounded output:
- interaction must be `completed`;
- only `model_output` text becomes candidate content;
- provider thought state is not copied into the candidate or treated as evidence;
- function/tool steps fail closed;
- non-text output fails closed;
- interaction ID and returned model are captured as provenance when present.

### Concrete pilot profile
`projects/FATHER_FACTORY_BUILDER/pilots/agent_rd_factory/providers/GEMINI_INTERACTIONS_V0_1.yaml`

The first real-provider pilot allows only `PUBLIC` data classification.

Runtime opt-in and credential remain external:
- `PX00_GEMINI_LIVE_ENABLED`;
- `GEMINI_API_KEY`.

Credential values are not stored in Git, call records, candidate artifacts or trace metadata.

## Tests

Added `tests/test_gemini_provider.py` proving:
1. request shape is bounded and tool-free;
2. extra provider capabilities are rejected;
3. text input size/emptiness is checked;
4. completed model text is extracted;
5. provider thought state is not copied as candidate evidence;
6. incomplete responses fail closed;
7. non-text output fails closed;
8. unexpected function calls fail closed;
9. interaction ID/model are preserved as provenance;
10. `x-goog-api-key` is used instead of Bearer Authorization for Gemini;
11. credential value is absent from call record/candidate provenance;
12. INTERNAL egress is blocked by the PUBLIC-only profile;
13. auth header/prefix injection syntax is rejected.

Existing provider-neutral Bearer tests remain green.

## CI evidence

Implementation head `eabc63454e4cc4b7dd83e8e5572d15c210824eeb` passed:
- unit/repository integration tests;
- secret leakage scan;
- PX00 contract validation.

## What is proven

`GENERIC HEADER-AUTH BOUNDARY → GEMINI-SPECIFIC REQUEST/RESPONSE MAPPING` is locally proven without changing role identity, executor authority semantics or verifier/Socrates position.

## What is NOT proven

- no authorized real Gemini inference has yet been executed through this runtime;
- credential validity/token/account lifecycle is unproven;
- real latency, cost, rate limits and provider error behavior are unproven;
- provider-side exact immutable model build identity is not claimed;
- live candidate quality and rework are unproven;
- `SUMMIT-FFB-02` is therefore NOT accepted.

## Key invariant

`DRIVER READY != LIVE CALL PROVEN != SUMMIT ACCEPTED`.

## Next gate

Execute exactly one explicitly authorized PUBLIC text inference through `LIVE-GEMINI-INTERACTIONS-0001`, persist sanitized call evidence, independently verify the candidate, run Socrates, then ARGUS.

No additional provider abstraction is justified before that real call exposes a concrete need.
