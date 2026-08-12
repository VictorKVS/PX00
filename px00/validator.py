from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

ROLE_RE = re.compile(r"^ROLE-\d{4}$")
PROTO_RE = re.compile(r"^PROTO-\d{4}$")
TF_RE = re.compile(r"^TF-(\d{4})_.*\.md$")
AUTONOMY = {"A0", "A1", "A2", "A3", "A4"}
ACCEPTANCE = {"NOT_TESTED", "PASS", "PASS_WITH_ACTIONS", "FAIL", "BLOCKED"}
TERMINAL = {"COMPLETED", "FAILED", "DENIED", "ESCALATED", "CANCELLED", "BLOCKED"}
SECRET_KEYS = {
    "api_key", "api_hash", "access_token", "refresh_token", "password",
    "passwd", "secret", "client_secret", "private_key",
}
SAFE_VALUES = {"", "null", "none", "prohibited", "forbidden", "not_set", "placeholder", "replace_me", "example"}


@dataclass(frozen=True)
class Issue:
    code: str
    path: str
    message: str
    severity: str = "ERROR"


def load_yaml(path: Path) -> tuple[Any | None, list[Issue]]:
    try:
        with path.open("r", encoding="utf-8") as stream:
            return yaml.safe_load(stream), []
    except FileNotFoundError:
        return None, [Issue("FILE_MISSING", str(path), "Required YAML file is missing.")]
    except yaml.YAMLError as exc:
        return None, [Issue("YAML_INVALID", str(path), f"Invalid YAML: {exc}")]
    except OSError as exc:
        return None, [Issue("FILE_READ_ERROR", str(path), str(exc))]


