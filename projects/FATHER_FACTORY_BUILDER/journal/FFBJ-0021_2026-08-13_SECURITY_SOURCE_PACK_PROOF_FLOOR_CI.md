# FFBJ-0021 — Security Source-Pack Proof-Floor CI

Date: 2026-08-13
Tree_F: `TF-0074`

A newly populated canonical Security Knowledge source pack exposed a control gap: the existing Regulatory Corpus Gate watched the older `security-corpus/**` path, not `security-knowledge/corpus/**`.

KNOWLEDGE_CORE now has a dedicated executable source-pack gate. It checks declared source packs for identity, source/fact reference integrity and minimum VERIFIED proof metadata, including official Russian publication metadata and locators for VERIFIED atomic facts.

The first workflow execution failed because the initial implementation selected unrelated corpus YAML and treated YAML dates as strings only. Failed evidence was preserved; the implementation was corrected without weakening VERIFIED semantics.

Green evidence: KNOWLEDGE_CORE commit `4333a0d9ddb51a53044d9564a8a7afb2b85a84e1`, `Security Source Pack Gate` run 3, validation step PASS.

Maturity remains conservative: a source-pack gate does not turn source metadata into an applicable atomic requirement and does not make Security Knowledge EXPERT_READY. The professional D3 Security path remains blocked until one strict requirement is promoted with exact primary-source proof and applicability.

`SUMMIT-FFB-02` remains OPEN because no authorized real Gemini inference has occurred.

Next: strict atomic requirement promotion → bounded D3 decision; live Gemini proceeds independently when a real credential is available.
