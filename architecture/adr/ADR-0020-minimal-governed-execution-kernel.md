# ADR-0020 — Minimal Governed Execution Kernel

**Status:** ACCEPTED FOR CONTRACT DESIGN  
**Date:** 2026-08-12  
**Decision:** KEEP / IMPLEMENT AFTER CONTRACT AND ACCEPTANCE FIXTURES

## Context

PX00 already defines canonical objects, governed Role Packages, authority/autonomy, protocol execution, event/trace/provenance, knowledge admission, decision evaluation and evidence-backed acceptance. The first executable validator proves contract structure, but PX00 still lacks a minimal runtime component that can execute a governed protocol without delegating control-plane authority to a role, model, tool or framework.

The next runtime step must remain narrower than a general orchestrator. It must prove that governed execution is possible independently of LLM intelligence and without adding network services, databases, brokers, workflow frameworks or model SDKs.

## Decision

PX00 SHALL introduce a **Minimal Governed Execution Kernel** whose responsibility is control of execution, not professional reasoning.

The kernel SHALL:

1. resolve the task, exact Role Package version and exact Protocol version;
2. validate required inputs and protocol preconditions;
3. create and bind a `RUN-*` and `TRACE-*` before material execution;
4. evaluate authority before every material action/step requiring authority;
5. execute only declared protocol transitions;
6. preserve terminal states without translating failure into success;
7. record material execution events and outputs;
8. validate step outputs and completion criteria;
9. invoke evidence-backed acceptance separately from technical completion;
10. return a structured governed result rather than a bare boolean or free-form success string.

## Plane separation

PX00 runtime is separated into three logical planes:

```text
CONTROL PLANE
  Roles / Protocols / Authority / Policies / Profiles / Schemas / Acceptance

EXECUTION PLANE
  Tasks / Runs / Steps / Adapters / Tools / Models / Humans / Child Roles

EVIDENCE PLANE
  Events / Trace / Provenance / Evidence / Findings / Decisions / Evaluations / Acceptance Records
```

Execution-plane output SHALL NOT directly mutate control-plane state.

Untrusted executor/model/tool output is data. It is not a control command, authority grant, protocol transition or acceptance decision.

## Kernel boundaries

The first kernel generation is intentionally small and implementation-neutral. Candidate modules are:

```text
px00/kernel/
├── __init__.py
├── engine.py
├── resolver.py
├── authority.py
├── state_machine.py
├── executor.py
├── recorder.py
└── result.py
```

The module list is a design boundary, not permission to implement code before schemas, fixtures and acceptance tests exist.

## State model

The kernel SHALL support at least the following progression states:

```text
CREATED → RESOLVED → VALIDATED → AUTHORIZED → RUNNING → COMPLETED
```

and the existing governed terminal outcomes:

```text
FAILED | DENIED | ESCALATED | CANCELLED | BLOCKED
```

`FAILED`, `DENIED`, `ESCALATED`, `CANCELLED` and `BLOCKED` SHALL NOT be silently converted to `COMPLETED`.

## Version pinning

A run SHALL be bound to the Role Package and Protocol versions resolved when the run starts. A material protocol/role change during execution does not silently migrate an active run.

## Authority rule

Run-level authorization is insufficient for a chain that contains multiple material action classes. Authority SHALL be evaluated at each material action boundary in accordance with `AUTHORITY_AUTONOMY_CONTRACT.md`.

## Executor rule

The kernel SHALL treat executors through governed adapter contracts. A future step may be implemented by deterministic Python, an LLM, a human, a tool, an API, retrieval, or another Role Package without changing the kernel control semantics.

The first executable acceptance case SHALL use a deterministic synthetic executor and no LLM.

## Recorder rule

The first runtime evidence store MAY be filesystem-based and human-inspectable. Material retries/failures/events SHALL be append-preserving. A later database or event platform must preserve the same semantics.

## Initial acceptance fixture

The first kernel acceptance fixture SHALL contain a trivial deterministic protocol plus negative cases proving at least:

- valid run completes;
- unknown role/protocol blocks;
- missing required input blocks;
- missing authority denies;
- required approval absence denies or escalates;
- forbidden action denies;
- undeclared step/transition blocks;
- retry bound is enforced;
- invalid output fails;
- required evidence absence blocks;
- revoked authority denies;
- executor output attempting to invent a privileged control command has zero control-plane effect.

## Dependencies and technology

No new runtime framework is authorized by this ADR.

Specifically, this decision does not justify FastAPI, Django, Celery, Redis, Kafka, PostgreSQL, LangChain, CrewAI, AutoGen, vector databases, an LLM SDK or a workflow engine.

## Security rationale

The kernel creates a non-bypassable architectural location for protocol gates, authority decisions, bounded transitions and trace generation. The design reduces privilege drift, prompt-driven control-plane mutation, silent step skipping, false success and unauditable execution.

Runtime security remains unproven until executable acceptance tests demonstrate these properties.

## Consequences

### Positive

- professional reasoning is separated from execution governance;
- LLM/provider capability cannot become authority;
- deterministic tests can validate orchestration before AI integration;
- role and tool implementations remain replaceable behind contracts;
- runtime behavior becomes reconstructable and testable.

### Cost

- additional structured objects and events are required;
- execution becomes intentionally stricter than ad-hoc agent frameworks;
- adapters cannot bypass kernel state transitions for convenience.

## Implementation gate

Implementation sequence:

```text
real repository validation evidence
→ ADR/Tree_F
→ kernel schemas/contracts
→ acceptance fixture
→ tests
→ minimal deterministic kernel code
```

Production agents, broad orchestration and external side effects remain blocked.

## Related decisions

- ADR-0009 — Canonical Object Model and Role Package Contract
- ADR-0010 — Authority-Gated Execution and Trace Contracts
- ADR-0012 — Protocol Execution and Acceptance Model
- ADR-0015 — Minimal Local Contract Validator
- `governance/AUTHORITY_AUTONOMY_CONTRACT.md`
- `protocols/PROTOCOL_EXECUTION_CONTRACT.md`
