# TF-0075 — First VERIFIED Article 22 Requirement

Date: 2026-08-13
Status: COMPLETE — FIRST STRICT VERIFIED APPLICABLE SECURITY ATOM
ADR: none; no architecture change justified
Summit: `SUMMIT-FFB-02` remains OPEN

## Why this generation exists

TF-0072 established a strict requirement proof floor and TF-0074 added a source-pack CI gate, but the Security product still had no genuinely VERIFIED applicable atomic requirement that could serve as admissible D3 decision evidence.

## Implemented in KNOWLEDGE_CORE

Added `security-knowledge/corpus/ru-personal-data/152fz-article22-notification-source-pack.yaml` with one narrowly bounded statutory atom from Federal Law 152-FZ, Article 22 part 1.

The atom records:
- exact locator: `Article 22, part 1`;
- short primary-source quote;
- conservative statement;
- actor, trigger, action and deadline boundary;
- explicit applicability condition requiring that no Article 22 part 2 exception applies;
- evidence expectations;
- form mapping to Roskomnadzor Order 180/2022;
- D3 decision materiality;
- explicit unresolved detail requiring separate atomization of part 2 exceptions before asserting that notification is unnecessary.

## Proof-source correction

While encoding the requirement, the existing source-pack validator exposed a real proof-model defect: it allowed only `publication.pravo.gov.ru`, which fits modern publication records but not the official consolidated text channel used for a long-lived federal law.

The validator now distinguishes:
- `official_publication` on `publication.pravo.gov.ru`;
- `official_text` on `ips.pravo.gov.ru`, with required `edition_as_of`.

This is not a relaxation to arbitrary mirrors. Non-official hosts remain rejected.

Regression tests were added for acceptance of the official IPS consolidated-text source and rejection of an untrusted host.

## Primary evidence

The current official consolidated text of Federal Law 152-FZ exposes Article 22 part 1: the operator must notify the competent authority before beginning personal-data processing, except for the cases in part 2. The same official text states the separate Article 22 part 7 clocks for changes and termination; those were deliberately not merged into this first atom.

## What is proven

Security Knowledge now has at least one strict VERIFIED D3-capable atomic legal requirement with primary-source locator, bounded applicability and explicit evidence expectations.

## What is not proven

This does not make the whole Security Knowledge Base `EXPERT_READY` and does not prove that every operator must notify. Article 22 part 2 exceptions remain to be atomized before any production decision may assert a no-notification exception.

It also does not complete a professional D3 reasoning RUN by itself; it removes the zero-VERIFIED-requirement blocker for a bounded test slice.

## Next

Exercise this atom through one bounded D3 professional Security decision path with independent review and fail-closed handling of unresolved Article 22 part 2 exceptions.

In parallel, `SUMMIT-FFB-02` still requires one authorized real PUBLIC Gemini inference; no credential was invented and no live call was simulated.
