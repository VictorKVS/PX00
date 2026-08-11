# ADR-0002 — Integrated Management System Architecture

Status: ACCEPTED FOR BASELINE 0.1

## Context

PX00 must support governance, quality, risk, security, AI governance, compliance, continuity, lifecycle management, audit, and improvement without creating isolated management silos.

## Decision

PX00 shall model these disciplines as one integrated management system with shared concepts for requirements, controls, risks, evidence, decisions, roles, audits, exceptions, corrective actions, and improvement.

Standards and regulatory frameworks are mapped into this canonical model. Referencing or mapping a standard does not constitute certification.

## Consequences

- One canonical control may satisfy multiple mapped requirements.
- Risk, compliance, security, quality, and AI governance share traceability primitives.
- Framework-specific terminology remains available through mappings and profiles.
- Duplicate control implementations are avoided where a canonical control is sufficient.
