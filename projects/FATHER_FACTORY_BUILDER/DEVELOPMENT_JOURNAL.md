# FATHER Factory Builder — Development Journal

Project: `PROJECT-FFB-0001`
Status: active

## Purpose
This journal is the authoritative chronological development record for the Factory Builder project. It is separate from the PX00/FATHER development journal because the two projects have different responsibilities, milestones, risks and maturity paths.

## Journal rule
Every material Factory Builder generation records:
- what changed;
- why it changed;
- affected principles/contracts;
- risks discovered or changed;
- evidence/tests/audit status;
- maturity impact;
- next summit/gate;
- whether extraction into a separate repository is becoming justified.

## Current position
- FFB-0 Internal Incubation: ACTIVE
- Current strategic objective: `SUMMIT-FFB-01 — Agent Factory Blueprint`
- First audited concept blueprint: `FFB-BP-0001-V2 v0.2 — PASS_WITH_ACTIONS at M0_CONCEPT`
- M1 strategy: MVP-first, frozen by `FFB-MVP-0001`.
- M1 control-flow skeleton: `PASS_WITH_RESTRICTIONS`.
- M1 functional reference MVP: `FFB-ACCEPT-FUNC-MVP-0001 — PASS_WITH_RESTRICTIONS`.
- First full functional run: `MVP-FUNC-RUN-0001`.
- Open maturity blockers include `RISK-0002`, `RISK-0003`, `RISK-0004` and `RISK-0009` according to affected scope.
- PX00/FATHER remains the runtime/governance management system.
- Factory Builder designs the factory/organization blueprint that FATHER may later operate.
- Next direction: prove repeatability on multiple bounded problems, then replace exactly one deterministic stage with a governed executor adapter.

## 2026-08-12 — FFBJ-0001 — Project foundation
Established `PROJECT-FFB-0001` inside PX00 with its own charter, design principles, factory construction lifecycle, risk/failure atlas, discovery/learning loop, roadmap and extraction plan.

Outcome: Factory Builder is now treated as an independent internal project rather than an informal architecture note.

## 2026-08-12 — FFBJ-0002 — Dual-project operating model
Established independent development journals for PX00/FATHER and Factory Builder. Introduced the role/knowledge design doctrine: every material organizational role must be specified as a governed Role Package and bound to stable logical knowledge spaces. Physical knowledge repositories may be split later without changing role or knowledge identities.

## 2026-08-12 — FFBJ-0003 — Core Factory Builder staff
Established the first reusable Factory Builder organizational staff as governed role blueprints:
- `FFB-ROLE-0001` Chief Factory Architect;
- `FFB-ROLE-0002` Enterprise and Systems Architect;
- `FFB-ROLE-0003` Organization Architect;
- `FFB-ROLE-0004` Knowledge Architect;
- `FFB-ROLE-0005` Security and Risk Architect.

Added a role registry, initial department/reporting seed and role-to-knowledge binding matrix. Roles explicitly define responsibilities, non-responsibilities, decision rights, authority ceilings, escalation, handoffs, evidence obligations, independence constraints, anti-Goodhart controls, failure modes and continuity rules.

Important boundaries:
- the Chief Factory Architect integrates but cannot independently audit its own blueprint;
- Security/Risk may block only the affected maturity path for unresolved S4 risk and cannot accept S4 risk;
- Knowledge Architecture governs provenance/version/context but cannot convert retrieved/generated text into truth or authority;
- Organization Architecture must detect shadow workflows, incentive gaming and orphan responsibilities;
- role identity remains independent of assigned model/provider/device.

Maturity impact: Factory Builder now has a minimal architectural team structure suitable for beginning `SUMMIT-FFB-01` design work, but roles remain `PROPOSED` until protocol/evaluation packages and independent review are added.

## 2026-08-12 — FFBJ-0004 — Minimum design team and blueprint synthesis protocol
Added:
- `FFB-ROLE-0006` Principal Software Engineer;
- `FFB-ROLE-0007` Quality and Assurance Architect;
- `FFB-ROLE-0008` Capability Architect.

Extended the organization seed and role knowledge matrix. Added `PROTO-FFB-0001 Factory Blueprint Synthesis`, a twelve-stage protocol from requirement qualification through capability decomposition, parallel specialist design, tension registration, synthesis, implementability, quality, security gate, Socrates challenge, ARGUS audit, rework/acceptance and governed handoff to FATHER.

Key decisions:
- capability decomposition occurs before executor/model/tool selection;
- specialist reviews run independently where possible;
- incompatible positions become explicit architectural tensions rather than being silently averaged;
- Principal Software Engineer can label architecture claims `UNPROVEN` when no executable verification path exists;
- Quality PASS requires declared criteria and evidence;
- unresolved S4 blocks the affected maturity path regardless of majority opinion;
- Socrates and ARGUS remain outside the producer chain;
- accepted blueprint handoff to FATHER contains no runtime grants.

Maturity impact: the minimum Factory Builder design team and collaboration sequence now exist as contracts. Roles are still `PROPOSED`; before SUMMIT-FFB-01 acceptance they need evaluation rubrics and at least one synthetic end-to-end blueprint dry-run.

## 2026-08-12 — FFBJ-0005 — First audited Agent R&D Factory concept
Created the machine contracts `FACTORY_REQUIREMENT`, `CAPABILITY` and `FACTORY_BLUEPRINT` and exercised them on the first synthetic design request `FFB-REQ-0001` for a governed Agent R&D Factory.

