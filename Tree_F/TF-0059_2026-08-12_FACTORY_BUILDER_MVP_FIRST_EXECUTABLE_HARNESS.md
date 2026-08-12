# TF-0059 — Factory Builder MVP-first executable harness

Date: 2026-08-12
Status: implemented; final CI pending
Project: PROJECT-FFB-0001
ADR: ADR-0052

## Objective
Move Factory Builder from audited M0 concept toward the smallest executable M1 prototype before adding further architecture.

## Implemented
- `schemas/FACTORY_MVP_SCOPE.yaml`;
- `projects/FATHER_FACTORY_BUILDER/pilots/agent_rd_factory/MVP_SCOPE_V0_1.yaml`;
- deterministic runtime harness `px00/factory_mvp.py`;
- negative and happy-path tests `tests/test_factory_mvp.py`;
- frozen MVP scope and explicit post-MVP backlog.

## MVP behavior
The harness enforces:
- strict workflow stage order;
- independent producer/verifier assignments;
- trust gate for untrusted input;
- mandatory security precheck before bounded prototype execution;
- verification and Socrates before delivery;
- append-only run identity/trace semantics;
- no material external action.

## Architectural meaning
Factory Builder is now judged by executable behavior rather than documentation growth alone. New features are excluded by default until evidence, audit, risk or measured use requires them.

## Risk impact
`RISK-0002` is not declared closed. For this narrow MVP it is isolated by synthetic/gated input and absence of material external tools. Wider M1 scope remains blocked pending adversarial trust-gate evidence.

## Summit position
- M0 audited concept: PASS_WITH_ACTIONS
- M1 MVP harness: IMPLEMENTED, validation/audit gate in progress
- production maturity: NOT CLAIMED

## Next gate
Run repository CI, inspect failures if any, then conduct Socrates/ARGUS review of the executable MVP evidence and decide M1 acceptance or rework.
