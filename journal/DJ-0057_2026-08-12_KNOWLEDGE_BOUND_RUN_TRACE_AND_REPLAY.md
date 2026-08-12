# DJ-0057 — Knowledge-Bound RUN Trace and Replay

Date: 2026-08-12
Generation: TF-0069
ADR: ADR-0062
Audit: ARGUS_AUDIT_0002

## What closed
The first real Security Knowledge snapshot is no longer only a ContextPackage fixture. It is now bound to a governed RUN trace and required during read-only replay.

Trace provenance includes:
- ContextPackage ref/hash;
- knowledge snapshot ref/digest;
- producer manifest ref/digest.

Replay fails closed if the knowledge context is omitted or changed.

## Important distinction
The RUN uses a deterministic synthetic operation to isolate provenance/replay mechanics.

Therefore TF-0069 proves:
`external knowledge provenance survives RUN/trace/replay`.

It does not prove:
`FATHER can already perform expert FSB regulatory reasoning`.

The real imported object remains `SOURCE_VERIFIED`, not a VERIFIED atomic requirement.

## Risk outcome
ARGUS Audit 0002 returns `PASS_WITH_RESTRICTIONS`.

`RISK-0012` is RESOLVED for the bounded M1 cross-repository provenance/replay scope with explicit reopen conditions.

## Next
Return to product-value work rather than extending snapshot plumbing:
- continue Security Knowledge corpus/atomicization in KNOWLEDGE_CORE;
- continue `SUMMIT-FFB-02` first governed live AI executor in PX00;
- when a true atomic VERIFIED Security requirement slice exists, use it in the first professional Security reasoning RUN with independent review.
