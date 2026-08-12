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
- FFB-0 Internal Incubation: ACTIVE.
- `SUMMIT-FFB-01 — Bounded Functional Agent Factory Reference MVP`: ACHIEVED WITH RESTRICTIONS.
- Current summit: `SUMMIT-FFB-02 — First Governed Live Executor`: OPEN.
- Executor boundary: proven with replaceable local workers.
- AI lifecycle/risk gates: integrated.
- Live HTTPS provider secret/data-egress boundary: locally proven and CI-green.
- Real provider-specific driver and authorized live call: pending.
- `RISK-0011`: MITIGATING, not resolved.
- PX00/FATHER remains the runtime/governance management system.
- Factory Builder designs the factory/organization blueprint that FATHER may later operate.

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
- Chief Factory Architect integrates but cannot independently audit its own blueprint;
- Security/Risk may block only the affected maturity path for unresolved S4 risk and cannot accept S4 risk;
- Knowledge Architecture governs provenance/version/context but cannot convert retrieved/generated text into truth or authority;
- Organization Architecture must detect shadow workflows, incentive gaming and orphan responsibilities;
- role identity remains independent of assigned model/provider/device.

## 2026-08-12 — FFBJ-0004 — Minimum design team and blueprint synthesis protocol
Added:
- `FFB-ROLE-0006` Principal Software Engineer;
- `FFB-ROLE-0007` Quality and Assurance Architect;
- `FFB-ROLE-0008` Capability Architect.

Added `PROTO-FFB-0001 Factory Blueprint Synthesis`, a twelve-stage protocol from requirement qualification through capability decomposition, parallel specialist design, tension registration, synthesis, implementability, quality, security gate, Socrates challenge, ARGUS audit, rework/acceptance and governed handoff to FATHER.

Key decisions:
- capability decomposition precedes executor/model/tool selection;
- incompatible expert positions become explicit architectural tensions;
- Principal Software Engineer may label architecture claims `UNPROVEN` without executable evidence;
- unresolved S4 blocks the affected maturity path;
- Socrates and ARGUS remain outside the producer chain;
- accepted blueprint handoff contains no runtime grants.

## 2026-08-12 — FFBJ-0005 — First audited Agent R&D Factory concept
Created `FACTORY_REQUIREMENT`, `CAPABILITY` and `FACTORY_BLUEPRINT`, then exercised them on `FFB-REQ-0001`.

The first candidate `FFB-BP-0001 v0.1` targeted M1 and was rejected by Socrates/ARGUS because `RISK-0002` remained blocking, the proposed R&D Manager duplicated FATHER, referenced protocols did not yet exist and reviewer independence was not proven.

The failed candidate was preserved. Immutable rework `FFB-BP-0001-V2 v0.2` reduced the maturity claim to honest M0, replaced the manager with an R&D Coordinator subordinate to FATHER and made missing protocols explicit future requirements.

Result: first full design → criticism → rework → independent re-review cycle completed without weakening maturity gates.

## 2026-08-12 — FFBJ-0006 — MVP-first execution cut
Adopted explicit MVP-first strategy and froze the smallest M1 scope in `FFB-MVP-0001`.

Implemented deterministic `AgentRdFactoryMvp` with strict stage order, independent producer/verifier, trust and security prechecks, verification/Socrates before delivery, append-only run identity and no material external action.

Deferred: live LLM, production DB, queue, UI, multi-tenancy, regulated data, autonomous tools, production SLA, scaling, robotics and broad optimization.

## 2026-08-12 — FFBJ-0007 — First functional reference MVP
Extended the harness from state transitions to typed immutable stage artifacts with SHA-256, lineage, verifier/Socrates independence and verdict/outcome consistency.

`MVP-FUNC-RUN-0001` completed a useful bounded R&D case and produced a governed delivery package. Socrates preserved that deterministic idempotency identity is not exactly-once execution.

Audit found and fixed ambiguous delimiter encoding and a possible FAIL/PASS evidence mismatch. ARGUS accepted the functional reference MVP with restrictions. `RISK-0009` records that payload hashing does not yet protect the full artifact envelope.

## 2026-08-12 — FFBJ-0008 — Scenario suite and governed rework
Expanded the single happy path into multiple observed behaviors:
- direct governed delivery;
- verifier FAIL → explicit rework → re-verification → delivery;
- security scope block before prototype execution.

Added an explicit `request_rework` transition with append-only failed evidence and lineage. Created reusable failure patterns `FFB-FP-0001` and `FFB-FP-0002`.

Key lesson: safe refusal is a valid control outcome and must not be optimized away merely to increase delivery rate.

## 2026-08-12 — FFBJ-0009 — Governed replaceable executor boundary
Introduced provider-neutral executor definitions/invocations and proved worker replacement without changing the role contract.

Proven chain:
`worker v0.1 → candidate → verifier FAIL → governed rework → worker v0.2 → verifier PASS → Socrates → delivery`.

Executor identity/version/provider/model, assignment and input/output hashes remain pinned. Provider invocation success is explicitly separate from verification and acceptance. Created `FFB-FP-0003` and `RISK-0011` for the still-unproven live-provider boundary.

## 2026-08-12 — FFBJ-0010 — AI lifecycle evidence gates and quantitative risk
Integrated CRISP-ML(Q), Demo→PoC→MVP→Production stage evidence and stage-aware CI/CD without conflating these with PX00 M0…M5 maturity.

Added reproducible quantitative risk simulation using Bernoulli occurrence × triangular impact, reporting expected loss, tail percentile and probability above tolerance. Qualitative S0…S4 remains independent and S4 cannot be overridden by a favorable expected-loss number.

Added TechnoMart as a regression/strategy seed with unknowns preserved as `TBD` rather than invented.

## 2026-08-12 — FFBJ-0011 — Live provider readiness boundary
Prepared the first real-provider integration without committing credentials or coupling FATHER to a vendor.

Implemented:
- `LIVE_PROVIDER_PROFILE` and `LIVE_PROVIDER_CALL_RECORD`;
- provider-neutral `LiveHttpsExecutorAdapter`;
- HTTPS and exact host allowlist;
- explicit live opt-in;
- credential reference/value separation;
- data-classification egress gate;
- bounded timeout and response size;
- HTTP/JSON/shape fail-closed behavior;
- request/response hashes and provider request/model identity capture;
- integration through the existing `GovernedExecutorBoundary`.

The first CI run failed the existing secret-hygiene test because a local variable matched the defensive scanner. The scanner was not weakened; implementation was changed. The corrected run passed unit/integration tests, secret scan and repository contract validation.

`RISK-0011` advanced from OPEN to MITIGATING. Local transport/auth/data-egress containment is now proven, but the external provider itself remains unproven.

Current gate:
- `LIVE_PROVIDER_BOUNDARY_READY = YES`;
- `LIVE_PROVIDER_PROVEN = NO`;
- `SUMMIT-FFB-02 = OPEN`.

Next action: configure exactly one authorized provider driver, send only PUBLIC/INTERNAL bounded data, perform one real inference with no tools/material external action, preserve provider evidence and submit the candidate to independent verification and Socrates. Bad live output must remain rejectable and reworkable.
