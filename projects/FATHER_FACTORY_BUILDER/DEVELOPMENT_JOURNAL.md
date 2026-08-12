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
- Gemini Interactions provider-specific driver/profile: locally proven and CI-green under TF-0073.
- Real authorized Gemini inference: pending.
- `RISK-0011`: MITIGATING, not resolved.
- Product portfolio: canonical master roadmap lives in `VictorKVS/KNOWLEDGE_CORE/father/product-roadmap/`.
- Security Knowledge: canonical professional product lives in `VictorKVS/KNOWLEDGE_CORE/security-knowledge/`; Factory Builder binds to `KB-SECURITY` instead of copying domain truth.
- First real cross-repository source-metadata snapshot has completed manifest → snapshot → ContextPackage → RUN trace → read-only replay.
- `RISK-0012`: RESOLVED for bounded M1 cross-repository provenance/replay after ARGUS Audit 0002.
- Decision materiality norm `PX00-NORM-DM-0001`: ACTIVE; Role Packages must declare materiality ranges/promotion triggers.
- Professional decision context is bound to exact RUN/role/assignment and persisted in trace/replay under TF-0071.
- Security atomic proof-floor gate is active; TF-0072 baseline observed 82 atomic requirements and 0 strict VERIFIED requirements.
- A true atomic VERIFIED Security requirement reasoning RUN remains NOT PROVEN.
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

## 2026-08-12 — FFBJ-0012 — Product portfolio roadmap
Established a product manufacturing portfolio so Factory Builder work is driven by active products and evidence gates rather than unrestricted architecture expansion.

Primary owner-priority sequence:
`Security Knowledge Base → Compliance Engine → Evidence-Based Security Architect → Vulnerability & Risk Expert → White-Hat / Continuous Security Assurance → Regulatory Change Engine → Continuous Security Audit Expert`.

Architect-proposed supporting/future tracks remain visible but non-displacing: FATHER/Factory Builder platform, Agent Factory, knowledge infrastructure, assurance, Software/Service Factory, Research Factory, Cyber-Physical/Robotics and Factory-of-Factories.

Rule: later products may be explored as bounded PoCs, but foundational gates cannot be bypassed by a successful demo or schedule pressure.

## 2026-08-12 — FFBJ-0013 — Security Knowledge canonical route
Corrected the repository boundary after recognizing that `SEC-PROD-0001` already has an active canonical implementation in `VictorKVS/KNOWLEDGE_CORE`.

Canonical ownership:
- `security-knowledge/` — Security Knowledge product tree;
- `father/domain-knowledge/` — professional domain management;
- `father/product-roadmap/` — canonical product roadmaps.

PX00 duplicate Security Knowledge coverage/readiness/source-backlog/runtime-gate artifacts were removed. PX00 now contains route-only product/roadmap records.

Factory Builder rule:
`ROLE KNOWLEDGE REQUIREMENT ≠ OWNED LOCAL KNOWLEDGE COPY`.

Security Knowledge remains evidence-first and is not ordinary RAG over PDFs. Canonical pipeline:
`SOURCE → VERSION → CHUNK → ATOMIC CLAIM/REQUIREMENT → APPLICABILITY → RELATIONS → CONTROL → CHECK → EVIDENCE → EXPERT REVIEW`.

`VERIFIED` requires an admitted primary source and exact locator.

Parallel decision: `SUMMIT-FFB-02` may proceed independently; live-provider readiness is not a blocker for normative corpus production.

## 2026-08-12 — FFBJ-0014 — Cross-repository knowledge snapshot pinning
Introduced the reusable boundary that separates current knowledge routing from immutable historical RUN context.

Pattern:
`ROLE KNOWLEDGE BINDING → ACTIVE ROUTE → PRODUCER SELECTION → IMMUTABLE KNOWLEDGE SNAPSHOT → CONTEXT PACKAGE → RUN`.

Implemented in PX00:
- `KNOWLEDGE_SNAPSHOT`;
- fail-closed snapshot builder;
- ContextPackage snapshot hashing;
- canonical `KB-SECURITY` external route;
- negative/reproducibility tests.

Implemented in KNOWLEDGE_CORE:
- producer-side Security Knowledge snapshot export schema.

Key invariant:
`ACTIVE ROUTE != HISTORICAL SNAPSHOT`.

Snapshot integrity records which knowledge was supplied; it does not create truth, applicability, acceptance or authority.

`RISK-0012` was initially MITIGATING because contracts existed but no real slice/replay had yet been proven.

## 2026-08-12 — FFBJ-0015 — First real Security Knowledge snapshot bridge
Moved the boundary from synthetic references to canonical `FSB-117-2025` source metadata.

KNOWLEDGE_CORE now validates the historical object bytes against a pinned Git commit even after `main` advances. PX00 independently validates the producer manifest and builds an immutable snapshot/ContextPackage.

Critical maturity restraint:
`SOURCE_VERIFIED ≠ VERIFIED REQUIREMENT`.

The first envelope design omitted classification/freshness from the manifest digest. This was caught before acceptance and corrected on both producer and consumer sides.

Real provenance transport is proven; expert Security reasoning remains unproven.

## 2026-08-12 — FFBJ-0016 — Knowledge-bound RUN trace and replay
Extended the real snapshot proof through a bounded governed RUN and read-only replay.

