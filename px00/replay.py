from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from px00.kernel.synthetic import ActionRequest, AuthorityDecision, MaterialEvent
from px00.profile_registry import PolicySnapshot
from px00.recorder import (
    AppendOnlyEventRecorder,
    RecorderIntegrityError,
    TraceDecisionContext,
    TraceKnowledgeContext,
)


@dataclass(frozen=True)
class ReplayReport:
    status: str
    run_id: str
    trace_id: str
    verified_event_count: int
    reason_code: str
    policy_snapshot_ref: str | None = None
    policy_snapshot_hash: str | None = None
    context_package_ref: str | None = None
    context_package_hash: str | None = None
    knowledge_snapshot_refs: tuple[str, ...] = ()
    knowledge_context_verified: bool = False
    decision_refs: tuple[str, ...] = ()
    decision_digests: tuple[str, ...] = ()
    decision_materiality_classes: tuple[str, ...] = ()
    decision_context_verified: bool = False


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
        knowledge_context: TraceKnowledgeContext | None = None,
        decision_context: TraceDecisionContext | None = None,
    ) -> ReplayReport:
        events = tuple(events)
        if not events:
            return self._report(
                "INSUFFICIENT_EVIDENCE", request, 0, "NO_MATERIAL_EVENTS", snapshot, knowledge_context, decision_context
            )

        if snapshot.run_id != request.run_id:
            return self._report(
                "POLICY_MISMATCH", request, 0, "POLICY_SNAPSHOT_RUN_MISMATCH", snapshot, knowledge_context, decision_context
            )
        if authority.run_id != request.run_id or authority.action_request_id != request.action_request_id:
            return self._report(
                "BROKEN_LINEAGE", request, 0, "AUTHORITY_REQUEST_RUN_MISMATCH", snapshot, knowledge_context, decision_context
            )
        if authority.policy_snapshot_ref != snapshot.snapshot_id or authority.policy_snapshot_hash != snapshot.snapshot_hash:
            return self._report(
                "POLICY_MISMATCH", request, 0, "AUTHORITY_POLICY_SNAPSHOT_MISMATCH", snapshot, knowledge_context, decision_context
            )

        for event in events:
            if event.trace_id != request.trace_id or event.run_id != request.run_id or event.task_id != request.task_id:
                return self._report(
                    "BROKEN_LINEAGE", request, 0, "EVENT_CONTEXT_MISMATCH", snapshot, knowledge_context, decision_context
                )
            if event.action_request_ref != request.action_request_id:
                return self._report(
                    "BROKEN_LINEAGE", request, 0, "EVENT_ACTION_REQUEST_MISMATCH", snapshot, knowledge_context, decision_context
                )
            if event.authority_decision_ref != authority.decision_id:
                return self._report(
                    "BROKEN_LINEAGE", request, 0, "EVENT_AUTHORITY_MISMATCH", snapshot, knowledge_context, decision_context
                )
            if event.policy_snapshot_ref != snapshot.snapshot_id or event.policy_snapshot_hash != snapshot.snapshot_hash:
                return self._report(
                    "POLICY_MISMATCH", request, 0, "EVENT_POLICY_SNAPSHOT_MISMATCH", snapshot, knowledge_context, decision_context
                )

        try:
            persisted = self._recorder.verify_persisted_manifest(
                request.trace_id,
                expected_knowledge_context=knowledge_context,
                expected_decision_context=decision_context,
            )
        except RecorderIntegrityError as exc:
            return self._report(
                "TAMPER_DETECTED", request, 0, str(exc), snapshot, knowledge_context, decision_context
            )

        if persisted.manifest.run_id != request.run_id or persisted.manifest.task_id != request.task_id:
            return self._report(
                "BROKEN_LINEAGE", request, 0, "TRACE_MANIFEST_CONTEXT_MISMATCH", snapshot, knowledge_context, decision_context
            )
        if persisted.manifest.event_refs != tuple(event.event_id for event in events):
            return self._report(
                "BROKEN_LINEAGE", request, 0, "TRACE_MANIFEST_EVENT_SET_MISMATCH", snapshot, knowledge_context, decision_context
            )

        if knowledge_context is not None and decision_context is not None:
            reason = "GOVERNED_LINEAGE_KNOWLEDGE_AND_DECISION_CONTEXT_VERIFIED"
        elif knowledge_context is not None:
            reason = "GOVERNED_LINEAGE_AND_KNOWLEDGE_CONTEXT_VERIFIED"
        elif decision_context is not None:
            reason = "GOVERNED_LINEAGE_AND_DECISION_CONTEXT_VERIFIED"
        else:
            reason = "GOVERNED_LINEAGE_VERIFIED"

        return self._report(
            "VERIFIED_RECORD",
            request,
            persisted.manifest.event_count,
            reason,
            snapshot,
            knowledge_context,
            decision_context,
        )

    @staticmethod
    def _report(
        status: str,
        request: ActionRequest,
        count: int,
        reason: str,
        snapshot: PolicySnapshot,
        knowledge_context: TraceKnowledgeContext | None = None,
        decision_context: TraceDecisionContext | None = None,
    ) -> ReplayReport:
        return ReplayReport(
            status=status,
            run_id=request.run_id,
            trace_id=request.trace_id,
            verified_event_count=count,
            reason_code=reason,
            policy_snapshot_ref=snapshot.snapshot_id,
            policy_snapshot_hash=snapshot.snapshot_hash,
            context_package_ref=knowledge_context.context_package_ref if knowledge_context else None,
            context_package_hash=knowledge_context.context_package_hash if knowledge_context else None,
            knowledge_snapshot_refs=knowledge_context.knowledge_snapshot_refs if knowledge_context else (),
            knowledge_context_verified=(status == "VERIFIED_RECORD" and knowledge_context is not None),
            decision_refs=decision_context.decision_refs if decision_context else (),
            decision_digests=decision_context.decision_digests if decision_context else (),
            decision_materiality_classes=decision_context.materiality_classes if decision_context else (),
            decision_context_verified=(status == "VERIFIED_RECORD" and decision_context is not None),
        )
