# 2026-08-12 — Secret hygiene gate

PX00 added a zero-new-dependency scanner for likely credential leakage in the canonical Git-tracked repository view.

## Change

- added `px00/secret_hygiene.py`;
- added `tests/test_secret_hygiene.py`;
- added explicit CI secret-hygiene step;
- accepted `security/SECRET_HYGIENE_BASELINE_0_1.md`;
- accepted ADR-0019 and TF-0021;
- recorded assurance run/acceptance evidence.

## Verification

Accepted GitHub Actions run `31573355366`, commit `2ce2af539f5909837a00d05da15fb410bc3337d0`:

```text
24 tests PASS
PX00 secret hygiene scan PASS
findings=0 errors=0
PX00 contract validation PASS
errors=0 warnings=0
```

Two failed runs (`31573227207`, `31573246011`) are intentionally retained. The first test implementation embedded literal generic-secret assignment fixtures in the tracked test file, so the repository scanner detected its own negative-test source. Fixtures were changed to runtime construction rather than weakening the scanner.

## Security conclusion

`PASS_WITH_SCOPE_LIMITS`.

This is current tracked-file detection, not proof of Git history cleanliness and not a substitute for GitHub Secret Scanning/Push Protection. No external dependency was added and suspected values are not echoed to logs.

## Next

Repository `main` change-control enforcement remains the blocking external gate. GitHub Secret Scanning and Push Protection remain separately unverified.