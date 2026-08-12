# ADR-0019 — Tracked-file secret hygiene gate

**Date:** 2026-08-12  
**Status:** ACCEPTED

## Context

PX00 already prevents obvious secret-like values in selected YAML governance data and keeps secret/configuration paths out of Git through `.gitignore`. GitHub Secret Scanning and Push Protection remain unverified through the current connector, and repository ruleset enforcement has not yet been established.

A small additional control can still reduce accidental credential publication immediately without adding a new dependency or claiming to replace platform-native secret protection.

## Decision

Add a standard-library-only scanner for the current canonical Git-tracked repository view and execute it in the existing contract-validation workflow.

The gate shall:

1. enumerate files with `git ls-files -z`;
2. scan bounded text files for selected high-signal credential patterns and generic secret assignments;
3. omit detected values from findings/output;
4. fail closed on findings or scan errors;
5. include negative tests plus a real-repository integration test;
6. remain explicitly distinct from GitHub Secret Scanning / Push Protection;
7. add no external runtime dependency.

## Consequences

Positive:

- current public tracked files receive a deterministic leakage check;
- the control runs on both pushes and pull requests through the existing CI workflow;
- no additional package enters the SBOM/hash-lock chain;
- findings do not copy suspected credentials into logs.

Limitations:

- pattern coverage is intentionally incomplete;
- Git history, binary content, ignored/untracked files and external systems are outside this baseline;
- without required branch/ruleset enforcement, CI success is not yet a non-bypassable merge/push boundary.

## Verification evidence

GitHub Actions run `31573355366`, commit `2ce2af539f5909837a00d05da15fb410bc3337d0`:

```text
24 tests                        PASS
tracked-file secret hygiene     PASS
findings                        0
errors                          0
PX00 contract validation        PASS
```

Runs `31573227207` and `31573246011` are retained failed attempts: the first integration version detected literal negative-test fixture assignments inside the tracked test source itself. Fixtures were corrected to be constructed at runtime rather than suppressing the scanner.

## Rejected alternatives

- Add a large secret-scanning package now: rejected because no coverage need yet justifies a new dependency and supply-chain surface.
- Treat this as equivalent to GitHub Secret Scanning/Push Protection: rejected because platform status is still unverified and feature semantics differ.
- Add a broad allow-list immediately: rejected because it creates a bypass mechanism before a real false-positive case requires one.

## Next gate

Establish and verify `main` branch/ruleset enforcement with the existing CI check required for governed changes; separately verify GitHub Secret Scanning and Push Protection.