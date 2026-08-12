# TF-0074 — Security Source-Pack CI Gate

Date: 2026-08-13
Status: COMPLETE — BOUNDED PROOF-FLOOR HARDENING
ADR: none; no architecture change justified
Summit: `SUMMIT-FFB-02` remains OPEN

## Why this generation exists

A fresh canonical Security Knowledge source pack had authoritative publication metadata and atomic facts, but `security-knowledge/corpus/**` was not covered by the existing Regulatory Corpus Gate. Generic repository CI and indexing therefore could not prove that VERIFIED source/fact claims met even the source-pack proof floor.

## Implemented in KNOWLEDGE_CORE

Added `tools/validate_security_source_packs.py` and `.github/workflows/security-source-pack-gate.yml`.

The gate now checks declared `*source-pack*.yaml|yml` records and fails closed when:
- pack identity or sources are absent;
- source IDs or fact IDs collide;
- a VERIFIED Russian source lacks official publication number/date/HTTPS `publication.pravo.gov.ru` URL;
- a VERIFIED atomic fact references an unresolved source;
- a VERIFIED atomic fact lacks locator or conservative statement.

The scope deliberately excludes unrelated corpus control files such as completeness matrices and snapshot schemas.

## Failed evidence preserved

The first workflow run failed. It revealed two validator defects:
1. the initial glob treated every corpus YAML as a source pack;
2. PyYAML parses ISO dates as `datetime.date`, while the validator initially accepted strings only.

Neither failure was hidden. The gate was corrected rather than the corpus weakened.

## Evidence

`Security Source Pack Gate` run 3 on KNOWLEDGE_CORE commit `4333a0d9ddb51a53044d9564a8a7afb2b85a84e1` completed successfully; its validation step passed.

Independent web verification during this generation confirmed the official publication identifiers for Roskomnadzor Order 140/2025 and Government Decree 1154/2025 used by the first source pack.

## What is proven

Declared Security Knowledge source packs can no longer rely only on generic CI/indexing when claiming VERIFIED source/fact state; a dedicated executable proof-floor check now runs on changes to those packs or the validator.

## What is not proven

This does not atomize annexes, prove applicability, prove every quoted requirement, or make Security Knowledge EXPERT_READY. It also does not unblock the D3 professional Security RUN by itself.

## Next

Promote one genuinely atomic requirement with exact primary-source proof and applicability, then exercise the bounded D3 decision path. In parallel, `SUMMIT-FFB-02` still needs one authorized PUBLIC Gemini inference.
