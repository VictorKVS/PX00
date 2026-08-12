from __future__ import annotations
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone


@dataclass(frozen=True)
class RiskEvent:
    event_id: str
    risk_id: str
    event_type: str
    actor_ref: str
    note: str
    created_at: str


@dataclass(frozen=True)
class ArchitecturalRisk:
    risk_id: str
    title: str
    category: str
    source_refs: tuple[str, ...]
    affected_component_refs: tuple[str, ...]
    description: str
    causal_hypothesis: str
    likelihood: str
    impact: str
    severity: str
    status: str
    owner_ref: str
    discovered_at: str
    last_reviewed_at: str
    mitigation_refs: tuple[str, ...] = ()
    verification_refs: tuple[str, ...] = ()
    history_refs: tuple[str, ...] = ()
    next_review_at: str | None = None
    accepted_by_ref: str | None = None
    acceptance_rationale: str | None = None


@dataclass
class RiskRegister:
    risks: dict[str, ArchitecturalRisk] = field(default_factory=dict)
    events: dict[str, RiskEvent] = field(default_factory=dict)

    def add(self, risk: ArchitecturalRisk) -> None:
        if risk.risk_id in self.risks:
            raise ValueError("RISK_ID_REUSE")
        if risk.status == "ACCEPTED" and (not risk.accepted_by_ref or not risk.acceptance_rationale):
            raise ValueError("RISK_ACCEPTANCE_REQUIRES_ACCOUNTABILITY")
        self.risks[risk.risk_id] = risk

    def record_event(self, event: RiskEvent) -> None:
        if event.event_id in self.events:
            raise ValueError("RISK_EVENT_ID_REUSE")
        if event.risk_id not in self.risks:
            raise ValueError("UNKNOWN_RISK_REF")
        self.events[event.event_id] = event
        risk = self.risks[event.risk_id]
        self.risks[event.risk_id] = replace(risk, history_refs=risk.history_refs + (event.event_id,))

    def transition(self, risk_id: str, status: str, *, actor_ref: str, note: str, event_id: str, verification_refs: tuple[str, ...] = (), accepted_by_ref: str | None = None, acceptance_rationale: str | None = None) -> None:
        if risk_id not in self.risks:
            raise ValueError("UNKNOWN_RISK_REF")
        allowed = {"OPEN","ACCEPTED","MITIGATING","MONITORING","RESOLVED","SUPERSEDED","REOPENED"}
        if status not in allowed:
            raise ValueError("UNKNOWN_RISK_STATUS")
        risk = self.risks[risk_id]
        if status == "ACCEPTED" and (not accepted_by_ref or not acceptance_rationale):
            raise ValueError("RISK_ACCEPTANCE_REQUIRES_ACCOUNTABILITY")
        if status == "RESOLVED" and not verification_refs:
            raise ValueError("RESOLUTION_REQUIRES_VERIFICATION")
        now = datetime.now(timezone.utc).isoformat()
        updated = replace(
            risk,
            status=status,
            last_reviewed_at=now,
            verification_refs=risk.verification_refs + verification_refs,
            accepted_by_ref=accepted_by_ref or risk.accepted_by_ref,
            acceptance_rationale=acceptance_rationale or risk.acceptance_rationale,
        )
        self.risks[risk_id] = updated
        self.record_event(RiskEvent(event_id, risk_id, status, actor_ref, note, now))

    def due_for_review(self, now_iso: str) -> tuple[ArchitecturalRisk, ...]:
        due=[]
        for risk in self.risks.values():
            if risk.status in {"RESOLVED","SUPERSEDED"}:
                continue
            if risk.next_review_at and risk.next_review_at <= now_iso:
                due.append(risk)
        return tuple(sorted(due, key=lambda r: (r.severity, r.risk_id), reverse=True))
