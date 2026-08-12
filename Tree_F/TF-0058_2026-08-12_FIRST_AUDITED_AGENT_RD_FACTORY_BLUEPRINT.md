# TF-0058 — First Audited Agent R&D Factory Blueprint

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0051
Factory Builder journal: FFBJ-0005

## Generation
Factory Builder performed its first complete synthetic factory-design exercise instead of only defining how future design should work.

## Added design contracts
- `projects/FATHER_FACTORY_BUILDER/contracts/FACTORY_REQUIREMENT.yaml`
- `projects/FATHER_FACTORY_BUILDER/contracts/CAPABILITY.yaml`
- `projects/FATHER_FACTORY_BUILDER/contracts/FACTORY_BLUEPRINT.yaml`

## First factory exercise
- qualified request: `FFB-REQ-0001 Agent R&D Factory`;
- capability map: `FFB-CAPMAP-0001`;
- target-factory role set: `FFB-RBSET-0001`;
- first candidate: `FFB-BP-0001 v0.1`;
- Socrates review: `REWORK_REQUIRED`;
- ARGUS audit: `CONDITIONAL_FAIL / M1 BLOCKED`;
- measurable acceptance matrix: `FFB-ACC-0001`;
- immutable rework revision: `FFB-BP-0001-V2 v0.2`;
- Socrates re-review: `PASS_FOR_M0_WITH_ACTIONS`;
- ARGUS re-audit: `PASS_WITH_ACTIONS_FOR_M0`;
- acceptance record: `FFB-ACCEPT-0001`.

## Important result
The first blueprint failed its requested maturity claim and was not forced through by weakening the controls. Factory Builder used its own audit/risk rules to lower maturity, preserve the failed version, fix management ambiguity and make undefined dependencies explicit.

`M0_CONCEPT = accepted with actions`.
`M1_PROTOTYPE = blocked`.

## Current blockers to M1
- unresolved/insufficiently isolated `RISK-0002` on future material-action paths;
- missing governed `PROTO-RD-*` execution contracts;
- runtime producer/reviewer assignment independence not yet proven;
- bounded reproducible prototype harness not yet complete;
- executor snapshot not yet sufficient for replay-grade comparisons.

## Next
Build the M1 evidence chain rather than adding cosmetic architecture: `PROTO-RD-*` contracts → adversarial trust boundary → assignment-independence enforcement → reproducible prototype harness → M1 acceptance attempt.
