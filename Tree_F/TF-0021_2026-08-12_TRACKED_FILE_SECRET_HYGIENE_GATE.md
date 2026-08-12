# TF-0021 — Tracked-file secret hygiene gate

**Date:** 2026-08-12  
**Status:** ACCEPTED WITH SCOPE LIMITS  
**Decision:** KEEP

## Trigger

`TF-0020` closed the Windows dependency artifact hash execution gate. Repository change-control enforcement is still externally blocked because no visible GitHub ruleset exists. The next useful independent control was to reduce accidental secret publication in the public repository without introducing another runtime dependency.

## Structural delta

Added:

```text
px00/secret_hygiene.py
tests/test_secret_hygiene.py
security/SECRET_HYGIENE_BASELINE_0_1.md
architecture/adr/ADR-0019-tracked-file-secret-hygiene-gate.md
assurance/runs/SECRET-HYGIENE-0001_GITHUB_ACTIONS_PASS_2026-08-12.md
assurance/records/ACCEPTANCE-SECRET-HYGIENE-0001.yaml
```

Modified:

```text
.github/workflows/contract-validation.yml
```

## File dossier

### `px00/secret_hygiene.py`

**Purpose:** deterministic scan of canonical Git-tracked text files for likely credential material.  
**Input:** `git ls-files -z` plus tracked file contents.  
**Output:** PASS/FAIL and findings containing path, line and class only.  
**Processing:** selected high-signal token patterns plus generic secret-assignment checks.  
**Dependencies:** Python standard library only.  
**Security:** suspected values are never echoed; findings/errors fail the process.

### `tests/test_secret_hygiene.py`

**Purpose:** prove detection and safe reporting plus scan the real repository.  
**Cases:** repository clean scan, GitHub token-like value, private-key header, generic secret assignment, safe placeholder.  
**Dependencies:** standard-library `unittest`.  
**Security:** negative-test credential material is assembled at runtime so the tracked source does not itself embed scanner-triggering examples.

### `.github/workflows/contract-validation.yml`

**Purpose change:** add explicit `python -m px00.secret_hygiene .` step after tests and before final PX00 contract validation.  
**Permissions:** unchanged `contents: read`.  
**External dependencies added:** none.

## Production-chain failure retained

Two intermediate workflow runs failed:

```text
31573227207  FAILURE
31573246011  FAILURE
```

Root cause was not a scanner defect in the repository gate. Literal generic-secret assignment fixtures in the new test file became tracked source and were correctly detected by the repository integration scan.

The fix was to construct fixture keys/values at runtime. No allow-list, suppression or weakened matching was introduced.

## Accepted verification

GitHub Actions run:

```text
run     31573355366
commit  2ce2af539f5909837a00d05da15fb410bc3337d0
status  SUCCESS
```

Observed:

```text
hash-locked dependency install  PASS
pip check                       PASS
24 tests                        PASS
tracked-file secret scan        PASS
findings                        0
scan errors                     0
PX00 contract validation        PASS
errors                          0
warnings                        0
```

## Algorithms / libraries

No new third-party library. Scanner uses regular expressions, bounded text-file reads and Git tracked-file enumeration from Python standard library.

No entropy classifier, history scanner or external signature feed was added because current evidence does not yet justify that complexity.

## Security conclusion

`PASS_WITH_SCOPE_LIMITS`.

Improved:

- current tracked repository receives explicit credential-leakage detection;
- negative cases are regression-tested;
- suspected secret values are not copied into CI output;
- no additional dependency/supply-chain surface was created;
- integration failure demonstrated that the scanner also examines its own tracked test material.

Not proven / still open:

- GitHub Secret Scanning;
- GitHub Push Protection;
- secret absence in prior Git history;
- binary/encoded/untracked/ignored content;
- non-bypassable required CI enforcement on `main`.

## Occam decision

Keep one small internal detector rather than importing a large scanning stack. Add broader signatures/entropy/history scanning only from observed need or release requirements.

## Next gate

Establish and verify `main` branch/ruleset enforcement. The existing contract-validation workflow now contains contract, dependency/hash and secret-hygiene controls, but it is not yet a proven mandatory change-control boundary.