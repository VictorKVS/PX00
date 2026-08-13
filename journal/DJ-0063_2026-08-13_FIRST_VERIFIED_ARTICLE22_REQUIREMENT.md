# DJ-0063 — First VERIFIED Article 22 Requirement

Date: 2026-08-13
Tree_F: `TF-0075`
ADR: none
Summit: `SUMMIT-FFB-02` remains OPEN

## Change

Promoted the first genuinely strict VERIFIED Security requirement in canonical `VictorKVS/KNOWLEDGE_CORE`: Federal Law 152-FZ, Article 22 part 1, notification before beginning personal-data processing, bounded by the explicit exceptions in part 2.

The atom now carries primary-source locator/quote, actor/trigger/action/deadline, D3 materiality, applicability boundary, evidence expectations and mapping to the Order 180 notification form.

## Proof-model defect found and fixed

The source-pack gate initially assumed every VERIFIED Russian source must be represented by a modern `publication.pravo.gov.ru` publication card. That model was too narrow for a long-lived federal law whose current official consolidated text is served by `ips.pravo.gov.ru`.

The gate now admits two explicit official evidence channels rather than arbitrary mirrors: official publication records and official consolidated legal text. A regression test rejects non-official hosts.

## Evidence restraint

This requirement is VERIFIED only for the positive duty in Article 22 part 1. It does not prove that notification is required in a concrete case until Article 22 part 2 exceptions are evaluated. A no-notification conclusion must fail closed until those exceptions are atomized or independently resolved from primary law.

`VERIFIED ATOM != CASE APPLICABILITY DECISION != EXPERT_READY`.

## Next

Run one bounded D3 professional decision using this atom and explicitly test the unresolved-exception path. The independent live-executor stream remains blocked only by absence of an authorized real Gemini credential; no live evidence is being imitated.