New reusable pattern:
`ROLE → BINDING → ROUTE → MANIFEST → SNAPSHOT → CONTEXT PACKAGE → RUN KNOWLEDGE PIN → TRACE → REPLAY`.

`RunKnowledgeBinder` rejects RUN/role/assignment/snapshot-set mismatch. A trace persisted with knowledge provenance cannot be replayed while silently omitting or changing that provenance.

Key distinction:
`HISTORICAL REPLAY != CURRENT REASSESSMENT`.

The bounded RUN uses a deterministic synthetic operation so the generation proves provenance/replay mechanics, not professional FSB reasoning.

`ARGUS_AUDIT_0002` returns `PASS_WITH_RESTRICTIONS`.

`RISK-0012` is RESOLVED for the bounded M1 cross-repository provenance/replay scope with explicit reopen conditions.

Next useful evidence must come from product value rather than more snapshot plumbing: first live governed AI executor and/or a truly atomic VERIFIED domain requirement used in a professional task.

## 2026-08-13 — FFBJ-0017 — Decision materiality project norm
Promoted the repeatedly stated proportional-assurance principle into a permanent project norm `PX00-NORM-DM-0001`.

Factory Builder must now declare, for every material role/responsibility, the typical D0–D3 materiality range, promotion triggers, acceptable evidence categories, independent-review requirement, approval/escalation requirement and verification/outcome-learning obligations.

Core invariant:
`higher cost of error / irreversibility / uncertainty / risk → stronger evidence + independent review + approval`.

The norm is intentionally proportional: D0 local/conventional choices remain lightweight; architecture/product decisions are normally D2; regulated/safety/critical decisions are D3. A nominally local decision is promoted when it materially affects a higher-level property.

Risk remains independent, but S3 imposes at least D2 and S4 imposes D3 while retaining veto semantics.

This makes Security's evidence-first discipline a reusable organizational principle for future architecture, programming, analytics, operations, finance, legal and engineering roles without copying Security-specific source semantics into those domains.

## 2026-08-13 — FFBJ-0018 — Professional decision trace and replay
Operationalized `PX00-NORM-DM-0001` inside the historical RUN evidence path.

A governed professional decision can now be bound only after the materiality gate passes and its RUN/role/assignment identity matches the execution context. D2/D3 decisions require structured requirements, constraints, options, evidence and independent review; D3 additionally requires accountable approval.

TRACE persists the minimum immutable professional-decision provenance envelope:
`decision_ref + decision_digest + materiality_class`.

Read-only replay fails closed if persisted decision context is omitted or substituted. Existing knowledge-only replay behavior remains backward compatible.

Important restraint: the system preserves formal rationale/evidence references, not hidden model chain-of-thought. Trace integrity proves which decision record was used; it does not prove that the professional conclusion was correct.

Next useful evidence is product value, not more provenance plumbing: close `SUMMIT-FFB-02` with one real governed AI inference and, when available, run one truly atomic VERIFIED Security requirement through a professional D2/D3 decision path.

## 2026-08-13 — FFBJ-0019 — Security requirement verification gate
Attempting the first professional D3 Security decision exposed a proof-state inconsistency before runtime execution: FSTEK-31 atomic requirements were labeled VERIFIED while lacking the `source_quote` required by their canonical schema.

Factory Builder did not consume the inflated state. KNOWLEDGE_CORE downgraded the affected atoms to REVIEWED without deleting their atomization and added an executable CI gate.

Observed strict baseline:
- 9 requirement files;
- 82 atomic requirements;
- 0 strict VERIFIED requirements.

`VERIFIED` now requires source document identity, exact locator and source quote; an absent status is conservatively UNVERIFIED.

Current professional D3 Security run result is correctly:
`BLOCKED_BY_KNOWLEDGE_PROOF_FLOOR`.

First promotion target: `FSTEK31-REQ-001` at locator `p. 10`.

## 2026-08-13 — FFBJ-0020 — Gemini provider driver readiness
Continued the independent live-executor stream while Security Knowledge waits for the first truly VERIFIED atom.

The first concrete provider selection exposed a transport assumption: the secret-safe M1 live boundary still hardcoded Bearer authentication. `ADR-0065` makes header-based authentication strategy profile-controlled while preserving Bearer as the default.

Added:
- Google Gemini Interactions provider driver;
- stable `v1` endpoint profile;
- pinned `gemini-3.6-flash` model reference;
- `x-goog-api-key` header configuration;
- PUBLIC-only egress;
- text-only candidate output;
- `store=false`;
- no tools, provider agent, grounding, files, multimodal input or background execution;
- fail-closed handling of incomplete, function/tool and non-text provider responses.

Provider interaction ID and returned model are retained as provenance when present. Credential values remain runtime-only and are absent from call records/candidate provenance.

Provider-specific mapping is locally CI-proven, but no authorized real Gemini inference has yet occurred. `RISK-0011` remains MITIGATING and `SUMMIT-FFB-02` remains OPEN.

Invariant:
`DRIVER READY != LIVE CALL PROVEN != SUMMIT ACCEPTED`.

Next evidence: exactly one authorized PUBLIC Gemini inference, then independent verification, governed rework if needed, Socrates and ARGUS. No second provider or broader provider abstraction before that path is exercised unless a concrete live blocker requires it.
