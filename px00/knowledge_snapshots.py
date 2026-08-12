from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import re
from typing import Iterable


_REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_SHA40_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


@dataclass(frozen=True)
class SnapshotObjectRef:
    object_id: str
    version_id: str
    content_digest: str
    knowledge_space_id: str

    def version_ref(self) -> str:
        return f"{self.object_id}@{self.version_id}#{self.content_digest.lower()}"


@dataclass(frozen=True)
class KnowledgeSnapshot:
    snapshot_id: str
    knowledge_space_id: str
    canonical_repository: str
    repository_commit_sha: str
    route_snapshot_ref: str
    content_root: str
    object_version_refs: tuple[str, ...]
    snapshot_digest: str
    hash_algorithm: str = "sha256"
    product_ref: str | None = None
    domain_ref: str | None = None


class KnowledgeSnapshotBuilder:
    """Build a fail-closed immutable reference to an external knowledge repository state."""

    @staticmethod
    def _canonical(value: object) -> bytes:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

    @staticmethod
    def _validate_content_root(value: str) -> str:
        normalized = value.strip().replace("\\", "/")
        if not normalized or normalized.startswith("/"):
            raise ValueError("INVALID_KNOWLEDGE_CONTENT_ROOT")
        parts = [part for part in normalized.split("/") if part]
        if not parts or any(part in {".", ".."} for part in parts):
            raise ValueError("INVALID_KNOWLEDGE_CONTENT_ROOT")
        return "/".join(parts) + ("/" if normalized.endswith("/") else "")

    def build(
        self,
        *,
        snapshot_id: str,
        knowledge_space_id: str,
        canonical_repository: str,
        repository_commit_sha: str,
        route_snapshot_ref: str,
        content_root: str,
        objects: Iterable[SnapshotObjectRef],
        product_ref: str | None = None,
        domain_ref: str | None = None,
    ) -> KnowledgeSnapshot:
        if not snapshot_id.strip():
            raise ValueError("KNOWLEDGE_SNAPSHOT_ID_REQUIRED")
        if not knowledge_space_id.strip():
            raise ValueError("KNOWLEDGE_SPACE_ID_REQUIRED")
        if not _REPOSITORY_RE.fullmatch(canonical_repository):
            raise ValueError("INVALID_CANONICAL_REPOSITORY")
        if not _SHA40_RE.fullmatch(repository_commit_sha):
            raise ValueError("IMMUTABLE_REPOSITORY_COMMIT_REQUIRED")
        if not route_snapshot_ref.strip():
            raise ValueError("ROUTE_SNAPSHOT_REF_REQUIRED")

        root = self._validate_content_root(content_root)
        items = tuple(objects)
        if not items:
            raise ValueError("KNOWLEDGE_SNAPSHOT_OBJECTS_REQUIRED")

        seen: set[tuple[str, str]] = set()
        version_refs: list[str] = []
        for item in items:
            if not item.object_id.strip() or item.object_id.startswith(("http://", "https://")):
                raise ValueError("INVALID_KNOWLEDGE_OBJECT_ID")
            if not item.version_id.strip():
                raise ValueError("KNOWLEDGE_VERSION_REQUIRED")
            if item.knowledge_space_id != knowledge_space_id:
                raise ValueError("KNOWLEDGE_SPACE_MISMATCH")
            if not _SHA256_RE.fullmatch(item.content_digest):
                raise ValueError("INVALID_KNOWLEDGE_CONTENT_DIGEST")
            key = (item.object_id, item.version_id)
            if key in seen:
                raise ValueError("DUPLICATE_KNOWLEDGE_OBJECT_VERSION")
            seen.add(key)
            version_refs.append(item.version_ref())

        ordered_refs = tuple(sorted(version_refs))
        material = {
            "snapshot_id": snapshot_id,
            "knowledge_space_id": knowledge_space_id,
            "canonical_repository": canonical_repository,
            "repository_commit_sha": repository_commit_sha.lower(),
            "route_snapshot_ref": route_snapshot_ref,
            "content_root": root,
            "object_version_refs": ordered_refs,
            "product_ref": product_ref,
            "domain_ref": domain_ref,
        }
        digest = sha256(self._canonical(material)).hexdigest()
        return KnowledgeSnapshot(
            snapshot_id=snapshot_id,
            knowledge_space_id=knowledge_space_id,
            canonical_repository=canonical_repository,
            repository_commit_sha=repository_commit_sha.lower(),
            route_snapshot_ref=route_snapshot_ref,
            content_root=root,
            object_version_refs=ordered_refs,
            snapshot_digest=digest,
            product_ref=product_ref,
            domain_ref=domain_ref,
        )
