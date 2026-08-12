# PX00 Secret Hygiene Baseline 0.1

**Scope:** current Git-tracked text files in the public `VictorKVS/PX00` repository.  
**Control type:** deterministic detection gate.  
**Status:** ACCEPTED WITH LIMITATIONS.

## Objective

Reduce accidental publication of obvious credential material without adding another third-party scanner to the validator dependency chain.

The control is intentionally narrow. It is not a replacement for GitHub Secret Scanning, push protection, credential rotation, history sanitation or organization-level secret management.

## Implementation

- Scanner: `px00/secret_hygiene.py`
- Tests: `tests/test_secret_hygiene.py`
- CI invocation: `python -m px00.secret_hygiene .`
- File selection source: `git ls-files -z`
- External runtime dependencies added: `NONE`

Only the canonical Git-tracked product view is scanned. Ignored `.venv`, caches and untracked local material are outside this repository gate.

## Detection baseline

The scanner currently detects selected high-signal forms:

- private-key PEM/OpenSSH headers;
- GitHub token-like values;
- AWS access-key identifiers;
- Google API-key-like values;
- Slack token-like values;
- generic assignments to common secret-bearing names such as API keys, access/refresh tokens, client secrets and passwords when the value is not an accepted placeholder.

The baseline deliberately does **not** add entropy scoring or a large signature database yet. Those approaches increase complexity and false positives and should be justified by observed misses or broader release requirements.

## Safety behavior

- findings contain file path, line number and finding class;
- detected values are intentionally not echoed into CI output;
- no automatic allow-list or suppression mechanism exists in baseline 0.1;
- a detected finding fails the process;
- Git enumeration/read errors fail the process;
- binary files and tracked text files larger than 2 MiB are skipped by this narrow baseline.

## Verification

Accepted GitHub Actions run: `31573355366` on commit `2ce2af539f5909837a00d05da15fb410bc3337d0`.

Observed result:

```text
24 tests                       PASS
secret hygiene repository scan PASS
findings                       0
errors                         0
PX00 contract validation       PASS
contract errors                0
contract warnings              0
```

## Failed attempt retained

Runs `31573227207` and `31573246011` failed because the newly added negative-test source itself contained literal generic-secret assignment fixtures. The repository scanner correctly detected those source lines. The fixtures were then constructed at runtime so the tests continue to exercise detection without embedding a scanner-triggering assignment in the tracked source.

This failure is retained as evidence that the repository-level integration check is capable of catching its own tracked test material.

## Security limits

This gate does not prove that the repository contains no secret of every possible format. It also does not inspect prior Git history, encrypted/encoded data, binary blobs, ignored/untracked files or external systems.

Until branch/ruleset enforcement exists, a direct push can still land before the CI result is known. Therefore the control is currently **detection after push and detection on PR**, not a proven pre-merge/pre-push prevention boundary.

GitHub Secret Scanning and Push Protection remain separately `UNVERIFIED` through the current connector.

## Next control decision

Keep this zero-new-dependency gate. Verify/establish `main` branch enforcement so the successful CI check becomes a required change-control boundary; separately verify GitHub Secret Scanning and Push Protection.