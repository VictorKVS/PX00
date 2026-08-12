# DJ-0062 — Security Source-Pack CI Gate

Date: 2026-08-13
Tree_F: `TF-0074`
ADR: none
Summit: `SUMMIT-FFB-02` remains OPEN

## Change

Closed a proof-floor gap in canonical `VictorKVS/KNOWLEDGE_CORE`: Security Knowledge source packs under `security-knowledge/corpus/**` were not covered by the older Regulatory Corpus Gate.

Added a dedicated source-pack validator and GitHub Actions gate that checks the minimum semantics behind VERIFIED source/fact claims rather than trusting YAML labels or generic repository CI.

## Failed evidence

The first new workflow run failed for two implementation reasons: an overbroad corpus glob included non-pack control YAML, and PyYAML materialized ISO dates as `datetime.date` rather than strings. Both failures remain in Actions history.

The fixes narrowed artifact selection and accepted the YAML date type; VERIFIED evidence requirements were not weakened.

## Evidence

KNOWLEDGE_CORE commit `4333a0d9ddb51a53044d9564a8a7afb2b85a84e1` completed `Security Source Pack Gate` run 3 successfully. The validation step passed.

## Maturity restraint

`SOURCE PACK GATE PASS != VERIFIED APPLICABLE REQUIREMENT != EXPERT_READY`.

The TF-0072 requirement-level baseline remains the controlling blocker for a real D3 Security reasoning RUN until a genuinely atomic requirement is promoted with exact primary-source proof and applicability.

No real Gemini credential was available or invented; `SUMMIT-FFB-02` and `RISK-0011` are unchanged.

## Next

Promote one atomic Security requirement through the strict proof floor, then use it in the bounded D3 professional decision path. The independent live-executor stream still requires exactly one authorized PUBLIC Gemini inference.
