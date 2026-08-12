from __future__ import annotations

from dataclasses import dataclass
from px00.replay import ReplayReport


@dataclass(frozen=True)
class AcceptanceDecision:
    state: str
    reason_code: str
    replay_status: str
    blocking_failures: tuple[str, ...]


class ReplayGatedAcceptance:
    """Reference acceptance gate: replay evidence constrains acceptance but is not authority by itself."""

    def evaluate(
        self,
        *,
        replay_report: ReplayReport,
        blocking_criteria_passed: bool,
        remaining_actions: tuple[str, ...] = (),
    ) -> AcceptanceDecision:
        if replay_report.status != "VERIFIED_RECORD":
            return AcceptanceDecision(
                state="BLOCKED",
                reason_code=f"REPLAY_{replay_report.status}",
                replay_status=replay_report.status,
                blocking_failures=(replay_report.reason_code,),
            )
        if not blocking_criteria_passed:
            return AcceptanceDecision(
                state="FAIL",
                reason_code="BLOCKING_CRITERIA_FAILED",
                replay_status=replay_report.status,
                blocking_failures=("BLOCKING_CRITERIA_FAILED",),
            )
        if remaining_actions:
            return AcceptanceDecision(
                state="PASS_WITH_ACTIONS",
                reason_code="ACCEPTED_WITH_NON_BLOCKING_ACTIONS",
                replay_status=replay_report.status,
                blocking_failures=(),
            )
        return AcceptanceDecision(
            state="PASS",
            reason_code="ACCEPTANCE_CRITERIA_AND_REPLAY_VERIFIED",
            replay_status=replay_report.status,
            blocking_failures=(),
        )
