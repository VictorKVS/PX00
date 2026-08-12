from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

from px00.context_packages import ContextPackage
from px00.knowledge_manifest_bridge import ImportedKnowledgeSlice
from px00.recorder import TraceKnowledgeContext


_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


@dataclass(frozen=True)
class RunKnowledgePin:
    run_id: str
    role_ref: str
    assignment_ref: str
    context_package_ref: str
    context_package_hash: str
    knowledge_snapshot_refs: tuple[str, ...]
    knowledge_snapshot_digests: tuple[str, ...]
    producer_manifest_refs: tuple[str, ...]
    producer_manifest_digests: tuple[str, ...]

    def to_trace_context(self) -> TraceKnowledgeContext:
        return TraceKnowledgeContext(
            context_package_ref=self.context_package_ref,
            context_package_hash=self.context_package_hash,
            knowledge_snapshot_refs=self.knowledge_snapshot_refs,
            knowledge_snapshot_digests=self.knowledge_snapshot_digests,
            producer_manifest_refs=self.producer_manifest_refs,
            producer_manifest_digests=self.producer_manifest_digests,
        )


class RunKnowledgeBinder:
    """Pin already-governed knowledge context to one RUN without granting authority."""

    def bind(
        self,
        *,
        run_id: str,
        role_ref: str,
        assignment_ref: str,
        context_package: ContextPackage,
        imported_slices: Iterable[ImportedKnowledgeSlice],
    ) -> RunKnowledgePin:
        if context_package.run_ref != run_id:
            raise ValueError("RUN_CONTEXT_PACKAGE_MISMATCH")
        if context_package.role_ref != role_ref:
            raise ValueError("ROLE_CONTEXT_PACKAGE_MISMATCH")
        if context_package.assignment_ref != assignment_ref:
            raise ValueError("ASSIGNMENT_CONTEXT_PACKAGE_MISMATCH")
        if not _SHA256_RE.fullmatch(context_package.package_hash):
            raise ValueError("INVALID_CONTEXT_PACKAGE_HASH")

        slices = tuple(imported_slices)
        if not slices:
            raise ValueError("IMPORTED_KNOWLEDGE_SLICE_REQUIRED")

        by_snapshot: dict[str, ImportedKnowledgeSlice] = {}
        for item in slices:
            snapshot_ref = item.snapshot.snapshot_id
            if snapshot_ref in by_snapshot:
                raise ValueError("DUPLICATE_IMPORTED_KNOWLEDGE_SNAPSHOT")
            if not _SHA256_RE.fullmatch(item.snapshot.snapshot_digest):
                raise ValueError("INVALID_IMPORTED_KNOWLEDGE_SNAPSHOT_DIGEST")
            if not _SHA256_RE.fullmatch(item.producer_manifest_digest):
                raise ValueError("INVALID_IMPORTED_PRODUCER_MANIFEST_DIGEST")
            by_snapshot[snapshot_ref] = item

        package_refs = tuple(sorted(context_package.knowledge_snapshot_refs))
        imported_refs = tuple(sorted(by_snapshot))
        if package_refs != imported_refs:
            raise ValueError("CONTEXT_IMPORTED_SNAPSHOT_SET_MISMATCH")

        snapshot_pairs = sorted(
            (ref, by_snapshot[ref].snapshot.snapshot_digest.lower()) for ref in imported_refs
        )
        manifest_pairs = sorted(
            (item.producer_manifest_id, item.producer_manifest_digest.lower()) for item in slices
        )
        manifest_refs = tuple(ref for ref, _ in manifest_pairs)
        if len(set(manifest_refs)) != len(manifest_refs):
            raise ValueError("DUPLICATE_PRODUCER_MANIFEST_REF")

        pin = RunKnowledgePin(
            run_id=run_id,
            role_ref=role_ref,
            assignment_ref=assignment_ref,
            context_package_ref=context_package.context_package_id,
            context_package_hash=context_package.package_hash.lower(),
            knowledge_snapshot_refs=tuple(ref for ref, _ in snapshot_pairs),
            knowledge_snapshot_digests=tuple(digest for _, digest in snapshot_pairs),
            producer_manifest_refs=manifest_refs,
            producer_manifest_digests=tuple(digest for _, digest in manifest_pairs),
        )
        pin.to_trace_context().validate()
        return pin