The first candidate `FFB-BP-0001 v0.1` targeted M1 and was intentionally sent through the critical path rather than accepted by its author. Socrates and ARGUS rejected its M1 claim because:
- `RISK-0002` remains S4 and blocks the affected maturity path;
- the proposed `R&D Manager` duplicated FATHER management responsibilities;
- referenced `PROTO-RD-*` contracts did not yet exist;
- acceptance criteria and runtime reviewer independence were not yet sufficiently proven.

The failed candidate was preserved unchanged. Rework produced immutable revision `FFB-BP-0001-V2 v0.2`:
- target maturity reduced to honest `M0_CONCEPT`;
- local management role reduced to `R&D Coordinator` subordinate to FATHER;
- undefined `PROTO-RD-*` objects moved to explicit required-next artifacts;
- `FFB-ACC-0001` now separates M0 acceptance from M1 entry evidence;
- S4 and assignment-independence blockers remain visible.

Socrates re-review result: `PASS_FOR_M0_WITH_ACTIONS`.
ARGUS re-audit result: `PASS_WITH_ACTIONS_FOR_M0`; `M1 BLOCKED`.
Acceptance record: `FFB-ACCEPT-0001`.

Achievement: Factory Builder has completed its first full design → criticism → rework → independent re-review loop and produced its first audited factory concept without weakening the maturity gate to obtain a PASS.

Maturity impact: `SUMMIT-FFB-01` has reached its concept-design sub-summit, but operational Agent Factory Blueprint acceptance remains incomplete until the M1 contract/runtime evidence is built.

## 2026-08-12 — FFBJ-0006 — MVP-first execution cut
Adopted an explicit MVP-first strategy after the audited M0 concept. Created `FFB-MVP-0001` and froze the smallest M1 scope before further architecture expansion.

Implemented the first executable deterministic Agent R&D Factory harness in `px00/factory_mvp.py` with tests in `tests/test_factory_mvp.py`.

The MVP enforces:
- strict problem-to-delivery stage order;
- independent producer and verifier assignments;
- explicit trust gate for untrusted input;
- security precheck before bounded prototype execution;
- verification and Socrates before delivery;
- append-only run identity and trace;
- no material external action.

Deliberately deferred until after MVP: live LLM providers, production database, distributed queue, UI, multi-tenancy, confidential/regulated data, autonomous external tools, production SLA, scaling, rich dashboards, automatic role generation, robotics and broad optimization work.

Risk decision: `RISK-0002` is not claimed closed. It is isolated for this narrow MVP through synthetic/explicitly gated input and absence of material external action. Wider scope remains blocked until adversarial trust-gate evidence exists.

Maturity impact: M1 moved from architecture-only backlog to executable implementation. The control-flow skeleton subsequently passed restricted audit/acceptance, but useful stage execution still required concrete artifacts.

## 2026-08-12 — FFBJ-0007 — First functional reference MVP
Extended the M1 harness from state transitions to concrete evidence-producing work.

Created `FACTORY_STAGE_ARTIFACT` and upgraded the runtime so every stage requires a fresh typed immutable artifact with content digest and explicit lineage. Verification evidence must come from the pinned verifier assignment; Socrates evidence must come from an assignment independent of producer and verifier. Security, Verification and Socrates artifact verdicts are checked against the runtime outcome so contradictory evidence cannot silently produce a PASS.

Executed `MVP-FUNC-RUN-0001`, the first complete bounded functional R&D case. The factory:
1. qualified a retry/deduplication problem;
2. recorded research evidence;
3. assessed claims;
4. compared design alternatives;
5. performed a security precheck;
6. implemented a deterministic idempotency-key prototype;
7. independently verified it;
8. passed Socrates with a preserved limitation;
9. produced a candidate factory lesson;
10. created a governed delivery package.

The selected design is SHA-256 over canonical JSON `[run_id, operation, target]`. Socrates explicitly preserved that deterministic idempotency identity does **not** guarantee exactly-once execution; durable uniqueness and atomic state transition remain future controls.

The audit cycle found and fixed two defects before acceptance:
- delimiter concatenation could encode distinct tuples ambiguously, so canonical JSON encoding replaced it and a negative test was added;
- assurance evidence could declare `FAIL` while runtime was told `PASS`, so gated artifact verdict/outcome consistency became a runtime invariant.

ARGUS verdict: `M1 FUNCTIONAL REFERENCE MVP — PASS_WITH_RESTRICTIONS`.
Acceptance: `FFB-ACCEPT-FUNC-MVP-0001`.

New risk: `RISK-0009` records that current SHA-256 protects artifact payload but not the full provenance envelope. The restriction is acceptable for the local in-memory M1 reference MVP but blocks higher persistent evidence maturity until the envelope is canonicalized and hashed/replay-verified.

Maturity impact: the Agent R&D Factory now has one audited useful end-to-end reference run rather than only a workflow skeleton. This is not a live autonomous agent factory and not production-ready.

Next gate: run several different bounded functional problems through the same artifact contract, measure failure/rework patterns, then replace exactly one deterministic producer stage with a governed executor adapter. Broader external input remains gated by `RISK-0002`; persistent evidence maturity remains gated by `RISK-0009`.
