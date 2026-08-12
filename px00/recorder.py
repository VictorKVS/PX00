from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Iterable

from px00.kernel.synthetic import MaterialEvent


class RecorderIntegrityError(ValueError):
    pass


_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


@dataclass(frozen=True)
class RecordedEvent:
    event_id: str
    previous_event_hash: str
    event_hash: str
    payload: dict


@dataclass(frozen=True)
class TraceKnowledgeContext:
    context_package_ref: str
    context_package_hash: str
    knowledge_snapshot_refs: tuple[str, ...] = ()
    knowledge_snapshot_digests: tuple[str, ...] = ()
    producer_manifest_refs: tuple[str, ...] = ()
    producer_manifest_digests: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.context_package_ref.strip():
            raise RecorderIntegrityError("CONTEXT_PACKAGE_REF_REQUIRED")
        if not _SHA256_RE.fullmatch(self.context_package_hash):
            raise RecorderIntegrityError("INVALID_CONTEXT_PACKAGE_HASH")
        if len(self.knowledge_snapshot_refs) != len(self.knowledge_snapshot_digests):
            raise RecorderIntegrityError("KNOWLEDGE_SNAPSHOT_REF_DIGEST_COUNT_MISMATCH")
        if len(self.producer_manifest_refs) != len(self.producer_manifest_digests):
            raise RecorderIntegrityError("PRODUCER_MANIFEST_REF_DIGEST_COUNT_MISMATCH")
        if len(set(self.knowledge_snapshot_refs)) != len(self.knowledge_snapshot_refs):
            raise RecorderIntegrityError("DUPLICATE_KNOWLEDGE_SNAPSHOT_REF")
        if len(set(self.producer_manifest_refs)) != len(self.producer_manifest_refs):
            raise RecorderIntegrityError("DUPLICATE_PRODUCER_MANIFEST_REF")
        for digest in (*self.knowledge_snapshot_digests, *self.producer_manifest_digests):
            if not _SHA256_RE.fullmatch(digest):
                raise RecorderIntegrityError("INVALID_KNOWLEDGE_PROVENANCE_DIGEST")


@dataclass(frozen=True)
class TraceManifestRecord:
    trace_id: str
    run_id: str
    task_id: str
    event_refs: tuple[str, ...]
    event_hashes: tuple[str, ...]
    event_count: int
    integrity_algorithm: str
    chain_head_hash: str | None
    context_package_ref: str | None = None
    context_package_hash: str | None = None
    knowledge_snapshot_refs: tuple[str, ...] = ()
    knowledge_snapshot_digests: tuple[str, ...] = ()
    producer_manifest_refs: tuple[str, ...] = ()
    producer_manifest_digests: tuple[str, ...] = ()


@dataclass(frozen=True)
class PersistedTraceManifest:
    manifest_ref: str
    manifest_hash: str
    hash_algorithm: str
    manifest: TraceManifestRecord


