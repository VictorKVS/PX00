# TF-0075 — Security Primary-Source Proof-Channel Hardening

Date: 2026-08-13
Status: COMPLETE — PROOF-CHANNEL + CI HARDENING
ADR: none; no architecture change justified
Summit: `SUMMIT-FFB-02` remains OPEN

## Trigger

During this generation the repository advanced concurrently: `KNOWLEDGE_CORE` gained a broader canonical 152-FZ requirement file with 19 VERIFIED atoms, including Article 22 part 1. The initially created one-atom Article 22 source pack was therefore redundant and, because it referenced an older consolidated edition, could become a conflicting truth source.

The duplicate source pack was removed rather than retained.

## Durable improvement

The source-pack validator exposed a real proof-model defect: it recognized only modern publication cards at `publication.pravo.gov.ru`, but long-lived laws may need a current official consolidated text from `ips.pravo.gov.ru`.

The validator now distinguishes two explicit official channels:
- `official_publication` → `publication.pravo.gov.ru`;
- `official_text` → `ips.pravo.gov.ru` + required `edition_as_of`.

Arbitrary mirrors remain rejected.

Regression tests prove acceptance of the official consolidated-text host and rejection of a non-official host.

## Failed evidence preserved

Full `Knowledge Quality Gate` on commit `b9e6fb9d8cc764fa34d9c6e1f3d4807044a0fc89` failed on pre-existing invalid YAML in `security-knowledge/audits/coverage-scorecard-2026-08-13-run-02.yaml` (`gap:` values containing unquoted colons). The scorecard YAML was corrected rather than bypassed.

## Current Security proof state

The controlling canonical file is `security-knowledge/legislation/requirements/152-fz-core-operator-obligations-verified.yaml`, which records 19 VERIFIED operator-duty atoms from Articles 18.1, 19, 21, 22 and 22.1, including Article 22 part 1.

The repository itself still marks the broader Security corpus `expert_ready: false`; Article 22 part 2 exception logic and exact KoAP consequence mappings remain open.

## What is proven

The proof-floor now supports an official consolidated-law evidence channel without opening verification to arbitrary third-party hosts, regression tests protect that boundary, and a duplicate stale source was removed when a fresher canonical requirement slice appeared.

## Next

Use the existing canonical 152-FZ VERIFIED slice in one bounded D3 professional decision path, including fail-closed handling where Article 22 part 2 exceptions are unresolved. `SUMMIT-FFB-02` remains independently OPEN pending one authorized PUBLIC Gemini inference.
