from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import re
from typing import Mapping, Sequence

from px00.context_packages import KnowledgeObjectRef
from px00.knowledge_snapshots import KnowledgeSnapshot, KnowledgeSnapshotBuilder, SnapshotObjectRef


_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_ALLOWED_KNOWLEDGE_STATES = {
    "CANDIDATE",
    "SOURCE_VERIFIED",
    "ATOMIZED",
    "APPLICABILITY_REVIEWED",
    "CONTROL_MAPPED",
    "EXPERT_REVIEWED",
    "VERIFIED",
    "STALE",
    "DISPUTED",
    "SUPERSEDED",
}
_ALLOWED_CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "SECRET"}


@dataclass(frozen=True)
class ImportedKnowledgeObject:
    context_object: KnowledgeObjectRef
    knowledge_state: str
    source_locator_ref: str | None
    repository_relative_path: str
    selection_reason: str
    freshness_state: str | None = None


@dataclass(frozen=True)
class ImportedKnowledgeSlice:
    producer_manifest_id: str
    producer_manifest_digest: str
    snapshot: KnowledgeSnapshot
    objects: tuple[ImportedKnowledgeObject, ...]


class KnowledgeManifestBridge:
    """Validate a producer manifest and turn it into a pinned runtime knowledge slice.

    The bridge verifies transport/provenance semantics only. It never upgrades the producer's
    knowledge state, decides applicability, or grants runtime authority.
    """

    @staticmethod
    def _canonical(value: object) -> bytes:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

    @classmethod
    def _producer_digest_material(cls, manifest: Mapping[str, object]) -> dict[str, object]:
        raw_objects = manifest.get("selected_objects")
        if not isinstance(raw_objects, Sequence) or isinstance(raw_objects, (str, bytes)):
            raise ValueError("SELECTED_OBJECTS_REQUIRED")

        selected: list[dict[str, object]] = []
        for raw in raw_objects:
            if not isinstance(raw, Mapping):
                raise ValueError("INVALID_SELECTED_OBJECT")
            selected.append(
                {
                    "object_id": raw.get("object_id"),
                    "version_id": raw.get("version_id"),
                    "object_type": raw.get("object_type"),
                    "repository_relative_path": raw.get("repository_relative_path"),
                    "content_digest_sha256": raw.get("content_digest_sha256"),
                    "knowledge_state": raw.get("knowledge_state"),
                    "selection_reason": raw.get("selection_reason"),
                    "source_locator_ref": raw.get("source_locator_ref"),
                    "freshness_state": raw.get("freshness_state"),
                    "classification": raw.get("classification"),
                }
            )
        selected.sort(key=lambda row: (str(row["object_id"]), str(row["version_id"])))
        return {
            "schema_version": manifest.get("schema_version"),
            "manifest_id": manifest.get("manifest_id"),
            "knowledge_space_id": manifest.get("knowledge_space_id"),
            "canonical_repository": manifest.get("canonical_repository"),
            "repository_commit_sha": manifest.get("repository_commit_sha"),
            "content_root": manifest.get("content_root"),
            "selection_request_ref": manifest.get("selection_request_ref"),
            "selected_objects": selected,
            "hash_algorithm": manifest.get("hash_algorithm"),
        }

    @classmethod
    def producer_manifest_digest(cls, manifest: Mapping[str, object]) -> str:
        return sha256(cls._canonical(cls._producer_digest_material(manifest))).hexdigest()

    def import_manifest(
        self,
        manifest: Mapping[str, object],
        *,
        expected_repository: str,
        expected_knowledge_space_id: str,
        expected_content_root: str,
        route_snapshot_ref: str,
        domain_id: str,
        product_ref: str | None = None,
        domain_ref: str | None = None,
    ) -> ImportedKnowledgeSlice:
        required = (
            "schema_version",
            "manifest_id",
            "knowledge_space_id",
            "canonical_repository",
            "repository_commit_sha",
            "content_root",
            "selection_request_ref",
            "selected_objects",
            "manifest_digest",
            "hash_algorithm",
        )
        for field in required:
            if field not in manifest:
                raise ValueError(f"PRODUCER_MANIFEST_FIELD_REQUIRED:{field}")

        if manifest["canonical_repository"] != expected_repository:
            raise ValueError("PRODUCER_REPOSITORY_MISMATCH")
        if manifest["knowledge_space_id"] != expected_knowledge_space_id:
            raise ValueError("PRODUCER_KNOWLEDGE_SPACE_MISMATCH")
        if manifest["content_root"] != expected_content_root:
            raise ValueError("PRODUCER_CONTENT_ROOT_MISMATCH")
        if manifest["hash_algorithm"] != "sha256":
            raise ValueError("UNSUPPORTED_PRODUCER_HASH_ALGORITHM")

        declared_manifest_digest = str(manifest["manifest_digest"]).lower()
        if not _SHA256_RE.fullmatch(declared_manifest_digest):
            raise ValueError("INVALID_PRODUCER_MANIFEST_DIGEST")
        actual_manifest_digest = self.producer_manifest_digest(manifest)
        if actual_manifest_digest != declared_manifest_digest:
            raise ValueError("PRODUCER_MANIFEST_DIGEST_MISMATCH")

        raw_objects = manifest["selected_objects"]
        if not isinstance(raw_objects, Sequence) or isinstance(raw_objects, (str, bytes)) or not raw_objects:
            raise ValueError("SELECTED_OBJECTS_REQUIRED")

        snapshot_objects: list[SnapshotObjectRef] = []
        imported: list[ImportedKnowledgeObject] = []
        for raw in raw_objects:
            if not isinstance(raw, Mapping):
                raise ValueError("INVALID_SELECTED_OBJECT")
            object_id = str(raw.get("object_id", "")).strip()
            version_id = str(raw.get("version_id", "")).strip()
            object_type = str(raw.get("object_type", "")).strip()
            digest = str(raw.get("content_digest_sha256", "")).lower()
            state = str(raw.get("knowledge_state", "")).strip()
            classification = str(raw.get("classification", "PUBLIC")).strip()
            path = str(raw.get("repository_relative_path", "")).strip()
            reason = str(raw.get("selection_reason", "")).strip()
            freshness_value = raw.get("freshness_state")
            freshness = str(freshness_value).strip() if freshness_value is not None else None
            locator_value = raw.get("source_locator_ref")
            locator = str(locator_value).strip() if locator_value is not None else None

            if not object_id or not version_id or not object_type or not path or not reason:
                raise ValueError("INCOMPLETE_SELECTED_OBJECT")
            if state not in _ALLOWED_KNOWLEDGE_STATES:
                raise ValueError("INVALID_PRODUCER_KNOWLEDGE_STATE")
            if state in {"SOURCE_VERIFIED", "VERIFIED"} and not locator:
                raise ValueError("VERIFIED_STATE_REQUIRES_SOURCE_LOCATOR")
            if classification not in _ALLOWED_CLASSIFICATIONS:
                raise ValueError("INVALID_PRODUCER_CLASSIFICATION")
            if not _SHA256_RE.fullmatch(digest):
                raise ValueError("INVALID_SELECTED_OBJECT_DIGEST")

            snapshot_object = SnapshotObjectRef(
                object_id=object_id,
                version_id=version_id,
                content_digest=digest,
                knowledge_space_id=expected_knowledge_space_id,
            )
            snapshot_objects.append(snapshot_object)
            imported.append(
                ImportedKnowledgeObject(
                    context_object=KnowledgeObjectRef(
                        object_id=object_id,
                        version_id=version_id,
                        content_digest=digest,
                        object_type=object_type,
                        knowledge_space_id=expected_knowledge_space_id,
                        domain_id=domain_id,
                        classification=classification,
                        route_snapshot_ref=route_snapshot_ref,
                        knowledge_snapshot_ref=str(manifest["manifest_id"]),
                    ),
                    knowledge_state=state,
                    source_locator_ref=locator,
                    repository_relative_path=path,
                    selection_reason=reason,
                    freshness_state=freshness,
                )
            )

        snapshot = KnowledgeSnapshotBuilder().build(
            snapshot_id=str(manifest["manifest_id"]),
            knowledge_space_id=expected_knowledge_space_id,
            canonical_repository=expected_repository,
            repository_commit_sha=str(manifest["repository_commit_sha"]),
            route_snapshot_ref=route_snapshot_ref,
            content_root=expected_content_root,
            objects=tuple(snapshot_objects),
            product_ref=product_ref,
            domain_ref=domain_ref,
        )
        return ImportedKnowledgeSlice(
            producer_manifest_id=str(manifest["manifest_id"]),
            producer_manifest_digest=declared_manifest_digest,
            snapshot=snapshot,
            objects=tuple(imported),
        )
