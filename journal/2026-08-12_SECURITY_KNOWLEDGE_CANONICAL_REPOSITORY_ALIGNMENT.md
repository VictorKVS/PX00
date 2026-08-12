# DJ-0054 — Security Knowledge Canonical Repository Alignment

Date: 2026-08-12
Related: ADR-0059, TF-0066

## Where we were wrong
During portfolio-roadmap work, PX00 briefly started creating its own Security Knowledge product coverage/readiness/source-backlog artifacts even though `SEC-PROD-0001` already exists and is actively populated in `VictorKVS/KNOWLEDGE_CORE`.

That would have created a long-term dual-source-of-truth risk.

## Correction
Canonical product/domain truth is now explicitly assigned to KNOWLEDGE_CORE:
- `security-knowledge/` — Security Knowledge product implementation;
- `father/domain-knowledge/` — Father professional domain management;
- `father/product-roadmap/` — canonical security/master product roadmaps.

PX00 now retains only route records plus runtime orchestration/assurance responsibilities.

Duplicate PX00 Security Knowledge coverage/readiness/source-backlog artifacts and duplicate runtime readiness gate were removed.

## Product state recognized
Security Knowledge is already beyond initial schema conception: evidence-driven KB architecture, atomic requirements/checklists, organization profile/applicability, legal-force classification, Unified Controls, expert metrics and completeness/expert-readiness structures exist, while the Russian normative P0 corpus is actively being populated.

Current evidence pipeline is preserved:
`SOURCE → VERSION → CHUNK → ATOMIC CLAIM/REQUIREMENT → APPLICABILITY → RELATIONS → CONTROL → CHECK → EVIDENCE → EXPERT REVIEW`.

`VERIFIED` remains restricted to knowledge backed by an admitted primary source and exact locator.

## Primary build order
FSTEC → FSB P0 (GosSOPKA/NKCKI/SKZI/revisions) → Roskomnadzor → base laws/government acts/decrees → sector regulators → GOST → ISO → NIST/CIS/OWASP → BDU/CVE/CWE/ATT&CK → pentest/vulnerability/risk → vendor hardening → large-scale Unified Control/evidence/expert consolidation.

## Architectural lesson
Security Knowledge must not become ordinary RAG over PDFs. Retrieval is infrastructure; the product is the evidence and applicability/control/verification/risk graph plus expert-reviewed derivation.

## Parallel work decision
`SUMMIT-FFB-02` live-provider work may continue in parallel. It is not a blocker for Security Knowledge corpus construction.

## Outcome
Cross-repository responsibility is now explicit and compatible with the long-term multi-domain model:
`KNOWLEDGE_CORE = domain/product knowledge truth`, `PX00 = governed organizational runtime`.
