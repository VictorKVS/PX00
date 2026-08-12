# TF-0023 — Minimal Governed Execution Kernel

**Date:** 2026-08-12  
**Status:** ACCEPTED FOR CONTRACT DESIGN  
**Lifecycle decision:** KEEP / IMPLEMENT AFTER CONTRACT FIXTURES  
**Primary ADR:** `architecture/adr/ADR-0020-minimal-governed-execution-kernel.md`

## Trigger

PX00 completed the first executable validator generation and defined the real-repository integration gate. The next architecture question is how a governed task can actually execute a protocol without giving a role, LLM, tool or external framework ownership of control-plane decisions.

## Material structural change

This generation introduces the design boundary for a minimal governed execution kernel and the explicit separation of three runtime planes:

```text
Control Plane
  ↓ governs
Execution Plane
  ↓ produces
Evidence Plane
```

The kernel is not a general agent orchestrator and does not itself provide professional intelligence.

## Intended production chain

```text
TASK
→ resolve exact ROLE version
→ resolve exact PROTO version
→ validate inputs/preconditions
→ create RUN / TRACE
→ evaluate material authority
→ execute declared step
→ record EVENT / output
→ validate transition
→ repeat only within protocol bounds
→ completion state
→ acceptance evidence
→ governed result
```

## Core invariants

1. Role capability is not execution authority.
2. Run-level approval does not authorize unrelated later actions.
3. Every material action is evaluated at its own authority boundary.
4. An executor cannot choose an undeclared protocol transition.
5. Executor/model/tool output is untrusted data relative to the control plane.
6. Terminal failures are not rewritten into success.
7. Role and protocol versions are pinned for the run.
8. Material events, retries and failures remain reconstructable.
9. Technical completion and acceptance remain separate decisions.
10. Initial kernel proof uses deterministic synthetic execution and no LLM.

## Candidate code structure

Code is not authorized by this TF alone. After schemas/fixtures/tests are accepted, the intended narrow boundary is:

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

Responsibilities:

- `engine.py` — coordinates the governed lifecycle, without domain reasoning;
- `resolver.py` — resolves and pins governed identities/versions;
- `authority.py` — evaluates existing authority contracts, never invents authority;
- `state_machine.py` — enforces allowed state transitions;
- `executor.py` — invokes an adapter only after the control plane permits it;
- `recorder.py` — preserves material execution evidence;
- `result.py` — returns structured run/acceptance output.

## Initial runtime evidence shape

A filesystem-backed, human-inspectable proof is acceptable for the first generation, for example:

```text
runtime/runs/RUN-*/
├── run.yaml
├── trace.yaml
├── authority/
├── events/
└── outputs/
```

This is not a commitment to filesystem storage in production. It is a deliberate way to prove event/trace semantics before choosing database or observability infrastructure.

## Acceptance design

The first acceptance fixture must include one deterministic successful protocol and negative cases for unknown identities, missing inputs, missing authority/approval, forbidden actions, undeclared transitions, retry exhaustion, invalid outputs, missing evidence, authority revocation and executor attempts to inject control commands.

The key security expectation is:

> Untrusted executor output cannot directly alter control-plane state.

## Algorithms / libraries

**Runtime algorithm design:** finite governed state machine + fail-closed authority evaluation + declared protocol transition resolution + append-preserving material evidence.

**New third-party libraries:** NONE.

No workflow framework, broker, database, web framework or LLM SDK is justified by this generation.

## DevOps conclusion

No CI widening or production deployment is authorized. The existing real-repository validation gate remains authoritative before runtime widening. When executable kernel code is later added, it must enter through contract fixtures and tests rather than framework-first implementation.

## Security conclusion

`PASS_WITH_ACTIONS` for architecture design.

This generation creates the intended non-bypassable location for authority and protocol gates, but no claim is made that those gates are runtime-enforced until executable tests exist.

## Evaluation

- traceability: 5/5 — run/control/evidence relationships are explicit;
- security architecture: 5/5 — control authority is separated from untrusted executors;
- maintainability: 4/5 — narrow interfaces reduce coupling, but schemas are still to be instantiated;
- implementation risk: 3/5 — state-machine semantics remain straightforward, but durability/retry details need tests.

Scores are coarse engineering decision aids, not statistical measurements.

## Next gate

Define the universal governed `Action Request / Tool Boundary` so no role or executor obtains a direct path to externally effective tools. Then instantiate schemas and acceptance fixtures before kernel implementation.

## Supersession / rollback

This record is append-only. A later kernel generation may supersede module layout or storage technology, but must preserve or explicitly replace the invariants recorded here with evaluated evidence.
