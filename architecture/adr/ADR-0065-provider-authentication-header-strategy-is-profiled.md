# ADR-0065 — Provider Authentication Header Strategy Is Profiled

Status: ACCEPTED
Date: 2026-08-13

## Context

The M1 live-provider boundary introduced in TF-0064 separated credential values from repository configuration, but the reference adapter still hardcoded one HTTP authentication shape:

`Authorization: Bearer <runtime credential>`.

That was sufficient for the synthetic reference provider but was not actually provider-neutral. The first concrete external provider selected for `SUMMIT-FFB-02`, Google Gemini Interactions API, uses an API key in the `x-goog-api-key` request header.

A provider-specific driver should map request/response semantics, but it should not need to fork the transport/secret boundary merely because an API uses a different safe header name/prefix.

## Decision

For header-based provider authentication, `LIVE_PROVIDER_PROFILE` owns:
- `auth_header_name`;
- `auth_header_prefix`;
- runtime credential environment reference.

The credential **value** remains runtime-only and is never persisted in the profile, call record, trace or candidate provenance.

Backward compatibility is preserved:
- default header: `Authorization`;
- default prefix: `Bearer `.

The Gemini pilot profile uses:
- header `x-goog-api-key`;
- empty prefix.

Header names are validated as restricted HTTP token characters. CR/LF are forbidden in the configured prefix.

## Scope boundary

This ADR does **not** claim universal support for every authentication mechanism.

The current boundary supports safe header-carried credentials. Providers requiring request signing, OAuth token exchange, mTLS, query-string credentials or other materially different authentication semantics require a separate governed extension and evidence review rather than being squeezed into this profile.

## Gemini pilot mapping

The first concrete driver is `GeminiInteractionsDriver` for the stable Gemini Interactions REST endpoint.

The M1 pilot intentionally allows only:
- text input;
- one pinned model reference;
- PUBLIC data classification;
- synchronous inference;
- candidate text output.

It explicitly excludes tools, provider agents, grounding, files, multimodal input and background execution.

Unexpected provider function/tool steps or non-text output fail closed.

## Consequences

Positive:
- live-provider transport remains reusable across multiple header-auth providers;
- Gemini does not require a duplicated credential/egress implementation;
- prior Bearer tests remain valid;
- provider-specific capability expansion stays isolated from authority semantics.

Cost:
- auth header configuration becomes integrity-sensitive profile data;
- providers outside the header-auth family still need a future explicit extension.

## Invariants

`PROVIDER AUTHENTICATION != RUNTIME AUTHORITY`.

`PROVIDER CALL SUCCESS != VERIFICATION PASS != ACCEPTANCE`.

`DRIVER READY != LIVE CALL PROVEN != SUMMIT ACCEPTED`.

## Evidence

- `px00/live_provider.py`
- `schemas/LIVE_PROVIDER_PROFILE.yaml`
- `px00/gemini_provider.py`
- `projects/FATHER_FACTORY_BUILDER/pilots/agent_rd_factory/providers/GEMINI_INTERACTIONS_V0_1.yaml`
- `tests/test_live_provider.py`
- `tests/test_gemini_provider.py`
