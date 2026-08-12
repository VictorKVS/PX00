# ADR-0032 — Immutable Temporal Claim Assessment

Date: 2026-08-12
Status: accepted

## Context
The provenance graph preserves claims and evidence, while ClaimEvidenceEvaluator computes a support state. PX00 needs to preserve what was believed at a specific time without allowing later evidence to rewrite prior assessments.

## Decision
Introduce immutable CLAIM_ASSESSMENT records. Each assessment binds one exact claim ID to an exact material evidence set, canonical evidence-set SHA-256, evaluator identity/version, timestamp, support/contradiction scores and visible confidence dimensions.

A new assessment references the previous assessment for the same claim. New or removed evidence always produces a new assessment; prior assessments remain unchanged.

## Boundary
Assessment status is a reproducible epistemic state, not a truth declaration. The current bridge from graph EvidenceNode to evaluator EvidenceItem uses reference quality defaults until quality metadata is governed in SOURCE/EVIDENCE contracts; those defaults must not be interpreted as external source certification.

## Consequences
PX00 can answer historically why a claim was SINGLE_SOURCE, CORROBORATED or DISPUTED at different moments and can reproduce the exact evidence set used for each assessment.
