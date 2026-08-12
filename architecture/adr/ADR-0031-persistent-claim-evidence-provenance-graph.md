# ADR-0031 — Persistent Claim/Evidence Provenance Graph

Date: 2026-08-12
Status: accepted

## Context
Claim status and evidence confidence require durable identities and explicit provenance. Updating one mutable record would erase how a conclusion changed over time.

## Decision
Introduce persistent SRC, EVD and CLM contracts plus an explicit provenance graph.

Edges are semantic and directional:
- EVD -> SRC via `source_ref`
- CLM -> EVD via support or contradiction edges
- CLM(new) -> CLM(old) via `supersedes`
- derived SRC/EVD nodes preserve parent references

Material revisions create new identities. Prior nodes are retained. Supersession is not deletion.

## Invariants
- source, evidence and claim identities are immutable
- support and contradiction are distinct edge types
- claim supersession is acyclic
- source independence is explicit and inherited conservatively for derivatives
- distinct URLs do not prove independent origin
- history cannot be rewritten to make the newest claim appear timeless

## Consequences
FATHER can reconstruct not only current confidence but how and why a belief changed, which evidence entered the graph, which source it came from, and what previous claim was superseded.
