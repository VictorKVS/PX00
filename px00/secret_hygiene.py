from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


MAX_TEXT_FILE_BYTES = 2 * 1024 * 1024
SAFE_GENERIC_VALUES = {
    "",
    "none",
    "null",
    "not_set",
    "unset",
    "placeholder",
    "replace_me",
    "example",
    "prohibited",
    "forbidden",
    "unverified",
}


@dataclass(frozen=True)
class SecretFinding:
    path: str
    line: int
    kind: str
    message: str


TOKEN_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----")),
    ("github_pat", re.compile(r"\bghp_[A-Za-z0-9]{36,}\b")),
    ("github_fine_grained_pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{20,}\b")),
)

GENERIC_ASSIGNMENT = re.compile(
    r"(?i)\b(api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|password|passwd|secret)\b"
    r"\s*[:=]\s*[\"']?([^\s\"'#]{8,})"
)


def scan_text(text: str, path: str) -> list[SecretFinding]:
    findings: list[SecretFinding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for kind, pattern in TOKEN_PATTERNS:
            if pattern.search(line):
                findings.append(
                    SecretFinding(
                        path=path,
                        line=line_number,
                        kind=kind,
                        message="Potential credential material detected; value intentionally omitted.",
                    )
                )

        match = GENERIC_ASSIGNMENT.search(line)
        if match:
            candidate = match.group(2).strip().rstrip(",;}")
            normalized = candidate.lower()
            if normalized not in SAFE_GENERIC_VALUES and not candidate.startswith("${"):
                findings.append(
                    SecretFinding(
                        path=path,
                        line=line_number,
                        kind="generic_secret_assignment",
                        message="Potential secret assignment detected; value intentionally omitted.",
                    )
                )
    return findings


def git_tracked_files(root: Path) -> tuple[list[Path], list[str]]:
    root = root.resolve()
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        return [], [f"cannot execute git ls-files: {exc}"]

    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        return [], [f"git ls-files failed: {detail or completed.returncode}"]

    names = completed.stdout.decode("utf-8", errors="surrogateescape").split("\0")
    return [root / name for name in names if name], []


def scan_repository(root: Path) -> tuple[list[SecretFinding], list[str]]:
    root = root.resolve()
    files, errors = git_tracked_files(root)
    findings: list[SecretFinding] = []

    for path in files:
        try:
            if not path.is_file() or path.stat().st_size > MAX_TEXT_FILE_BYTES:
                continue
            data = path.read_bytes()
        except OSError as exc:
            errors.append(f"cannot read {path}: {exc}")
            continue

        if b"\x00" in data:
            continue
        text = data.decode("utf-8", errors="replace")
        try:
            rel = str(path.relative_to(root))
        except ValueError:
            rel = str(path)
        findings.extend(scan_text(text, rel))

    return findings, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan Git-tracked PX00 text files for likely secret leakage.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    findings, errors = scan_repository(Path(args.root))
    status = "PASS" if not findings and not errors else "FAIL"

    if args.as_json:
        print(
            json.dumps(
                {
                    "status": status,
                    "findings": [asdict(item) for item in findings],
                    "errors": errors,
                },
                indent=2,
            )
        )
    else:
        print(f"PX00 secret hygiene scan: {status}")
        print(f"findings={len(findings)} errors={len(errors)}")
        for finding in findings:
            print(f"{finding.path}:{finding.line}: {finding.kind}: {finding.message}")
        for error in errors:
            print(f"ERROR: {error}")

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
