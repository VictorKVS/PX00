# TF-0072 — Security Atomic Requirement Verification Gate

Date: 2026-08-13
Status: COMPLETE — PRODUCT INTEGRITY GATE
Affected canonical product: `VictorKVS/KNOWLEDGE_CORE/security-knowledge/`

## Trigger

TF-0071 made evidence-backed professional decisions traceable. The next planned step was the first real D3 Security decision using a canonical atomic `VERIFIED` requirement.

During readiness inspection, FSTEK Order No. 31 requirement files contained atomic records labeled `VERIFIED` with exact locators but without `source_quote`, while the canonical FSTEK requirement schema explicitly requires both locator and source quote for VERIFIED state.

This meant the repository could be CI-green while a Security requirement self-declared a stronger verification state than the stated proof rule allowed.

## Correction

The affected FSTEK-31 atomization was preserved but verification state was downgraded from `VERIFIED` to `REVIEWED` in:
- `requirements/core.yaml`;
- `requirements/technical-specification.yaml`;
- `requirements/threat-model.yaml`.

No normative quote was fabricated and no semantic content was deleted.

## New executable gate

KNOWLEDGE_CORE now runs:
- `tools/test_security_requirement_validation.py`;
- `tools/validate_security_requirements.py`.

A requirement can be `VERIFIED` only when it has:
1. stable requirement ID;
2. source document identity;
3. exact `source_locator`;
4. non-empty `source_quote` from the admitted source.

Missing verification state is conservatively interpreted as `UNVERIFIED`, allowing legacy seed/extraction records to remain without creating false trust.

## Evidence

Knowledge Quality Gate on head `37669d23fc4c3f88ad2b13946ff9e93ff3f3f667` passed all steps, including 6 validator tests, corpus validation and historical snapshot validation.

Observed corpus baseline:
- requirement files: 9;
- atomic requirements: 82;
- requirements satisfying strict VERIFIED proof floor: **0**.

Canonical readiness record:
`security-knowledge/expert-evaluation/atomic-requirement-verification-readiness.yaml`.

## Maturity consequence

First real D3 Security reasoning RUN is **BLOCKED_BY_KNOWLEDGE_PROOF_FLOOR** until at least one applicable atomic requirement is truly VERIFIED and exportable.

This does not block:
- continued Security corpus production;
- REVIEWED/EXTRACTED atomization;
- `SUMMIT-FFB-02` live-provider work.

## First promotion target

`FSTEK31-REQ-001` — p. 10 — appointment of a structural unit or employee responsible for information protection.

Current state: `REVIEWED`.

Promotion requires:
- exact source quote from the admitted primary source/revision;
- independent check that the normalized atomic interpretation faithfully represents that quote.

## Principle reinforced

`VERIFIED IS AN EARNED STATE, NOT A LABEL.`

A green repository must prove the promotion conditions; it must not merely parse YAML containing the word VERIFIED.

## Next

Two independent productive tracks continue:
1. Security Knowledge: produce the first true VERIFIED atomic requirement without weakening the gate;
2. Factory Builder: close `SUMMIT-FFB-02` with one governed real AI inference.

The first closed professional FATHER loop starts only after both prerequisites are available.
