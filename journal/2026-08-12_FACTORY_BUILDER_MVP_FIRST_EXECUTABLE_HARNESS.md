# DJ-0047 — Factory Builder MVP-first executable harness

Date: 2026-08-12
Project: PX00 / PROJECT-FFB-0001
Related: TF-0059, ADR-0052, FFBJ-0006

## Decision
After the first audited Agent R&D Factory M0 concept, development switched to MVP-first execution. Architectural breadth is frozen unless evidence, audit, measured use or risk treatment requires expansion.

## Added
- generic `FACTORY_MVP_SCOPE` contract;
- frozen pilot scope `FFB-MVP-0001`;
- deterministic executable harness `px00/factory_mvp.py`;
- negative and happy-path tests `tests/test_factory_mvp.py`.

## Critical runtime gates
- strict stage order;
- producer/verifier assignment separation;
- trust gate before untrusted input can reach prototype execution;
- security precheck before prototype;
- verification and Socrates before delivery;
- append-only run identity/trace;
- no material external action in MVP.

## Risk status
`RISK-0002` remains open at S4 for wider scope. The current MVP treats it by isolation, not closure. Any expansion to wider input or tool access requires adversarial trust-gate evidence and a new maturity decision.

## Deferred backlog
UI, production storage, queues, scaling, multi-tenancy, confidential data, live LLM integration, autonomous external tools, production SLA, automatic role generation and robotics are explicitly post-MVP.

## Achievement
Factory Builder now has a first executable M1 candidate rather than only an M0 architecture. Acceptance is intentionally pending CI plus independent critical review.

## Next
Validate full repository CI. If green, conduct Socrates/ARGUS review of executable evidence and either accept the narrow M1 MVP or return it to rework.
