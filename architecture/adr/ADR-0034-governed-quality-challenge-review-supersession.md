# ADR-0034 — Governed Quality Challenge, Review and Supersession

Date: 2026-08-12
Status: accepted

## Context
Source and evidence quality assessments are now immutable governed objects. They must still be challengeable without allowing a challenger or reviewer to rewrite historical assessments.

## Decision
Introduce immutable ASSESSMENT_CHALLENGE and ASSESSMENT_REVIEW records. A challenge may propose revised quality dimensions but is never self-executing. A review may reject, escalate, or accept the challenge. Acceptance requires creation of a new replacement assessment for the same underlying source/evidence. The replacement explicitly supersedes the challenged assessment; the old assessment remains immutable and addressable.

## Invariants
- challenger cannot mutate or directly supersede target assessment
- reviewer cannot rewrite target assessment
- accepted challenge requires a distinct replacement assessment
- replacement must address the same source/evidence subject
- rejected challenge preserves target history unchanged
- challenge, review, basis and replacement lineage remain inspectable
- proposed `truth` or other undeclared dimensions are invalid

## Consequences
Socrates and future reviewers can contest not only claims, but the quality assumptions beneath claims. Historical reasoning remains reproducible because every prior assessment survives supersession.
