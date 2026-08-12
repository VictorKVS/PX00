# RISK-0001 — Knowledge Context Reproducibility Gap

Status: OPEN
Severity: S4
Category: KNOWLEDGE / SECURITY
Source: ARGUS-SEC-001
Owner: ROLE-ARCHITECT

## Risk
Context Package integrity currently binds stable object IDs and route snapshots but not immutable content/version digests for each knowledge object.

## Causal hypothesis
If knowledge content changes behind a stable logical ID, a historical RUN may resolve the same ID to semantically different material.

## Required mitigation
Introduce immutable KNOWLEDGE_OBJECT_VERSION with content digest and include exact version/digest refs in Context Package material/hash.

## Verification
A test must prove that changing content under the same logical object ID necessarily changes the Context Package identity or fails resolution to the historic version.
