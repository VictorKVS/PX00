from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

PIN_RE = re.compile(r"^([A-Za-z0-9_.-]+)==([A-Za-z0-9_.+!-]+)$")
HASHED_PIN_RE = re.compile(r"^([A-Za-z0-9_.-]+)==([A-Za-z0-9_.+!-]+)(?:\s+.+)?$")
SHA256_RE = re.compile(r"--hash=sha256:([0-9a-fA-F]{64})(?:\s|$)")


def normalize_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_pinned_requirements(path: Path) -> tuple[dict[str, str], list[str]]:
    requirements: dict[str, str] = {}
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return {}, [f"cannot read requirements: {exc}"]

    for line_number, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = PIN_RE.fullmatch(line)
        if not match:
            errors.append(f"requirements line {line_number} is not an exact name==version pin: {line}")
            continue
        name, version = match.groups()
        normalized = normalize_name(name)
        if normalized in requirements:
            errors.append(f"duplicate requirement: {normalized}")
            continue
        requirements[normalized] = version
    if not requirements:
        errors.append("no pinned runtime requirements found")
    return requirements, errors


def parse_hashed_requirements(path: Path) -> tuple[dict[str, dict[str, Any]], list[str]]:
    locked: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return {}, [f"cannot read hashed requirements: {exc}"]

    for line_number, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = HASHED_PIN_RE.fullmatch(line)
        if not match:
            errors.append(f"lock line {line_number} is not an exact name==version pin: {line}")
            continue
        name, version = match.groups()
        normalized = normalize_name(name)
        if normalized in locked:
            errors.append(f"duplicate locked requirement: {normalized}")
            continue
        if "--hash=" in line and "--hash=sha256:" not in line:
            errors.append(f"lock line {line_number} contains a non-SHA256 hash")
        hashes = {value.lower() for value in SHA256_RE.findall(line)}
        if not hashes:
            errors.append(f"lock line {line_number} has no SHA256 artifact hash")
        locked[normalized] = {"version": version, "hashes": hashes}

    if not locked:
        errors.append("no hash-locked runtime requirements found")
    return locked, errors


def load_sbom(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, ["SBOM file is missing"]
    except json.JSONDecodeError as exc:
        return None, [f"SBOM JSON is invalid: {exc}"]
    except OSError as exc:
        return None, [f"cannot read SBOM: {exc}"]
    if not isinstance(value, dict):
        return None, ["SBOM root must be a JSON object"]
    return value, []


def validate_dependency_provenance(
    requirements_path: Path,
    sbom_path: Path,
    lock_path: Path | None = None,
) -> list[str]:
    requirements, errors = parse_pinned_requirements(requirements_path)

    if lock_path is not None:
        locked, lock_errors = parse_hashed_requirements(lock_path)
        errors.extend(lock_errors)
        locked_versions = {
            name: value.get("version")
            for name, value in locked.items()
            if isinstance(value, dict)
        }
        if requirements != locked_versions:
            errors.append(
                f"requirements/hash-lock mismatch: requirements={requirements}, lock={locked_versions}"
            )

    sbom, sbom_errors = load_sbom(sbom_path)
    errors.extend(sbom_errors)
    if sbom is None:
        return errors

    if sbom.get("bomFormat") != "CycloneDX":
        errors.append("SBOM bomFormat must be CycloneDX")
    if sbom.get("specVersion") != "1.7":
        errors.append("SBOM specVersion must be 1.7 for this baseline")

    metadata = sbom.get("metadata")
    root_component = metadata.get("component") if isinstance(metadata, dict) else None
    root_ref = root_component.get("bom-ref") if isinstance(root_component, dict) else None
    if not isinstance(root_ref, str) or not root_ref:
        errors.append("SBOM metadata.component.bom-ref is required")

    components = sbom.get("components")
    if not isinstance(components, list):
        return errors + ["SBOM components must be a list"]

    sbom_requirements: dict[str, str] = {}
    component_refs: set[str] = set()
    for index, component in enumerate(components):
        if not isinstance(component, dict):
            errors.append(f"SBOM component {index} must be an object")
            continue
        purl = component.get("purl")
        name = component.get("name")
        version = component.get("version")
        bom_ref = component.get("bom-ref")
        if isinstance(bom_ref, str) and bom_ref:
            if bom_ref in component_refs:
                errors.append(f"duplicate SBOM bom-ref: {bom_ref}")
            component_refs.add(bom_ref)
        if not (isinstance(purl, str) and purl.startswith("pkg:pypi/")):
            continue
        if not isinstance(name, str) or not isinstance(version, str):
            errors.append(f"PyPI SBOM component {index} requires name and version")
            continue
        normalized = normalize_name(name)
        expected_purl = f"pkg:pypi/{normalized}@{version}"
        if purl != expected_purl:
            errors.append(f"component {normalized} purl mismatch: {purl} != {expected_purl}")
        if normalized in sbom_requirements:
            errors.append(f"duplicate PyPI SBOM component: {normalized}")
        sbom_requirements[normalized] = version
        licenses = component.get("licenses")
        if not isinstance(licenses, list) or not licenses:
            errors.append(f"component {normalized} must record license metadata")
        refs = component.get("externalReferences")
        if not isinstance(refs, list) or not refs:
            errors.append(f"component {normalized} must record an external provenance reference")

    if requirements != sbom_requirements:
        errors.append(
            f"requirements/SBOM mismatch: requirements={requirements}, sbom={sbom_requirements}"
        )

    dependencies = sbom.get("dependencies")
    if not isinstance(dependencies, list):
        errors.append("SBOM dependencies must be a list")
    elif isinstance(root_ref, str) and root_ref:
        root_dependency = next(
            (item for item in dependencies if isinstance(item, dict) and item.get("ref") == root_ref),
            None,
        )
        if root_dependency is None:
            errors.append("SBOM dependency graph must contain the root component")
        else:
            depends_on = set(root_dependency.get("dependsOn") or [])
            if depends_on != component_refs:
                errors.append(
                    f"SBOM root dependency set mismatch: dependsOn={sorted(depends_on)}, components={sorted(component_refs)}"
                )

    return errors


def validate_repository_dependency_provenance(root: Path) -> list[str]:
    return validate_dependency_provenance(
        root / "requirements-validator.txt",
        root / "security" / "sbom" / "PX00-validator.cdx.json",
        root / "requirements-validator-lock.txt",
    )