def scan_secrets(value: Any, path: str) -> list[Issue]:
    issues: list[Issue] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if str(key).lower() in SECRET_KEYS and isinstance(child, (str, int, float)):
                if str(child).strip().lower() not in SAFE_VALUES:
                    issues.append(Issue("POTENTIAL_SECRET", child_path, "Potential secret value in public governance data."))
            issues.extend(scan_secrets(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            issues.extend(scan_secrets(child, f"{path}[{index}]"))
    return issues


def require_map(doc: Any, path: str) -> tuple[dict[str, Any] | None, list[Issue]]:
    if isinstance(doc, dict):
        return doc, []
    return None, [Issue("MAPPING_REQUIRED", path, "Expected a mapping/object.")]


def validate_role_document(doc: Any, path: str = "ROLE.yaml") -> list[Issue]:
    role, issues = require_map(doc, path)
    if role is None:
        return issues

    identity = role.get("identity")
    if not isinstance(identity, dict):
        return issues + [Issue("ROLE_IDENTITY_MISSING", path, "identity mapping is required.")]
    role_id = identity.get("role_id")
    if not isinstance(role_id, str) or not ROLE_RE.fullmatch(role_id):
        issues.append(Issue("ROLE_ID_INVALID", path, "identity.role_id must match ROLE-####."))
    for field in ("canonical_name", "package_version", "status"):
        if not identity.get(field):
            issues.append(Issue("ROLE_IDENTITY_FIELD_MISSING", path, f"identity.{field} is required."))

    mission = role.get("mission")
    if not isinstance(mission, dict) or not mission.get("purpose"):
        issues.append(Issue("ROLE_MISSION_MISSING", path, "mission.purpose is required."))

    authority = role.get("authority")
    if not isinstance(authority, dict):
        issues.append(Issue("ROLE_AUTHORITY_MISSING", path, "authority mapping is required."))
    else:
        level = authority.get("autonomy_level")
        if level not in AUTONOMY:
            issues.append(Issue("ROLE_AUTONOMY_INVALID", path, f"autonomy_level must be one of {sorted(AUTONOMY)}."))
        for field in ("allowed_actions", "prohibited_actions", "human_approval_required_for"):
            if not isinstance(authority.get(field), list):
                issues.append(Issue("ROLE_AUTHORITY_FIELD_MISSING", path, f"authority.{field} list is required."))
        if level in {"A0", "A1"} and "execute_external_side_effects" not in set(authority.get("prohibited_actions") or []):
            issues.append(Issue(
                "ROLE_LOW_AUTONOMY_SIDE_EFFECT_GUARD_MISSING",
                path,
                "A0/A1 role must explicitly prohibit execute_external_side_effects.",
            ))

    for block in ("knowledge", "protocols", "schemas", "evaluation", "traceability", "failure_policy", "security"):
        if not isinstance(role.get(block), dict):
            issues.append(Issue("ROLE_CONTRACT_BLOCK_MISSING", path, f"{block} mapping is required."))

    knowledge = role.get("knowledge") or {}
    if isinstance(knowledge, dict) and knowledge.get("retrieval_is_evidence") is not False:
        issues.append(Issue("ROLE_RETRIEVAL_EVIDENCE_POLICY", path, "knowledge.retrieval_is_evidence must be false."))

    trace = role.get("traceability") or {}
    if isinstance(trace, dict):
        for field in (
            "task_id_required", "run_id_required", "trace_id_required",
            "protocol_version_required", "material_input_ids_required", "material_output_ids_required",
        ):
            if trace.get(field) is not True:
                issues.append(Issue("ROLE_TRACE_REQUIREMENT_MISSING", path, f"traceability.{field} must be true."))

    security = role.get("security") or {}
    if isinstance(security, dict) and security.get("secrets_in_role_package") != "prohibited":
        issues.append(Issue("ROLE_SECRET_POLICY_MISSING", path, "security.secrets_in_role_package must be prohibited."))

    return issues + scan_secrets(role, path)


def validate_protocol_document(doc: Any, path: str = "protocol.yaml") -> list[Issue]:
    proto, issues = require_map(doc, path)
    if proto is None:
        return issues

    if not isinstance(proto.get("protocol_id"), str) or not PROTO_RE.fullmatch(proto["protocol_id"]):
        issues.append(Issue("PROTOCOL_ID_INVALID", path, "protocol_id must match PROTO-####."))
    for field in ("version", "status", "purpose"):
        if not proto.get(field):
            issues.append(Issue("PROTOCOL_FIELD_MISSING", path, f"{field} is required."))

    bounds = proto.get("bounds")
    if not isinstance(bounds, dict):
        issues.append(Issue("PROTOCOL_BOUNDS_MISSING", path, "bounds mapping is required."))
    else:
        if bounds.get("unbounded_loops") != "prohibited":
            issues.append(Issue("PROTOCOL_UNBOUNDED_LOOP", path, "bounds.unbounded_loops must be prohibited."))
        if not any(k.startswith("max_") and isinstance(v, int) and v > 0 for k, v in bounds.items()):
            issues.append(Issue("PROTOCOL_BOUND_NOT_ENFORCEABLE", path, "Pilot protocol needs a positive integer max_* bound."))

    steps = proto.get("steps")
    if not isinstance(steps, list) or not steps:
        issues.append(Issue("PROTOCOL_STEPS_MISSING", path, "steps must be non-empty."))
    else:
        seen: set[str] = set()
        for index, step in enumerate(steps):
            step_path = f"{path}.steps[{index}]"
            if not isinstance(step, dict):
                issues.append(Issue("PROTOCOL_STEP_INVALID", step_path, "Step must be a mapping."))
                continue
            step_id = step.get("step_id")
            if not step_id:
                issues.append(Issue("PROTOCOL_STEP_ID_MISSING", step_path, "step_id is required."))
            elif step_id in seen:
                issues.append(Issue("PROTOCOL_STEP_ID_DUPLICATE", step_path, f"Duplicate step_id {step_id}."))
            else:
                seen.add(str(step_id))
            for field in ("purpose", "action_class", "success_condition", "failure_transition", "event_requirement"):
                if not step.get(field):
                    issues.append(Issue("PROTOCOL_STEP_FIELD_MISSING", step_path, f"{field} is required."))
            if step.get("optional") is True and not step.get("optional_when"):
                issues.append(Issue("PROTOCOL_OPTIONAL_CONDITION_MISSING", step_path, "Optional step requires optional_when."))

    if not isinstance(proto.get("completion_criteria"), list) or not proto["completion_criteria"]:
        issues.append(Issue("PROTOCOL_COMPLETION_MISSING", path, "completion_criteria must be non-empty."))
    if not TERMINAL.issubset(set(proto.get("terminal_states") or [])):
        issues.append(Issue("PROTOCOL_TERMINAL_STATES_INCOMPLETE", path, f"terminal_states must include {sorted(TERMINAL)}."))
    return issues + scan_secrets(proto, path)


def validate_acceptance_fixture_document(doc: Any, path: str) -> list[Issue]:
    fixture, issues = require_map(doc, path)
    if fixture is None:
        return issues
    if fixture.get("status") not in ACCEPTANCE:
        issues.append(Issue("ACCEPTANCE_STATUS_INVALID", path, f"status must be one of {sorted(ACCEPTANCE)}."))
    if not isinstance(fixture.get("blocking_criteria"), list) or not fixture["blocking_criteria"]:
        issues.append(Issue("ACCEPTANCE_BLOCKING_CRITERIA_MISSING", path, "blocking_criteria must be non-empty."))
    state_rule = fixture.get("acceptance_state_rule")
    if not isinstance(state_rule, dict) or state_rule.get("pass_requires_all_blocking_criteria_with_evidence") is not True:
        issues.append(Issue("ACCEPTANCE_EVIDENCE_GATE_MISSING", path, "PASS must require all blocking criteria with evidence."))
    security = fixture.get("security")
    if not isinstance(security, dict):
        issues.append(Issue("ACCEPTANCE_SECURITY_MISSING", path, "security mapping is required."))
    elif security.get("runtime_side_effects") != "prohibited":
        issues.append(Issue("PILOT_RUNTIME_SIDE_EFFECT_POLICY", path, "Pilot runtime_side_effects must be prohibited."))
    return issues + scan_secrets(fixture, path)


def validate_tree_f(root: Path) -> list[Issue]:
    tree = root / "Tree_F"
    if not tree.is_dir():
        return [Issue("TREE_F_MISSING", "Tree_F", "Tree_F directory is required.")]
    numbers = sorted(
        int(match.group(1))
        for path in tree.glob("TF-*.md")
        if (match := TF_RE.fullmatch(path.name))
    )
    if not numbers:
        return [Issue("TREE_F_EMPTY", "Tree_F", "No TF history records found.")]
    expected = list(range(1, numbers[-1] + 1))
    return [] if numbers == expected else [Issue("TREE_F_SEQUENCE_GAP", "Tree_F", f"actual={numbers}, expected={expected}")]


def validate_role_package(role_file: Path, root: Path) -> list[Issue]:
    doc, issues = load_yaml(role_file)
    if doc is None:
        return issues
    rel = str(role_file.relative_to(root))
    issues.extend(validate_role_document(doc, rel))
    if not isinstance(doc, dict):
        return issues
    refs = [
        ("instructions", "prompt"),
        ("knowledge", "role_manifest"),
        ("protocols", "manifest"),
        ("schemas", "manifest"),
        ("evaluation", "rubric"),
    ]
    for section, field in refs:
        block = doc.get(section)
        ref = block.get(field) if isinstance(block, dict) else None
        if not isinstance(ref, str) or not ref:
            issues.append(Issue("ROLE_REFERENCE_MISSING", rel, f"{section}.{field} reference is required."))
        elif not (role_file.parent / ref).is_file():
            issues.append(Issue("ROLE_REFERENCE_NOT_FOUND", rel, f"Missing referenced file: {(role_file.parent / ref).relative_to(root)}"))
    return issues


def validate_repository(root: Path) -> list[Issue]:
    root = root.resolve()
    issues: list[Issue] = []
    for rel in (
        "README.md", "PX00.yaml", "DEVELOPMENT_JOURNAL.md", "Tree_F/README.md",
        "governance/FATHER_CONSTITUTION.md", "protocols/PROTOCOL_EXECUTION_CONTRACT.md",
        "assurance/ACCEPTANCE_MODEL.md",
    ):
        if not (root / rel).is_file():
            issues.append(Issue("ROOT_FILE_MISSING", rel, "Required baseline file is missing."))

    manifest, manifest_issues = load_yaml(root / "PX00.yaml")
    issues.extend(manifest_issues)
    if isinstance(manifest, dict):
        if manifest.get("product_id") != "PX-00":
            issues.append(Issue("PRODUCT_ID_INVALID", "PX00.yaml", "product_id must remain PX-00."))
        identity = manifest.get("identity_policy")
        if not isinstance(identity, dict) or identity.get("canonical_identity_mutable") is not False:
            issues.append(Issue("CANONICAL_IDENTITY_POLICY_INVALID", "PX00.yaml", "canonical_identity_mutable must be false."))
        gate = manifest.get("runtime_gate")
        if not isinstance(gate, dict) or gate.get("production_runtime_allowed") is not False:
            issues.append(Issue("PRODUCTION_RUNTIME_GATE_INVALID", "PX00.yaml", "production_runtime_allowed must remain false."))
        issues.extend(scan_secrets(manifest, "PX00.yaml"))

    role_ids: set[str] = set()
    required_protocols: set[str] = set()
    for role_file in sorted((root / "roles").glob("ROLE-*/ROLE.yaml")):
        doc, _ = load_yaml(role_file)
        if isinstance(doc, dict):
            identity = doc.get("identity")
            role_id = identity.get("role_id") if isinstance(identity, dict) else None
            if isinstance(role_id, str):
                if role_id in role_ids:
                    issues.append(Issue("ROLE_ID_DUPLICATE", str(role_file.relative_to(root)), role_id))
                role_ids.add(role_id)
            protocols = doc.get("protocols")
            if isinstance(protocols, dict):
                required_protocols.update(x for x in protocols.get("required", []) if isinstance(x, str))
        issues.extend(validate_role_package(role_file, root))
    if not role_ids:
        issues.append(Issue("ROLE_PILOTS_MISSING", "roles", "No governed role packages found."))

    protocol_ids: set[str] = set()
    for path in sorted((root / "protocols" / "pilots").glob("PROTO-*.yaml")):
        doc, load_issues = load_yaml(path)
        issues.extend(load_issues)
        if not isinstance(doc, dict):
            continue
        rel = str(path.relative_to(root))
        issues.extend(validate_protocol_document(doc, rel))
        protocol_id = doc.get("protocol_id")
        if isinstance(protocol_id, str):
            if protocol_id in protocol_ids:
                issues.append(Issue("PROTOCOL_ID_DUPLICATE", rel, protocol_id))
            protocol_ids.add(protocol_id)
        applicability = doc.get("applicability")
        if isinstance(applicability, dict):
            for role_id in applicability.get("roles", []) or []:
                if role_id not in role_ids:
                    issues.append(Issue("PROTOCOL_ROLE_UNKNOWN", rel, f"Unknown role {role_id}."))
    if not protocol_ids:
        issues.append(Issue("PILOT_PROTOCOLS_MISSING", "protocols/pilots", "No pilot protocols found."))
    for protocol_id in sorted(required_protocols - protocol_ids):
        issues.append(Issue("ROLE_PROTOCOL_REFERENCE_UNKNOWN", "roles", f"Required protocol not found: {protocol_id}."))

    fixture_files = sorted((root / "assurance" / "fixtures").glob("*.yaml"))
    if not fixture_files:
        issues.append(Issue("ACCEPTANCE_FIXTURE_MISSING", "assurance/fixtures", "No acceptance fixture found."))
    for path in fixture_files:
        doc, load_issues = load_yaml(path)
        issues.extend(load_issues)
        if doc is not None:
            issues.extend(validate_acceptance_fixture_document(doc, str(path.relative_to(root))))

    issues.extend(validate_tree_f(root))
    return issues


def report(issues: list[Issue]) -> dict[str, Any]:
    errors = sum(issue.severity == "ERROR" for issue in issues)
    warnings = sum(issue.severity == "WARNING" for issue in issues)
    return {
        "status": "PASS" if errors == 0 else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "issues": [asdict(issue) for issue in issues],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate PX00 contracts and pilot packages.")
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = report(validate_repository(args.root))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"PX00 contract validation: {result['status']}")
        print(f"errors={result['errors']} warnings={result['warnings']}")
        for item in result["issues"]:
            print(f"{item['severity']} {item['code']} {item['path']}: {item['message']}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
