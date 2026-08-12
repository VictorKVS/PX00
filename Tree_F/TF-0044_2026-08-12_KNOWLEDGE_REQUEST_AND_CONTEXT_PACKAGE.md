# TF-0044 — Knowledge Request and Context Package

Date: 2026-08-12
Status: implemented; CI pending on generation head
ADR: ADR-0039

## Generation
Added bounded knowledge requests and immutable context packages delivered to one agent assignment for one RUN.

## Surfaces
- `schemas/KNOWLEDGE_REQUEST.yaml`
- `schemas/CONTEXT_PACKAGE.yaml`
- `px00/context_packages.py`
- `tests/test_context_packages.py`
- `architecture/adr/ADR-0039-knowledge-request-and-context-package.md`

## Core proof
A role binding identifies allowed logical knowledge domains; a KnowledgeRequest narrows them for a task/run; ContextPackage records the exact stable object IDs and route snapshots delivered to the agent.

## Next
Task-to-responsibility routing and RUN assignment pinning should consume ContextPackage rather than raw KB access.