class AppendOnlyEventRecorder:
    ALGORITHM = "sha256_chain_v1"
    GENESIS = "0" * 64

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _canonical_payload(event: MaterialEvent) -> dict:
        return asdict(event)

    @staticmethod
    def _canonical_json(payload: dict) -> bytes:
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

    @classmethod
    def _digest(cls, previous_hash: str, payload: dict) -> str:
        return sha256(previous_hash.encode("ascii") + cls._canonical_json(payload)).hexdigest()

    def append(self, event: MaterialEvent) -> RecordedEvent:
        path = self.root / f"{event.trace_id}.jsonl"
        existing = self.read_trace(event.trace_id)
        if existing:
            first = existing[0].payload
            if event.run_id != first["run_id"] or event.task_id != first["task_id"]:
                raise RecorderIntegrityError("TRACE_CONTEXT_MISMATCH")
            if any(item.event_id == event.event_id for item in existing):
                raise RecorderIntegrityError("EVENT_ID_REUSE")
            previous = existing[-1].event_hash
        else:
            previous = self.GENESIS
        payload = self._canonical_payload(event)
        digest = self._digest(previous, payload)
        record = {"event_id": event.event_id, "previous_event_hash": previous, "event_hash": digest, "payload": payload}
        with path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(self._canonical_json(record).decode("utf-8") + "\n")
        return RecordedEvent(event.event_id, previous, digest, payload)

    def read_trace(self, trace_id: str) -> tuple[RecordedEvent, ...]:
        path = self.root / f"{trace_id}.jsonl"
        if not path.exists():
            return ()
        result = []
        for line in path.read_text(encoding="utf-8").splitlines():
            raw = json.loads(line)
            result.append(RecordedEvent(raw["event_id"], raw["previous_event_hash"], raw["event_hash"], raw["payload"]))
        return tuple(result)

    def verify(self, trace_id: str, knowledge_context: TraceKnowledgeContext | None = None) -> TraceManifestRecord:
        records = self.read_trace(trace_id)
        if not records:
            raise RecorderIntegrityError("TRACE_EMPTY")
        first = records[0].payload
        previous = self.GENESIS
        seen = set()
        refs, hashes = [], []
        for record in records:
            if record.event_id in seen:
                raise RecorderIntegrityError("EVENT_ID_REUSE")
            seen.add(record.event_id)
            if record.previous_event_hash != previous:
                raise RecorderIntegrityError("PREVIOUS_HASH_MISMATCH")
            expected = self._digest(previous, record.payload)
            if record.event_hash != expected:
                raise RecorderIntegrityError("EVENT_HASH_MISMATCH")
            if record.payload["trace_id"] != trace_id or record.payload["run_id"] != first["run_id"] or record.payload["task_id"] != first["task_id"]:
                raise RecorderIntegrityError("TRACE_CONTEXT_MISMATCH")
            refs.append(record.event_id)
            hashes.append(record.event_hash)
            previous = record.event_hash

        context_package_ref = None
        context_package_hash = None
        knowledge_snapshot_refs: tuple[str, ...] = ()
        knowledge_snapshot_digests: tuple[str, ...] = ()
        producer_manifest_refs: tuple[str, ...] = ()
        producer_manifest_digests: tuple[str, ...] = ()
        if knowledge_context is not None:
            knowledge_context.validate()
            context_package_ref = knowledge_context.context_package_ref
            context_package_hash = knowledge_context.context_package_hash.lower()
            knowledge_snapshot_refs = tuple(knowledge_context.knowledge_snapshot_refs)
            knowledge_snapshot_digests = tuple(value.lower() for value in knowledge_context.knowledge_snapshot_digests)
            producer_manifest_refs = tuple(knowledge_context.producer_manifest_refs)
            producer_manifest_digests = tuple(value.lower() for value in knowledge_context.producer_manifest_digests)

        return TraceManifestRecord(
            trace_id,
            first["run_id"],
            first["task_id"],
            tuple(refs),
            tuple(hashes),
            len(refs),
            self.ALGORITHM,
            previous,
            context_package_ref,
            context_package_hash,
            knowledge_snapshot_refs,
            knowledge_snapshot_digests,
            producer_manifest_refs,
            producer_manifest_digests,
        )

    def persist_manifest(
        self,
        trace_id: str,
        knowledge_context: TraceKnowledgeContext | None = None,
    ) -> PersistedTraceManifest:
        manifest = self.verify(trace_id, knowledge_context)
        payload = asdict(manifest)
        digest = sha256(self._canonical_json(payload)).hexdigest()
        ref = f"TRACEMAN-{trace_id.removeprefix('TRACE-')}"
        envelope = {"manifest_ref": ref, "manifest_hash": digest, "hash_algorithm": "sha256", "manifest": payload}
        path = self.root / f"{trace_id}.manifest.json"
        path.write_bytes(self._canonical_json(envelope) + b"\n")
        return PersistedTraceManifest(ref, digest, "sha256", manifest)

    @staticmethod
    def _persisted_manifest_has_knowledge_context(manifest: dict) -> bool:
        return bool(
            manifest.get("context_package_ref")
            or manifest.get("context_package_hash")
            or manifest.get("knowledge_snapshot_refs")
            or manifest.get("knowledge_snapshot_digests")
            or manifest.get("producer_manifest_refs")
            or manifest.get("producer_manifest_digests")
        )

    def verify_persisted_manifest(
        self,
        trace_id: str,
        expected_knowledge_context: TraceKnowledgeContext | None = None,
    ) -> PersistedTraceManifest:
        path = self.root / f"{trace_id}.manifest.json"
        if not path.exists():
            raise RecorderIntegrityError("TRACE_MANIFEST_MISSING")
        envelope = json.loads(path.read_text(encoding="utf-8"))
        manifest = envelope["manifest"]
        expected = sha256(self._canonical_json(manifest)).hexdigest()
        if envelope.get("hash_algorithm") != "sha256" or envelope.get("manifest_hash") != expected:
            raise RecorderIntegrityError("TRACE_MANIFEST_HASH_MISMATCH")
        if self._persisted_manifest_has_knowledge_context(manifest) and expected_knowledge_context is None:
            raise RecorderIntegrityError("TRACE_KNOWLEDGE_CONTEXT_EXPECTATION_REQUIRED")
        live = self.verify(trace_id, expected_knowledge_context)
        if self._canonical_json(manifest) != self._canonical_json(asdict(live)):
            raise RecorderIntegrityError("TRACE_MANIFEST_EVENT_OR_KNOWLEDGE_CONTEXT_MISMATCH")
        return PersistedTraceManifest(envelope["manifest_ref"], expected, "sha256", live)

    def record_all(self, events: Iterable[MaterialEvent]) -> TraceManifestRecord:
        events = tuple(events)
        if not events:
            raise RecorderIntegrityError("TRACE_EMPTY")
        trace_id = events[0].trace_id
        for event in events:
            self.append(event)
        return self.verify(trace_id)
