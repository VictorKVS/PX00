# DJ-0063 — Security Primary-Source Proof-Channel Hardening

Date: 2026-08-13
Tree_F: `TF-0075`
ADR: none
Summit: `SUMMIT-FFB-02` remains OPEN

## Change

Hardened the Security source-pack verifier so VERIFIED legal sources can use either a modern official publication card (`publication.pravo.gov.ru`) or an official consolidated legal text (`ips.pravo.gov.ru` with `edition_as_of`), while arbitrary mirrors remain rejected.

Added regression tests for the accepted official consolidated-text path and rejected non-official-host path.

## Concurrent-state correction

During the run, KNOWLEDGE_CORE independently advanced with `security-knowledge/legislation/requirements/152-fz-core-operator-obligations-verified.yaml`: 19 VERIFIED 152-FZ atoms, including Article 22 part 1, on a newer checked edition. The one-atom Article 22 source pack created earlier in this run became redundant and potentially stale, so it was deleted. Canonical truth was not duplicated.

## Failed evidence

Full Knowledge Quality Gate then exposed invalid YAML in `coverage-scorecard-2026-08-13-run-02.yaml` caused by unquoted colons inside plain scalar gap descriptions. The file was corrected; the quality gate was not bypassed.

## Maturity restraint

The wider Security KB remains `expert_ready: false`. Article 22 part 2 exception logic and exact KoAP mappings remain open. `VERIFIED REQUIREMENTS != COMPLETE APPLICABILITY != EXPERT_READY`.

`SUMMIT-FFB-02` remains OPEN because no authorized real Gemini credential/inference is available; no live evidence was fabricated.

## Next

Exercise the current canonical 152-FZ VERIFIED slice through one bounded D3 professional decision, including a fail-closed exception path.
