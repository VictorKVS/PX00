from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from px00.kernel.synthetic import ActionRequest, AuthorityDecision, MaterialEvent
from px00.profile_registry import PolicySnapshot
from px00.recorder import AppendOnlyEventRecorder, RecorderIntegrityError


@dataclass(frozen=True)
class ReplayReport:
    status: str
    run_id: str
    trace_id: str
    verified_event_count: int
    reason_code: str
    policy_snapshot_ref: str | None = None
    policy_snapshot_hash: str | None = None


class ReadOnlyReplayVerifier:
    """Verifies persisted governed lineage without executing any tool or side effect."""

    def __init__(self, recorder: AppendOnlyEventRecorder) -> None:
        self._recorder = recorder

    def verify(
        self,
        *,
        request: ActionRequest,
        authority: AuthorityDecision,
        snapshot: PolicySnapshot,
        events: Iterable[MaterialEvent],
    ) -> ReplayReport:
        events = tuple(events)
        if not events:
            return self._report("INSUFFICIENT_EVIDENCE", request, 0, "NO_MATERIAL_EVENTS", snapshot)

        if snapshot.run_id != request.run_id:
            return self._report("POLICY_MISMATCH", request, 0, "POLICY_SNAPSHOT_RUN_MISMATCH", snapshot)
        if authority.run_id != request.run_id or authority.action_request_id != request.action_request_id:
            return self._report("BROKEN_LINEAGE", request, 0, "AUTHORITY_REQUEST_RUN_MISMATCH", snapshot)
        if authority.policy_snapshot_ref != snapshot.snapshot_id or authority.policy_snapshot_hash != snapshot.snapshot_hash:
            return self._report("POLICY_MISMATCH", request, 0, "AUTHORITY_POLICY_SNAPSHOT_MISMATCH", snapshot)

        for event in events:
            if event.trace_id != request.trace_id or event.run_id != request.run_id or event.task_id != request.task_id:
                return self._report("BROKEN_LINEAGE", request, 0, "EVENT_CONTEXT_MISMATCH", snapshot)
            if event.action_request_ref != request.action_request_id:
                return self._report("BROKEN_LINEAGE", request, 0, "EVENT_ACTION_REQUEST_MISMATCH", snapshot)
            if event.authority_decision_ref != authority.decision_id:
                return self._report("BROKEN_LINEAGE", request, 0, "EVENT_AUTHORITY_MISMATCH", snapshot)
            if event.policy_snapshot_ref != snapshot.snapshot_id or event.policy_snapshot_hash != snapshot.snapshot_hash:
                return self._report("POLICY_MISMATCH", request, 0, "EVENT_POLICY_SNAPSHOT_MISMATCH", snapshot)

        try:
            persisted = self._recorder.verify_persisted_manifest(request.trace_id)
        except RecorderIntegrityError as exc:
            return self._report("TAMPER_DETECTED", request, 0, str(exc), snapshot)

        if persisted.manifest.run_id != request.run_id or persisted.manifest.task_id != request.task_id:
            return self._report("BROKEN_LINEAGE", request, 0, "TRACE_MANIFEST_CONTEXT_MISMATCH", snapshot)
        if persisted.manifest.event_refs != tuple(event.event_id for event in events):
            return self._report("BROKEN_LINEAGE", request, 0, "TRACE_MANIFEST_EVENT_SET_MISMATCH", snapshot)

        return self._report(
            "VERIFIED_RECORD",
            request,
            persisted.manifest.event_count,
            "GOVERNED_LINEAGE_VERIFIED",
            snapshot,
        )

    @staticmethod
    def _report(status: str, request: ActionRequest, count: int, reason: str, snapshot: PolicySnapshot) -> ReplayReport:
        return ReplayReport(
            status=status,
            run_id=request.run_id,
            trace_id=request.trace_id,
            verified_event_count=count,
            reason_code=reason,
            policy_snapshot_ref=snapshot.snapshot_id,
            policy_snapshot_hash=snapshot.snapshot_hash,
        )
